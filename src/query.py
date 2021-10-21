import readline  # noqa
from argparse import ArgumentParser
from pathlib import Path

import whoosh
from whoosh import index, qparser, scoring

PROMPT = ">>> "


def main():
    idx = index.open_dir(args.index_path, indexname="pdfs")

    while True:
        try:
            term = input(f"\n{PROMPT}").strip()

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


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--index_path", type=Path, required=True, help="Location of the index."
    )
    parser.add_argument(
        "--max_results",
        type=int,
        required=False,
        default=10,
        help="Max number of results to show for one query.",
    )
    args = parser.parse_args()

    main()
