"""Interactive wrapper for ghostwriter."""
=======
"""Interactive wrapper for Ghostwriter."""

from __future__ import annotations

from pathlib import Path

from .parser import read_epub
from .vector_store import VectorStore
from .llm import generate_next_book, DEFAULT_MODELS
from .cli import _load_dependencies


def _gather_epubs(path: Path) -> list[Path]:
    if path.is_dir():
        return sorted(path.glob("*.epub"))
    return [path]


def main() -> None:

    """Run interactive prompts to generate a new book."""
    print("Ghostwriter interactive wrapper")

    raw_inputs = input(
        "Enter path(s) to EPUB files or directories (comma separated): "
    ).strip()
    epub_paths = [p.strip() for p in raw_inputs.split(",") if p.strip()]
    guidance = input("Enter outline/guidance for the next book: ").strip()
    chapters_str = input("Number of chapters [10]: ").strip()
    chapters = int(chapters_str) if chapters_str else 10
    provider = input("LLM provider (openai/anthropic) [openai]: ").strip() or "openai"
    suggested = DEFAULT_MODELS.get(provider, "gpt-4")
    print(f"Suggested model: {suggested}")
    model = input(f"Model name [{suggested}]: ").strip() or suggested
    out_file = input("Output filename [next_book.txt]: ").strip() or "next_book.txt"

    VectorStore, generate_next_book = _load_dependencies()
    store = VectorStore()
    chapters_text = []
    for path_str in epub_paths:
        for book_path in _gather_epubs(Path(path_str)):
            texts = read_epub(str(book_path))
            chapters_text.extend(texts)
            store.add_texts(texts)

    generated, cost = generate_next_book(
        chapters_text,
        guidance,
        store,
        chapters=chapters,
        provider=provider,
        model=model,
    )


    Path(out_file).write_text(generated, encoding="utf-8")
    print(f"Book saved as {out_file}")
    print(f"Estimated cost: ${cost:.4f}")


if __name__ == "__main__":
    main()
