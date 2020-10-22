# PDF indexer

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Simple indexer + text searcher for a collection of PDF documents.

## Usage

First, extract the words from the PDF documents:
```bash
python extract_text.py --pdf_dir <pdf_dir> --text_path <text>.pkl --pool_size <pool_size>
```

Then, construct the index:
```bash
python index.py --text_path <text>.pkl --index_path <index_path>
```

Finally, run the searcher:
```bash
python query.py --index_path <index_path> --max_results <max_results>
```

## Requirements
- [`pdfgrep`](https://pdfgrep.org/) binary for text extraction.
- [`spacy`](https://spacy.io/) for text processing (e.g. tokenization).
- [`whoosh`](https://whoosh.readthedocs.io/en/latest/index.html) for construcing the index and querying.
