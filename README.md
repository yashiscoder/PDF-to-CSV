# Handwritten Form → CSV Web Application
### Project Specification & Architecture Document

## Table of Contents
1. [Overview](#overview)
2. [Objectives](#objectives)
3. [Recommended Tech Stack](#recommended-tech-stack)
4. [Feature Set](#feature-set)
5. [Can This Use RAG / LangChain / LangGraph?](#can-this-use-rag--langchain--langgraph)
6. [System Architecture](#system-architecture)
7. [Processing Pipeline](#processing-pipeline)
8. [Database Schema](#database-schema)
9. [REST API Design](#rest-api-design)
10. [Suggested Project Structure](#suggested-project-structure)
11. [Security Checklist](#security-checklist)
12. [OCR / Handwriting API Comparison](#ocr--handwriting-api-comparison)
13. [Environment Variables](#environment-variables)
14. [Development Roadmap](#development-roadmap)
15. [Key Challenges & Mitigations](#key-challenges--mitigations)
16. [Next Steps](#next-steps)

---

## Overview

A full-stack web application that lets a user upload a photo or scan of a handwritten form, runs it through a pretrained handwriting-recognition (OCR/HTR) API, extracts the fields into structured data, and lets the user download the result as a CSV. Every upload — the original document (saved as a PDF) and the generated CSV — is stored and tied to an authenticated user account, so users can log in, upload, review, correct, and revisit their form history at any time.

## Objectives

- [ ] Let a user register and log in securely (credentials stored, hashed, in the database)
- [ ] Let a logged-in user upload a handwritten form (image or PDF)
- [ ] Send the file to a pretrained handwriting-recognition API and get structured field data back
- [ ] Let the user review/correct extracted fields before finalizing — handwriting OCR is never 100% accurate
- [ ] Generate and save a CSV of the extracted data
- [ ] Save the original file as a PDF and the CSV, both linked to the user's account, in the database
- [ ] Let the user view, search, and re-download their upload history
- [ ] *(Recommended)* Layer in LangChain to structure raw OCR output, LangGraph to run the review/approval workflow, and RAG to make form history searchable in natural language

## Recommended Tech Stack

| Layer | Recommended | Why | Alternatives |
|---|---|---|---|
| Frontend framework | React (Vite) | Fast dev server, huge ecosystem — matches your requirement | Next.js if you want SSR/SEO |
| Styling | Tailwind CSS | Rapid, consistent UI without fighting CSS | Chakra UI, MUI |
| Frontend state/data | React Query + Context API | Caches server data, simple auth state | Redux Toolkit |
| Backend framework | FastAPI (Python) | Async, auto-generated OpenAPI docs, and its Pydantic models plug directly into LangChain's structured output | Node.js + Express, if you'd rather use one language end-to-end |
| ORM / migrations | SQLAlchemy + Alembic | Mature, type-safe, versioned schema changes | Prisma (Node) |
| Database | PostgreSQL | Relational integrity for users/documents; the `pgvector` extension gives you a vector store for RAG in the *same* database | MongoDB, if your form fields vary wildly between form types |
| Authentication | JWT (access + refresh) via `python-jose`, passwords via `passlib[bcrypt]` | Stateless, scales horizontally | Managed auth (Auth0, Clerk) if you'd rather not run your own |
| File storage | AWS S3 / Azure Blob Storage (local disk in dev) | Binary files don't belong in a relational DB row — store the file, save the *path* in the DB | Google Cloud Storage, Cloudinary |
| OCR / handwriting recognition | Azure AI Document Intelligence | Purpose-built for forms — prebuilt models return key-value pairs and tables directly, which maps cleanly onto CSV columns | AWS Textract, Google Cloud Vision, self-hosted TrOCR |
| AI orchestration | LangChain | Turns messy OCR text into a validated, structured schema | Hand-rolled prompt + JSON parsing (more brittle) |
| Workflow orchestration | LangGraph | Models extract → validate → (auto-approve *or* human-review) → save as a real state graph | A custom if/else pipeline — fine for a first pass, harder to extend |
| Vector store (for RAG) | `pgvector` | One database instead of two moving parts | Chroma, Pinecone, Weaviate |
| Containerization | Docker + docker-compose | Reproducible dev environment, easy deploy | — |

## Feature Set

### Core (MVP)
1. Registration & login (email + password, JWT-based sessions)
2. Upload a handwritten form as an image (JPG/PNG) or PDF
3. Send the file to the OCR/handwriting API and receive extracted fields
4. Display extracted data in an editable table before saving
5. Generate a CSV from the confirmed extracted data
6. Store the original file as a normalized PDF + the generated CSV, both linked to the user's account
7. Dashboard listing past uploads with download links (PDF/CSV)
8. Logout and a basic profile view

### Recommended Enhancements
1. Per-field confidence scores, with low-confidence fields visually flagged for review
2. Multi-page form / multi-page PDF support
3. Drag-and-drop upload with a live preview
4. Batch upload — process several forms in one go via a background job queue
5. Export to Excel (.xlsx) and JSON in addition to CSV
6. Search & filter past uploads by date, filename, or extracted field value
7. Reusable "form templates" — define a field schema once for a recurring form type, reuse it on every upload of that type
8. Email verification on signup + password reset flow
9. Usage quota / rate limiting per user (OCR API calls cost money per page)
10. Soft-delete and data-retention controls so users can remove their own data

### Advanced — AI-Orchestrated Layer
*(this is where LangChain / LangGraph / RAG live — see the next section)*
1. LangChain-based structuring: raw OCR text → validated, typed JSON via a Pydantic output parser
2. LangGraph pipeline: OCR → structure → confidence check → auto-finalize *or* route to human review → save
3. RAG "ask your documents" chat — natural-language Q&A over a user's entire upload history
4. Semantic search across historical forms (find similar forms, not just exact filename matches)
5. LLM-assisted anomaly flags (e.g. "date of birth is in the future") surfaced during review, never silently auto-corrected

## Can This Use RAG / LangChain / LangGraph?

**Yes — and they're a genuinely good fit here, not just buzzwords bolted on.** Here's specifically where each one earns its place, and where it doesn't.

### LangChain — cleaning up what the OCR API gives you
A handwriting API returns raw text or loose key-value pairs — never a guaranteed, validated schema. LangChain's prompt templates plus a Pydantic output parser let you force that raw text through an LLM and get back a strict, typed object every time:

```python
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

class FormFields(BaseModel):
    full_name: str
    date_of_birth: str
    address: str
    phone_number: str

parser = PydanticOutputParser(pydantic_object=FormFields)
prompt = PromptTemplate(
    template="Extract these fields from the raw OCR text below.\n{format_instructions}\n\nOCR TEXT:\n{ocr_text}",
    input_variables=["ocr_text"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

chain = prompt | ChatOpenAI(model="gpt-4o-mini", temperature=0) | parser
structured = chain.invoke({"ocr_text": raw_ocr_output})
```

### LangGraph — the review/approval workflow
The pipeline isn't linear: a high-confidence extraction should save automatically, a low-confidence one should stop and wait for a human to fix it. That's a branching, stateful workflow — exactly what LangGraph is designed for (it's the same pattern companies use in production for durable, human-in-the-loop agent pipelines):

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class PipelineState(TypedDict):
    raw_ocr: str
    structured: dict
    confidence: float

def structure_node(state): ...   # calls the LangChain chain above
def route_on_confidence(state):
    return "human_review" if state["confidence"] < 0.8 else "finalize"

graph = StateGraph(PipelineState)
graph.add_node("structure", structure_node)
graph.add_node("human_review", human_review_node)
graph.add_node("finalize", finalize_node)
graph.add_conditional_edges("structure", route_on_confidence, {
    "human_review": "human_review",
    "finalize": "finalize",
})
graph.add_edge("human_review", "finalize")
graph.add_edge("finalize", END)
```

### RAG — an "ask your documents" feature
Once a user has dozens or hundreds of processed forms, a table gets hard to search. Embed each document's extracted text, store the vectors in `pgvector`, and let the user ask questions in plain language:

```python
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

vectorstore = PGVector(
    embeddings=OpenAIEmbeddings(),
    connection=DATABASE_URL,
    collection_name="user_documents",
)
vectorstore.add_texts(
    texts=[extracted_text],
    metadatas=[{"user_id": user_id, "document_id": doc_id}],
)

retriever = vectorstore.as_retriever(search_kwargs={"filter": {"user_id": user_id}})
results = retriever.invoke("forms with an address in California")
```

### Where *not* to use an LLM
Don't route simple, rule-based checks (is this field empty? is this a valid date format?) through an LLM call — a Pydantic validator or a regex is faster, cheaper, and 100% deterministic. Save LangChain for genuinely fuzzy interpretation (messy handwriting → clean field) and LangGraph for orchestration where the path actually branches.

## System Architecture

```
┌──────────────────┐      ┌───────────────────┐
│  React Frontend   │─────▶│  FastAPI Backend   │
│ (Vite + Tailwind) │ REST │ Auth / Upload /    │
│                   │ JWT  │ Pipeline Orchestr. │
└──────────────────┘      └─────────┬──────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │                      │                      │
              ▼                      ▼                      ▼
     ┌─────────────────┐   ┌──────────────────┐   ┌───────────────────┐
     │   PostgreSQL     │   │   OCR / HTR API   │   │   File Storage     │
     │ users, documents │   │ (Azure Document   │   │  (S3 / local disk) │
     │ extracted_fields │   │  Intelligence)    │   │  PDFs + CSVs       │
     │ pgvector         │   └──────────────────┘   └───────────────────┘
     └─────────────────┘
              ▲
              │  structured data, embeddings
     ┌────────┴──────────┐
     │  LangChain +       │
     │  LangGraph         │
     │ (structuring,      │
     │  review routing,   │
     │  RAG retrieval)    │
     └────────────────────┘
```

## Processing Pipeline

1. **Upload** — user drags/selects an image or PDF in the React app; frontend checks file type and size before sending.
2. **Validate & store original** — backend re-validates the file, saves it to file storage, creates a `documents` row with `status = 'pending'`.
3. **OCR / handwriting recognition** — backend sends the file to the pretrained OCR API (e.g. Azure AI Document Intelligence's prebuilt layout/form model), which returns raw text plus any key-value pairs and tables it detected.
4. **Structuring (LangChain)** — the raw OCR output is passed through a LangChain chain with a Pydantic output parser, mapping it onto your target schema (`full_name`, `date_of_birth`, `address`, ...) with a per-field confidence score.
5. **Routing (LangGraph)** — high-confidence results move straight to step 7; low-confidence results are flagged `needs_review` and the pipeline pauses.
6. **Human review (if flagged)** — the user sees extracted fields in an editable table, with low-confidence fields highlighted, and corrects anything wrong.
7. **CSV generation** — the confirmed structured data is written to a CSV file.
8. **Persist** — the CSV and a normalized PDF of the original are saved to file storage; their paths, plus the structured field values, are saved to PostgreSQL against the user's account; `status` is set to `completed`.
9. **Embed for RAG** *(optional)* — the extracted text is embedded and stored in `pgvector`, making it searchable via the chat/search feature.
10. **Done** — the document appears in the user's dashboard with download links for the PDF and CSV.

## Database Schema

```sql
-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,   -- bcrypt/argon2 hash, NEVER plaintext
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Uploaded forms
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    original_filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(10) NOT NULL,          -- 'image' | 'pdf'
    original_file_path TEXT NOT NULL,        -- storage path/URL, not the file itself
    pdf_path TEXT,                           -- normalized PDF
    csv_path TEXT,                           -- generated CSV
    status VARCHAR(20) DEFAULT 'pending',    -- pending|processing|needs_review|completed|failed
    avg_confidence FLOAT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Structured, per-field extracted data
CREATE TABLE extracted_fields (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    field_name VARCHAR(100) NOT NULL,
    field_value TEXT,
    confidence FLOAT,
    was_edited BOOLEAN DEFAULT FALSE          -- true if the user corrected it
);

-- Embeddings for RAG (requires the pgvector extension)
CREATE TABLE document_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    chunk_text TEXT,
    embedding VECTOR(1536)                    -- dimension matches your embedding model
);
```

> **On "saving the PDF/CSV into the database":** store the *files* in disk/object storage and the *path or URL* in the row above. Storing large binaries directly in Postgres (as `bytea`) technically works for a small prototype, but it bloats the database and slows backups as you scale — the schema above already reflects the recommended pattern.

## REST API Design

```
Auth
POST   /api/auth/register       Create a new account
POST   /api/auth/login          Authenticate, return access + refresh tokens
POST   /api/auth/refresh        Exchange a refresh token for a new access token
POST   /api/auth/logout         Invalidate the refresh token
GET    /api/auth/me             Current user's profile

Documents
POST   /api/documents/upload        Upload a handwritten form (multipart/form-data)
GET    /api/documents               List the user's documents (paginated, filterable)
GET    /api/documents/{id}          Document detail + extracted fields
PATCH  /api/documents/{id}/fields   Correct one or more extracted field values
GET    /api/documents/{id}/pdf      Download the stored PDF
GET    /api/documents/{id}/csv      Download the generated CSV
DELETE /api/documents/{id}          Delete a document and its files

Chat / RAG  (Phase 4)
POST   /api/chat/query              Natural-language query over the user's documents
```

## Suggested Project Structure

```
handwritten-form-app/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadDropzone.jsx
│   │   │   ├── ExtractedDataTable.jsx
│   │   │   ├── ConfidenceBadge.jsx
│   │   │   └── Navbar.jsx
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── DocumentReview.jsx
│   │   │   └── History.jsx
│   │   ├── context/AuthContext.jsx
│   │   ├── services/api.js
│   │   ├── hooks/useAuth.js
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── documents.py
│   │   │   └── chat.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── models/                 # SQLAlchemy models
│   │   ├── schemas/                # Pydantic schemas
│   │   ├── services/
│   │   │   ├── ocr_service.py
│   │   │   ├── csv_service.py
│   │   │   ├── langchain_pipeline.py
│   │   │   ├── langgraph_workflow.py
│   │   │   └── rag_service.py
│   │   ├── db/session.py
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml
└── README.md
```

## Security Checklist

- [ ] Hash passwords with bcrypt or argon2 — never store plaintext, ever
- [ ] Short-lived JWT access tokens + rotating refresh tokens, stored in httpOnly secure cookies (not `localStorage`)
- [ ] Validate uploaded file type and size on both frontend and backend — don't trust the client
- [ ] Use an ORM with parameterized queries (SQLAlchemy) to prevent SQL injection
- [ ] Enforce HTTPS in production
- [ ] Restrictive CORS policy (only your frontend's origin)
- [ ] Rate-limit auth endpoints (brute-force protection) and upload endpoints (cost control, since OCR calls cost money per page)
- [ ] Secrets and API keys in environment variables, never committed to source control
- [ ] Row-level access control — a user can only read/edit/delete their own documents
- [ ] Encrypt sensitive files at rest if forms contain PII
- [ ] Let users delete their own account and data

## OCR / Handwriting API Comparison

| API | Provider | Strengths | Handwriting quality | Pricing model |
|---|---|---|---|---|
| Azure AI Document Intelligence | Microsoft | Purpose-built for forms; prebuilt models return key-value pairs & tables directly, which maps cleanly onto CSV columns. Recently folded into the broader "Azure AI Foundry" / Content Understanding branding, but the API and capabilities are unchanged. | Strong | Pay per page |
| Amazon Textract | AWS | `AnalyzeDocument` with Forms/Tables features; solid structured extraction with built-in confidence scores and a human-review workflow option | Strong | Pay per page |
| Google Cloud Vision | Google | `DOCUMENT_TEXT_DETECTION`; excellent general OCR | Good, more raw-text than form-structure-aware | Pay per request |
| Mathpix | Mathpix | Excellent accuracy on messy/cursive handwriting and math notation | Excellent | Subscription / credits |
| TrOCR (self-hosted, via Hugging Face) | Open source (Microsoft) | Free to run, fully customizable/fine-tunable to your form types | Good, depends on fine-tuning | Free (you pay for GPU hosting) |

**Recommendation:** start with Azure AI Document Intelligence — its prebuilt layout model already returns structured key-value pairs and tables, which is the closest match to "extract fields → CSV row" with the least glue code. Fall back to AWS Textract or Google Vision if you're already committed to that cloud, or to a self-hosted TrOCR if per-page API costs become a concern at scale.

## Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/formapp

# JWT
JWT_SECRET_KEY=change-me
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# OCR API (pick one)
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=
AZURE_DOCUMENT_INTELLIGENCE_KEY=
# AWS_ACCESS_KEY_ID=
# AWS_SECRET_ACCESS_KEY=

# LLM (LangChain structuring + RAG)
OPENAI_API_KEY=
# or: ANTHROPIC_API_KEY=

# File storage
STORAGE_BACKEND=local        # local | s3
S3_BUCKET_NAME=
```

## Development Roadmap

**Phase 1 — Core MVP**
Auth (register/login/JWT), file upload, OCR API integration, CSV generation, PDF + CSV storage, basic dashboard/history.

**Phase 2 — Usability**
Editable extraction review screen, confidence-score highlighting, multi-page support, search/filter history, email verification + password reset.

**Phase 3 — AI Orchestration**
Swap the raw OCR → CSV mapping for the LangChain structuring chain; introduce LangGraph to route low-confidence extractions to human review automatically.

**Phase 4 — RAG**
Embed extracted document text into `pgvector`; add a chat/search interface so users can query their form history in natural language.

## Key Challenges & Mitigations

| Challenge | Mitigation |
|---|---|
| Handwriting OCR accuracy varies a lot (cursive, messy writing, non-English text) | Confidence scoring + mandatory human review step for low-confidence fields; never auto-finalize blindly |
| Inconsistent form layouts across different form types | Reusable "template" schemas, or lean on LLM-based structuring (LangChain) instead of fixed-position parsing |
| Per-page OCR API costs add up | Usage quotas per user, caching, and batch processing instead of one call per page where avoidable |
| Storage growth over time | Object storage (S3/Blob) with lifecycle/archival policies instead of storing files in the DB |
| Sensitive data in forms (PII) | Encryption at rest, strict row-level access control, clear data-retention/delete options for users |
| LLM hallucination during structuring | Strict Pydantic schema validation on every LangChain output; treat the LLM's output as a draft the user confirms, not a final answer |

## Next Steps

This document is meant to be a blueprint, not the build itself. When you're ready, the actual React frontend, the FastAPI backend, the database migrations, or the LangChain/LangGraph pipeline can be scaffolded one piece at a time.
