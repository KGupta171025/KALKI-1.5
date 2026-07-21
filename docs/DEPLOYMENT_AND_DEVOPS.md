# KALKI AI — Deployment, DevOps & Edge Intelligence

## 1. Kubernetes Production Cluster Architecture

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kalki-backend-api
  namespace: kalki-production
spec:
  replicas: 5
  selector:
    matchLabels:
      app: kalki-backend
  template:
    metadata:
      labels:
        app: kalki-backend
    spec:
      containers:
      - name: api-gateway
        image: kalki/backend:1.5.0
        resources:
          limits:
            cpu: "4"
            memory: "8Gi"
            nvidia.com/gpu: "1"
          requests:
            cpu: "2"
            memory: "4Gi"
        env:
        - name: VECTOR_DB_URL
          value: "http://qdrant.kalki-production:6333"
        ports:
        - containerPort: 8000
```

---

## 2. Edge SLM Deployment Pipeline

For edge nodes (mobile, smartwatch, IoT):
1. **Model Distillation**: Distill 70B LLM teacher into 3.8B SLM student (Phi-3 / Llama-3.2).
2. **Quantization**: INT4 AWQ / GGUF quantization reducing VRAM footprint to <2.2 GB.
3. **Execution Runtime**: ExecuTorch (Mobile) / ONNX Runtime (Desktop/IoT) / WebGPU (Browser).

---

## 3. Observability & Monitoring Metrics

- **Prometheus Collector**: Scrapes `/metrics` for query rates, token latency, and VRAM utilization.
- **Grafana Dashboard**: Real-time panels for Time-To-First-Token (TTFT), RAG cache hit ratio, and Agent execution success percentage.
