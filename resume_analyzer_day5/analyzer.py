import os
import re
import json
import time
import logging
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import HTTPException

load_dotenv()
logger = logging.getLogger(__name__)

api_key = os.getenv("API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

client = OpenAI(api_key=api_key, base_url="https://models.inference.ai.azure.com")

KNOWN_SKILLS = [
    "Python", "SQL", "PostgreSQL", "MySQL", "MongoDB", "FastAPI", "Django", "Flask",
    "Docker", "Kubernetes", "AWS", "Azure", "GCP", "Git", "Linux", "REST API",
    "JavaScript", "TypeScript", "React", "Node.js", "Java", "Spring Boot", "C++",
    "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch", "Machine Learning",
    "Deep Learning", "NLP", "LLM", "OpenAI", "LangChain", "RAG", "Redis", "Kafka",
    "CI/CD", "Jenkins", "Terraform", "HTML", "CSS", "Excel", "Power BI", "Tableau"
]

def estimate_tokens(text: str) -> int:
    return len(text) // 4

def calculate_cost(prompt_tokens: int, completion_tokens: int) -> float:
    cost = ((prompt_tokens / 1_000_000) * 0.15) + ((completion_tokens / 1_000_000) * 0.60)
    return round(cost, 6)

def _extract_skills(text: str) -> list:
    found = []
    text_lower = text.lower()
    for skill in KNOWN_SKILLS:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, text_lower):
            found.append(skill)
    return found

def _local_deterministic_analysis(resume_text: str, job_description: str) -> dict:
    lines = [line.strip() for line in resume_text.strip().splitlines() if line.strip()]
    candidate_name = lines[0][:40] if lines else "Candidate"
    if len(candidate_name.split()) > 4:
        candidate_name = "Candidate"

    jd_skills = _extract_skills(job_description)
    res_skills = _extract_skills(resume_text)

    if not jd_skills:
        jd_skills = res_skills[:3] if res_skills else ["Python", "SQL"]

    matched = [s for s in jd_skills if s in res_skills]
    missing = [s for s in jd_skills if s not in res_skills]

    score = int(round((len(matched) / len(jd_skills)) * 100)) if jd_skills else 50
    reasoning = (
        f"Matched {len(matched)} of {len(jd_skills)} required skills "
        f"({', '.join(matched) if matched else 'none'})."
    )

    p_tokens = estimate_tokens(resume_text + job_description)
    c_tokens = 65
    return {
        "candidate_name": candidate_name,
        "score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "reasoning": reasoning,
        "token_usage": {
            "prompt_tokens": p_tokens,
            "completion_tokens": c_tokens,
            "total_tokens": p_tokens + c_tokens
        },
        "estimated_cost_usd": calculate_cost(p_tokens, c_tokens)
    }

def analyze_resume_with_llm(resume_text: str, job_description: str, request_id: str) -> dict:
    if estimate_tokens(resume_text) > 3500:
        logger.warning(f"[{request_id}] Token limit exceeded")
        raise HTTPException(status_code=413, detail="Resume exceeds maximum token limit.")

    system_prompt = (
        "You are an objective technical recruiter. Extract skills from the resume and compare with the job description. "
        "Respond ONLY in valid JSON with exact keys: "
        '{"candidate_name": "string", "score": int, "matched_skills": ["str"], "missing_skills": ["str"], "reasoning": "short string"}'
    )
    user_prompt = f"JD:\n{job_description}\n\nResume:\n{resume_text}"

    max_retries = 2
    for attempt in range(max_retries + 1):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.0,
                max_tokens=500,
                timeout=8.0
            )
            raw_text = response.choices[0].message.content
            data = json.loads(raw_text)

            usage = response.usage
            p_tokens = usage.prompt_tokens if usage else 0
            c_tokens = usage.completion_tokens if usage else 0
            t_tokens = usage.total_tokens if usage else 0

            data["token_usage"] = {
                "prompt_tokens": p_tokens,
                "completion_tokens": c_tokens,
                "total_tokens": t_tokens
            }
            data["estimated_cost_usd"] = calculate_cost(p_tokens, c_tokens)
            return data

        except json.JSONDecodeError:
            logger.error(f"[{request_id}] Invalid JSON on attempt {attempt + 1}")
            if attempt == max_retries:
                raise HTTPException(status_code=502, detail="AI returned invalid JSON format.")
        except Exception as e:
            logger.warning(f"[{request_id}] Falling back to local analyzer due to upstream error: {e}")
            return _local_deterministic_analysis(resume_text, job_description)