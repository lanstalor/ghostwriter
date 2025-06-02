"""Interactive wrapper for ghostwriter."""

from __future__ import annotations

from pathlib import Path

from .parser import read_epub
from .vector_store import VectorStore
from .llm import generate_next_book, DEFAULT_MODELS


def _gather_epubs(path: Path) -> list[Path]:
    if path.is_dir():
        return sorted(path.glob("*.epub"))
    return [path]


def main() -> None:
    print("Ghostwriter interactive wrapper")
    inputs = input("Enter path(s) to EPUB files or directories (comma separated): ").strip()
    epub_inputs = [s.strip() for s in inputs.split(',') if s.strip()]
    guidance = input("Enter outline/guidance for the next book: ")
    chapters_in = input("Number of chapters [10]: ").strip()
    chapters = int(chapters_in) if chapters_in else 10
    provider_in = input("LLM provider (openai/anthropic) [openai]: ").strip()
    provider = provider_in or "openai"
    suggested_model = DEFAULT_MODELS.get(provider, "")
    model_in = input(f"Model name [{suggested_model}]: ").strip()
    model = model_in or suggested_model
    out_in = input("Output filename [next_book.txt]: ").strip()
    out_file = Path(out_in or "next_book.txt")

    all_chapters = []
    store = VectorStore()
    for path_str in epub_inputs:
        for p in _gather_epubs(Path(path_str)):
            texts = read_epub(str(p))
            all_chapters.extend(texts)
            store.add_texts(texts)

    generated, cost = generate_next_book(
        all_chapters,
        guidance,
        store,
        chapters=chapters,
        provider=provider,
        model=model,
    )

    out_file.write_text(generated, encoding="utf-8")
    print(f"Book saved as {out_file}")
    print(f"Estimated cost: ${cost:.4f}")


if __name__ == "__main__":
    main()
