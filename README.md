# Ghostwriter

Command-line tool to generate a new book in a series using an LLM. Provide your
existing EPUB files and a prompt describing the next installment, and the tool
will produce a draft continuation.

## Requirements

- Python 3.10+
- `ebooklib` for reading EPUB files
- `openai` for LLM and embeddings
- `anthropic` for optional Anthropic LLM support
- `numpy` for simple similarity search

The repository provides a `requirements.txt` file containing these
dependencies. Install them with:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python -m ghostwriter.cli path/to/epubs --prompt "Short outline" --provider anthropic --out next_book.txt
```

The resulting text is saved to `next_book.txt`. Specify directories instead of individual files to process all `.epub` files within. Use `--provider` (`openai` or `anthropic`) and `--model` to select the language model. After generation the estimated API cost is printed.

For an interactive experience, run:

```bash
python -m ghostwriter.wrapper
```

The wrapper will prompt for the EPUB paths, outline, provider, model, and output
file, then print the estimated cost after generation.

