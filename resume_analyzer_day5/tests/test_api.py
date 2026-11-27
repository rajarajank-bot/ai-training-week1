import json
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def make_mock_response(payload: dict):
    mock_resp = MagicMock()
    mock_resp.choices = [MagicMock(message=MagicMock(content=json.dumps(payload)))]
    mock_resp.usage = MagicMock(prompt_tokens=80, completion_tokens=40, total_tokens=120)
    return mock_resp

def test_health():
    res = client.get("/health")
    assert res.status_code == 200

@patch("analyzer.client.chat.completions.create")
def test_analyze_success(mock_create):
    mock_create.return_value = make_mock_response({
        "candidate_name": "Karthik",
        "score": 82,
        "matched_skills": ["Python", "SQL"],
        "missing_skills": ["Docker"],
        "reasoning": "Good match."
    })
    res = client.post("/analyze", data={"job_description": "Python SQL Docker", "resume_text": "Karthik Python SQL"})
    assert res.status_code == 200
    assert res.json()["score"] == 82

@patch("analyzer.client.chat.completions.create")
def test_invalid_json_then_success(mock_create):
    bad = MagicMock()
    bad.choices = [MagicMock(message=MagicMock(content="not-a-json"))]
    good = make_mock_response({
        "candidate_name": "Meena",
        "score": 90,
        "matched_skills": ["FastAPI"],
        "missing_skills": [],
        "reasoning": "Strong FastAPI."
    })
    mock_create.side_effect = [bad, good]

    res = client.post("/analyze", data={"job_description": "FastAPI", "resume_text": "Meena FastAPI"})
    assert res.status_code == 200
    assert res.json()["candidate_name"] == "Meena"

def test_empty_file():
    res = client.post(
        "/analyze",
        data={"job_description": "Python"},
        files={"resume_file": ("empty.txt", b"", "text/plain")}
    )
    assert res.status_code == 400

def test_wrong_file_type():
    res = client.post(
        "/analyze",
        data={"job_description": "Python"},
        files={"resume_file": ("virus.exe", b"1234", "application/octet-stream")}
    )
    assert res.status_code == 400