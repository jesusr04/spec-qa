"""Stage 4 — Retrieve: question vector -> top-k most relevant chunks.

In-memory cosine similarity. For one document this beats standing up a vector
DB. Printing what comes back per question (see pipeline.ask) is your main
debugging window when an answer looks wrong — usually retrieval, not the LLM.
"""
import numpy as np

from src.chunk import Chunk


def _cosine(query: np.ndarray, matrix: np.ndarray) -> np.ndarray:
    q = query / (np.linalg.norm(query) + 1e-8)
    m = matrix / (np.linalg.norm(matrix, axis=1, keepdims=True) + 1e-8)
    return m @ q


def top_k(
    query_vec: np.ndarray, chunk_vecs: np.ndarray, chunks: list[Chunk], k: int = 4
) -> list[tuple[Chunk, float]]:
    scores = _cosine(query_vec, chunk_vecs)
    best = np.argsort(scores)[::-1][:k]
    return [(chunks[i], float(scores[i])) for i in best]
