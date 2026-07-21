# KALKI AI — Krishna Artificial Lattice Keystone Intelligence

<p align="center">
  <b>Next-Generation Enterprise Intelligence Operating System (IOS)</b>
</p>

---

## 🌟 Executive Summary

**KALKI AI** (**Krishna Artificial Lattice Keystone Intelligence**) is a next-generation, unified artificial intelligence ecosystem engineered to operate as a full **Intelligence Operating System (IOS)**. Designed for cloud, desktop, mobile, smartwatch, and edge IoT devices, KALKI AI brings together Large Language Models (LLMs), Vision-Language Models (VLMs), Small Language Models (SLMs), Mixture-of-Experts (MoE) task routing, multi-agent orchestration (via Model Context Protocol and Agent-to-Agent IPC), hybrid RAG search, hierarchical memory, and defensive cybersecurity safeguards.

---

## 🏗️ 7-Layer System Architecture Blueprint

```
+-----------------------------------------------------------------------+
|  LAYER 1: USER INTERFACE LAYER                                        |
|  Web (Next.js) | Mobile (Flutter) | Desktop (Tauri) | Smartwatch | API  |
+-----------------------------------------------------------------------+
|  LAYER 6: SECURITY & GOVERNANCE LAYER (Perimeter & In-Line Audit)     |
|  OAuth2 / MFA | RBAC Control | AES-256 E2EE | AI Safety & Defense    |
+-----------------------------------------------------------------------+
|  LAYER 2: MULTIMODAL PERCEPTION LAYER                                 |
|  Text & PDF Parsing | OCR & Scene VLM | Whisper Audio | Sensor Stream |
+-----------------------------------------------------------------------+
|  LAYER 4: AGENT ORCHESTRATION LAYER                                   |
|  Planner | Research | Memory | Executor | Validator | Security        |
|  Standard Protocols: MCP (Model Context Protocol) & A2A Inter-Agent   |
+-----------------------------------------------------------------------+
|  LAYER 3: REASONING & MODEL LAYER                                     |
|  MoE Task Router | LLM Cluster | Edge SLMs (INT4) | LCM Conversational |
+-----------------------------------------------------------------------+
|  LAYER 5: KNOWLEDGE & RAG LAYER                                       |
|  Dense Vector + BM25 Sparse | Cross-Encoder Re-Ranker | Neo4j KG    |
+-----------------------------------------------------------------------+
|  LAYER 7: INFRASTRUCTURE LAYER                                        |
|  Kubernetes (EKS/GKE) | Docker Compose | Edge Runtime | Prometheus     |
+-----------------------------------------------------------------------+
```

---

## 🚀 Key Features & Capabilities

- **Ultra-Fast Performance**: End-to-end response latency budget targeted under **<500ms**, with hybrid RAG retrieval **<200ms**.
- **Autonomous Multi-Agent Orchestration**: Specialized Planner, Research, Memory, Executor, Validator, and Security agents communicating via **MCP** and **A2A**.
- **Hierarchical Memory System**: Short-term context, Long-term user preferences, Semantic embeddings, Episodic history, and Procedural DAG patterns.
- **Hybrid RAG Engine**: Reciprocal Rank Fusion (RRF) combining dense vector search and BM25 sparse keyword indexing with Cross-Encoder re-ranking.
- **Defensive Cybersecurity**: Built-in security audit tools, SAST/DAST compliance reporting, anomaly detection, and strict safety guardrails.
- **Edge AI Deployment**: Quantized INT4 SLMs capable of running offline on mobile and IoT devices.

---

## 📚 Technical Documentation Index

Detailed blueprints and specifications are available in the [`docs/`](./docs/) directory:

- 📐 **[System Architecture Blueprint](./docs/ARCHITECTURE.md)** — Comprehensive 7-layer design & latency budget.
- 🗄️ **[Database & Memory Schema](./docs/DATABASE_SCHEMA.sql)** — PostgreSQL relational schema & vector indexes.
- 🌐 **[API Specification](./docs/API_SPECIFICATION.yaml)** — OpenAPI 3.0 specs for Gateway, Agents, RAG, and Security.
- 🤖 **[Multi-Agent Protocols](./docs/AGENT_PROTOCOLS.md)** — Model Context Protocol (MCP) & Agent-to-Agent (A2A) IPC.
- 🔍 **[RAG Pipeline Specification](./docs/RAG_PIPELINE.md)** — Hybrid retrieval, RRF math, re-ranking, and citation model.
- 🛡️ **[Security & Governance](./docs/SECURITY_AND_GOVERNANCE.md)** — RBAC matrix, E2EE, defensive cybersecurity, and HITL.
- 🐳 **[Deployment & DevOps](./docs/DEPLOYMENT_AND_DEVOPS.md)** — Kubernetes manifests, Edge SLM pipeline, Prometheus metrics.
- 📊 **[Business & Scalability](./docs/BUSINESS_AND_SCALABILITY.md)** — Infrastructure cost model, 10M user scaling roadmap, risk matrix.

---

## 💻 Tech Stack Overview

- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS, Lucide Icons.
- **Backend**: Python 3.11+, FastAPI, Pydantic v2, Asyncio, gRPC.
- **AI & ML**: PyTorch, Hugging Face Transformers, vLLM, ONNX Runtime, llama.cpp.
- **Data & Storage**: PostgreSQL (with `pgvector`), Redis, Qdrant Vector Store, Neo4j Knowledge Graph.
- **DevOps**: Docker, Docker Compose, Kubernetes, Helm, Prometheus, Grafana.

---

## 🛠️ Quickstart Guide

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+

### 1. Running via Docker Compose

```bash
# Clone the repository
git clone https://github.com/KGupta171025/KALKI-1.5.git
cd KALKI-1.5

# Launch full stack (FastAPI Backend, Next.js Frontend, PostgreSQL, Redis, Qdrant)
docker compose up --build
```

Access services:
- **Web UI Dashboard**: `http://localhost:3000`
- **FastAPI OpenAPI Documentation**: `http://localhost:8000/docs`
- **Qdrant Vector Dashboard**: `http://localhost:6333/dashboard`

---

## 📜 License & Governance

Developed under responsible AI guidelines. Designed for authorized, ethical enterprise deployment and defensive cybersecurity monitoring.
