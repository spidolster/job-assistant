# task.md
> Short-term technical checklist for the current active task.
>
> **How to use:**
> - Break down the "Active Task" from `progress.md` into actionable technical steps.
> - Mark with `[x]` when completed.
> - Mark with `[/]` when in progress.
> - Clear and recreate this file when moving to a completely new Phase/Epic.

---

## Current Epic: Phase 3 — Separated (FastAPI backend + React frontend)

### 1. Backend API Foundation (FastAPI)
- [x] Buat entrypoint FastAPI `job_assistant/backend/main.py`
- [x] Tambahkan startup hook (`init_db`, `sync_resumes_from_disk`, `load_config`)
- [x] Tambahkan endpoint dasar: `/health`, `/providers`, `/resumes`, `/tracker`
- [x] Tambahkan endpoint upload resume (`/resumes/upload`) dan analisis (`/analyze`)

### 2. API Schema & Validation
- [x] Definisikan request/response schema Pydantic untuk endpoint analisis
- [x] Validasi error handling: API key missing, resume kosong, API error upstream

### 3. Frontend Foundation (React + Vite)
- [x] Inisialisasi app frontend pada folder `frontend/`
- [x] Implement UI dasar: upload/select resume, form JD, hasil analisis, tracker table
- [x] Integrasikan fetch API ke backend FastAPI

### 4. Tooling & Dependencies
- [x] Tambahkan dependency backend FastAPI ke `requirements.txt`
- [x] Tambahkan dependency frontend React/Vite pada `frontend/package.json`

### 5. Quality Checks
- [x] Tambahkan unit test API minimal (`health`, `analyze success`, `analyze missing API key`)
- [x] Jalankan full test suite Python
- [x] Build frontend produksi (`npm run build`)

### 6. Documentation
- [x] Update README untuk cara menjalankan backend FastAPI + frontend React

### 7. Next Micro-Task
- [ ] Migrasi auth/config setting dari Streamlit sidebar ke halaman setting frontend
- [ ] Tambahkan endpoint detail tracker (`GET /tracker/{id}`) + delete action di UI
- [ ] Siapkan adapter DB agar mudah switch SQLite -> PostgreSQL
