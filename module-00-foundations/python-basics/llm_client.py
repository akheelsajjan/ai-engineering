import asyncio
import logging
from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel, Field

# --- Logging setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)


# --- Config (dataclass: internal data, no external input, no validation needed) ---
@dataclass
class LLMConfig:
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 256


# --- Response (Pydantic: data crosses a boundary from "outside", needs validation) ---
class LLMResponse(BaseModel):
    content: str
    model: str
    tokens_used: int = Field(gt=0)  # must be > 0
    finish_reason: Optional[str] = None


# --- Async LLM caller ---
async def call_llm(prompt: str, config: LLMConfig) -> LLMResponse:
    logger.info(f"Calling LLM | model={config.model} | prompt_length={len(prompt)}")

    await asyncio.sleep(1)  # simulates real network latency

    # Simulated raw API response — in reality this comes back as a dict/JSON
    raw_response = {
        "content": f"Response to: '{prompt}'",
        "model": config.model,
        "tokens_used": len(prompt.split()) * 2,
        "finish_reason": "stop",
    }

    response = LLMResponse.model_validate(raw_response)
    logger.info(
        f"LLM responded | tokens={response.tokens_used} | finish_reason={response.finish_reason}"
    )
    return response


async def main() -> None:
    config = LLMConfig(model="gpt-4o", temperature=0.3)

    prompts = [
        "What is a vector embedding?",
        "What is RAG?",
        "What is an AI agent?",
    ]

    logger.info(f"Sending {len(prompts)} prompts concurrently")

    # asyncio.gather runs all 3 calls at the same time — ~1s total, not ~3s
    responses = await asyncio.gather(*[call_llm(p, config) for p in prompts])

    for prompt, response in zip(prompts, responses):
        print(f"\nPrompt   : {prompt}")
        print(f"Response : {response.content}")
        print(f"Tokens   : {response.tokens_used}")


if __name__ == "__main__":
    asyncio.run(main())
