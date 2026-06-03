# Job Analyzer 🎯

> Analyze your job fit instantly — upload your CV, paste a job description, and discover your match score, skill gaps, and learning roadmap.

🔗 **Live Demo:** [job-analyzer-yuli.streamlit.app](https://job-analyzer-yuli.streamlit.app)

---

## What It Does

Job Analyzer helps job seekers understand how well they match a job posting before applying. It extracts skills from your CV, compares them to job requirements, and gives you:

- **Match score** (0–100%)
- **Skills you already have** ✓
- **Skills you're missing** ✗
- **Estimated learning time** for each gap
- **Personal job tracker** to manage your applications

---

## Screenshots

| Login | Analysis | Tracker |
|-------|----------|---------|
| Secure auth with email | AI-powered match score | Track all your applications |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit |
| **Backend** | FastAPI (Python) |
| **AI / LLM** | Groq API (LLaMA 3.3 70B) |
| **Database** | Supabase (PostgreSQL) |
| **Auth** | Supabase Auth |
| **CV Parsing** | pdfplumber |
| **CI/CD** | GitHub Actions |
| **Deployment** | Streamlit Cloud + Render |

---

## Features

- 📄 **CV Upload** — Upload your PDF resume and auto-extract all technical skills
- ➕ **Manual Skill Addition** — Add skills not detected in the CV
- 🤖 **AI Analysis** — LLaMA 3.3 analyzes job fit with context-aware matching
- 📊 **Match Score** — Visual percentage with progress bar
- 📚 **Learning Roadmap** — Estimated time to learn each missing skill
- 🔐 **User Authentication** — Each user sees only their own data
- 📋 **Application Tracker** — Save jobs with status (applied/pending/interview/accepted/rejected)
- 🗑️ **Status Updates** — Update application status in real-time
- ⏰ **Auto Logout** — Session expires after 30 minutes of inactivity

---

## Architecture

```
User (Browser)
      │
      ▼
Streamlit Cloud          ← Frontend UI
      │
      ▼
Render (FastAPI)         ← REST API
      │
      ├──► Supabase      ← Database + Auth
      │
      └──► Groq API      ← LLM (LLaMA 3.3)
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/analyze` | Analyze job fit |
| `POST` | `/extract-skills` | Extract skills from CV |
| `GET` | `/applications` | Get user's saved jobs |
| `POST` | `/applications` | Save a new job |
| `PUT` | `/applications/{id}` | Update job status |
| `DELETE` | `/applications/{id}` | Delete a job |

Full API docs: [job-analyzer-oi1o.onrender.com/docs](https://job-analyzer-oi1o.onrender.com/docs)

---

## Running Locally

### Prerequisites
- Python 3.9+
- Groq API key (free at [console.groq.com](https://console.groq.com))
- Supabase project (free at [supabase.com](https://supabase.com))

### Setup

```bash
# Clone the repo
git clone https://github.com/yuliiix/job-analyzer
cd job-analyzer

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Fill in your API keys
```

### Environment Variables

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
GROQ_API_KEY=your_groq_api_key
```

### Run

```bash
# Terminal 1 — Backend
uvicorn main:app --reload

# Terminal 2 — Frontend
streamlit run streamlit_app.py
```

---

## Testing

```bash
pytest
```

Tests include:
- **Unit tests** — `calculate_match` function
- **Integration tests** — API routes
- **E2E tests** — Full user flow

---

## CI/CD

Every push to `main` triggers GitHub Actions:

1. ✅ Code formatting check (Black)
2. ✅ Run all tests (pytest)
3. 🚀 Auto-deploy to Streamlit Cloud + Render

---

## Known Limitations

> ⚠️ **Session Persistence:** Due to Streamlit's session architecture, a full page refresh requires re-login. This is a known Streamlit limitation — the fix would require migrating the frontend to React with localStorage support.

> ⏳ **Cold Start:** The Render free tier spins down after inactivity. The first request after idle may take ~30 seconds.

---

## What I Learned

Building this project, I learned and implemented:

- **FastAPI** — REST API design, Pydantic validation, async endpoints
- **Groq API (LLaMA)** — LLM integration, prompt engineering, JSON-structured outputs
- **Supabase** — PostgreSQL database, Row-Level Security, JWT authentication
- **pdfplumber** — PDF text extraction
- **CI/CD** — GitHub Actions pipeline with formatting, testing, and deployment
- **Streamlit** — Rapid UI development, session state management, custom CSS
- **Deployment** — Multi-service cloud architecture (Streamlit Cloud + Render)

---

## Author

**Yuli Ittah** — Computer Science Student @ Bar-Ilan University

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Yuli_Ittah-blue?logo=linkedin)](https://il.linkedin.com/in/yuli-ittah-802b5429a)
[![GitHub](https://img.shields.io/badge/GitHub-yuliiix-black?logo=github)](https://github.com/yuliiix)