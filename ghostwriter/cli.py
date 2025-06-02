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
    parser.add_argument("epub_files", nargs="+", help="Paths to existing book EPUB files")
    parser.add_argument("--prompt", required=True, help="Outline or guidance for next book")
    parser.add_argument("--out", default="next_book.txt", help="Output text filename")
    parser.add_argument("--chapters", type=int, default=10, help="Number of chapters to generate")
    args = parser.parse_args(argv)

    chapters = []
    VectorStore, generate_next_book = _load_dependencies()
    store = VectorStore()
    for book_path in args.epub_files:
        texts = read_epub(book_path)
        chapters.extend(texts)
        store.add_texts(texts)

    generated = generate_next_book(chapters, args.prompt, store, chapters=args.chapters)

    Path(args.out).write_text(generated, encoding="utf-8")
    print(f"Book saved as {args.out}")


if __name__ == "__main__":
    main()
