# PDF indexer

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Simple indexer + text searcher for a collection of PDF documents.

## Usage

First, extract the words from the PDF documents:
```sh
python extract_text.py --pdf_dir PDF_DIR --text_path TEXT_PATH [--pool_size POOL_SIZE]
```

Then, construct the index:
```sh
python construct_index.py --text_path TEXT_PATH --index_path INDEX_PATH
```

Finally, run the searcher:
```sh
python query.py --index_path INDEX_PATH [--max_results MAX_RESULTS]
```

## Requirements
- [`pdfgrep`](https://pdfgrep.org/) binary for text extraction.
- [`spacy`](https://spacy.io/) for text preprocessing (e.g. tokenization).
- [`whoosh`](https://whoosh.readthedocs.io/en/latest/index.html) for index construction and querying.
