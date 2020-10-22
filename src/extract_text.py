import os
import re
from argparse import ArgumentParser
from pathlib import Path

from collections import Counter
import subprocess as sp
import multiprocessing as mp

from spacy.tokenizer import Tokenizer
from spacy.lang.en import English


parser = ArgumentParser()
parser.add_argument("--pdf_dir", type=str, help="Directory of PDF files to process.")
parser.add_argument("--text_path", type=str, help="Where to dump the extracted text.")
parser.add_argument(
    "--pool_size", type=int, default=4, help="Size of multiprocessing pool."
)
args = parser.parse_args()

nlp = English()
tokenizer = Tokenizer(nlp.vocab)


def is_garbage(tok) -> bool:
    return any([len(tok) < 3, tok.is_punct, tok.is_stop, tok.is_space, tok.like_num])


def extract_strings(pdf: str) -> (str, Counter):
    """
    Construct a Counter object of {token: frequency}; tokens are extracted with pdfgrep.
    """
    print(pdf)
    cmd = ["pdfgrep", "-i", "[a-z0-9]", str(Path(args.pdf_dir) / pdf)]
    out = sp.run(cmd, stdout=sp.PIPE, stderr=sp.PIPE)

    tokens = tokenizer(out.stdout.decode("utf8"))
    tokens = [
        re.sub(r"[^a-z]", "", t.text.lower()) for t in tokens if not is_garbage(t)
    ]
    tokens = [t for t in tokens if len(t) > 0]

    return pdf, Counter(tokens)


pdfs = sorted(
    os.listdir(args.pdf_dir), key=lambda x: os.path.getsize(Path(args.pdf_dir) / x)
)

with mp.Pool(processes=args.pool_size) as pool:
    out = pool.map(extract_strings, pdfs)

pickle.dump(out, open(args.text_path, "wb"))
