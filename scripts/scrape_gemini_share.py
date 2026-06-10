"""Scrape a public Gemini share link and export to markdown."""

from __future__ import annotations

import re
import sys
import time
from pathlib import Path

import html2text
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

SHARE_URL = "https://gemini.google.com/share/005642214c6a"
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "brainstorming" / "raw"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


def html_to_md(fragment: str) -> str:
    converter = html2text.HTML2Text()
    converter.body_width = 0
    converter.ignore_links = False
    return converter.handle(fragment).strip()


def clean_user_text(text: str) -> str:
    text = re.sub(r"^Vous avez dit\s*", "", text.strip())
    return text.strip()


def extract_title(soup: BeautifulSoup) -> str:
    h1 = soup.find("h1")
    if h1:
        title = h1.get_text(strip=True)
        if title and "gemini" not in title.lower():
            return title.replace("\u200e", "").strip()

    og = soup.find("meta", property="og:title")
    if og and og.get("content"):
        title = re.sub(r"^Gemini\s*[-:]\s*", "", og["content"]).strip()
        return title.replace("\u200e", "").strip()

    return "Discussion Gemini"


def extract_turns(soup: BeautifulSoup) -> list[dict[str, str]]:
    """Extract ordered user/model pairs from share-turn-viewer blocks."""
    turns: list[dict[str, str]] = []
    seen_ids: set[str] = set()

    for viewer in soup.select("share-turn-viewer"):
        turn_id = viewer.get("id")
        if turn_id:
            if turn_id in seen_ids:
                continue
            seen_ids.add(turn_id)

        user_el = viewer.select_one("user-query")
        model_el = viewer.select_one("message-content")

        if user_el:
            user_text = clean_user_text(user_el.get_text("\n", strip=True))
            if user_text:
                turns.append({"role": "user", "text": user_text})

        if model_el:
            model_text = html_to_md(str(model_el))
            if model_text:
                turns.append({"role": "model", "text": model_text})

    return turns


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")[:80] or "discussion"


def to_markdown(url: str, title: str, turns: list[dict[str, str]]) -> str:
    lines = [
        f"# {title}",
        "",
        f"- **Source:** {url}",
        f"- **Exporté le:** {time.strftime('%Y-%m-%d %H:%M')}",
        f"- **Messages:** {len(turns)}",
        "",
        "---",
        "",
    ]

    exchange = 0
    for msg in turns:
        role = msg["role"]
        text = msg["text"].strip()
        if not text:
            continue

        if role == "user":
            exchange += 1
            lines.append(f"## Échange {exchange}")
            lines.append("")
            lines.append("### Utilisateur")
            lines.append("")
            lines.append(text)
            lines.append("")
        else:
            lines.append("### Gemini")
            lines.append("")
            lines.append(text)
            lines.append("")
            lines.append("---")
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def fetch_page_html(url: str) -> str:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(channel="msedge", headless=True)
        context = browser.new_context(user_agent=USER_AGENT, locale="fr-FR")
        context.add_cookies(
            [
                {
                    "name": "CONSENT",
                    "value": "YES+cb.20210328-17-p0.fr+FX+667",
                    "domain": ".google.com",
                    "path": "/",
                },
                {"name": "SOCS", "value": "CAI", "domain": ".google.com", "path": "/"},
            ]
        )
        page = context.new_page()
        page.goto(url, wait_until="commit", timeout=60_000)
        page.wait_for_timeout(15_000)

        try:
            page.get_by_role("button", name="Tout accepter").click(timeout=3000)
            page.wait_for_timeout(4000)
        except Exception:  # noqa: BLE001
            pass

        for _ in range(40):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(500)

        html = page.content()
        browser.close()
        return html


def main() -> int:
    url = sys.argv[1] if len(sys.argv) > 1 else SHARE_URL
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    html = fetch_page_html(url)
    soup = BeautifulSoup(html, "lxml")
    title = extract_title(soup)
    turns = extract_turns(soup)

    if not turns:
        sys.stderr.write("ERROR: aucun message extrait.\n")
        return 1

    out_path = OUTPUT_DIR / f"gemini-{slugify(title)}.md"
    out_path.write_text(to_markdown(url, title, turns), encoding="utf-8")

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
