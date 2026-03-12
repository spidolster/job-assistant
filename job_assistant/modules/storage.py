"""
storage.py — Manage local file storage for resumes.
Saves uploaded PDFs to data/resumes/ and lists available files.
"""
import os
import shutil
from pathlib import Path
from datetime import datetime

# Path to the resumes directory
_RESUMES_DIR = Path(__file__).resolve().parent.parent / "data" / "resumes"

def _ensure_resumes_dir():
    """Create the resumes directory if it doesn't exist."""
    _RESUMES_DIR.mkdir(parents=True, exist_ok=True)

def save_resume(uploaded_file, custom_name: str = "") -> str:
    """
    Save an uploaded PDF file to the local resumes directory.
    Args:
        uploaded_file: Streamlit UploadedFile object.
        custom_name: Optional custom filename (without extension).
    Returns:
        The filename that was saved.
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
    
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return filename

def get_saved_resumes() -> list[str]:
    """
    Get a list of saved resume filenames.
    Returns:
        List of PDF filenames in the resumes directory.
    """
    _ensure_resumes_dir()
    files = sorted(
        [f.name for f in _RESUMES_DIR.glob("*.pdf")],
        reverse=True  # newest first (if timestamped)
    )
    return files

def get_resume_path(filename: str) -> str:
    """
    Get the full absolute path to a saved resume.
    Args:
        filename: The resume filename.
    Returns:
        Absolute path string.
    """
    return str(_RESUMES_DIR / filename)

def delete_resume(filename: str) -> bool:
    """
    Delete a saved resume file.
    Args:
        filename: The resume filename to delete.
    Returns:
        True if deleted successfully, False otherwise.
    """
    filepath = _RESUMES_DIR / filename
    try:
        filepath.unlink()
        return True
    except FileNotFoundError:
        return False
