# MEMORY.md
> Long-term project memory. Updated by AI or Ari when important decisions are made.
> Load this file at the start of any new session on this project.
> ⚠️ Jika file ini > 150 baris, arsipkan entry lama ke `MEMORY_ARCHIVE.md`.

---

## Project Identity

- **Project name**: Job Assistant (job_assistant)
- **Client / For**: Ari Wahyudi — personal use, job seeking
- **Started**: 2026-03-12
- **Status**: [x] Active  [ ] On Hold  [ ] Completed

---

## Stack Decisions

> Why did we choose X over Y? Record it here so we never debate it again.

| Decision | What We Chose | Why |
|---|---|---|
| Language | Python | Ari's strength, works for all phases |
| UI (Phase 1-2) | Streamlit | Dead simple, pure Python, fast prototyping |
| UI (Phase 3+) | React/Next.js + FastAPI backend | Richer UI, mobile-friendly, scalable |
| Database (Phase 1) | File lokal | Belum perlu DB untuk MVP |
| Database (Phase 2) | SQLite | Ringan, cukup untuk 1 user |
| Database (Phase 3+) | PostgreSQL | Multi-user, cloud-ready |
| AI API | TBD | Belum dipilih (DeepSeek / OpenAI / lainnya) |

---

## Key Files & Folders

> Help the AI navigate without exploring every time.

| Path | What It Is |
|---|---|
| `job_assistant/app.py` | Entry point Streamlit |
| `job_assistant/modules/` | Semua logika bisnis (analysis, builder, dll) |
| `job_assistant/data/my_resume/` | Master resume Ari |
| `job_assistant/.env` | API keys |

---

## Architecture Roadmap

> Evolusi dari MVP ke Platform.

| Phase | Arsitektur | UI | DB | Effort |
|---|---|---|---|---|
| 1.0 - MVP ✅ | Streamlit monolith | Streamlit | File lokal | 1-2 hari |
| 1.5 - UX Polish 🔄 | Streamlit monolith | Streamlit | File lokal | 1-2 hari |
| 2 - Feature-rich | Streamlit + modules | Streamlit | SQLite | 1-2 minggu |
| 3 - Separated | FastAPI + Frontend | React/Next.js | SQLite/PostgreSQL | 2-4 minggu |
| 4 - Platform | Modular + Workers | Full Web App | PostgreSQL | Ongoing |

**Aturan Emas:** Pisahkan logika bisnis dari UI sejak Phase 1. `modules/` tidak boleh import Streamlit.

---

## Important Context

> Facts the AI must know to work correctly on this project.

- Sumber data utama: Resume (PDF) + Job Description (teks/PDF)
- MVP fokus: Match score antara resume & JD (strengths, gaps, rekomendasi)
- Semua fitur masa depan (builder, tracker, research, interview prep) dibangun di atas 2 sumber data ini
- Bahasa output: Indonesia (kecuali diminta lain)

---

## Lessons Learned

> Mistakes made, dead ends explored, things that didn't work.

---

## People & Roles (if collaborative)

| Name | Role | Contact |
|---|---|---|
| Ari Wahyudi | Owner / Lead | - |

---

## Lessons Learned

- Phase numbering: fitur yang masih pakai file lokal = Phase 1.x, bukan Phase 2. Phase 2 dimulai ketika arsitektur berubah (SQLite).

---

*Last updated: 2026-03-12*
