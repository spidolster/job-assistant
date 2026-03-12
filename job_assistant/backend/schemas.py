from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    jd_text: str = Field(min_length=1)
    provider: str = "openai"
    model_name: str = ""
    resume_id: int | None = None
    resume_text: str | None = None
    save_to_tracker: bool = True


class AnalyzeResponse(BaseModel):
    analysis_result: str
    company: str
    role: str
    match_score: int
    salary_range: str
    tracker_id: int | None = None
