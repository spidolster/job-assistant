# progress.md
> Short-term session memory. Updated frequently — after every work session.
> Always load this file when resuming work on this project.

---

## Current Status

> One sentence. Where are we RIGHT NOW?

**Status**: Phase 2.1 selesai! Fitur auto-extract Company dan Role menggunakan Gemini 2.0 Flash Lite sudah tersambung dan verified di UI.

---

## Active Task

> What is being worked on this session?

- **Task**: Coding Phase 2.1 Auto-Extract Feature
- **Started**: 2026-03-12
- **Target done**: 2026-03-12

---

## Phases Overview

> Check off as completed.

- [x] Phase 1.0: MVP — Resume vs JD Matcher (Streamlit monolith)
- [x] Phase 1.5: UX Polish — Persistent Keys, Model Select, Resume History
- [x] Phase 2.0: Feature-rich — Tracker Dashboard (Streamlit + SQLite)
- [x] Phase 2.1: Auto-Extract — Single JD input, Gemini Flash Lite extraction
- [ ] Phase 3: Separated — FastAPI backend + React frontend
- [ ] Phase 4: Platform — Analytics, AI pipeline, background jobs

---

## Last Session Summary

> What was done last time? AI writes this at end of each session.

**Date**: 2026-03-12
**Done**:
- Phase 2: Integrasi SQLite, tab layout Tracker, dan history lamaran otomatis.
- Phase 2.1: Refactor UI JD menjadi satu *raw input* saja.
- Menambahkan fungsi pemisah otomatis (auto-extract) menggunakan Gemini 2.0 Flash Lite yang mem-parsing nama Perusahaan dan Posisi dalam output JSON.

**Left unfinished**:
- Lakukan test integrasi / real use-case oleh User (kemungkinan Gemini limit 429).
- Eksplorasi Phase 3 (FastAPI/React).

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
