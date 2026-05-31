"""CLI entry point.

    python ask.py "What compressive strength is required for sidewalk concrete?"

First run embeds the document (see BRIEF.md / README.md for setup).
"""
import sys

from dotenv import load_dotenv

# Load .env BEFORE importing the pipeline: src/embed.py and src/generate.py
# read their API keys and build clients at import time.
load_dotenv()

from src.pipeline import ask, build_index

# Your spec PDF. See BRIEF.md, step 0.
PDF_PATH = "data/spec.pdf"


def main() -> None:
    if len(sys.argv) < 2:
        print('Usage: python ask.py "your question"')
        sys.exit(1)

    question = " ".join(sys.argv[1:])
    chunks, vecs = build_index(PDF_PATH)
    print(ask(question, chunks, vecs))


if __name__ == "__main__":
    main()
