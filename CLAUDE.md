# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A deliberately minimal RAG CLI: answer questions about a **single** construction-spec PDF, citing the page each fact came from. It is a demo, not a product. Hold the line on scope — **no auth, no web UI, no vector DB, one document, one happy path** (ask → cited answer). If a change can't justify itself against those guardrails, it doesn't belong here. (A local-only `BRIEF.md`, kept out of the repo, holds the fuller planning notes.)

## Commands

```powershell
# setup
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env   # then paste OPENAI_API_KEY + ANTHROPIC_API_KEY

# inspect stage 1 (ingest) output — do this first when answers look wrong
python -m src.ingest data/spec.pdf

# ask a question (embeds the doc on first run, caches to .cache/)
python ask.py "What compressive strength is required for sidewalk concrete?"
```

There is no test suite, linter, or build step. The "test" is the 3–5 demo questions in `BRIEF.md` returning correct, page-cited answers.

## Architecture

Five swappable stages, one file each in `src/`, wired together by `src/pipeline.py` and invoked from `ask.py`:

```
ingest → chunk → embed → retrieve → generate
load_pdf  chunk_pages  embed_texts  top_k  answer
```

- **ingest** (`fitz`/pymupdf) → `Page(number, text)`, dropping empty pages.
- **chunk** → `Chunk(text, page, index)`, fixed word-windows with overlap.
- **embed** → OpenAI `text-embedding-3-small` → `np.ndarray`.
- **retrieve** → in-memory cosine similarity, top-k.
- **generate** → Anthropic `claude-sonnet-4-6` with a system prompt that forces page citations and refuses with the exact string `"That isn't covered in this document."` when the answer isn't in the excerpts.

**The page number is the load-bearing thread.** It originates in `ingest` and is carried through `Page` → `Chunk` → the `[page N]` context block in `generate` so the final answer can cite it. Preserve it across any change.

**Caching:** `build_index` in `pipeline.py` caches embeddings to `.cache/` (`vectors.npy` + `chunks.json`). It is keyed only by existence, not by content — **after changing the PDF, chunk size, or embedding model you must delete `.cache/`** or you'll query stale vectors.

## Where answer quality lives (in order)

1. `src/chunk.py` — `words_per_chunk` / `overlap`. Start here when answers are wrong.
2. `src/retrieve.py` — `k` (chunks fed to the LLM; also a param on `pipeline.ask`).
3. `src/generate.py` — the system prompt and model choice.

`pipeline.ask(show_sources=True)` prints retrieved chunks + scores per question — this is the primary debugging window. A wrong answer is usually a retrieval miss, not an LLM failure.

## Swapping providers

The stage-per-file boundary is the point: to reuse this skeleton, swap one file without touching the rest. `src/embed.py` notes a zero-API-key local alternative (sentence-transformers / all-MiniLM). `src/generate.py` can drop to `claude-haiku-4-5` for speed/cost.
