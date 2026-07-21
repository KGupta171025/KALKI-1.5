# KALKI AI — System Architecture Blueprint

## Executive Overview
**KALKI AI** (**Krishna Artificial Lattice Keystone Intelligence**) is designed as an **Intelligence Operating System (IOS)**. It unifies large language models (LLMs), vision-language models (VLMs), small language models (SLMs), mixture-of-experts (MoE) routing, autonomous multi-agent orchestration, retrieval-augmented generation (RAG), and defensive cybersecurity into a single, high-throughput, low-latency framework operating across Cloud, Edge, Mobile, Desktop, Smartwatch, and IoT devices.

---

## High-Level System Architecture Diagram

```mermaid
graph TD
    subgraph Layer 1: User Interface Layer
        UI_Web["Web App (Next.js/React)"]
        UI_Mob["Mobile App (Flutter)"]
        UI_Desk["Desktop App (Tauri/Electron)"]
        UI_IoT["Smartwatch & IoT Nodes"]
        UI_API["Third-Party API Gateway"]
    end

    subgraph Layer 6: Security & Governance Layer (Perimeter & In-Line)
        SEC_Auth["OAuth2 / MFA / JWT"]
        SEC_RBAC["Role-Based Access Control"]
        SEC_Enc["TLS 1.3 & AES-256 E2EE"]
        SEC_Guard["AI Safety & Defense Guardrails"]
    end

    subgraph Layer 2: Multimodal Perception Layer
        PERC_Text["Text & Structured Doc Parser"]
        PERC_Vision["OCR & Scene Understanding (VLM)"]
        PERC_Audio["Speech-to-Text / Audio Features"]
        PERC_Sensor["IoT & Sensor Stream Ingestion"]
    end

    subgraph Layer 4: Agent Orchestration Layer
        AGENT_Planner["Planner Agent"]
        AGENT_Research["Research Agent"]
        AGENT_Memory["Memory Agent"]
        AGENT_Executor["Executor Agent"]
        AGENT_Validator["Validator Agent"]
        AGENT_Security["Security Agent"]
        MCP_Bus["MCP & A2A Protocol Router"]
    end

    subgraph Layer 3: Reasoning & Model Layer
        MOE["MoE Router (Mixture of Experts)"]
        LLM["High-Reasoning LLM Cluster"]
        SLM["Edge Quantized SLMs (ONNX/GGML)"]
        LCM["Low-Latency Conversational Model"]
        VLM["Vision-Language Model Engine"]
    end

    subgraph Layer 5: Knowledge & RAG Layer
        RAG_Hybrid["Hybrid Search (Dense + Sparse BM25)"]
        RAG_VecDB["Vector Store (Qdrant / FAISS)"]
        RAG_KG["Knowledge Graph (Neo4j / RDF)"]
        RAG_Rerank["Cross-Encoder Re-Ranker"]
        MEM_Hier["Hierarchical Memory Store"]
    end

    subgraph Layer 7: Infrastructure Layer
        INFRA_K8s["Kubernetes Cloud Cluster"]
        INFRA_Edge["Edge Runtime (TFLite / ExecuTorch)"]
        INFRA_Obs["Prometheus / Grafana / Jaeger"]
    end

    UI_Web --> SEC_Auth
    UI_Mob --> SEC_Auth
    UI_Desk --> SEC_Auth
    UI_IoT --> SEC_Auth
    UI_API --> SEC_Auth

    SEC_Auth --> SEC_Guard
    SEC_Guard --> PERC_Text
    SEC_Guard --> PERC_Vision
    SEC_Guard --> PERC_Audio
    SEC_Guard --> PERC_Sensor

    PERC_Text --> MCP_Bus
    PERC_Vision --> MCP_Bus
    PERC_Audio --> MCP_Bus
    PERC_Sensor --> MCP_Bus

    MCP_Bus <--> AGENT_Planner
    AGENT_Planner <--> AGENT_Research
    AGENT_Planner <--> AGENT_Memory
    AGENT_Planner <--> AGENT_Executor
    AGENT_Planner <--> AGENT_Validator
    AGENT_Planner <--> AGENT_Security

    AGENT_Executor <--> MOE
    MOE --> LLM
    MOE --> SLM
    MOE --> LCM
    MOE --> VLM

    AGENT_Research <--> RAG_Hybrid
    RAG_Hybrid --> RAG_VecDB
    RAG_Hybrid --> RAG_KG
    RAG_Hybrid --> RAG_Rerank

    AGENT_Memory <--> MEM_Hier

    MOE --> INFRA_K8s
    SLM --> INFRA_Edge
    INFRA_K8s --> INFRA_Obs
```

---

## Detailed Layer Breakdown

### Layer 1: User Interface Layer
- **Web Application**: Next.js 14 App Router, React 18, Tailwind CSS, WebSockets streaming.
- **Mobile Application**: Flutter cross-platform mobile client supporting iOS, Android, and WearOS.
- **Desktop Application**: Tauri (Rust + Web frontend) for minimal footprint and native hardware integration.
- **Voice & IoT Assistants**: Micro-client SDK providing push-to-talk, wake-word detection, and MQTT telemetry.
- **API Gateway**: REST & gRPC endpoints protected by OAuth2, rate limiting, and mTLS.

### Layer 2: Multimodal Perception Layer
- **Text & PDF Processing**: PyMuPDF + Tesseract OCR fallback for scanned multi-page documents.
- **Vision Perception**: CLIP / Qwen2-VL embeddings for object classification, visual Q&A, and chart analysis.
- **Audio Perception**: Whisper Large v3 for multilingual speech recognition; Bark / Coqui for low-latency TTS.
- **Sensor Ingestion**: Real-time event streams (JSON/Protobuf over WebSockets & MQTT) normalized into structured state matrices.

### Layer 3: Reasoning & Model Layer
- **MoE Router**: Dynamic routing based on prompt complexity, required context size, and SLA requirements.
- **LLM Cluster**: Llama-3 70B / Claude-3.5 Sonnet / Mixtral-8x22B for complex multi-step reasoning.
- **SLMs for Edge**: Phi-3 Mini (3.8B), Llama-3.2 1B/3B quantized to INT4 via llama.cpp / ONNX runtime for offline edge deployment.
- **LCMs (Low-Latency Conversational Models)**: Speculative decoding and KV-cache optimization yielding <150ms time-to-first-token (TTFT).

### Layer 4: Agent Orchestration Layer
- **Planner Agent**: ReAct + Tree-of-Thought decomposition into graph execution DAGs.
- **Research Agent**: Deep web search, RAG querying, and document synthesis.
- **Memory Agent**: Context resolution, memory index retrieval, and dynamic prompt injection.
- **Executor Agent**: MCP tool execution, sandboxed code execution (Docker/Wasm), and API calling.
- **Validator Agent**: Output assertion, hallucination detection, and schema verification.
- **Security Agent**: Defensive threat monitoring, prompt injection detection, and compliance authorization.

### Layer 5: Knowledge & RAG Layer
- **Hybrid Vector & Keyword Search**: Reciprocal Rank Fusion (RRF) joining Qdrant dense vector search (Cosine distance) and BM25 sparse keyword indexing.
- **Re-Ranker**: Cross-Encoder (bge-reranker-large) scoring top 50 candidates down to top 5 context windows.
- **Knowledge Graph**: Entity-Relation extraction storing semantic triples in Neo4j for multi-hop graph reasoning.

### Layer 6: Security & Governance Layer
- **Zero Trust Model**: Mandatory JWT validation per RPC, role-based capability boundaries.
- **Data Encryption**: TLS 1.3 in-transit, AES-256-GCM at-rest for all memory vectors and user documents.
- **AI Safety Guardrails**: Llama-Guard 3 + custom rule filter preventing unsafe code generation or privilege escalation attempts.

### Layer 7: Infrastructure Layer
- **Cloud Cluster**: Kubernetes (EKS/GKE) with Horizontal Pod Autoscaler (HPA) and Nvidia Kube-Ray GPU management.
- **Edge Deployment**: Cross-compiled binaries for ARM64 / Apple Silicon / Android NDK with local vector index storage (SQLite-vec).

---

## Latency Budget Allocation (<500ms Target)

| Stage | Component | Latency Budget |
|---|---|---|
| 1 | API Gateway & Security Auth | 15ms |
| 2 | Perception & Audio/Text Tokenization | 35ms |
| 3 | Memory & RAG Retrieval | 180ms |
| 4 | MoE Routing & Agent Planner | 40ms |
| 5 | LLM Speculative Token Generation (TTFT) | 180ms |
| 6 | Security Audit & Guardrail Verification | 30ms |
| **Total** | **End-to-End Latency Target** | **480ms** |
