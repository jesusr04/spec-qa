"""Stage 3 — Embed: text -> vectors.

Default: OpenAI text-embedding-3-small (one cheap key, tiny dependency).
This whole file exists so you can swap providers without touching the rest of
the pipeline. Zero-API-key alternative: install sentence-transformers and
return model.encode(texts) from a local 'all-MiniLM-L6-v2'.
"""
import os

import numpy as np
from openai import OpenAI

MODEL = "text-embedding-3-small"  # public: the cache fingerprint keys on it

_client: OpenAI | None = None


def _get_client() -> OpenAI:
    """Build the client lazily so the module imports without a key set."""
    global _client
    if _client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("Missing OPENAI_API_KEY — set it in .env")
        _client = OpenAI(api_key=api_key)
    return _client


def embed_texts(texts: list[str]) -> np.ndarray:
    resp = _get_client().embeddings.create(model=MODEL, input=texts)
    return np.array([d.embedding for d in resp.data], dtype=np.float32)


def embed_query(text: str) -> np.ndarray:
    return embed_texts([text])[0]
