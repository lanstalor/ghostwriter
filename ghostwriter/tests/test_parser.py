import os
from ebooklib import epub


def _read(path: str):
    import importlib
    read_epub = importlib.import_module("ghostwriter.parser").read_epub
    return read_epub(path)

def test_read_epub(tmp_path):
    book = epub.EpubBook()
    c1 = epub.EpubHtml(title="Intro", file_name="intro.xhtml", content="<p>hi</p>")
    book.add_item(c1)
    book.toc = [c1]
    book.spine = ["nav", c1]
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    path = tmp_path / "test.epub"
    epub.write_epub(str(path), book)
    texts = _read(str(path))
    assert any("hi" in t for t in texts)

