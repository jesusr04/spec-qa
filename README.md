# spec-qa — a reusable RAG demo skeleton

Answer questions about a single PDF with citations back to the page. Five
swappable stages, one CLI. Built as a learning milestone and an interview
proof-of-work. See `BRIEF.md` for the scope contract before touching code.

## The five stages
```
ingest  → chunk  → embed  → retrieve  → generate
 PDF       text     vectors   top-k       cited answer
```
Each stage is one file in `src/`. To reuse this for a different build (email
triage, submittal tracker), copy the folder and swap `ingest.py` + the prompt
in `generate.py`. That's the whole "reusable foundation" — earned by extraction,
not designed up front.

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
Changed the PDF or chunking? Delete `.cache/` so it re-embeds.

## Where to tune answer quality
1. `src/chunk.py` — chunk size/overlap. Start here when answers are wrong.
2. `src/retrieve.py` — `k` (how many chunks feed the LLM).
3. `src/generate.py` — the prompt.

## Deliberately out of scope (see BRIEF.md)
No auth, no web UI, no vector DB, one document. Ship the demo, not the product.

## Later, if this grows up
Prompt caching on the system prompt, a real vector store (pgvector — you already
know it), section-aware chunking, multi-doc. None of it belongs in the demo.
