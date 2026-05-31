"""Wire the five stages into one callable.

Embeddings are cached to .cache/ so you only pay to embed the document once,
not on every question. Changed the PDF or chunking? Delete .cache/ to rebuild.
"""
import json
import os

import numpy as np

from src.chunk import Chunk, chunk_pages
from src.embed import embed_query, embed_texts
from src.generate import answer
from src.ingest import load_pdf
from src.retrieve import top_k

_CACHE = ".cache"


def build_index(pdf_path: str) -> tuple[list[Chunk], np.ndarray]:
    vec_path = os.path.join(_CACHE, "vectors.npy")
    meta_path = os.path.join(_CACHE, "chunks.json")

    if os.path.exists(vec_path) and os.path.exists(meta_path):
        vecs = np.load(vec_path)
        with open(meta_path, encoding="utf-8") as f:
            chunks = [Chunk(**c) for c in json.load(f)]
        return chunks, vecs

    chunks = chunk_pages(load_pdf(pdf_path))
    vecs = embed_texts([c.text for c in chunks])

    os.makedirs(_CACHE, exist_ok=True)
    np.save(vec_path, vecs)
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump([c.__dict__ for c in chunks], f)
    return chunks, vecs


def ask(
    question: str,
    chunks: list[Chunk],
    vecs: np.ndarray,
    k: int = 4,
    show_sources: bool = True,
) -> str:
    hits = top_k(embed_query(question), vecs, chunks, k=k)
    if show_sources:
        print("Retrieved chunks:")
        for c, score in hits:
            print(f"  [{c.source}]  score={score:.3f}  {c.text[:80]}...")
        print()
    return answer(question, hits)
