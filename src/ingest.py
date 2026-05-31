"""Stage 1 — Ingest: spec PDF -> text, tagged with a real citation.

The only job here is to turn one PDF into clean text, tagged with the citation
a reader would actually use: the specification item ("Item 422 — Concrete
Superstructures") and the printed page number from the page header/footer
("543") — NOT the PDF's internal page index. Eyeball the output before moving on
(`python -m src.ingest data/spec.pdf`): garbage in here means garbage answers.
"""
import re
from dataclasses import dataclass

import fitz  # pymupdf


@dataclass
class Page:
    number: int  # PDF index, 1-based (internal — used for caching/debug only)
    text: str
    source: str  # human citation carried to the answer, e.g. "Item 422 — Concrete Superstructures, p. 543"


def _spec_label(text: str) -> str | None:
    """The spec item + title, e.g. 'Item 422 — Concrete Superstructures'.

    TxDOT specs print this as 'Item <n>' on one line and the title on the next.
    """
    m = re.search(r"Item\s+(\d+)\s*\n\s*([^\n]+)", text)
    if not m:
        return None
    return f"Item {m.group(1)} — {m.group(2).strip()}"


def _printed_page(text: str) -> str | None:
    """The printed page number from the page header.

    The header reads '<year> Specifications / <item no.> / <page no.>', so the
    page number is the second standalone integer after 'Specifications'.
    """
    m = re.search(r"Specifications\s*\n\s*\d+\s*\n\s*(\d+)", text)
    return m.group(1) if m else None


def load_pdf(path: str) -> list[Page]:
    doc = fitz.open(path)
    raw = [
        (i, text)
        for i, page in enumerate(doc, start=1)
        if (text := page.get_text("text").strip())
    ]
    doc.close()

    # The spec item/title is a document-level fact; take it from the first page
    # that prints it and reuse it for every page's citation.
    spec = next((label for _, t in raw if (label := _spec_label(t))), None)

    pages = []
    for i, text in raw:
        printed = _printed_page(text) or str(i)
        source = f"{spec}, p. {printed}" if spec else f"p. {printed}"
        pages.append(Page(number=i, text=text, source=source))
    return pages


if __name__ == "__main__":
    import sys

    pages = load_pdf(sys.argv[1])
    print(f"Loaded {len(pages)} pages with text.")
    print(f"Citation for page 1: {pages[0].source}")
    print("---- page 1 preview ----")
    print(pages[0].text[:1000])
