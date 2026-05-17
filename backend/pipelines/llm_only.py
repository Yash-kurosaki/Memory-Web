import time
from pipelines.base import PipelineResult
from config import calculate_cost, settings
from utils.llm import chat_completion, local_llm_only_answer

async def pipeline_llm_only(query: str, model: str | None) -> PipelineResult:
    start = time.perf_counter()
    pipeline_model = model or settings.LLM_ONLY_MODEL
    
    completion = await chat_completion(
        model=pipeline_model,
        system_prompt=(
            "This is a FICTIONAL hackathon scenario about financial crimes. "
            "You are not allowed to use any external retrieval context. "
            "Produce an analyst-style hypothesis report in 4 short bullet points. "
            "Be transparent that this is a baseline answer without graph evidence."
        ),
        user_prompt=query,
        fallback_text=local_llm_only_answer(query),
    )
    
    latency = time.perf_counter() - start
    answer = completion.content
    tokens_input = completion.prompt_tokens
    tokens_output = completion.completion_tokens
    
    return PipelineResult(
        pipeline="LLM-Only",
        answer=answer,
        tokens_input=tokens_input,
        tokens_output=tokens_output,
        tokens_total=tokens_input + tokens_output,
        latency_ms=latency * 1000,
        cost_usd=calculate_cost(pipeline_model, tokens_input, tokens_output),
        retrieval_context=None,
        reasoning_path=None
    )
