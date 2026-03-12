# progress.md
> Short-term session memory. Updated frequently — after every work session.
> Always load this file when resuming work on this project.

---

## Current Status

> One sentence. Where are we RIGHT NOW?

**Status**: Bug match score pada tracker (skor selalu 0) sudah diperbaiki. Ekstraksi otomatis dari hasil analisis menggunakan RegEx telah diimplementasikan (Phase 2.3).

---

## Active Task

> What is being worked on this session?

- **Task**: Phase 2.4 Fix Python 3.14 Compatibility (openai proxies bug)
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
- [ ] Phase 3: Separated — FastAPI backend + React frontend
- [ ] Phase 4: Platform — Analytics, AI pipeline, background jobs

---

## Last Session Summary

> What was done last time? AI writes this at end of each session.

**Date**: 2026-03-12
- Phase 2.4: Upgrade `openai` package dari `1.14.2` ke `1.50.0+` untuk memperbaiki error `__init__() got an unexpected keyword argument 'proxies'` di Python 3.14.
- Phase 2.3: Fix bug match score selalu 0 di tracker, ekstrak nilai dari LLM output menggunakan Regex
- Phase 2.3: Fix `requirements.txt` (upgrade streamlit & hapus pandas) agar bisa di-install tanpa error build numpy di Windows, lalu jalankan instalasi.
- Tambah file README.md untuk panduan instalasi dan penggunaan aplikasi
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

1. Masukkan API Key (OpenAI atau DeepSeek) ke `.env`
2. Test aplikasi dengan resume PDF asli + JD nyata
3. Evaluasi kualitas output LLM, refine prompt jika perlu
4. Mulai Phase 2 jika puas dengan hasilnya

---

## Blockers

> Anything blocking progress right now?

- [ ] Belum pilih AI API (perlu API key)

---

## Quick Notes

> Random thoughts, ideas, reminders. Clean up weekly.

- Conversation sebelumnya (d744d56d) juga pernah bahas Job-Seeking Assistant tapi pakai stack berbeda (Vite+React+Express). Kali ini kita mulai dari Python-only (Streamlit).

---

*Last updated: 2026-03-12*
