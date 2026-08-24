# 📝 Handwritten Form to CSV Web Application

<div align="center">

![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?style=for-the-badge&logo=postgresql)
![LangChain](https://img.shields.io/badge/LangChain-AI-green?style=for-the-badge)
![LangGraph](https://img.shields.io/badge/LangGraph-Workflow-purple?style=for-the-badge)
![OCR](https://img.shields.io/badge/OCR-Handwriting%20Recognition-orange?style=for-the-badge)

### AI-Powered Handwritten Form Processing & CSV Generation

Upload handwritten forms, extract structured data using OCR and AI, review extracted fields, and export them as CSV while maintaining a secure document history.

---

## 📖 Overview

The **Handwritten Form to CSV Web Application** is a full-stack AI-powered platform that converts handwritten forms into structured CSV files.

Users can upload handwritten images or PDF documents, where an OCR engine extracts text and AI organizes it into structured fields. Before finalizing, users can review and edit the extracted information to ensure accuracy. Every uploaded document, along with its generated CSV, is securely stored and linked to the user's account for future access. fileciteturn1file0L26-L37

---

# ✨ Features

### 🔐 User Authentication

- User Registration
- Secure Login
- JWT Authentication
- Password Encryption
- User Profile
- Logout

### 📄 Document Upload

- Upload Images (JPG, PNG)
- Upload PDF Documents
- Drag & Drop Upload
- File Validation
- Live Preview

### 🤖 AI & OCR Processing

- Handwriting Recognition
- OCR Text Extraction
- Automatic Field Detection
- Confidence Score Generation
- AI-based Data Structuring

### ✍ Review & Correction

- Editable Extracted Fields
- Highlight Low-Confidence Values
- Human Verification
- Auto Validation

### 📊 Export Options

- CSV Export
- Excel Export *(Future)*
- JSON Export *(Future)*

### 📂 Document Management

- Upload History
- Search Documents
- Download PDF
- Download CSV
- Delete Documents

### 🧠 AI Features

- LangChain Structured Output
- LangGraph Workflow
- RAG-powered Document Search
- Natural Language Querying
- Semantic Search

---

# 🏗 System Architecture

```
User
   │
   ▼
React Frontend
   │
REST API
   │
FastAPI Backend
   │
────────────────────────────────────────
│            │             │
▼            ▼             ▼
OCR API   PostgreSQL   File Storage
│            │             │
▼            ▼             ▼
LangChain → LangGraph → CSV Generator
                    │
                    ▼
              User Dashboard
```

---

# 🛠 Tech Stack

## Frontend

- React (Vite)
- Tailwind CSS
- React Query
- Context API

## Backend

- FastAPI
- Python
- SQLAlchemy
- Alembic

## Database

- PostgreSQL
- pgvector

## Authentication

- JWT
- Passlib (bcrypt)

## AI & Machine Learning

- Azure AI Document Intelligence
- LangChain
- LangGraph
- OpenAI
- RAG

## Storage

- AWS S3
- Azure Blob Storage
- Local Storage (Development)

---

# ⚙ Workflow

1. User registers and logs in.
2. Upload a handwritten image or PDF.
3. OCR extracts handwritten text.
4. LangChain converts raw OCR output into structured JSON.
5. LangGraph decides whether the extraction should be automatically accepted or sent for manual review.
6. User reviews and edits extracted fields if needed.
7. The application generates a CSV file.
8. Original PDF and CSV are stored securely.
9. Document appears in the user's dashboard.
10. Users can download, search, or query previous documents. fileciteturn1file0L202-L211

---

# 📁 Project Structure

```
handwritten-form-app/
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   └── context/
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── db/
│   │   └── core/
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml
├── README.md
└── .env
```

---

# 📦 Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/handwritten-form-app.git

cd handwritten-form-app
```

---

## Backend Setup

```bash
cd backend

python -m venv venv

source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

---

## Frontend Setup

```bash
cd frontend

npm install
```

---

## Environment Variables

Create a `.env` file:

```env
DATABASE_URL=

JWT_SECRET_KEY=

AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=

AZURE_DOCUMENT_INTELLIGENCE_KEY=

OPENAI_API_KEY=

STORAGE_BACKEND=local
```

---

## Start Backend

```bash
uvicorn app.main:app --reload
```

---

## Start Frontend

```bash
npm run dev
```

---

# 📡 REST API

## Authentication

```
POST   /api/auth/register

POST   /api/auth/login

POST   /api/auth/logout

GET    /api/auth/me
```

## Documents

```
POST   /api/documents/upload

GET    /api/documents

GET    /api/documents/{id}

PATCH  /api/documents/{id}/fields

GET    /api/documents/{id}/pdf

GET    /api/documents/{id}/csv

DELETE /api/documents/{id}
```

## AI Chat

```
POST /api/chat/query
```

---

# 🚀 Future Enhancements

- Multi-page document support
- Batch document processing
- Email verification
- Password reset
- Excel export
- JSON export
- Mobile application
- Voice commands
- Custom form templates
- Multi-language handwriting support
- Offline OCR model
- AI-powered anomaly detection

---

# 🔒 Security Features

- Password Hashing (bcrypt)
- JWT Authentication
- Secure File Validation
- SQL Injection Protection
- HTTPS Support
- Rate Limiting
- Environment Variable Management
- Row-Level Authorization
- Encrypted File Storage

---

# 📸 Screenshots

### Login

> Add Screenshot

### Dashboard

> Add Screenshot

### Upload Page

> Add Screenshot

### OCR Results

> Add Screenshot

### CSV Export

> Add Screenshot

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature-name
```

3. Commit changes

```bash
git commit -m "Added new feature"
```

4. Push to GitHub

```bash
git push origin feature-name
```

5. Open a Pull Request

---

# 📜 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Yash Kumawat**

🎓 MCA Student | AI & Machine Learning Enthusiast

- LinkedIn: https://linkedin.com/in/kumawatyash
- Portfolio: https://yashiscoder.github.io/Hii/

---

## ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.

It motivates further development and helps others discover the project.

---
**Built with ❤️ using React, FastAPI, OCR, LangChain, LangGraph, and AI.**