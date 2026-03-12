"""
storage.py — Manage local file storage for resumes and DB records.
Saves uploaded PDFs to data/resumes/ and saves records to SQLite DB.
"""
import os
from pathlib import Path
from datetime import datetime
from modules.db import get_db_connection
from modules.document_utils import extract_text_from_uploaded_pdf

_RESUMES_DIR = Path(__file__).resolve().parent.parent / "data" / "resumes"

def _ensure_resumes_dir():
    """Create the resumes directory if it doesn't exist."""
    _RESUMES_DIR.mkdir(parents=True, exist_ok=True)

def save_resume(uploaded_file, custom_name: str = "") -> dict:
    """
    Save an uploaded PDF file locally and its text to SQLite.
    Returns:
        A dict with 'id' and 'filename'.
    """
    _ensure_resumes_dir()
    
    if custom_name:
        filename = f"{custom_name}.pdf"
    else:
        # Use original filename, prepend timestamp to avoid collisions
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_name = Path(uploaded_file.name).stem
        filename = f"{timestamp}_{original_name}.pdf"
    
    filepath = _RESUMES_DIR / filename
    
    # Save the physical PDF file
    file_bytes = uploaded_file.getvalue()
    with open(filepath, "wb") as f:
        f.write(file_bytes)
    
    # Reset pointer and extract text
    uploaded_file.seek(0)
    text_content = extract_text_from_uploaded_pdf(uploaded_file)
    uploaded_file.seek(0)
    
    # Insert record into database
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO resumes (filename, content_text) VALUES (?, ?)",
            (filename, text_content)
        )
        resume_id = cursor.lastrowid
        conn.commit()
    except Exception as e:
        print(f"Error saving to db: {e}")
        # If DB fails for uniqueness, attempt update (or just ignore for simplicity in MVP)
        resume_id = None
    finally:
        conn.close()
        
    return {"id": resume_id, "filename": filename}

def get_saved_resumes() -> list[dict]:
    """
    Get a list of saved resume records from DB.
    Returns:
        List of dicts: [{'id': 1, 'filename': '...', 'created_at': '...'}, ...]
    """
    _ensure_resumes_dir()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, filename, created_at FROM resumes ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(r) for r in rows]

def get_resume_path(filename: str) -> str:
    """Get the full absolute path to a saved resume PDF."""
    return str(_RESUMES_DIR / filename)

def get_resume_text_from_db(resume_id: int) -> str:
    """Fetch pre-extracted text for a resume directly from the SQLite DB."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT content_text FROM resumes WHERE id = ?", (resume_id,))
    row = cursor.fetchone()
    conn.close()
    return row["content_text"] if row else ""

def delete_resume(resume_id: int, filename: str) -> bool:
    """Delete a saved resume file and DB record."""
    filepath = _RESUMES_DIR / filename
    try:
        # Check if linked to applications (soft restrict instead of hard fail)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM applications WHERE resume_id = ?", (resume_id,))
        count = cursor.fetchone()["count"]
        
        if count > 0:
            conn.close()
            return False # Cannot delete, it has applications history

        # Delete physical file
        if filepath.exists():
            filepath.unlink()
        
        # Delete DB record
        cursor.execute("DELETE FROM resumes WHERE id = ?", (resume_id,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False
