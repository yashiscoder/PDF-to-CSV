# AI-Powered Handwritten Form Digitizer
### Placement Project Specification — 100% Free-Tier Stack

## Table of Contents
1. [Why This Project](#why-this-project)
2. [Skill-Demand Coverage Map](#skill-demand-coverage-map)
3. [Objectives](#objectives)
4. [100%-Free Tech Stack](#100-free-tech-stack)
5. [Feature Set by Build Phase](#feature-set-by-build-phase)
6. [The AI Core: RAG / LangChain / LangGraph / Vector DB](#the-ai-core-rag--langchain--langgraph--vector-db)
7. [System Architecture](#system-architecture)
8. [Processing Pipeline](#processing-pipeline)
9. [Database Schema](#database-schema)
10. [REST API Design](#rest-api-design)
11. [Suggested Project Structure](#suggested-project-structure)
12. [Free-Tier Setup Notes & Gotchas](#free-tier-setup-notes--gotchas)
13. [Security Checklist](#security-checklist)
14. [Build Roadmap & Time Budget](#build-roadmap--time-budget)
15. [Resume Bullets & Interview Prep](#resume-bullets--interview-prep)
16. [Key Challenges & Mitigations](#key-challenges--mitigations)
17. [Next Steps](#next-steps)

---

## Why This Project

This build is scoped around what Indian AI Engineering job postings are actually screening for right now, based on the JD research you shared (342 postings, last 90 days): RAG at 89%, LangChain at 82%, FastAPI at 76%, vector databases at 71%, prompt engineering at 64%, Docker at 61%, cloud deployment at 58%, and LangGraph/multi-agent systems at 49%. Instead of a generic CRUD app, every major feature below maps to one of those lines — so the finished project is simultaneously your GitHub portfolio piece, your resume evidence, and your interview story.

## Skill-Demand Coverage Map

| Skill (JD demand, from your research) | Status in this project | Where it lives |
|---|---|---|
| RAG — 89% | **Core** | "Ask your forms" natural-language search over extracted data (Phase 3) |
| LangChain — 82% | **Core** | Structuring raw OCR text into validated JSON (Phase 2) |
| FastAPI — 76% | **Core** | The entire backend |
| Vector DBs — 71% | **Core** | `pgvector`, storing an embedding for every processed form |
| Prompt Engineering — 64% | **Core** | Structured extraction prompts, documented and iterated in `PROMPTS.md` |
| Docker — 61% | **Core** | Backend + Postgres containerized via `docker-compose` |
| AWS / GCP Deployment — 58% | **Core (free-tier)** | Live deploy — see the deployment options below |
| LangGraph / Multi-Agent — 49% | **Recommended** | Confidence-based review-routing workflow (Phase 4) |
| Langfuse / Observability — 28% | **Easy differentiator** | Tracing on the LangChain/LangGraph pipeline — cheap to add, rare enough that most other candidates won't have it |
| LoRA / QLoRA Fine-tuning — 37% | **Stretch goal** | Optional: fine-tune a small open model on your own review-correction data (Phase 6) |

> Percentages are from the research you provided, not independently re-verified by me — treat them as directional signal for what to prioritize, not exact statistics to cite.

## Objectives

- [ ] Secure auth: register/login, credentials hashed and stored in Postgres
- [ ] Upload a handwritten form (image or PDF) from the React frontend
- [ ] Extract fields via a pretrained OCR/handwriting API
- [ ] **Structure** the raw extraction with LangChain into validated, typed JSON
- [ ] Let the user review/correct low-confidence fields before finalizing
- [ ] Generate and save a CSV; store the original as a PDF
- [ ] Embed extracted text and enable **RAG** search across a user's form history
- [ ] Route the review decision through a **LangGraph** state graph, not an if/else
- [ ] Containerize with **Docker** and deploy live on a free tier
- [ ] Instrument the AI pipeline with **Langfuse** so you can show real traces in an interview

## 100%-Free Tech Stack

| Layer | Free tool | Free-tier reality check |
|---|---|---|
| Frontend | React (Vite) + Tailwind → **Vercel** or Netlify | Free forever for personal projects, no card required for the hobby tier |
| Backend hosting | FastAPI → **Render** free web service (or GCP Cloud Run free tier if you specifically want "GCP" on your resume) | Render's free tier sleeps after inactivity — first request after sleeping takes 30–60s. Fine for a demo, just don't be surprised mid-interview |
| Database | PostgreSQL → **Supabase** (or Neon) | Supabase free tier: 500MB database + 1GB file storage + `pgvector`, all bundled. **Free projects pause after 7 days with zero requests** — set up a free scheduled ping (GitHub Actions cron hitting a health-check endpoint) so it's alive whenever a recruiter clicks your link |
| File storage | Supabase Storage (bundled with the DB above) | 1GB free — plenty for form images/PDFs/CSVs at project scale |
| Auth | Self-built JWT (`python-jose` + `passlib[bcrypt]`) | $0, and a stronger resume line than an off-the-shelf auth provider |
| OCR / handwriting | **Azure AI Document Intelligence** (F0 free tier) | 500 pages/month free. Only reads the first 2 pages per document and caps files at 4MB — a non-issue for single-page handwritten forms. **Requires a card on file to create the Azure account**, even though F0 itself won't charge you; set a $0 spending alert as a safety net |
| OCR alternative | Google Cloud Vision | Also has a monthly free quota — check current terms in the console before relying on it, since these shift |
| LLM (LangChain structuring + RAG answers) | **Google Gemini API** (Flash/Flash-Lite) or **Groq** (Llama/Qwen models) | Both genuinely free, **no credit card required**. Gemini: ~1,500 requests/day on Flash, resets at midnight Pacific. Groq: ~30 req/min, up to ~14,400 req/day, very fast inference on their LPU hardware. Use Groq for demo-day speed, Gemini if you want a slightly stronger model |
| Embeddings (for RAG) | `sentence-transformers` (runs locally) | Completely free, no rate limits — keeps embeddings off any paid API entirely |
| Vector store | `pgvector` inside the same Supabase Postgres | No separate vector DB service to run or pay for |
| Observability | **Langfuse Cloud** free tier | No card required, generous quota for a portfolio project. Full self-hosting is also free but needs its own Postgres + ClickHouse + Redis stack — overkill here |
| Containerization | Docker + docker-compose | Free, open source — this alone covers your "Docker" resume line |

> Free-tier terms change. These were verified in August 2026 — recheck each provider's current limits before a big test run or before you rely on the demo staying up during placement season.

## Feature Set by Build Phase

*(See [Build Roadmap](#build-roadmap--time-budget) for suggested time budgets per phase.)*

### Phase 1 — Core MVP
1. Register/login with JWT (self-built)
2. Upload a handwritten form (image or PDF) with drag-and-drop
3. Send it to the OCR API, store the raw response
4. Generate a CSV, store the original as a PDF
5. Save file paths + metadata to Postgres, scoped to the logged-in user
6. Dashboard listing past uploads with download links

### Phase 2 — LangChain + Prompt Engineering
1. Pass raw OCR text through a LangChain chain with a Pydantic output parser to get validated, typed fields
2. Attach a per-field confidence score
3. Build an editable review table in the frontend for low-confidence fields
4. Keep a `PROMPTS.md` documenting your prompt iterations — this *is* the "prompt engineering" line on your resume, and interviewers will ask you to walk through it

### Phase 3 — RAG + Vector DB
1. Embed each document's extracted text (`sentence-transformers`, free, local)
2. Store vectors in `pgvector`
3. Build a natural-language "ask your forms" endpoint + a simple chat UI
4. This is your single highest-value phase — 89% of the JDs you scanned want exactly this skill

### Phase 4 — LangGraph
1. Model the pipeline (OCR → structure → confidence check → auto-finalize *or* human review) as an actual state graph
2. Same behavior as a plain if/else, but now it's a genuine "stateful, multi-step workflow" you can defend in an interview

### Phase 5 — Docker + Cloud Deployment
1. Dockerize the backend + Postgres via `docker-compose`
2. Deploy: frontend → Vercel, backend → Render or GCP Cloud Run, DB → Supabase
3. Put the live link at the top of your GitHub README — recruiters click that before they read code

### Phase 6 — Stretch Goals (only if time allows)
1. **Langfuse tracing** on the LangChain/LangGraph pipeline — cheap to add (a few lines), and only 28% of JDs mention it, so it's a genuine differentiator
2. **LoRA/QLoRA fine-tuning** — fine-tune a small open model (e.g. Qwen2.5-1.5B or Llama-3.2-1B/3B) with [Unsloth](https://github.com/unslothai/unsloth) on a free Colab T4 GPU. Notice this dataset writes itself: every field a user corrects in your Phase 2 review screen is a training example (`raw OCR text → corrected structured value`) — a genuinely nice "the system improves itself over time" story for an interview

## The AI Core: RAG / LangChain / LangGraph / Vector DB

### LangChain — cleaning up what the OCR API gives you
A handwriting API returns raw text or loose key-value pairs, never a guaranteed schema. LangChain's prompt templates plus a Pydantic output parser force that raw text through an LLM and back into a strict, typed object:

```python
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq   # free, no card — swap for langchain_google_genai for Gemini
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

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
chain = prompt | llm | parser
structured = chain.invoke({"ocr_text": raw_ocr_output})
```

### LangGraph — the review/approval workflow
A high-confidence extraction should save automatically; a low-confidence one should stop and wait for a human. That's a branching, stateful workflow — exactly what LangGraph models:

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
Embed each document's extracted text, store the vectors in `pgvector`, and let the user query in plain language:

```python
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")  # local, $0 per call
vectorstore = PGVector(
    embeddings=embeddings,
    connection=DATABASE_URL,   # your Supabase connection string
    collection_name="user_documents",
)
vectorstore.add_texts(
    texts=[extracted_text],
    metadatas=[{"user_id": user_id, "document_id": doc_id}],
)

retriever = vectorstore.as_retriever(search_kwargs={"filter": {"user_id": user_id}})
results = retriever.invoke("forms with an address in California")
```

### Langfuse — tracing the pipeline (Phase 6)
```python
from langfuse.langchain import CallbackHandler

langfuse_handler = CallbackHandler()  # reads keys from env vars, free Langfuse Cloud project

structured = chain.invoke(
    {"ocr_text": raw_ocr_output},
    config={"callbacks": [langfuse_handler]},
)
```
Check Langfuse's current docs for the exact integration path when you build this — SDKs shift their APIs fairly often.

### Where *not* to use an LLM
Don't route simple, rule-based checks (is this field empty? is this a valid date format?) through an LLM call — a Pydantic validator or a regex is faster, cheaper, and deterministic. Save LangChain for genuinely fuzzy interpretation and LangGraph for orchestration where the path actually branches. An interviewer who asks "why not just use an LLM for everything?" wants to hear this answer.

## System Architecture

```
┌──────────────────┐      ┌───────────────────┐
│  React Frontend   │─────▶│  FastAPI Backend   │
│ (Vite + Tailwind) │ REST │ Auth / Upload /    │
│  on Vercel        │ JWT  │ Pipeline Orchestr. │
│                   │      │  on Render/Cloud Run│
└──────────────────┘      └─────────┬──────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │                      │                      │
              ▼                      ▼                      ▼
     ┌─────────────────┐   ┌──────────────────┐   ┌───────────────────┐
     │ Supabase Postgres │   │  OCR / HTR API   │   │ Supabase Storage   │
     │ users, documents  │   │ (Azure Document  │   │ PDFs + CSVs        │
     │ extracted_fields  │   │  Intelligence)   │   └───────────────────┘
     │ pgvector          │   └──────────────────┘
     └─────────────────┘
              ▲
              │  structured data, embeddings, traces
     ┌────────┴──────────┐
     │  LangChain +       │
     │  LangGraph         │
     │ (structuring,      │
     │  review routing,   │
     │  RAG retrieval)     │
     │ ── traced by ──▶ Langfuse
     └────────────────────┘
```

## Processing Pipeline

1. **Upload** — user drags/selects an image or PDF in the React app; frontend checks file type and size.
2. **Validate & store original** — backend saves it to Supabase Storage, creates a `documents` row with `status = 'pending'`.
3. **OCR** — backend sends the file to Azure Document Intelligence, which returns raw text plus any key-value pairs/tables it found.
4. **Structuring (LangChain)** — raw OCR output → validated JSON via the Pydantic output parser, with a per-field confidence score.
5. **Routing (LangGraph)** — high-confidence results move straight to step 7; low-confidence ones are flagged `needs_review`.
6. **Human review (if flagged)** — user sees an editable table with low-confidence fields highlighted, corrects anything wrong.
7. **CSV generation** — confirmed structured data is written to a CSV.
8. **Persist** — CSV + normalized PDF saved to Supabase Storage; paths and field values saved to Postgres; `status = 'completed'`.
9. **Embed for RAG** — extracted text is embedded and stored in `pgvector`.
10. **Done** — document appears in the dashboard with PDF/CSV download links and is now searchable via chat.

## Database Schema

```sql
-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,   -- bcrypt hash, NEVER plaintext
    created_at TIMESTAMP DEFAULT NOW()
);

-- Uploaded forms
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    original_filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(10) NOT NULL,          -- 'image' | 'pdf'
    original_file_path TEXT NOT NULL,        -- storage path, not the file itself
    pdf_path TEXT,
    csv_path TEXT,
    status VARCHAR(20) DEFAULT 'pending',    -- pending|processing|needs_review|completed|failed
    avg_confidence FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Structured, per-field extracted data
CREATE TABLE extracted_fields (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    field_name VARCHAR(100) NOT NULL,
    field_value TEXT,
    confidence FLOAT,
    was_edited BOOLEAN DEFAULT FALSE          -- true if the user corrected it — this is your LoRA training signal
);

-- Embeddings for RAG (pgvector extension, included on Supabase free tier)
CREATE TABLE document_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    chunk_text TEXT,
    embedding VECTOR(384)   -- 384 dims for all-MiniLM-L6-v2; adjust if you pick a different embedding model
);
```

> Store the *files* in Supabase Storage and the *path* in the row above — storing large binaries directly in Postgres works for a toy demo but bloats the database fast.

## REST API Design

```
Auth
POST   /api/auth/register       Create a new account
POST   /api/auth/login          Authenticate, return access + refresh tokens
POST   /api/auth/refresh        Exchange a refresh token for a new access token
GET    /api/auth/me             Current user's profile

Documents
POST   /api/documents/upload        Upload a handwritten form (multipart/form-data)
GET    /api/documents               List the user's documents (paginated)
GET    /api/documents/{id}          Document detail + extracted fields
PATCH  /api/documents/{id}/fields   Correct one or more extracted field values
GET    /api/documents/{id}/pdf      Download the stored PDF
GET    /api/documents/{id}/csv      Download the generated CSV
DELETE /api/documents/{id}          Delete a document and its files

Chat / RAG  (Phase 3)
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
│   │   │   └── ChatPanel.jsx
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── DocumentReview.jsx
│   │   │   └── History.jsx
│   │   ├── context/AuthContext.jsx
│   │   ├── services/api.js
│   │   └── App.jsx
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── api/{auth,documents,chat}.py
│   │   ├── core/{config,security}.py
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/
│   │   │   ├── ocr_service.py
│   │   │   ├── csv_service.py
│   │   │   ├── langchain_pipeline.py
│   │   │   ├── langgraph_workflow.py
│   │   │   └── rag_service.py
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml
├── PROMPTS.md          # your prompt-engineering iteration log
└── README.md           # live demo link goes at the very top
```

## Free-Tier Setup Notes & Gotchas

These are the specific things that trip people up — worth reading before you start, not after you hit a wall:

- **Azure requires a card, even for F0.** It won't charge you under 500 pages/month, but set a ₹1/$1 billing alert in the Azure portal as a tripwire.
- **Supabase free projects pause after 7 days of no requests.** During placement season, your demo link needs to be reliably up. Add a free GitHub Actions workflow that pings a health-check endpoint every few days.
- **Render's free backend sleeps when idle** and takes 30–60s to wake on the first request. Either accept this (and mention it in your README so it doesn't look broken) or use the same keep-alive ping.
- **Don't enable billing on the same Gemini/Google Cloud project you're using for the free tier** — it silently removes the free quota on that project. If you ever add a paid key for something else, use a separate project.
- **Gemini's free-tier terms allow Google to use your prompts/outputs to improve their models.** Fine for a demo with sample/dummy forms — don't run real people's sensitive documents (ID numbers, medical info) through the free tier.
- **Groq and Gemini genuinely don't require a card** — if you want to avoid entering payment details anywhere, lean on those two for the LLM layer and Google Cloud Vision (rather than Azure) for OCR.

## Security Checklist

- [ ] Hash passwords with bcrypt — never store plaintext
- [ ] Short-lived JWT access tokens + refresh tokens in httpOnly cookies (not `localStorage`)
- [ ] Validate file type and size on both frontend and backend
- [ ] Use an ORM with parameterized queries (SQLAlchemy) to prevent SQL injection
- [ ] Restrictive CORS policy (only your deployed frontend's origin)
- [ ] Rate-limit auth and upload endpoints
- [ ] Secrets in environment variables, never committed — add `.env` to `.gitignore` before your first commit
- [ ] Row-level access control — a user only sees their own documents
- [ ] "How would you secure this for production?" is a near-guaranteed interview question — be ready to talk through this list even for the parts you didn't fully implement

## Build Roadmap & Time Budget

Rough estimates for evenings/weekends alongside other placement prep — adjust to your own pace:

| Phase | Focus | Rough time |
|---|---|---|
| 1 | Core MVP (auth, upload, OCR, CSV, storage) | 1–2 weeks |
| 2 | LangChain structuring + review UI | 3–5 days |
| 3 | RAG + vector search | 3–5 days |
| 4 | LangGraph workflow | 2–4 days |
| 5 | Docker + live deployment | 2–3 days |
| 6 | Langfuse tracing (do this) | ~1 day |
| 6 | LoRA/QLoRA fine-tuning (optional) | 1–2 weeks |

**If you're tight on time:** Phases 1–5 alone already cover RAG, LangChain, FastAPI, vector DBs, prompt engineering, Docker, and cloud deployment — the top 7 skills in your research. Treat Langfuse as a cheap add-on and LoRA as genuinely optional; don't let it eat into DSA/CS-fundamentals prep, which off-campus interviews still screen for hard.

## Resume Bullets & Interview Prep

Fill in real numbers once you've actually tested the project — don't put fabricated metrics on a resume:

- "Built a full-stack AI document pipeline (React, FastAPI, PostgreSQL) extracting structured data from handwritten forms via Azure Document Intelligence OCR and LangChain-based structured output parsing, achieving **[X]%** field-level accuracy on a **[N]**-form test set."
- "Implemented a RAG pipeline with `pgvector` and sentence-transformer embeddings enabling natural-language search across a user's document history."
- "Designed a LangGraph workflow that routes low-confidence extractions to human review, reducing **[manual-review rate / error rate]** by **[X]%**."
- "Containerized with Docker and deployed on [Render/GCP Cloud Run] with a live demo; added Langfuse tracing to monitor latency, cost, and structured-output failures across the LLM pipeline."

**Questions to be ready for:**
- Walk me through what happens end-to-end when a user uploads a form.
- Why LangGraph instead of if/else logic? *(state persistence, human-in-the-loop, resumability)*
- How do you handle a bad OCR extraction? *(confidence scoring + mandatory review, never silent auto-correct)*
- Why `pgvector` instead of Pinecone/Weaviate? *(one database instead of two services; be ready to discuss when a dedicated vector DB would actually matter — very large scale, advanced hybrid search)*
- How would this scale to 10,000 users? *(queueing, per-user rate limits, batch OCR calls)*
- What would you change for production? *(encryption at rest, stricter access control, paid OCR/LLM tiers, real monitoring — your Security Checklist, basically)*

## Key Challenges & Mitigations

| Challenge | Mitigation |
|---|---|
| Handwriting OCR accuracy varies (cursive, messy writing) | Confidence scoring + mandatory human review for low-confidence fields |
| Free-tier rate limits during a demo or bulk test | Batch carefully, cache results, don't re-run the same file through the API repeatedly while testing |
| Inconsistent form layouts | Lean on LLM-based structuring (LangChain) rather than fixed-position parsing |
| Sensitive data in test forms | Use synthetic/dummy forms for your demo, not real people's documents, given free-tier data-usage terms |
| LLM hallucination during structuring | Strict Pydantic schema validation on every LangChain output; treat it as a draft the user confirms |

## Next Steps

This document is the blueprint. When you're ready to start building, the React frontend, FastAPI backend, database migrations, or the LangChain/LangGraph pipeline can be scaffolded one piece at a time — Phase 1 first.
