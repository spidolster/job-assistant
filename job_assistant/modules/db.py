import sqlite3
import os
from pathlib import Path

# Database path
DB_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent / "data"
DB_PATH = DB_DIR / "job_assistant.db"

def get_db_connection():
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

def init_db():
    """Initializes the database schema if it doesn't exist."""
    os.makedirs(DB_DIR, exist_ok=True)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create resumes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE NOT NULL,
            content_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create applications table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            company TEXT NOT NULL,
            jd_text TEXT NOT NULL,
            resume_id INTEGER,
            Match_score INTEGER,
            salary_range TEXT,
            analysis_result TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (resume_id) REFERENCES resumes (id)
        )
    """)

    # Lightweight migration for existing database files.
    cursor.execute("PRAGMA table_info(applications)")
    columns = [row[1] for row in cursor.fetchall()]
    if "salary_range" not in columns:
        cursor.execute("ALTER TABLE applications ADD COLUMN salary_range TEXT")

    # Indexes for common query patterns (JOIN on resume_id, ORDER BY created_at).
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_applications_resume_id ON applications(resume_id)"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_applications_created_at ON applications(created_at)"
    )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
