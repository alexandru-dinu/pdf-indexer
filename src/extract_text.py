import functools
import multiprocessing as mp
import pickle
import random
import re
import subprocess as sp
from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
from typing import Dict, Tuple

from spacy.lang.en import English
from spacy.tokenizer import Tokenizer


def is_garbage(tok) -> bool:
    return any([len(tok) < 3, tok.is_punct, tok.is_stop, tok.is_space, tok.like_num])


def extract_strings(pdf_path: str, tokenizer: Tokenizer) -> Tuple[str, Counter]:
    """
    Construct a Counter object of {token: frequency}; tokens are extracted with pdfgrep.
    """
    cmd = ["pdfgrep", "-i", "[a-z0-9]", args.pdf_dir / pdf_path]
    out = sp.run(cmd, stdout=sp.PIPE, stderr=sp.PIPE)

    tokens = tokenizer(out.stdout.decode("utf8"))
    tokens = [
        re.sub(r"[^a-z]", "", t.text.lower()) for t in tokens if not is_garbage(t)
    ]
    tokens = [t for t in tokens if len(t) > 0]

    return pdf_path, Counter(tokens)


def main():
    nlp = English()

    pdfs = list(args.pdf_dir.glob("**/*.pdf"))
    random.shuffle(pdfs)

    work_fn = functools.partial(extract_strings, tokenizer=Tokenizer(nlp.vocab))

    out: Dict[str, Counter] = {}

    with mp.Pool(processes=args.pool_size) as pool:
        for pdf_path, counter in pool.imap_unordered(work_fn, pdfs):
            out[str(pdf_path)] = counter
            print(f"Extracting text: {len(out)} / {len(pdfs)}", end="\r")

    with open(args.text_path, "wb") as fp:
        pickle.dump(out, fp)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--pdf_dir", type=Path, required=True, help="Directory of PDF files to process."
    )
    parser.add_argument(
        "--text_path",
        type=Path,
        required=True,
        help="Where to dump the extracted text.",
    )
    parser.add_argument(
        "--pool_size",
        type=int,
        required=False,
        default=4,
        help="Size of multiprocessing pool.",
    )
    args = parser.parse_args()

    # ensure parent dir exists
    args.text_path.resolve().parents[0].mkdir(exist_ok=True, parents=True)

    main()
