"""Interactive wrapper for Ghostwriter."""

from __future__ import annotations

from pathlib import Path

from .cli import _load_dependencies
from .parser import read_epub
from .llm import DEFAULT_MODELS


def _gather_epubs(path: Path) -> list[Path]:
    if path.is_dir():
        return sorted(path.glob("*.epub"))
    return [path]


def main() -> None:
    print("Ghostwriter interactive wrapper")
    paths = input("Enter path(s) to EPUB files or directories (comma separated): ")
    guidance = input("Enter outline/guidance for the next book: ")
    chapters_str = input("Number of chapters [10]: ") or "10"
    provider = input("LLM provider (openai/anthropic) [openai]: ") or "openai"
    suggestion = DEFAULT_MODELS.get(provider, "")
    if suggestion:
        print(f"Suggested model: {suggestion}")
    model = input(f"Model name [{suggestion}]: ") or suggestion
    out = input("Output filename [next_book.txt]: ") or "next_book.txt"

    VectorStore, generate_next_book = _load_dependencies()
    store = VectorStore()
    texts: list[str] = []
    for p in [p.strip() for p in paths.split(',') if p.strip()]:
        for book_path in _gather_epubs(Path(p)):
            chapters = read_epub(str(book_path))
            texts.extend(chapters)
            store.add_texts(chapters)

    result, cost = generate_next_book(
        texts,
        guidance,
        store,
        chapters=int(chapters_str),
        provider=provider,
        model=model,
    )

    Path(out).write_text(result, encoding="utf-8")
    print(f"Book saved as {out}")
    print(f"Estimated cost: ${cost:.4f}")


if __name__ == "__main__":
    main()

