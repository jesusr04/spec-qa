"""Stage 5 — Generate: cited answer from the retrieved chunks.

What makes this credible in a demo:
  1. It cites the real source — spec item + printed page, e.g.
     (Item 422 — Concrete Superstructures, p. 543) — carried in each chunk.
  2. It anchors the answer in the spec's DESCRIPTION (what the spec governs).
  3. It surfaces "unless otherwise shown on the plans" style qualifiers so the
     reader knows the plans/engineer may specify an alternative.
  4. It refuses ("That isn't covered in this document.") instead of guessing.
"""
import os

from anthropic import Anthropic

from src.chunk import Chunk

_client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
_MODEL = "claude-sonnet-4-6"  # swap to claude-haiku-4-5 for speed/cost

_SYSTEM = (
    "You answer questions about a construction specification using ONLY the "
    "provided excerpts. Never guess or invent facts not in the excerpts.\n"
    "Each excerpt is preceded by its source in brackets, e.g. "
    "[Item 422 — Concrete Superstructures, p. 543]. Cite that exact source for "
    "every fact you state, like (Item 422 — Concrete Superstructures, p. 543). "
    "Use the printed page number from the source, never an internal index.\n"
    "The spec's first section is DESCRIPTION — it states what the spec governs. "
    "When it is present in the excerpts, open your answer by briefly noting that "
    "scope (e.g. this spec covers bridge slabs, decks, flat slabs, slab and "
    "girder units, approach slabs, and other superstructure elements), so the "
    "reader knows the answer applies to that element.\n"
    "When the spec qualifies a requirement with a phrase like 'unless otherwise "
    "shown on the plans', 'unless otherwise directed', or 'unless specified "
    "otherwise', state the requirement and then end your answer by calling out "
    "that qualifier, so the reader knows the plans may specify a different "
    "material or value.\n"
    "If the answer is genuinely not in the excerpts, reply with exactly this and "
    'nothing else: "That isn\'t covered in this document." Never both give an '
    "answer and append that refusal sentence — do one or the other."
)


def answer(question: str, retrieved: list[tuple[Chunk, float]]) -> str:
    context = "\n\n".join(f"[{c.source}]\n{c.text}" for c, _ in retrieved)
    msg = _client.messages.create(
        model=_MODEL,
        max_tokens=600,
        temperature=0,  # deterministic answers — a demo must answer the same way every time
        system=_SYSTEM,
        messages=[
            {
                "role": "user",
                "content": f"Excerpts:\n{context}\n\nQuestion: {question}",
            }
        ],
    )
    return msg.content[0].text
