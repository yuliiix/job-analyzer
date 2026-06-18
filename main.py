from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from models import JobRequest, AnalysisResponse, Application
from analyzer import analyze_job, extract_text_from_pdf, extract_skills_from_cv
from database import (
    save_application,
    get_applications,
    update_status,
    delete_application,
)
import io
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

app = FastAPI()


def get_user_id(authorization: str) -> str:
    try:
        token = authorization.replace("Bearer ", "")
        user = supabase.auth.get_user(token)
        return user.user.id
    except Exception:
        raise HTTPException(status_code=401, detail="לא מורשה")


@app.post("/analyze")
async def analyze(job: JobRequest):
    result = await analyze_job(job.description, job.user_skills)
    return result


@app.get("/applications")
def get_all_applications(authorization: str = Header(...)):
    user_id = get_user_id(authorization)
    return get_applications(user_id)


@app.post("/applications")
def create_application(application: Application, authorization: str = Header(...)):
    user_id = get_user_id(authorization)
    return save_application(application, user_id)


@app.put("/applications/{id}")
def update_application_status(id: int, status: str):
    return update_status(id, status)


@app.delete("/applications/{id}")
def delete_app(id: int):
    return delete_application(id)


@app.post("/extract-skills")
async def extract_skills_from_upload(file: UploadFile = File(...)):
    contents = await file.read()
    pdf_file = io.BytesIO(contents)
    cv_text = extract_text_from_pdf(pdf_file)
    skills = await extract_skills_from_cv(cv_text)
    return {"skills": skills}

@app.get("/health")
def health():
    return {"status": "ok"}