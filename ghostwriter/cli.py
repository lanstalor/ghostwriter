"""Command-line interface for ghostwriter."""

from __future__ import annotations

import argparse
from pathlib import Path

from .parser import read_epub


def _load_dependencies():
    """Import modules that require optional third-party packages."""
    from .vector_store import VectorStore
    from .llm import generate_next_book

    return VectorStore, generate_next_book


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Ghostwriter CLI")
    parser.add_argument(
        "epub_inputs",
        nargs="+",
        help="Paths to existing book EPUB files or directories containing them",
    )
    parser.add_argument("--prompt", required=True, help="Outline or guidance for next book")
    parser.add_argument("--out", default="next_book.txt", help="Output text filename")
    parser.add_argument("--chapters", type=int, default=10, help="Number of chapters to generate")
    parser.add_argument(
        "--provider",
        choices=["openai", "anthropic"],
        default="openai",
        help="LLM provider to use",
    )
    parser.add_argument("--model", help="Specific model name to use")
    args = parser.parse_args(argv)

    chapters = []
    VectorStore, generate_next_book = _load_dependencies()
    store = VectorStore()
    def _gather_epubs(path: Path) -> list[Path]:
        if path.is_dir():
            return sorted(path.glob("*.epub"))
        return [path]

    for path_str in args.epub_inputs:
        for book_path in _gather_epubs(Path(path_str)):
            texts = read_epub(str(book_path))
            chapters.extend(texts)
            store.add_texts(texts)

    generated, cost = generate_next_book(
        chapters,
        args.prompt,
        store,
        chapters=args.chapters,
        provider=args.provider,
        model=args.model,
    )

    Path(args.out).write_text(generated, encoding="utf-8")
    print(f"Book saved as {args.out}")
    print(f"Estimated cost: ${cost:.4f}")


if __name__ == "__main__":
    main()
