# AGENTS.md
> Last updated: March 2026

## Universal Agent Directives
- **Primary Instruction File**: This `AGENTS.md` file serves as the definitive central configuration for *all* AI coding agents (including Gemini, Claude, ChatGPT, Cursor, GitHub Copilot, etc.). 
- **Mitigation for Agent-Specific Files**: If you as an AI typically look for `GEMINI.md`, `CLAUDE.md`, `.cursorrules`, or similar agent-specific rule files, you must treat this `AGENTS.md` as your ultimate source of truth. Do not request, expect, or generate a separate file for your specific model. All global behavioral rules and memory protocols are consolidated here.

## Who I Am
Ari Wahyudi — Senior Data Analyst + Freelance Consultant, Bontang, East Kalimantan, ID.

## Code Style
- Python: PEP8, type hints, comment non-obvious logic
- JavaScript: vanilla first
- General: simple > clever, working > elegant

## Permissions
- ✅ Free to do: read/write code, analyze files, suggest improvements
- ⚠️ Ask first: install packages, push to Git, call paid APIs, delete files
- ❌ Never: hardcode credentials, use nested subqueries, assume English output

---

## Memory Protocol

### Session START (always, automatically):
1. Read `MEMORY.md` — load project context, stack decisions, and rules.
2. Read `progress.md` — know current status, active phase, and blockers.
3. Read `task.md` — check the exact technical steps left to do.
4. Confirm: `"Memory loaded. Last status: [X]. Next micro-task: [Y]."`

### Session END (always, automatically):
1. Update `task.md` — check off completed items.
2. Update `progress.md` — summarize what was done in the session.
3. Update `MEMORY.md` — only if a new major decision or lesson was made.
4. Confirm: `"Memory saved. Next session starts at: [X]."`

### Mid-session — write immediately when:
- Micro-task completed → check off `[x]` in `task.md`
- New technical sub-step discovered → add it to `task.md`
- Major decision made → `MEMORY.md` decisions table
- Phase completed → check off in `progress.md`
- Blocker appears → `progress.md` blockers
- Lesson learned → `MEMORY.md` lessons learned

### Rules:
- Never skip start-of-session memory read
- Never end without updating `progress.md`
- One line per item. No permission needed — just do it.
- If `MEMORY.md` exceeds 150 lines, archive old/resolved entries to `MEMORY_ARCHIVE.md`. Keep only active, relevant decisions in `MEMORY.md`.
- `MEMORY_ARCHIVE.md` exists as historical reference. Only read it when needing context about past/resolved decisions not found in `MEMORY.md`.
- If conflicting info exists between memory files, truth hierarchy: `MEMORY.md` > `progress.md` > `task.md`.
- If previous session has no clear "Session END", start new session by inspecting actual code state (existing files, passing tests) to reconstruct progress before continuing.