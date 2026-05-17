import json
import time
from pathlib import Path

from pipelines.base import PipelineResult
from config import calculate_cost, settings
from utils.llm import (
    chat_completion,
    estimate_tokens,
    lexical_similarity,
    local_vector_answer,
)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CHUNKS_PATH = DATA_DIR / "chunks.json"

_chunks_cache: list[dict] | None = None
_chunks_mtime: float | None = None


def _load_chunks() -> list[dict]:
    global _chunks_cache, _chunks_mtime

    if not CHUNKS_PATH.exists():
        return []

    current_mtime = CHUNKS_PATH.stat().st_mtime
    if _chunks_cache is not None and _chunks_mtime == current_mtime:
        return _chunks_cache

    with CHUNKS_PATH.open("r", encoding="utf-8") as file:
        _chunks_cache = json.load(file)
        _chunks_mtime = current_mtime
    return _chunks_cache


def _rank_chunks(query: str, chunks: list[dict], top_k: int) -> list[str]:
    scored: list[tuple[float, str]] = []
    for chunk in chunks:
        text = chunk.get("text", "")
        if not text:
            continue
        score = lexical_similarity(query, text)
        if score > 0:
            scored.append((score, text))

    scored.sort(key=lambda item: item[0], reverse=True)
    top = scored[:top_k]

    return [f"[Score: {round(score, 2)}] {text}" for score, text in top]


async def pipeline_vector_rag(query: str, model: str | None, top_k: int = 6) -> PipelineResult:
    start = time.perf_counter()
    pipeline_model = model or settings.VECTOR_RAG_MODEL

    chunks = _load_chunks()
    retrieved_contexts = _rank_chunks(query, chunks, top_k=top_k)

    context_str = (
        "\n".join(f"Document {i + 1}: {item}" for i, item in enumerate(retrieved_contexts))
        if retrieved_contexts
        else "NO RELEVANT DOCUMENTS FOUND."
    )

    prompt = f"""You are executing a Vector RAG retrieval pipeline.

REQUIREMENTS:
1. Answer ONLY using the provided Context.
2. If the Context is fragmented or missing key multi-hop links, explicitly state: \"Vector retrieval failed: No unified relationship chain detected.\"
3. Mention \"Disconnected evidence warning\" if you can only find parts of the entities requested.
4. Do NOT hallucinate connections that are not in the text.
5. Include a short confidence note.
6. Keep it to 2-4 sentences.

Context:
{context_str}

Query: {query}"""

    local_answer = local_vector_answer(query, retrieved_contexts)
    completion = await chat_completion(
        model=pipeline_model,
        system_prompt=(
            "You are a highly strict RAG agent. You expose the flaws of vector similarity "
            "by strictly rejecting fragmented context."
        ),
        user_prompt=prompt,
        fallback_text=local_answer,
    )
    answer = completion.content
    tokens_input = completion.prompt_tokens if completion.prompt_tokens > 0 else estimate_tokens(prompt)
    tokens_output = completion.completion_tokens if completion.completion_tokens > 0 else estimate_tokens(answer)

    latency = time.perf_counter() - start

    return PipelineResult(
        pipeline="Vector-RAG",
        answer=answer,
        tokens_input=tokens_input,
        tokens_output=tokens_output,
        tokens_total=tokens_input + tokens_output,
        latency_ms=latency * 1000,
        cost_usd=calculate_cost(pipeline_model, tokens_input, tokens_output),
        retrieval_context=retrieved_contexts,
        reasoning_path=None,
    )
