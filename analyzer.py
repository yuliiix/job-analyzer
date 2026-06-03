import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

def calculate_match(job_skills: list, user_skills: list) -> int:
    if not job_skills:
        return 0
    matching = [skill for skill in user_skills if skill in job_skills]
    score = len(matching) / len(job_skills) * 100
    return int(score)

async def analyze_job(description: str, user_skills: list) -> dict:
    prompt = f"""
    תיאור משרה: {description}
    כישורי המועמדת: {user_skills}
    
    נתח את ההתאמה והחזר JSON בלבד עם השדות:
    - match_score: מספר בין 0-100
    - missing_skills: רשימת כישורים חסרים
    - time_to_learn: מילון עם זמן לימוד לכל כישור חסר
    """
    try:
        response = model.generate_content(prompt)
        result = json.loads(response.text)
        return result
    except Exception as error:
        return {
            "match_score": 0,
            "missing_skills": [],
            "time_to_learn": {}
        }