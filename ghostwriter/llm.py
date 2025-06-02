"""LLM interaction utilities."""

from __future__ import annotations

from typing import Iterable, List

try:
    import openai
except ImportError:  # pragma: no cover - optional dependency
    openai = None


MODEL = "gpt-4"


def summarize_text(text: str) -> str:
    """Return a short summary of the given text using the LLM."""
    if openai is None:
        raise ImportError("openai package is required for LLM calls")
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[{"role": "user", "content": f"Summarize the following:\n{text}"}],
    )
    return response["choices"][0]["message"]["content"].strip()


def generate_next_book(
    existing_texts: Iterable[str],
    guidance: str,
    vector_store,
    chapters: int = 10,
) -> str:
    """Generate a new book continuation given existing texts and guidance."""
    if openai is None:
        raise ImportError("openai package is required for LLM calls")
    summaries = [summarize_text(t) for t in existing_texts]
    context = "\n".join(summaries)
    prompt = (
        "You are the author continuing this saga. Keep tone and world consistent.\n"
        f"Guidance: {guidance}\n"
        f"Context from previous books: {context}\n"
        f"Write {chapters} chapters."
    )
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response["choices"][0]["message"]["content"].strip()
