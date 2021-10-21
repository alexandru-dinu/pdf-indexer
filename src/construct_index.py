import os
import pickle
from argparse import ArgumentParser
from pathlib import Path

from tqdm import tqdm
from whoosh import index
from whoosh.analysis import StemmingAnalyzer
from whoosh.fields import TEXT, Schema


def main():
    with open(args.text_path, "rb") as fp:
        pdf2text = pickle.load(fp)

    os.makedirs(args.index_path, exist_ok=True)

    schema = Schema(
        title=TEXT(stored=True, analyzer=StemmingAnalyzer()), content=TEXT(stored=False)
    )

    index.create_in(args.index_path, schema=schema, indexname="pdfs")
    idx = index.open_dir(args.index_path, indexname="pdfs")

    writer = idx.writer()

    for pdf_path, words in tqdm(pdf2text.items(), desc="Indexing"):
        title = Path(pdf_path).resolve().stem
        content = sum([[w] * f for (w, f) in words.items()], [])
        writer.add_document(title=title, content=" ".join(content))

    writer.commit()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--text_path",
        type=Path,
        required=True,
        help="Location of the object containing extracted text.",
    )
    parser.add_argument(
        "--index_path", type=Path, required=True, help="Path of the constructed index."
    )
    args = parser.parse_args()

    # ensure out dir exists
    args.index_path.mkdir(exist_ok=True, parents=True)

    main()
