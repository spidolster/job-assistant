"""
tracker.py — Manage application tracking histories in the database.
"""
from modules.db import get_db_connection

def save_application(role: str, company: str, jd_text: str, resume_id: int, match_score: int, analysis_result: str) -> int:
    """
    Save an application tracking record.
    Returns:
        The ID of the newly inserted application.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO applications (role, company, jd_text, resume_id, Match_score, analysis_result)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (role, company, jd_text, resume_id, match_score, analysis_result))
    
    app_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return app_id

def get_all_applications() -> list[dict]:
    """
    Get all application records, joining with resumes to get the resume filename.
    Returns:
        List of dicts representing the applications.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT 
            a.id, a.role, a.company, a.Match_score, a.created_at, 
            r.filename as resume_filename
        FROM applications a
        LEFT JOIN resumes r ON a.resume_id = r.id
        ORDER BY a.created_at DESC
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(r) for r in rows]

def get_application_by_id(app_id: int) -> dict:
    """
    Get full details of a specific application.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT 
            a.*, r.filename as resume_filename
        FROM applications a
        LEFT JOIN resumes r ON a.resume_id = r.id
        WHERE a.id = ?
    """
    cursor.execute(query, (app_id,))
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else None

def delete_application(app_id: int) -> bool:
    """Delete an application record."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM applications WHERE id = ?", (app_id,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False
