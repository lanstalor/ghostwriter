import tempfile
from pathlib import Path

from ghostwriter.parser import read_epub

from ebooklib import epub


def _make_epub(path: Path) -> None:
    book = epub.EpubBook()
    chapter = epub.EpubHtml(title='Intro', file_name='chap1.xhtml')
    chapter.content = '<p>Hello world</p>'
    book.add_item(chapter)
    book.spine = ['nav', chapter]
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    epub.write_epub(str(path), book)


def test_read_epub(tmp_path: Path) -> None:
    file_path = tmp_path / 'book.epub'
    _make_epub(file_path)
    chapters = read_epub(str(file_path))
    assert len(chapters) >= 1
    assert any('Hello world' in ch for ch in chapters)

