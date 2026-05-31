# spec-qa

Ask a construction spec a question in plain English and get the answer with a
citation back to the exact page. A working RAG demo over a single TxDOT
specification (Item 422 — Concrete Superstructures).

## The problem
Every infrastructure project runs on specifications. On a TxDOT bridge, a single
document like Item 422 (Concrete Superstructures) dictates the class of concrete
for the deck, the curing material for the slab, the sealant for the expansion
joints, the expansion material at the approach slab, and the tolerances for all
of it.

The answer to almost any field question is in those documents. The problem is
finding it. Today that means scrolling a dense, cross-referenced PDF, or
interrupting a senior engineer, or guessing. When the guess is wrong (the wrong
class of concrete on a bridge deck) the result is a rejected pour, a delay, or a
costly rework.

## The solution
Ask the spec a question the way you would ask a colleague. The tool returns the
answer and cites the exact page it came from. If the document does not cover the
question, it says so instead of making something up. That last part is what makes
it usable for engineering work, where a confident wrong answer is worse than no
answer.

Real questions from the demo:
- What class of concrete do I use for the bridge deck?
- What material do I need for curing the bridge slab?
- What expansion material is allowed at the approach slab?
- What sealant is allowed for expansion joints?
- What evaporation retardant can I use for the bridge slab?

## Who faces this
Project engineers, estimators, QA/QC and field inspectors, and submittal
reviewers, on the contractor, owner, and engineering sides. Anyone who has to
pull one precise requirement out of a hundred-plus-page spec book under time
pressure.

## How it works (RAG, in five stages)
```
ingest  → chunk  → embed  → retrieve  → generate
 PDF       text     vectors   top-k       cited answer
```
1. **Ingest** the spec PDF into page-tagged text (citation = spec item + printed page).
2. **Chunk** it into retrievable pieces.
3. **Embed** each chunk as a vector.
4. **Retrieve** the chunks most relevant to your question.
5. **Generate** an answer from only those chunks, with a page citation.

Built in Python. One document, command-line interface, no cloud database. This
is a demo, not a product. Each stage is one file in `src/`; to reuse the
skeleton for a different build, copy the folder and swap `ingest.py` + the prompt
in `generate.py`.

## Setup
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env   # then paste your keys into .env
```
You need two keys in `.env`:
- `OPENAI_API_KEY` — embeddings (stage 3). Cheap. Swappable (see `src/embed.py`).
- `ANTHROPIC_API_KEY` — generation (stage 5).

Put your spec at `data/spec.pdf` (or edit `PDF_PATH` in `ask.py`).

## Run
```powershell
# eyeball stage 1 output first
python -m src.ingest data/spec.pdf

# ask a question (embeds the doc once, caches to .cache/)
python ask.py "What compressive strength is required for sidewalk concrete?"
```
Change the PDF, chunk settings, or embedding model and the cache rebuilds
itself — it's fingerprinted, so there's no `.cache/` to remember to delete.

## Where to tune answer quality
1. `src/chunk.py` — chunk size/overlap. Start here when answers are wrong.
2. `src/retrieve.py` — `k` (how many chunks feed the LLM).
3. `src/generate.py` — the prompt.

## Deliberately out of scope
No auth, no web UI, no vector DB, one document. Ship the demo, not the product.

## Later, if this grows up
Prompt caching on the system prompt, a real vector store (pgvector),
section-aware chunking, multi-doc. None of it belongs in the demo.
