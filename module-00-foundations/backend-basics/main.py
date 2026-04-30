import asyncio
import logging
import sqlite3
import time
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)

# --- Database ---
DB_PATH = "llm_logs.db"


def init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS llm_calls (
            id          INTEGER PRIMARY KEY,
            prompt      TEXT NOT NULL,
            response    TEXT,
            model       TEXT,
            tokens_used INTEGER,
            latency_ms  INTEGER,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    logger.info("Database initialised")


# --- Lifespan: runs once on startup, then yields, then runs on shutdown ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield  # app runs here
    logger.info("Shutting down")


app = FastAPI(title="LLM Service", lifespan=lifespan)


# --- Internal config (dataclass: we control this, no external input) ---
@dataclass
class LLMConfig:
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 256


# --- API boundary models (Pydantic: data crosses the HTTP boundary) ---
class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = Field(default=256, gt=0)


class GenerateResponse(BaseModel):
    content: str
    model: str
    tokens_used: int
    latency_ms: int


class LogEntry(BaseModel):
    id: int
    prompt: str
    response: Optional[str]
    model: Optional[str]
    tokens_used: Optional[int]
    latency_ms: Optional[int]
    created_at: str


# --- Mock LLM (replace with real API call in Module 2) ---
async def call_llm(prompt: str, config: LLMConfig) -> dict:
    logger.info(f"Calling LLM | model={config.model} | prompt_length={len(prompt)}")
    await asyncio.sleep(1)  # simulates network latency
    return {
        "content": f"Response to: '{prompt}'",
        "model": config.model,
        "tokens_used": len(prompt.split()) * 2,
    }


# --- Routes ---
@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest) -> GenerateResponse:
    config = LLMConfig(max_tokens=request.max_tokens)

    start = time.monotonic()
    raw = await call_llm(request.prompt, config)
    latency_ms = int((time.monotonic() - start) * 1000)

    # Log every call to SQLite — this is your audit trail and eval dataset
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO llm_calls (prompt, response, model, tokens_used, latency_ms) VALUES (?, ?, ?, ?, ?)",
        (request.prompt, raw["content"], raw["model"], raw["tokens_used"], latency_ms)
    )
    conn.commit()
    conn.close()

    logger.info(f"Request complete | tokens={raw['tokens_used']} | latency_ms={latency_ms}")

    return GenerateResponse(
        content=raw["content"],
        model=raw["model"],
        tokens_used=raw["tokens_used"],
        latency_ms=latency_ms,
    )


@app.get("/logs", response_model=list[LogEntry])
async def get_logs(limit: int = 10) -> list[LogEntry]:
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        """SELECT id, prompt, response, model, tokens_used, latency_ms, created_at
           FROM llm_calls ORDER BY created_at DESC LIMIT ?""",
        (limit,)
    ).fetchall()
    conn.close()

    return [
        LogEntry(
            id=r[0], prompt=r[1], response=r[2], model=r[3],
            tokens_used=r[4], latency_ms=r[5], created_at=r[6]
        )
        for r in rows
    ]
