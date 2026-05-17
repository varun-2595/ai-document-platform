# AI Document Intelligence Platform

Production-oriented FastAPI backend for ingesting PDFs, processing them asynchronously, indexing semantic chunks, and answering questions over documents.

## Local services

```bash
docker compose up -d
```

Services:
- PostgreSQL: metadata and chunks
- Redis: Celery broker/result backend
- OpenSearch: semantic index

## Backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example app/.env
alembic upgrade head
uvicorn app.main:app --reload
```

If you already created the old `documents` table with `create_all()` in this local database, first mark the baseline migration as applied, then run the hardening migration:

```bash
alembic stamp 20260518_0001
alembic upgrade head
```

Run a worker when queueing is enabled:

```bash
celery -A app.worker.celery_app.celery_app worker --loglevel=info
```

## Current API surface

- `POST /documents/upload`
- `GET /documents/{id}`
- `GET /documents/search?q=...`
- `POST /query`

The retrieval and answer endpoints require OpenSearch plus an OpenAI API key. The upload path works independently while `QUEUE_ENABLED=false`.

## Architecture

```text
API -> storage -> PostgreSQL metadata -> Celery worker
    -> extraction -> chunking -> embeddings -> OpenSearch -> RAG query
```
