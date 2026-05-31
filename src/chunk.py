"""Stage 2 — Chunk: page text -> overlapping chunks (with page metadata).

Start dumb: fixed-size word windows with a little overlap. This is the stage
where chunking strategy visibly changes answer quality. Don't optimize it up
front — improve it only after you watch your demo questions fail.
"""
from dataclasses import dataclass

from src.ingest import Page


@dataclass
class Chunk:
    text: str
    page: int  # PDF index of the source page (internal — debug/caching)
    index: int  # position within the document
    source: str  # citation carried from the page, e.g. "Item 422 — Concrete Superstructures, p. 543"


def chunk_pages(
    pages: list[Page], words_per_chunk: int = 220, overlap: int = 40
) -> list[Chunk]:
    chunks: list[Chunk] = []
    idx = 0
    for page in pages:
        words = page.text.split()
        start = 0
        while start < len(words):
            window = words[start : start + words_per_chunk]
            chunks.append(
                Chunk(
                    text=" ".join(window),
                    page=page.number,
                    index=idx,
                    source=page.source,
                )
            )
            idx += 1
            if start + words_per_chunk >= len(words):
                break
            start += words_per_chunk - overlap
    return chunks
