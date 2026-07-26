# KALKI — Production Deployment Runbook

This guide covers step-by-step instructions to deploy, monitor, backup, and troubleshoot the KALKI Autonomous AI Operating System.

---

## 📋 System Prerequisites

Ensure the following runtimes are installed on your host system:
- **Docker Engine** (v24.0.0+) and **Docker Compose** (v2.20.0+)
- **Kubernetes Client CLI** (`kubectl`) & `helm` (for cloud cluster deployments)
- **Terraform** (v1.5.0+)

---

## 🚀 Deployment Playbooks

### Option A: Local Multi-Container Run (Docker Compose)
To launch the complete gateway, worker pool, dashboard, and database engines:

```bash
# 1. Clone the repository workspace
git clone https://github.com/KGupta171025/KALKI-1.5.git
cd KALKI-1.5

# 2. Build and launch all 9 services in background daemon mode
docker compose up --build -d

# 3. Verify container statuses
docker compose ps
```

### Option B: Cloud Cluster Orchestration (Kubernetes)
To deploy the system into Amazon EKS (provisioned via the Terraform configurations in `kubernetes/terraform.tf`):

```bash
# 1. Apply AWS VPC, subnets, and cluster infrastructure
cd kubernetes
terraform init
terraform apply -auto-approve

# 2. Update kubectl context pointer to the new EKS cluster
aws eks update-kubeconfig --name kalki-eks-cluster --region us-east-1

# 3. Deploy gateway namespaces, configs, services, and deployments
kubectl apply -f k8s-deployment.yml

# 4. Verify system pod running status
kubectl get pods -n kalki-system
```

---

## 🔒 Security & Secrets Management

All secrets (API credentials, private database passwords, encryption keys) must be managed securely:
1. **Never commit raw `.env` files** to version control.
2. In production, load settings from cloud secrets managers (e.g. AWS Secrets Manager or HashiCorp Vault) and mount them as environment variables inside container specs.
3. To rotate the primary JWT signature key:
   ```bash
   # Generate a new cryptographically secure hex key
   python -c "import secrets; print(secrets.token_hex(32))"
   # Replace SECRET_KEY inside your environment settings profile
   ```

---

## 💾 Backup & Disaster Recovery

### 1. PostgreSQL DB Backup (Relational States & Users)
```bash
# Export schema and row data to SQL dump file
docker exec -t kalki-postgres pg_dumpall -c -U postgres > kalki_pg_backup.sql
```

### 2. MongoDB Document Backup (Episodic Logs)
```bash
# Export all BSON collections to backup directory
docker exec -t kalki-mongodb mongodump --db kalki_db --out /data/db/backup
```

### 3. Qdrant Vector Collection Snapshot
```bash
# Trigger an HTTP API call to generate a binary vector snapshot
curl -X POST http://localhost:6333/collections/kalki_kb/snapshots
```

---

## 🔍 Active System Monitoring & Diagnostics

- **REST API Gateway Docs**: `http://localhost:8000/docs`
- **GraphQL Interactive Playground**: `http://localhost:8000/graphql`
- **RabbitMQ Queue Metrics**: `http://localhost:15672` (Username: `guest`, Password: `guest`)
- **Celery Worker Execution Traces**:
  ```bash
  docker compose logs celery-worker -f
  ```
