# AI Resume Analyzer API

## Purpose
An automated FastAPI service that evaluates candidate resumes (PDF/TXT) against a Job Description using LLMs, returning a structured match score, skill gap analysis, reasoning, and token cost.

## Architecture
Client (Swagger/cURL) -> FastAPI (/analyze) -> File Validation & Text Extraction -> LLM (JSON Mode + Retry/Timeout) -> Structured JSON Response

## Setup & Run Steps
1. Clone the repository and open the project folder.
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment: `.\venv\Scripts\activate`
4. Install dependencies: `pip install fastapi uvicorn python-multipart openai python-dotenv pypdf pytest httpx pytest-cov`
5. Copy `.env.example` to `.env` and add your `API_KEY`.
6. Start server: `uvicorn main:app --reload`
7. Open Swagger UI: `http://127.0.0.1:8000/docs`

## Example cURL
```bash
curl -X POST "[http://127.0.0.1:8000/analyze](http://127.0.0.1:8000/analyze)" \
  -F "job_description=Looking for a Python backend developer with FastAPI and PostgreSQL." \
  -F "resume_text=Arun - Python, FastAPI, PostgreSQL developer with 2 years experience."