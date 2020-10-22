import readline
from argparse import ArgumentParser

import whoosh
from whoosh import index
from whoosh import qparser
from whoosh import scoring

parser = ArgumentParser()
parser.add_argument("--index_path", type=str, help="Location of the index.")
parser.add_argument(
    "--max_results",
    type=int,
    default=10,
    help="Max number of results to show for one query.",
)
args = parser.parse_args()

idx = index.open_dir(args.index_path, indexname="pdfs")

while True:
    try:
        term = input("\n>>> ").strip()

        with idx.searcher(weighting=scoring.TF_IDF()) as searcher:
            query = qparser.QueryParser("content", idx.schema).parse(term)
            hits = searcher.search(query, limit=args.max_results)

            for i, h in enumerate(hits, start=1):
                print(f'{i:2d}: {h["title"]}')

        print("=" * 80)

    except whoosh.query.qcore.QueryError as e:
        print(f"QUERY ERROR: {e}")

    except (KeyboardInterrupt, EOFError):
        break
