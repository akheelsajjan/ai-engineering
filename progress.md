# Progress Tracker

> Source of truth for where we are, what's done, and what's next.
> Updated after every session.

---

## Current Status
**Module:** 1.1 — Tokenization  
**Status:** Not started  
**Date started:** —

---

## Completed
- [x] Installed `uv` (Python package manager)
- [x] Installed Python 3.12.11 via `uv`
- [x] Confirmed Git installed
- [x] Confirmed VS Code installed
- [x] Created GitHub repo: https://github.com/akheelsajjan/ai-engineering
- [x] Cloned repo locally to `C:\Users\aksaj\Documents\Claude\Projects\AI Application Engineering\ai-engineering`
- [x] Created README.md, progress.md, LEARNINGS.md
- [x] First commit and push to GitHub — Module 0.1 complete ✓
- [x] Module 0.2: type hints, dataclasses, Pydantic, async/await, logging — complete ✓
- [x] Built llm_client.py — concurrent async LLM mock, Pydantic validation, structured logging
- [x] Module 0.3: FastAPI, SQLite logging, Docker — complete ✓
- [x] Built main.py — FastAPI service with /generate, /logs, /health + Dockerfile

---

## Up Next
- [ ] Module 1.1: Tokenization — what tokens are and why they break things

## Weak Spots / To Revisit
- Missing `await` bug — silently returns coroutine object, no error raised. High risk.
- Docker layer caching — needed a prompt, now solid.
- `/logs` vs plain logging distinction — needed a prompt.

---

## Process Note
From Module 1 onwards: Akheel writes all code. Claude teaches + reviews only.

---

## Module Log
| Module | Status | Date | Notes |
|--------|--------|------|-------|
| 0.1 Dev Setup | ✅ Complete | 2026-04-30 | uv + Python 3.12.11, Git, VS Code, GitHub repo live |
| 0.2 Python Refresher | ✅ Complete | 2026-04-30 | type hints, dataclass, Pydantic, async, logging. Built llm_client.py |
| 0.3 Backend Foundations | ✅ Complete | 2026-04-30 | FastAPI, SQLite, Docker. Built llm service with audit trail. |