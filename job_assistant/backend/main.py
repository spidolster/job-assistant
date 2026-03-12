"""Phase 3 API layer for Job Assistant (FastAPI)."""

import os
import sys
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

_MAX_UPLOAD_BYTES = 5 * 1024 * 1024  # 5 MB
_MAX_JD_LENGTH = 50_000  # characters
_PDF_MAGIC = b"%PDF"


ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from backend.schemas import AnalyzeRequest, AnalyzeResponse
from modules.analyzer import (
    analyze_resume_vs_jd,
    extract_company_and_role,
    extract_match_score,
    extract_salary_range,
)
from modules.config import AVAILABLE_MODELS, get_api_key, load_config
from modules.db import init_db
from modules.storage import (
    get_resume_text_from_db,
    get_saved_resumes,
    save_resume,
    sync_resumes_from_disk,
)
from modules.tracker import delete_application, get_all_applications, save_application

app = FastAPI(title="Job Assistant API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:5173").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event() -> None:
    init_db()
    sync_resumes_from_disk()
    load_config()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/providers")
def providers() -> dict:
    return {"providers": AVAILABLE_MODELS}


@app.get("/resumes")
def list_resumes() -> list[dict]:
    return get_saved_resumes()


@app.post("/resumes/upload")
async def upload_resume(file: UploadFile = File(...)) -> dict:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File harus PDF")

    content = await file.read()

    if len(content) > _MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=400, detail="Ukuran file melebihi batas 5 MB")

    if not content[:4].startswith(_PDF_MAGIC):
        raise HTTPException(status_code=400, detail="File bukan PDF yang valid")

    class UploadedFileWrapper:
        def __init__(self, name: str, payload: bytes):
            self.name = name
            self._payload = payload

        def getvalue(self) -> bytes:
            return self._payload

        def seek(self, _offset: int) -> None:
            return None

    saved = save_resume(UploadedFileWrapper(file.filename, content), custom_name="")
    if not saved.get("id"):
        raise HTTPException(status_code=500, detail="Gagal menyimpan resume")
    return saved


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest) -> AnalyzeResponse:
    if len(payload.jd_text) > _MAX_JD_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Job description terlalu panjang (maks {_MAX_JD_LENGTH:,} karakter)",
        )

    api_key = get_api_key(payload.provider)
    if not api_key:
        raise HTTPException(
            status_code=400,
            detail=f"API key untuk provider '{payload.provider}' belum diset.",
        )

    resume_text = (payload.resume_text or "").strip()
    if payload.resume_id is not None:
        resume_text = get_resume_text_from_db(payload.resume_id)

    if not resume_text:
        raise HTTPException(status_code=400, detail="Resume text kosong")

    analysis_result = analyze_resume_vs_jd(
        resume_text,
        payload.jd_text,
        provider=payload.provider,
        model_name=payload.model_name,
    )

    if analysis_result.startswith("Error"):
        raise HTTPException(status_code=500, detail=analysis_result)

    extracted = extract_company_and_role(payload.jd_text)
    company_name = extracted.get("company", "Unknown Company")
    role_name = extracted.get("role", "Unknown Role")

    extracted_score = extract_match_score(analysis_result)
    extracted_salary = extract_salary_range(payload.jd_text)

    tracker_id = None
    if payload.save_to_tracker:
        tracker_id = save_application(
            role=role_name,
            company=company_name,
            jd_text=payload.jd_text,
            resume_id=payload.resume_id,
            match_score=extracted_score,
            salary_range=extracted_salary,
            analysis_result=analysis_result,
        )

    return AnalyzeResponse(
        analysis_result=analysis_result,
        company=company_name,
        role=role_name,
        match_score=extracted_score,
        salary_range=extracted_salary,
        tracker_id=tracker_id,
    )


@app.get("/tracker")
def list_tracker() -> list[dict]:
    return get_all_applications()


@app.delete("/tracker/{app_id}")
def remove_tracker(app_id: int) -> dict:
    deleted = delete_application(app_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Data tracker tidak ditemukan")
    return {"deleted": True}
