from models import JobRequest, AnalysisResponse, Application
from analyzer import analyze_job, extract_text_from_pdf, extract_skills_from_cv
from fastapi import FastAPI, UploadFile, File
import io

from database import (
    save_application,
    get_applications,
    update_status,
    delete_application,
)

app = FastAPI()


# POST /analyze an application
@app.post("/analyze")
async def analyze(job: JobRequest):
    result = await analyze_job(job.description, job.user_skills)
    return result


# GET / get a list of all applications
@app.get("/applications")
def get_all_applications():
    result = get_applications()
    return result


# PUT /applications/{id} - update status of application
@app.put("/applications/{id}")
def update_application_status(id: int, status: str):
    result = update_status(id, status)
    return result


# DELETE /applications/{id} — delete an application
@app.delete("/applications/{id}")
def delete_app(id: int):
    result = delete_application(id)
    return result


@app.post("/applications")
def create_application(application: Application):
    result = save_application(application)
    return result


@app.post("/extract-skills")
async def extract_skills_from_upload(file: UploadFile = File(...)):
    contents = await file.read()
    pdf_file = io.BytesIO(contents)
    cv_text = extract_text_from_pdf(pdf_file)
    skills = await extract_skills_from_cv(cv_text)
    return {"skills": skills}
