"""Extract Gemini share conversation from saved HTML to markdown."""

from __future__ import annotations

import re
import sys
import time
from pathlib import Path

import html2text
from bs4 import BeautifulSoup

from scrape_gemini_share import (
    OUTPUT_DIR,
    SHARE_URL,
    extract_title,
    extract_turns,
    slugify,
    to_markdown,
)

HTML_PATH = Path(__file__).resolve().parent / "_pw_page.html"


def main() -> int:
    if not HTML_PATH.exists():
        raise FileNotFoundError(f"HTML introuvable: {HTML_PATH}")

    soup = BeautifulSoup(HTML_PATH.read_text(encoding="utf-8"), "lxml")
    title = extract_title(soup)
    turns = extract_turns(soup)

    if not turns:
        raise RuntimeError("Aucun message extrait du HTML.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"gemini-{slugify(title)}.md"
    out_path.write_text(to_markdown(SHARE_URL, title, turns), encoding="utf-8")

    sys.stdout.buffer.write(
        (
            f"Title: {title}\n"
            f"Messages: {len(turns)}\n"
            f"Written: {out_path}\n"
            f"Size: {out_path.stat().st_size} bytes\n"
        ).encode("utf-8")
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
