"""LLM interaction utilities."""

from __future__ import annotations

from typing import Iterable, List, Tuple

try:
    import openai
except ImportError:  # pragma: no cover - optional dependency
    openai = None

try:  # pragma: no cover - optional dependency
    import anthropic
except ImportError:
    anthropic = None


DEFAULT_MODELS = {"openai": "gpt-4", "anthropic": "claude-v1"}
# Rough cost per 1k tokens (input/output) for example models
COST_PER_1K = {
    "openai": {"gpt-4": {"input": 0.03, "output": 0.06}},
    "anthropic": {"claude-v1": {"input": 0.008, "output": 0.024}},
}


def _count_tokens(text: str) -> int:
    """Very rough token estimator based on whitespace."""
    return max(1, len(text.split()))


def _estimate_cost(prompt_tokens: int, completion_tokens: int, provider: str, model: str) -> float:
    info = COST_PER_1K.get(provider, {}).get(model)
    if info is None:
        return 0.0
    return (
        prompt_tokens * info["input"] / 1000
        + completion_tokens * info["output"] / 1000
    )


def _call_openai(prompt: str, model: str) -> Tuple[str, int, int]:
    if openai is None:
        raise ImportError("openai package is required for LLM calls")
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    content = response["choices"][0]["message"]["content"].strip()
    usage = response.get("usage", {})
    prompt_tokens = usage.get("prompt_tokens", _count_tokens(prompt))
    completion_tokens = usage.get("completion_tokens", _count_tokens(content))
    return content, prompt_tokens, completion_tokens


def _call_anthropic(prompt: str, model: str) -> Tuple[str, int, int]:
    if anthropic is None:
        raise ImportError("anthropic package is required for LLM calls")
    client = anthropic.Client()
    full_prompt = f"{anthropic.HUMAN_PROMPT} {prompt}{anthropic.AI_PROMPT}"
    resp = client.completions.create(
        model=model,
        prompt=full_prompt,
        max_tokens_to_sample=1000,
    )
    content = resp["completion"].strip()
    # anthropic API may not return token counts; approximate
    prompt_tokens = _count_tokens(prompt)
    completion_tokens = _count_tokens(content)
    return content, prompt_tokens, completion_tokens


def _call_model(prompt: str, provider: str, model: str) -> Tuple[str, int, int]:
    if provider == "openai":
        return _call_openai(prompt, model)
    if provider == "anthropic":
        return _call_anthropic(prompt, model)
    raise ValueError(f"Unknown provider: {provider}")


def summarize_text(text: str, provider: str = "openai", model: str | None = None) -> Tuple[str, float]:
    """Return a short summary of the given text using the selected LLM."""
    model = model or DEFAULT_MODELS[provider]
    content, p_tokens, c_tokens = _call_model(
        f"Summarize the following:\n{text}", provider, model
    )
    cost = _estimate_cost(p_tokens, c_tokens, provider, model)
    return content, cost


def generate_next_book(
    existing_texts: Iterable[str],
    guidance: str,
    vector_store,
    chapters: int = 10,
    provider: str = "openai",
    model: str | None = None,
) -> Tuple[str, float]:
    """Generate a new book continuation given existing texts and guidance."""
    model = model or DEFAULT_MODELS[provider]

    summaries = []
    total_cost = 0.0
    for t in existing_texts:
        summary, cost = summarize_text(t, provider, model)
        summaries.append(summary)
        total_cost += cost

    context = "\n".join(summaries)
    prompt = (
        "You are the author continuing this saga. Keep tone and world consistent.\n"
        f"Guidance: {guidance}\n"
        f"Context from previous books: {context}\n"
        f"Write {chapters} chapters."
    )

    content, p_tokens, c_tokens = _call_model(prompt, provider, model)
    total_cost += _estimate_cost(p_tokens, c_tokens, provider, model)
    return content, total_cost
