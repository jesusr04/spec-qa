# Demo Brief — Spec/Submittal Q&A

> This is your reusable **Demo Brief** template. It is deliberately ~one page.
> Every future build starts by copying this file and filling it in *before* you
> write code. It is the anti-DIE artifact: if the build can't fit on this page,
> the scope is too big. When a demo earns the right to become a product, this
> page grows into a PRD — not before.

*Created: 2026-05-31*

## The one-liner
A CLI that answers questions about a single construction spec PDF and cites the
page each answer came from.

## Why this build (the real goal)
A working, demoable RAG pipeline I can show in an AEC AI startup conversation
(Trunk Tools, Belidor). The prize is a 2-minute Loom of a cited answer over a
real spec — not a reusable framework. Reuse is a byproduct of clean module
boundaries, extracted on build #2.

## The ONE document
- File: `Item 422 - Concrete Superstructures.pdf`  ← replace with a real spec section you have
- What it is: 1st page of the specification for Concrete Superstrucutres

## The 3–5 demo questions (must work reliably)
These define "done." Write real ones you know the answers to.
1. What class of concrete do I use for the bridge deck? 
2. What material do I need for curing the bridge slab?
3. What kind of fiber expansion can I use at the bridge approach slab?
4. What sealant is allowed for expansion joints?
5. What type of evaporation Retardants can I use for the bridge slab? 

## Definition of done
- [ ] All 5 questions return a correct answer
- [ ] Every answer cites a page number
- [ ] A question NOT in the doc returns "That isn't covered in this document."
- [ ] 2-minute Loom recorded

## Scope guardrails (do NOT cross these)
- One document. One happy path: upload → ask → cited answer.
- No auth, no multi-user, no web UI (CLI + Loom is the demo).
- No vector DB — in-memory cosine is enough for one doc.
- Time-box: ship in one week. If a stage eats more than a day, simplify it.

## The 5 stages (your learning milestone)
| Stage | File | What you'll learn |
|-------|------|-------------------|
| 1 Ingest | `src/ingest.py` | PDF → clean, page-tagged text |
| 2 Chunk | `src/chunk.py` | chunking strategy directly drives answer quality |
| 3 Embed | `src/embed.py` | text → vectors |
| 4 Retrieve | `src/retrieve.py` | vector search for relevant chunks |
| 5 Generate | `src/generate.py` | cited answer, refuses when absent |

## First move (next 48h)
Fill in the document + 5 questions above. Drop the PDF at `data/spec.pdf`.
Then `python -m src.ingest data/spec.pdf` and eyeball the text. That's stage 1.
