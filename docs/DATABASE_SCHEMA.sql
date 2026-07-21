-- =============================================================================
-- KALKI AI — Intelligence Operating System (IOS) Database Schema
-- Dialect: PostgreSQL 16+ with pgvector extension
-- =============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- -----------------------------------------------------------------------------
-- 1. SECURITY & IDENTITY GOVERNANCE
-- -----------------------------------------------------------------------------

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    mfa_enabled BOOLEAN DEFAULT FALSE,
    mfa_secret VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_roles (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_id)
);

CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    resource_target VARCHAR(255) NOT NULL,
    status_code INT NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    payload_hash VARCHAR(64),
    risk_score FLOAT DEFAULT 0.0,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 2. HIERARCHICAL MEMORY SYSTEM
-- -----------------------------------------------------------------------------

-- Short-Term Memory: Active conversation context window & scratchpad
CREATE TABLE short_term_memory (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) CHECK (role IN ('system', 'user', 'assistant', 'tool', 'agent')),
    content TEXT NOT NULL,
    token_count INT NOT NULL,
    sequence_order INT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Long-Term Memory: User persistent preferences, goals, and constraints
CREATE TABLE long_term_memory (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    preference_key VARCHAR(100) NOT NULL,
    preference_value JSONB NOT NULL,
    privacy_level VARCHAR(20) DEFAULT 'private' CHECK (privacy_level IN ('public', 'private', 'encrypted')),
    is_deleted BOOLEAN DEFAULT FALSE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_user_pref UNIQUE (user_id, preference_key)
);

-- Semantic Memory: High-level concepts, facts, and entity relations
CREATE TABLE semantic_memory (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    entity_subject VARCHAR(255) NOT NULL,
    predicate VARCHAR(100) NOT NULL,
    entity_object VARCHAR(255) NOT NULL,
    confidence FLOAT DEFAULT 1.0,
    embedding VECTOR(1536), -- 1536-dim dense vector (OpenAI/bge)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Episodic Memory: Past interaction events, execution histories & outcomes
CREATE TABLE episodic_memory (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    task_goal TEXT NOT NULL,
    execution_trace JSONB NOT NULL, -- Steps, sub-agent calls, tools used
    success_status BOOLEAN NOT NULL,
    user_feedback_score INT, -- 1 to 5 scale
    embedding VECTOR(1536),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Procedural Memory: Learned execution patterns, macros, and workflow plans
CREATE TABLE procedural_memory (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    trigger_condition TEXT NOT NULL,
    action_dag JSONB NOT NULL, -- Directed Acyclic Graph of execution steps
    performance_rating FLOAT DEFAULT 1.0,
    version INT DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 3. KNOWLEDGE & RAG INGESTION
-- -----------------------------------------------------------------------------

CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    mime_type VARCHAR(100) NOT NULL,
    file_size_bytes BIGINT NOT NULL,
    storage_path TEXT NOT NULL,
    checksum_sha256 VARCHAR(64) NOT NULL,
    status VARCHAR(30) DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'indexed', 'failed')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE document_chunks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index INT NOT NULL,
    chunk_content TEXT NOT NULL,
    token_length INT NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    embedding VECTOR(1536), -- Dense vector index
    sparse_bm25_tokens JSONB, -- Sparse token frequencies
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexing for high-performance vector search
CREATE INDEX idx_doc_chunks_embedding ON document_chunks USING hnsw (embedding vector_cosine_ops);
CREATE INDEX idx_semantic_mem_embedding ON semantic_memory USING hnsw (embedding vector_cosine_ops);
CREATE INDEX idx_episodic_mem_embedding ON episodic_memory USING hnsw (embedding vector_cosine_ops);
CREATE INDEX idx_audit_logs_user_timestamp ON audit_logs (user_id, timestamp DESC);
