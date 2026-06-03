import os
import json
import pdfplumber
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"


def calculate_match(job_skills: list, user_skills: list) -> int:
    if not job_skills:
        return 0
    matching = [skill for skill in user_skills if skill in job_skills]
    score = len(matching) / len(job_skills) * 100
    return int(score)


async def analyze_job(description: str, user_skills: list) -> dict:
    prompt = f"""
    תיאור משרה: {description}
    כישורי המועמד: {user_skills}
    
    נתח את ההתאמה והחזר JSON בלבד עם השדות:
    - match_score: מספר בין 0-100
    - missing_skills: רשימת כישורים חסרים
    - time_to_learn: מילון עם זמן לימוד לכל כישור חסר
    """
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as error:
        print("ERROR:", error)
        return {"match_score": 0, "missing_skills": [], "time_to_learn": {}}


def extract_text_from_pdf(pdf_file) -> str:
    with pdfplumber.open(pdf_file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
        return text


async def extract_skills_from_cv(cv_text: str) -> list[str]:
    prompt = f"""
    זהו טקסט של קורות חיים:
    {cv_text}
    
    החזר JSON בלבד — רשימת כישורים טכניים:
    {{"skills": ["Python", "FastAPI", ...]}}
    """
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
        )
        result = json.loads(response.choices[0].message.content)
        return result.get("skills", [])
    except Exception as e:
        print("ERROR:", e)
        return []