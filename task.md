# task.md
> Short-term technical checklist for the current active task.
> 
> **How to use:**
> - Break down the "Active Task" from `progress.md` into actionable technical steps.
> - Mark with `[x]` when completed.
> - Mark with `[/]` when in progress.
> - Clear and recreate this file when moving to a completely new Phase/Epic.

---

## Current Epic: Phase 2.1 — Auto-Extract Company & Role

### 1. Extractor Function
- [x] In `modules/analyzer.py`, create `extract_company_and_role(raw_text: str, api_key: str) -> dict`
- [x] Craft a prompt instructing Gemini 2.0 Flash Lite to extract the company name and job title from the text and return valid JSON (e.g., `{"company": "...", "role": "..."}`).
- [x] Use the provided Gemini API key specifically for this function.

### 2. UI Refactor
- [x] In `app.py`, remove the `company_name` and `role_name` `st.text_input` fields.
- [x] Update the JD text area to indicate the user should paste the *entire* raw text (Company, Title, and Description).
- [x] When the Analysis button is clicked, call `extract_company_and_role` first.
- [x] Display the extracted company and role to the user (e.g., using `st.info`).
- [x] Use the extracted data when calling `save_application` for the tracker.
