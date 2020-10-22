import os
import pickle
import random
from tqdm import tqdm

from whoosh import index
from whoosh.fields import Schema, TEXT
from whoosh.analysis import StemmingAnalyzer


pkl_path = '../bin/pdfs_txt.pkl'


out = pickle.load(open(pkl_path, 'rb'))
out = {k: v for (k, v) in out}

index_path = './index'
os.makedirs(index_path, exist_ok=True)

schema = Schema(
    title   = TEXT(stored=True, analyzer=StemmingAnalyzer()),
    content = TEXT(stored=False)
)

_   = index.create_in(index_path, schema=schema, indexname='pdfs')
idx = index.open_dir(index_path, indexname='pdfs')

writer = idx.writer()

for title, words in tqdm(out.items(), desc='indexing'):
    title = os.path.splitext(os.path.basename(title))[0].lower()

    content = []
    for w, f in words.items():
        content.extend([w] * f)
    random.shuffle(content)

    writer.add_document(title=title, content=' '.join(content))

writer.commit()
