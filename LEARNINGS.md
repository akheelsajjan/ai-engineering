# Learnings

> After each topic, I write a 5–10 line teach-back in my own words.
> Graded on: Correctness | Tradeoffs | Failure modes | Rebuildability

---

## Module 0.1 — Dev Environment Setup
Installed uv, Python 3.12.11, confirmed Git and VS Code. Created portfolio repo on GitHub. First commit pushed.

---

## Module 0.2 — Python Refresher
**Date:** 2026-04-30

**In my own words:**
- Type hints make Python more readable and tool-friendly but don't enforce types at runtime — like TypeScript without the errors. Pydantic and FastAPI use them to enforce.
- Dataclasses give structure to internal data objects we define and control. No validation. Use when data never crosses an external boundary.
- Pydantic adds validation at the boundary — when data arrives from outside (API responses, user input). Validates on creation, coerces where possible, raises clear errors on failure.
- async/await lets Python do other work while waiting for slow I/O (like an LLM API call). asyncio.gather runs multiple coroutines concurrently — 3 x 1s calls finish in ~1s, not ~3s.
- logging replaces print in production — timestamps, severity levels, filterable output. Always use a named logger (getLogger(__name__)), not the root logger.

**What I got wrong / missed:**
- Missing `await` is a silent bug — Python returns a coroutine object with no error raised. This is a high-risk failure mode to remember.
- Needed a prompt on the dataclass vs Pydantic boundary rule.

**Grade:**
- Correctness: Pass
- Tradeoffs: Pass (with prompt)
- Failure modes: Needs work — missed the missing-await failure mode
- Rebuildability: Pass

---

## Template for each entry

### [Module X.Y — Topic Name]
**Date:** YYYY-MM-DD

**In my own words:**
...

**What I got wrong / missed:**
...

**Grade:**
- Correctness: Pass / Needs work
- Tradeoffs: Pass / Needs work
- Failure modes: Pass / Needs work
- Rebuildability: Pass / Needs work