import readline

import whoosh
from whoosh import index
from whoosh import qparser
from whoosh import scoring

idx = index.open_dir('../bin/index', indexname='pdfs')

while True:
    try:
        term = input('\n>>> ').strip()

        with idx.searcher(weighting=scoring.TF_IDF()) as searcher:
            query = qparser.QueryParser("content", idx.schema).parse(term)
            hits = searcher.search(query, limit=10)

            for i, h in enumerate(hits, start=1):
                print(f'{i:2d}: {h["title"]}')

        print('=' * 80)

    except whoosh.query.qcore.QueryError as e:
        print(red_text(f'QUERY ERROR: {e}'))

    except (KeyboardInterrupt, EOFError):
        break
