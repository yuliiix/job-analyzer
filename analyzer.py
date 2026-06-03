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
    job_lower = [s.lower().strip() for s in job_skills]
    user_lower = [s.lower().strip() for s in user_skills]
    matching = [s for s in user_lower if s in job_lower]
    score = len(matching) / len(job_lower) * 100
    return int(score)


async def analyze_job(description: str, user_skills: list) -> dict:
    prompt = f"""
You are an expert job matching analyst.

Job description:
{description}

Candidate skills:
{user_skills}

Instructions:
- Compare skills case-insensitively (e.g. "Python" == "python")
- Consider partial matches and related skills (e.g. "VMware vSphere" counts if candidate has "VMware")
- Consider experience-based skills (e.g. system administration experience covers basic IT tasks)
- Be generous but accurate — if the candidate clearly has the skill in a different form, count it as a match
- missing_skills should only include skills the candidate genuinely lacks
- time_to_learn should consider the candidate's existing background

Return ONLY a JSON object with these exact fields:
{{
  "match_score": <number 0-100>,
  "missing_skills": [<list of skills the candidate truly lacks>],
  "time_to_learn": {{<skill>: <estimated time considering candidate background>}}
}}
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
You are an expert CV analyst.

CV text:
{cv_text}

Extract ALL technical and professional skills from this CV.
Include: programming languages, frameworks, tools, platforms, methodologies, certifications, soft skills relevant to tech roles.
Be thorough — extract skills even if mentioned in experience descriptions, not just in a skills section.

Return ONLY a JSON object:
{{
  "skills": [<list of skills as strings>]
}}
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
