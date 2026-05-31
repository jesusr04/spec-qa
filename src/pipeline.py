"""Wire the five stages into one callable.

Embeddings are cached to .cache/ so you only pay to embed the document once,
not on every question. The cache is keyed by a fingerprint of the PDF contents,
the chunk settings, and the embedding model — so changing any of them rebuilds
the cache automatically. No need to remember to delete .cache/.
"""
import hashlib
import json
import os

import numpy as np

from src import embed
from src.chunk import Chunk, chunk_pages
from src.embed import embed_query, embed_texts
from src.generate import answer
from src.ingest import load_pdf
from src.retrieve import top_k

_CACHE = ".cache"

# Chunk settings live here (not as bare defaults) so the cache fingerprint can
# see them — change one and the cache rebuilds. See src/chunk.py to tune.
WORDS_PER_CHUNK = 220
OVERLAP = 40


def _fingerprint(pdf_path: str) -> str:
    """A stable id for "this PDF + these settings + this model"."""
    h = hashlib.sha256()
    with open(pdf_path, "rb") as f:
        h.update(f.read())
    h.update(f"{WORDS_PER_CHUNK}:{OVERLAP}:{embed.MODEL}".encode())
    return h.hexdigest()


def build_index(pdf_path: str) -> tuple[list[Chunk], np.ndarray]:
    vec_path = os.path.join(_CACHE, "vectors.npy")
    meta_path = os.path.join(_CACHE, "chunks.json")
    fp_path = os.path.join(_CACHE, "fingerprint.txt")
    fingerprint = _fingerprint(pdf_path)

    cached = all(os.path.exists(p) for p in (vec_path, meta_path, fp_path))
    if cached:
        with open(fp_path, encoding="utf-8") as f:
            if f.read().strip() == fingerprint:
                vecs = np.load(vec_path)
                with open(meta_path, encoding="utf-8") as f:
                    chunks = [Chunk(**c) for c in json.load(f)]
                return chunks, vecs

    chunks = chunk_pages(
        load_pdf(pdf_path), words_per_chunk=WORDS_PER_CHUNK, overlap=OVERLAP
    )
    vecs = embed_texts([c.text for c in chunks])

    os.makedirs(_CACHE, exist_ok=True)
    np.save(vec_path, vecs)
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump([c.__dict__ for c in chunks], f)
    with open(fp_path, "w", encoding="utf-8") as f:
        f.write(fingerprint)
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
