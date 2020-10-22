import os
import pickle
import random
from tqdm import tqdm
from argparse import ArgumentParser

from whoosh import index
from whoosh.fields import Schema, TEXT
from whoosh.analysis import StemmingAnalyzer


parser = ArgumentParser()
parser.add_argument(
    "--text_path", type=str, help="Location of the object containing extracted text."
)
parser.add_argument("--index_path", type=str, help="Where to store the index.")
args = parser.parse_args()

out = pickle.load(open(args.text_path, "rb"))
out = {k: v for (k, v) in out}

os.makedirs(args.index_path, exist_ok=True)

schema = Schema(
    title=TEXT(stored=True, analyzer=StemmingAnalyzer()), content=TEXT(stored=False)
)

_ = index.create_in(args.index_path, schema=schema, indexname="pdfs")
idx = index.open_dir(args.index_path, indexname="pdfs")

writer = idx.writer()

for title, words in tqdm(out.items(), desc="indexing"):
    title = os.path.splitext(os.path.basename(title))[0].lower()

    content = []
    for w, f in words.items():
        content.extend([w] * f)
    random.shuffle(content)

    writer.add_document(title=title, content=" ".join(content))

writer.commit()
