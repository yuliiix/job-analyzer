from pydantic import BaseModel
from typing import Optional

class JobRequest(BaseModel):
    description: str
    user_skills: list[str]

class AnalysisResponse(BaseModel):
    match_score: int
    missing_skills: list[str]
    time_to_learn: dict

class Application(BaseModel):
    id: Optional[int] = None
    company: str
    status: str
    match_score: int