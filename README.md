# Ghostwriter

Command-line tool to generate a new book in a series using an LLM. Provide your
existing EPUB files and a prompt describing the next installment, and the tool
will produce a draft continuation.

## Requirements

- Python 3.10+
- `ebooklib` for reading EPUB files
- `openai` for LLM and embeddings
- `numpy` for simple similarity search

The repository provides a `requirements.txt` file containing these
dependencies. Install them with:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python -m ghostwriter.cli book1.epub book2.epub --prompt "Short outline" --out next_book.txt
```

The resulting text is saved to `next_book.txt`.
