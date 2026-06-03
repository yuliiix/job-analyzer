from analyzer import calculate_match


def test_perfect_match():
    result = calculate_match(
        job_skills=["Python", "FastAPI"], user_skills=["Python", "FastAPI"]
    )
    assert result == 100


def test_no_match():
    result = calculate_match(
        job_skills=["React", "TypeScript"], user_skills=["Python", "FastAPI"]
    )
    assert result == 0


def test_partial_match():
    result = calculate_match(job_skills=["Python", "React"], user_skills=["Python"])
    assert result == 50


def test_empty_job_skills():
    result = calculate_match(job_skills=[], user_skills=["Python"])
    assert result == 0
