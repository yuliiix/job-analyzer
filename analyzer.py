def calculate_match(job_skills: list, user_skills: list) -> int:
    if not job_skills:
        return 0
    
    matching = [skill for skill in user_skills if skill in job_skills]
    score =len(matching) / len(job_skills) * 100
    return int(score)