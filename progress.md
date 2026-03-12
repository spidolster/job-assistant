# progress.md
> Short-term session memory. Updated frequently — after every work session.
> Always load this file when resuming work on this project.

---

## Current Status

> One sentence. Where are we RIGHT NOW?

**Status**: Phase 3 bootstrap selesai: backend FastAPI dan frontend React sudah berjalan end-to-end untuk flow dasar analyze + tracker.

---

## Active Task

> What is being worked on this session?

- **Task**: Phase 3 — Separated architecture bootstrap (FastAPI + React)
- **Started**: 2026-03-12
- **Target done**: 2026-03-12

---

## Phases Overview

> Check off as completed.

- [x] Phase 1.0: MVP — Resume vs JD Matcher (Streamlit monolith)
- [x] Phase 1.5: UX Polish — Persistent Keys, Model Select, Resume History
- [x] Phase 2.0: Feature-rich — Tracker Dashboard (Streamlit + SQLite)
- [x] Phase 2.1: Auto-Extract — Single JD input, Gemini Flash Lite extraction
- [x] Phase 2.2: Bugfix — Fix resume upload/tracker flow, isolate extract key
- [x] Phase 2.5: Tracker Enhancement — Salary Range parsing dari JD
- [/] Phase 3: Separated — FastAPI backend + React frontend
- [ ] Phase 4: Platform — Analytics, AI pipeline, background jobs

---

## Last Session Summary

> What was done last time? AI writes this at end of each session.


**Date**: 2026-03-12
- Mulai eksekusi Phase 3: tambah layer backend FastAPI (`job_assistant/backend/main.py`) dengan endpoint health, providers, resumes, analyze, dan tracker.
- Tambah schema Pydantic untuk payload analisis (`job_assistant/backend/schemas.py`) agar validasi request/response lebih rapi.
- Inisialisasi frontend React + Vite (`frontend/`) dengan UI dasar untuk upload/select resume, input JD, hasil analisis, dan tabel tracker.
- Sinkronkan dependency: update `requirements.txt` (fastapi, uvicorn, python-multipart) dan tambahkan `frontend/package.json`.
- Tambah unit test API di `tests/unit/test_phase3_api.py` (health + analyze success + missing API key).
- Validasi implementasi: full Python test suite lulus (16 test), frontend build sukses, dan screenshot UI Phase 3 berhasil diambil.
**Date**: 2026-03-12
- Jalankan audit baseline: `pytest -q`, `compileall`, dan smoke test `test_extract.py` untuk memetakan kesehatan project saat ini.
- Temukan inkonsistensi storage: re-upload resume dengan `custom_name` yang sama dapat menimpa file fisik meski record DB tetap lama.
- Fix `save_resume()`: early-return jika `custom_name` sudah ada, gunakan timestamp microseconds + guard collision untuk upload normal, dan batasi fallback exception ke `sqlite3.IntegrityError`.
- Perkuat integration test duplicate resume: verifikasi file asli tidak tertimpa pada upload duplikat.
- Revert commit test suite otomatis karena user meminta diskusi strategi testing dulu sebelum ada perubahan kode baru.
- Tindak lanjuti blocker merge dengan hardening integration test: restore global path (`db.DB_DIR`, `db.DB_PATH`, `storage._RESUMES_DIR`) di tearDown agar tidak meninggalkan side effect lintas test.
- Rapikan log test duplicate resume dengan patch `print` agar output CI lebih bersih.
- Sepakati batas eksekusi testing: berhenti setelah area urgent tercakup (parser + tracker/storage), dan tunda test non-urgent agar scope tetap rapi.
- Implement tahap 2 integration tests di `tests/integration/test_tracker_storage_integration.py` untuk alur storage/tracker berbasis SQLite temporary DB.
- Tambah skenario integration: duplicate handling `save_resume`, save/read application via tracker, dan migration legacy schema untuk `salary_range`.
- Jalankan ulang suite `python -m unittest discover -s tests -v` (13 test) dan semua lulus.
- Sepakati prioritas implementasi test pertama: parser kritikal (`extract_match_score`, `extract_salary_range`) agar eksekusi tetap pelan dan fokus risiko tertinggi.
- Tambah test unit terpusat di `tests/unit/test_analyzer_parsers.py` untuk parser score/salary (10 test case) + setup package discovery (`tests/__init__.py`, `tests/unit/__init__.py`).
- Jalankan test suite `python -m unittest discover -s tests -v` dan semua test lulus.
- Rumuskan draft best practice testing yang menekankan test terpusat di modul/folder terpisah (`tests/`) agar tidak berceceran.
- Dokumentasikan blueprint sederhana tapi efektif untuk scaling di `docs/testing_strategy.md` (unit/integration/e2e, risk-based priority, mocking policy).
- Audit project end-to-end untuk error/inkonsistensi dan kecocokan dokumentasi.
- Perbaiki `test_extract.py`: hapus hardcoded API key, perbaiki signature function call agar sesuai implementasi terbaru, dan tambah warning saat env key belum tersedia.
- Koreksi README agar fitur extractor konsisten (DeepSeek-only untuk auto-extract company/role).
- Jalankan validasi `compileall` dan smoke test `python test_extract.py`.
- Phase 2.5: Tambah kolom `salary_range` di DB `applications` + migration `ALTER TABLE` otomatis jika DB lama belum punya kolom.
- Phase 2.5: Implement parsing salary range dari JD (`extract_salary_range`) dan simpan ke tracker saat analisis.
- Phase 2.5: Tampilkan kolom "Salary Range" di tabel My Tracker dan ambil dari query SQLite.
- Phase 2.4: Upgrade `openai` package dari `1.14.2` ke `1.50.0+` untuk memperbaiki error `__init__() got an unexpected keyword argument 'proxies'` di Python 3.14.
- Phase 2.3: Fix bug match score selalu 0 di tracker, ekstrak nilai dari LLM output menggunakan Regex
- Phase 2.3: Fix `requirements.txt` (upgrade streamlit & hapus pandas) agar bisa di-install tanpa error build numpy di Windows, lalu jalankan instalasi.
- Tambah file README.md untuk panduan instalasi dan penggunaan aplikasi
- Version Control: Commit (fix regex match score & openai deps) dan Push ke GitHub
- Phase 2.2: Fix resume upload → tracker flow (3 bugs diperbaiki)
- Switch JD parser dari Gemini (key leaked) ke DeepSeek (`deepseek-chat`)
- `sync_resumes_from_disk()` — auto-register existing PDFs ke SQLite saat startup
- Handle duplikat resume di `storage.py` (return existing ID instead of None)
- Refactor `app.py`: hapus tombol simpan terpisah, auto-save saat analisis, tracker selalu menyimpan
- QA Testing 8/8 passed: load, dropdown, JD input, sidebar, tabs, analysis, extraction, tracker
- Fix Streamlit deprecation warning (`use_container_width` → `width`)

**Left unfinished**:
- Test upload resume baru (belum ditest, hanya saved resume yang ditest)
- Eksplorasi Phase 3 (FastAPI/React)

---

## Next Session — Start Here

> First thing to do when resuming. Be specific.

1. Tambahkan halaman Settings di frontend untuk simpan provider/model/API key (menggantikan sidebar Streamlit)
2. Tambahkan endpoint detail tracker (`GET /tracker/{id}`) dan aksi delete/edit dari UI React
3. Mulai desain lapisan data access agar transisi SQLite -> PostgreSQL minim perubahan modul bisnis
4. Review parity fitur Streamlit vs React dan buat checklist migrasi fitur yang belum pindah

## Blockers

> Anything blocking progress right now?

- [ ] Belum pilih AI API (perlu API key)

---

## Quick Notes

> Random thoughts, ideas, reminders. Clean up weekly.

- Conversation sebelumnya (d744d56d) juga pernah bahas Job-Seeking Assistant tapi pakai stack berbeda (Vite+React+Express). Kali ini kita mulai dari Python-only (Streamlit).

---

*Last updated: 2026-03-12 (session update: merge blocker handled via test hardening)*
*Last updated: 2026-03-12 (session update: testing strategy discussion draft documented)*
*Last updated: 2026-03-12 (session update: health check + resume overwrite fix)*
*Last updated: 2026-03-12 (session update: moved test_extract.py from root to scripts/)*
