# AI-Powered Document Intelligence Platform

A production-style AI-powered document intelligence and Retrieval-Augmented Generation (RAG) platform built using FastAPI, PostgreSQL, OpenSearch, Celery, Redis, OpenAI embeddings, and AWS S3.

This project demonstrates modern backend engineering, AI retrieval architecture, distributed processing, vector search, and cloud-native system design.

---

# Features

## Document Ingestion

* Upload PDF documents through FastAPI APIs
* Store uploaded files locally and in AWS S3
* Asynchronous document processing using Celery workers
* Metadata persistence using PostgreSQL

## PDF Processing Pipeline

* Extract text from PDFs using PyMuPDF
* Clean and normalize extracted content
* Word-aware overlapping chunking strategy
* Generate OpenAI embeddings for semantic understanding

## Semantic Search

* OpenSearch vector database integration
* kNN vector similarity search
* Semantic retrieval over uploaded documents
* Chunk-level retrieval architecture

## Retrieval-Augmented Generation (RAG)

* Ask natural language questions over uploaded documents
* Retrieve relevant chunks from OpenSearch
* Generate contextual AI answers using OpenAI GPT models

## Distributed Processing

* Redis-backed task queue
* Celery background workers
* Async ingestion and indexing pipeline

## Cloud Integration

* AWS S3 document storage
* Dockerized local infrastructure
* Environment-based configuration management

---

# Architecture

```text
                +----------------+
                |   FastAPI API  |
                +--------+-------+
                         |
                         |
                 Upload Document
                         |
                         v
                +----------------+
                |   PostgreSQL   |
                +----------------+
                         |
                         |
                  Queue Task
                         |
                         v
                +----------------+
                |     Redis      |
                +----------------+
                         |
                         |
                +--------v-------+
                | Celery Worker  |
                +--------+-------+
                         |
                         |
          +--------------+--------------+
          |                             |
          v                             v
+-------------------+       +----------------------+
| PDF Extraction    |       | AWS S3 Storage       |
| Cleaning          |       +----------------------+
| Chunking          |
| Embeddings        |
+---------+---------+
          |
          |
          v
+-------------------------+
| OpenSearch Vector Index |
+-------------------------+
          |
          |
          v
+-------------------------+
| RAG Question Answering  |
+-------------------------+
```

---

# Tech Stack

## Backend

* FastAPI
* Python
* SQLAlchemy
* Pydantic

## AI / Retrieval

* OpenAI Embeddings
* GPT-4.1 Mini
* OpenSearch Vector Search
* NumPy

## Databases / Queues

* PostgreSQL
* Redis

## Async Processing

* Celery

## Cloud

* AWS S3
* Docker
* Docker Compose

## PDF Processing

* PyMuPDF

---

# Project Structure

```text
backend/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── tasks/
│   └── main.py
│
├── uploads/
├── venv/
├── .env
└── requirements.txt
```

---

# APIs

## Health Check

```http
GET /
```

---

## Upload Document

```http
POST /documents/upload
```

Uploads a PDF document and triggers asynchronous processing.

---

## Semantic Search

```http
POST /search/
```

Example:

```json
{
  "query": "AWS Lambda event-driven compute"
}
```

---

## RAG Question Answering

```http
POST /rag/ask
```

Example:

```json
{
  "question": "What are the benefits of AWS Lambda?"
}
```

---

# Local Development Setup

## 1. Clone Repository

```bash
git clone <repo-url>
cd ai-document-platform
```

---

## 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create:

```text
backend/.env
```

Example:

```env
APP_NAME=AI Document Intelligence Platform
APP_VERSION=1.0.0
DEBUG=True

DATABASE_URL=postgresql://admin:password@localhost:5432/document_db

OPENAI_API_KEY=your_openai_api_key

OPENSEARCH_HOST=http://localhost:9200

REDIS_URL=redis://localhost:6379/0

AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_REGION=ap-south-1
S3_BUCKET_NAME=your_bucket
```

---

## 5. Start Infrastructure

```bash
docker compose up -d
```

Services started:

* PostgreSQL
* Redis
* OpenSearch

---

## 6. Start FastAPI Server

```bash
uvicorn app.main:app --reload
```

---

## 7. Start Celery Worker

For macOS local development:

```bash
celery -A app.tasks.document_tasks worker --pool=solo --loglevel=info
```

---

# Swagger Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

---

# Current Capabilities

* PDF upload pipeline
* Text extraction and cleaning
* Word-aware overlapping chunking
* OpenAI embedding generation
* OpenSearch vector similarity search
* Retrieval-Augmented Generation (RAG)
* Async background processing
* AWS S3 integration
* Dockerized infrastructure

---

# Future Improvements

* Authentication and user management
* Streaming LLM responses
* Full AWS deployment (ECS / Lambda)
* Kubernetes deployment
* Observability and monitoring
* CI/CD pipelines
* Better chunking strategies
* OCR support for scanned PDFs
* Multi-document conversational memory

---

# Learning Outcomes

This project demonstrates:

* Backend engineering
* AI retrieval systems
* Vector databases
* RAG architecture
* Distributed systems
* Async task processing
* Cloud-native engineering
* OpenSearch vector search
* AWS integration
* Production-style system design

---

# License

MIT License
