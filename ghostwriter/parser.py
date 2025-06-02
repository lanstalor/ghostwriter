"""Utilities for reading EPUB files."""

from typing import List

try:
    from ebooklib import epub
except ImportError as e:  # pragma: no cover - library might not be installed
    epub = None


def read_epub(file_path: str) -> List[str]:
    """Return a list of chapter texts from an EPUB file."""
    if epub is None:
        raise ImportError("ebooklib is required to read EPUB files")

    book = epub.read_epub(file_path)
    chapters = []
    for item in book.get_items():
        if item.get_type() == epub.ITEM_DOCUMENT:
            chapters.append(item.get_content().decode("utf-8"))
    return chapters
