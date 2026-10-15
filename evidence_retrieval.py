"""Small citation-backed retrieval demonstration using supplied source records.

This is a local retrieval component, not an autonomous full-paper RAG system.
An AI assistant can inspect the retrieved records before drafting an answer.
"""
from pathlib import Path
import json
import argparse
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).resolve().parent


def retrieve(query, top_k=3):
    corpus = json.loads((ROOT / 'research_evidence.json').read_text(encoding='utf-8'))
    records = corpus['records']
    documents = [' '.join([item['title'], item['summary'], item['scope']]) for item in records]
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(documents)
    scores = cosine_similarity(vectorizer.transform([query]), matrix)[0]
    selected = [i for i in np.argsort(scores)[::-1] if scores[i] > .02][:top_k]
    return [{'id': records[i]['id'], 'score': round(float(scores[i]), 4),
             'title': records[i]['title'], 'url': records[i]['url'],
             'evidence_summary': records[i]['summary'], 'scope': records[i]['scope']} for i in selected]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', default='Equivalent circuit fitting for electrochemical impedance spectra')
    args = parser.parse_args()
    result = retrieve(args.query)
    (ROOT / 'results').mkdir(exist_ok=True)
    (ROOT / 'results' / 'retrieved_evidence.json').write_text(
        json.dumps({'query': args.query, 'results': result}, indent=2), encoding='utf-8')
    if args.query == parser.get_default('query'):
        assert result[0]['id'] == 'impedance'
        assert retrieve('qzxv qzxvunknown') == []
    print(json.dumps(result, indent=2))
