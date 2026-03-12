# task.md
> Short-term technical checklist for the current active task.
> 
> **How to use:**
> - Break down the "Active Task" from `progress.md` into actionable technical steps.
> - Mark with `[x]` when completed.
> - Mark with `[/]` when in progress.
> - Clear and recreate this file when moving to a completely new Phase/Epic.

---

## Current Epic: Phase 1.5 — UX Polish ✅

### 1. API Key Persistence
- [x] Create `modules/config.py` for `.env` management
  - [x] Implement `save_api_key()`
  - [x] Implement `get_api_key()`
- [x] Update `app.py` Sidebar to use persistent API key saving

### 2. LLM Model Selection
- [x] Update `modules/analyzer.py`
  - [x] Make `analyze_resume_vs_jd` accept `model_name`
  - [x] Remove hardcoded models in API calls
- [x] Update `app.py` Sidebar
  - [x] Add model dropdown based on selected provider
  - [x] Pass selected model to analyzer

### 3. Local Resume Storage
- [x] Create `data/resumes/` directory
- [x] Create `modules/storage.py`
  - [x] Implement `save_resume()`
  - [x] Implement `get_saved_resumes()`
- [x] Update `app.py` Main UI
  - [x] Add Resume selection dropdown (History)
  - [x] Add logic to handle new uploads vs selecting existing PDFs
  - [x] Pass the correct file path/object to the text extractor

### 4. Integration & UI Polish
- [x] Test end-to-end flow with saved keys and selected resumes
- [x] Ensure clear error messages (e.g., if a saved resume file is deleted)
