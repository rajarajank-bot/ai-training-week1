import time
from analyzer import analyze_resume_with_llm

golden_set = [
    {"text": "Name: Arun. Skills: Python, FastAPI, PostgreSQL", "expected": ["python", "fastapi", "postgresql"]},
    {"text": "Name: Divya. Skills: React, JavaScript, HTML, CSS", "expected": ["react", "javascript", "html", "css"]},
    {"text": "Name: Bala. Skills: Java, Spring Boot, MySQL", "expected": ["java", "spring boot", "mysql"]},
    {"text": "Name: Sneha. Skills: Python, Pandas, Machine Learning", "expected": ["python", "pandas", "machine learning"]},
    {"text": "Name: Raj. Skills: Docker, Kubernetes, AWS", "expected": ["docker", "kubernetes", "aws"]},
    {"text": "Name: Kavya. Skills: Node.js, Express, MongoDB", "expected": ["node.js", "express", "mongodb"]},
    {"text": "Name: Mani. Skills: C++, Linux, Git", "expected": ["c++", "linux", "git"]},
    {"text": "Name: Anu. Skills: SQL, Excel, PowerBI", "expected": ["sql", "excel", "powerbi"]},
]

jd = "Looking for a software engineer with Python, FastAPI, PostgreSQL, React, JavaScript, Java, Spring Boot, MySQL, Pandas, Machine Learning, Docker, Kubernetes, AWS, Node.js, Express, MongoDB, C++, Linux, Git, SQL, Excel, PowerBI."

precisions, recalls, run1_scores, run2_scores = [], [], [], []

for idx, item in enumerate(golden_set):
    res1 = analyze_resume_with_llm(item["text"], jd, f"eval-1-{idx}")
    time.sleep(1.5)
    res2 = analyze_resume_with_llm(item["text"], jd, f"eval-2-{idx}")
    time.sleep(1.5)

    extracted = {s.lower() for s in res1.get("matched_skills", [])}
    expected = set(item["expected"])

    tp = len(extracted & expected)
    precision = tp / len(extracted) if extracted else 0
    recall = tp / len(expected) if expected else 0

    precisions.append(precision)
    recalls.append(recall)
    run1_scores.append(res1.get("score", 0))
    run2_scores.append(res2.get("score", 0))

avg_precision = round(sum(precisions) / len(precisions), 2)
avg_recall = round(sum(recalls) / len(recalls), 2)
avg_score_diff = round(sum(abs(a - b) for a, b in zip(run1_scores, run2_scores)) / len(run1_scores), 2)

print(f"Skill Extraction Precision: {avg_precision}")
print(f"Skill Extraction Recall: {avg_recall}")
print(f"Average Score Difference between 2 runs: {avg_score_diff}")