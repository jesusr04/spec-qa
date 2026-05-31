"""Stage 3 — Embed: text -> vectors.

Default: OpenAI text-embedding-3-small (one cheap key, tiny dependency).
This whole file exists so you can swap providers without touching the rest of
the pipeline. Zero-API-key alternative: install sentence-transformers and
return model.encode(texts) from a local 'all-MiniLM-L6-v2'.
"""
import os

import numpy as np
from openai import OpenAI

_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
_MODEL = "text-embedding-3-small"


def embed_texts(texts: list[str]) -> np.ndarray:
    resp = _client.embeddings.create(model=_MODEL, input=texts)
    return np.array([d.embedding for d in resp.data], dtype=np.float32)


def embed_query(text: str) -> np.ndarray:
    return embed_texts([text])[0]
