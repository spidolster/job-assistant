# task.md
> Short-term technical checklist for the current active task.
> 
> **How to use:**
> - Break down the "Active Task" from `progress.md` into actionable technical steps.
> - Mark with `[x]` when completed.
> - Mark with `[/]` when in progress.
> - Clear and recreate this file when moving to a completely new Phase/Epic.

---

## Current Epic: Phase 2.2 — Fix JD Parser Model & Resume Upload/Tracker

### 1. Config — Pindah Auto-Extract Key ke `.env`
- [x] Tambah `get_gemini_extract_key()` di `config.py`
- [x] Hapus hardcode API key dari `app.py`, ganti pakai fungsi baru
- [x] Tambah `GEMINI_EXTRACT_API_KEY` di `.env`

### 2. Storage — Handle duplikat resume
- [x] Ubah `save_resume()` agar handle duplikat filename (return ID existing)
- [x] Tambah `sync_resumes_from_disk()` untuk register file PDF yang belum ada di DB

### 3. App — Refactor resume upload flow
- [x] Perbaiki flow: resume auto-save saat analisis, hindari duplikat
- [x] Pastikan `resume_id` selalu terisi saat save ke tracker
- [x] Pastikan `resume_text` selalu terisi dari upload baru atau DB
- [x] Hapus tombol "Simpan Resume" terpisah, resume otomatis tersimpan saat analisis
- [x] Panggil `sync_resumes_from_disk()` saat startup

### 4. Switch JD Parser to DeepSeek
- [x] Ubah `extract_company_and_role` dari Gemini ke DeepSeek
- [x] Update `app.py` (hapus Gemini extract key dependency)
- [x] Test CLI extraction → PT Tokopedia (GoTo Group) / Senior Data Analyst ✅

### 5. QA Testing
- [x] App load & resume dropdown
- [x] Sidebar settings (provider, model, key)
- [x] Tab navigation
- [x] Full analysis flow (resume + JD → result)
- [x] Auto-extract company & role
- [x] Tracker saves entry
- [x] Fix Streamlit deprecation warning (`use_container_width` → `width`)

### 6. Phase 2.3 — Fix Match Score Saving
- [x] Tambah `extract_match_score(text)` dengan RegExp di `analyzer.py`
- [x] Implementasi passthrough score real ke tracker di `app.py`
- [x] Verifikasi muncul di tabel My Tracker

### 7. Documentation & Setup
- [x] Buat file `README.md` tentang cara setup dan menjalankan project
- [x] Install dependensi (`requirements.txt`) agar `streamlit` bisa dijalankan

### 8. Phase 2.4 — Python 3.14 Compatibility Fix
- [x] Upgrade `openai` (v1.14.x incompatible with httpx di Python 3.14 karena keyword `proxies`)
- [x] Test re-run server Streamlit

### 9. Version Control
- [/] Push semua perubahan ke GitHub


### 10. Phase 2.5 — Salary Range di Tracker
- [x] Tambah kolom `salary_range` pada tabel `applications` (+ migration aman untuk DB existing)
- [x] Implement `extract_salary_range(jd_text)` di analyzer
- [x] Simpan hasil parse salary range saat save ke tracker
- [x] Tampilkan kolom "Salary Range" di tab My Tracker
- [x] Validasi compile + smoke test parsing


### 11. Project Health Check — Error & Documentation Consistency
- [x] Audit smoke test script (`test_extract.py`) dan hilangkan hardcoded credential
- [x] Samakan dokumentasi README dengan implementasi extractor saat ini (DeepSeek)
- [x] Jalankan validasi cepat (`compileall`, smoke test extraction)


### 12. Test Strategy Discussion (pre-implementation)
- [x] Revert commit test suite yang dibuat tanpa persetujuan user
- [x] Diskusikan best practice desain test (unit/integration/e2e + scope tiap layer)
- [x] Sepakati prioritas test pertama sebelum implementasi (parser critical)

- [x] Dokumentasikan draft strategi testing terpusat di `docs/testing_strategy.md`

- [x] Implement tahap 1: unit test parser (`extract_match_score`, `extract_salary_range`)
- [x] Implement tahap 2: integration test tracker/storage (SQLite temp DB)

- [x] Sepakati batas: test non-urgent ditunda, kembali ke core task

- [x] Hardening integration tests: restore patched global paths (`DB_PATH`, `DB_DIR`, `_RESUMES_DIR`) di tearDown untuk mencegah flaky side effects
- [ ] Sepakati prioritas test pertama sebelum implementasi

- [x] Dokumentasikan draft strategi testing terpusat di `docs/testing_strategy.md`
