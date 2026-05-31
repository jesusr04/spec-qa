# Showcase — Spec Q&A

Public-facing copy for the repo README, the demo video, and the social post.
Edit freely. The grounding examples come from TxDOT Item 422 (Concrete
Superstructures), the document used in the demo.

---

## Repo "About" one-liner
Ask a construction spec a question in plain English and get the answer with a
citation back to the exact page. A working RAG demo.

---

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
1. Ingest the spec PDF into page-tagged text.
2. Chunk it into retrievable pieces.
3. Embed each chunk as a vector.
4. Retrieve the chunks most relevant to your question.
5. Generate an answer from only those chunks, with a page citation.

Built in Python. One document, command-line interface, no cloud database. This
is a demo, not a product.

---

## Demo video outline (aim for 60 to 90 seconds)
- 0:00  Hook. Show the dense spec PDF and say the problem in one line: "The
  answer to this question is somewhere in here. Finding it is the job."
- 0:12  Type the first question in the terminal. Let the cited answer appear.
- 0:30  Ask a second and third question. Show the page citation each time.
- 0:50  Ask something the document does not cover. Show it refusing instead of
  guessing. This is the moment that earns trust.
- 1:00  One sentence on how it works (five-stage RAG) and who it is for.
- Close. "Civil engineer, building AI tools in the space. Repo in the comments."

Tip: keep your real answer key on screen or in hand so a viewer who knows specs
can see the answers are correct.

---

## Social post draft (LinkedIn primary)
Construction specs hold the answer to almost every field question, and almost no
one can find it fast.

On a TxDOT bridge, one document sets the class of concrete for the deck, the
curing material for the slab, the sealant for the expansion joints, the
expansion material at the approach slab. The answers are all in there. Getting
one wrong means a rejected pour or a rework.

So I built a tool you can ask in plain English. "What class of concrete do I use
for the bridge deck?" It answers and cites the exact page. Ask it something the
spec does not cover and it tells you that, instead of guessing.

Under the hood it is RAG: the document is chunked, embedded, searched by meaning,
and an LLM answers from only the retrieved text. Five stages, built in Python,
running on one real spec.

This is a demo, not a product. I am a structural engineer who got tired of
hunting through PDFs, so I built the thing I wanted.

If you are working on document AI in construction, I would like to compare notes.

Demo video below. Repo in the comments.

---

## Short version (X / threads)
Construction specs hold the answer to almost every field question. Finding it is
the hard part.

So I built a tool you ask in plain English. "What class of concrete for the
bridge deck?" It answers and cites the page. Does not cover it? It says so
instead of guessing.

RAG, in Python, on a real TxDOT spec. Demo below.
