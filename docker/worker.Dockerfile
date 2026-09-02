FROM python:3.11-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
# Add celery dependencies explicitly for worker builds
RUN echo "celery>=5.3.0" >> requirements.txt
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim as runner

WORKDIR /app

# Copy python packages
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy all Clean Architecture directories from repository root
COPY agents/ ./agents/
COPY api/ ./api/
COPY auth/ ./auth/
COPY config/ ./config/
COPY database/ ./database/
COPY memory/ ./memory/
COPY models/ ./models/
COPY rag/ ./rag/
COPY services/ ./services/
COPY tools/ ./tools/
COPY vector_database/ ./vector_database/
COPY workflows/ ./workflows/
COPY backend/app/ ./app/

ENV PYTHONPATH=/app

CMD ["celery", "-A", "services.task_queue.celery_app", "worker", "--loglevel=info"]
