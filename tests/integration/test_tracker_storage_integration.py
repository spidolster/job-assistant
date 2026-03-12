"""Integration tests for storage/tracker/database with temporary SQLite DB."""

from __future__ import annotations

import io
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

# Ensure `modules.*` imports resolve exactly like app runtime.
PROJECT_APP_ROOT = Path(__file__).resolve().parents[2] / "job_assistant"
if str(PROJECT_APP_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_APP_ROOT))

from modules import db, storage, tracker  # type: ignore  # noqa: E402


class _FakeUploadedFile(io.BytesIO):
    """Small UploadedFile-like object for storage integration tests."""

    def __init__(self, name: str, payload: bytes) -> None:
        super().__init__(payload)
        self.name = name

    def getvalue(self) -> bytes:
        return super().getvalue()


class TestTrackerStorageIntegration(unittest.TestCase):
    """Validate storage + tracker behavior over a temporary SQLite database."""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_path = Path(self.temp_dir.name)

        db.DB_DIR = self.base_path / "data"
        db.DB_PATH = db.DB_DIR / "job_assistant_test.db"
        storage._RESUMES_DIR = self.base_path / "resumes"

        db.init_db()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_save_resume_duplicate_returns_existing_id(self) -> None:
        uploaded = _FakeUploadedFile("resume.pdf", b"fake-pdf-binary")

        with patch("modules.storage.extract_text_from_uploaded_pdf", return_value="resume text"):
            first = storage.save_resume(uploaded, custom_name="ari_resume")

        uploaded.seek(0)
        with patch("modules.storage.extract_text_from_uploaded_pdf", return_value="resume text"):
            second = storage.save_resume(uploaded, custom_name="ari_resume")

        self.assertIsNotNone(first["id"])
        self.assertEqual(first["id"], second["id"])
        self.assertEqual(first["filename"], "ari_resume.pdf")
        self.assertEqual(second["filename"], "ari_resume.pdf")

        conn = db.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM resumes")
        count = cursor.fetchone()["count"]
        conn.close()

        self.assertEqual(count, 1)

    def test_tracker_save_and_read_application(self) -> None:
        uploaded = _FakeUploadedFile("resume.pdf", b"fake-pdf-binary")

        with patch("modules.storage.extract_text_from_uploaded_pdf", return_value="resume text"):
            resume = storage.save_resume(uploaded, custom_name="ari_tracker")

        app_id = tracker.save_application(
            role="Senior Data Analyst",
            company="PT Maju Jaya",
            jd_text="Membutuhkan SQL, Python, dashboarding",
            resume_id=resume["id"],
            match_score=87,
            salary_range="Rp 10 juta - Rp 15 juta / bulan",
            analysis_result="Kandidat cocok dan butuh peningkatan komunikasi stakeholder",
        )

        rows = tracker.get_all_applications()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["id"], app_id)
        self.assertEqual(rows[0]["resume_filename"], "ari_tracker.pdf")
        self.assertEqual(rows[0]["salary_range"], "Rp 10 juta - Rp 15 juta / bulan")

        detail = tracker.get_application_by_id(app_id)
        self.assertIsNotNone(detail)
        self.assertEqual(detail["company"], "PT Maju Jaya")
        self.assertEqual(detail["role"], "Senior Data Analyst")
        self.assertEqual(detail["Match_score"], 87)

    def test_init_db_migrates_legacy_applications_table(self) -> None:
        db.DB_DIR.mkdir(parents=True, exist_ok=True)
        raw_conn = sqlite3.connect(str(db.DB_PATH))
        cursor = raw_conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS resumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT UNIQUE NOT NULL,
                content_text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                company TEXT NOT NULL,
                jd_text TEXT NOT NULL,
                resume_id INTEGER,
                Match_score INTEGER,
                analysis_result TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (resume_id) REFERENCES resumes (id)
            )
            """
        )
        raw_conn.commit()
        raw_conn.close()

        db.init_db()

        check_conn = db.get_db_connection()
        check_cursor = check_conn.cursor()
        check_cursor.execute("PRAGMA table_info(applications)")
        columns = [row["name"] for row in check_cursor.fetchall()]
        check_conn.close()

        self.assertIn("salary_range", columns)


if __name__ == "__main__":
    unittest.main()
