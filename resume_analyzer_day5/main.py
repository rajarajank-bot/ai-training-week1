import uuid
import io
import asyncio
import logging
from typing import Optional, List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pypdf import PdfReader
from analyzer import analyze_resume_with_llm

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Resume Analyzer API", version="1.0.0")

ALLOWED_EXTENSIONS = {".pdf", ".txt"}
MAX_FILE_SIZE = 2 * 1024 * 1024

def extract_text(filename: str, content: bytes) -> str:
    fname = filename.lower()
    if fname.endswith(".txt"):
        return content.decode("utf-8", errors="ignore").strip()
    elif fname.endswith(".pdf"):
        try:
            reader = PdfReader(io.BytesIO(content))
            return "\n".join(page.extract_text() or "" for page in reader.pages).strip()
        except Exception:
            raise HTTPException(status_code=400, detail="Corrupted or unreadable PDF file.")
    raise HTTPException(status_code=400, detail="Unsupported file type. Only .pdf and .txt allowed.")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze(
    job_description: str = Form(...),
    resume_text: Optional[str] = Form(None),
    resume_file: Optional[UploadFile] = File(None)
):
    request_id = str(uuid.uuid4())[:8]
    logger.info(f"[{request_id}] /analyze called")

    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty.")

    text = ""
    if resume_file and resume_file.filename:
        if not any(resume_file.filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
            raise HTTPException(status_code=400, detail="Invalid file type. Upload .pdf or .txt")
        
        content = await resume_file.read()
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File exceeds 2MB size limit.")
            
        text = extract_text(resume_file.filename, content)
    elif resume_text and resume_text.strip():
        text = resume_text.strip()
    else:
        raise HTTPException(status_code=400, detail="Provide either resume_file or resume_text.")

    if not text:
        raise HTTPException(status_code=422, detail="No readable text found in resume.")

    result = analyze_resume_with_llm(text, job_description, request_id)
    result["request_id"] = request_id
    return result

@app.post("/analyze-batch")
async def analyze_batch(
    job_description: str = Form(...),
    files: List[UploadFile] = File(...)
):
    semaphore = asyncio.Semaphore(2)

    async def worker(file: UploadFile):
        async with semaphore:
            req_id = str(uuid.uuid4())[:8]
            content = await file.read()
            text = extract_text(file.filename, content)
            return await asyncio.to_thread(analyze_resume_with_llm, text, job_description, req_id)

    results = await asyncio.gather(*(worker(f) for f in files), return_exceptions=True)
    return {"results": [str(r) if isinstance(r, Exception) else r for r in results]}