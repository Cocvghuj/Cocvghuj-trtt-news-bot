#!/usr/bin/env python3
"""Generate a Blogger-ready TRTT HTML draft with OpenRouter's free-model router.

This script never publishes to Blogger and never sends to Telegram.
"""
from __future__ import annotations

import datetime as dt
import html
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
SITE_URL = "https://trttvoyage.com"
TOPICS = [
    "A practical checklist for planning a low-stress international trip",
    "How to compare airport transfer options before you travel",
    "What to check before choosing an eSIM for an international journey",
    "How to prepare documents and digital backups before a trip",
    "Ways to make a travel itinerary flexible without losing structure",
    "How to pack thoughtfully for a multi-climate journey",
    "A first-time traveler's guide to understanding flight connections",
]

def request_draft(topic: str) -> dict:
    key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if not key:
        raise RuntimeError("Missing GitHub Actions Secret: OPENROUTER_API_KEY")

    system = (
        "You are the editorial assistant for TRTT Voyage. Write accurate, useful, "
        "evergreen travel guidance in clear international English. Never invent "
        "statistics, current prices, policies, laws, named sources, quotations, "
        "product availability, or URLs. Do not present legal or airline-policy "
        "claims as universal; tell readers to verify current rules with official "
        "providers. Do not create fake citations or image URLs. Return ONLY one "
        "valid JSON object with keys title, slug, html. The html value must be a "
        "Blogger-ready HTML fragment containing an introduction, exactly five "
        "substantive <h2> sections, an FAQ section with at least three questions, "
        "a transparent affiliate disclosure, and the marker 787950 in an HTML "
        "comment. Include a natural link to https://trttvoyage.com. No markdown "
        "fences. Do not include an image element unless a real image URL was "
        "provided in the input (none is provided)."
    )
    user = (
        f"Create one original TRTT Voyage blog draft about: {topic}. "
        "Target 800-1100 words. Avoid time-sensitive claims and fabricated "
        "recommendations. Keep the five main sections distinct. The disclosure "
        "must say affiliate links may be used where relevant, not that this "
        "specific article contains a link if none is present. "
        "Return JSON only."
    )
    payload = {
        "model": MODEL,
        "temperature": 0.4,
        "max_tokens": 5000,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "HTTP-Referer": SITE_URL,
            "X-Title": "TRTT Voyage Draft Agent",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:500]
        raise RuntimeError(f"OpenRouter HTTP {exc.code}: {detail}") from exc
    content = data["choices"][0]["message"]["content"]
    if not isinstance(content, str) or not content.strip():
        raise RuntimeError("OpenRouter returned an empty draft.")
    match = re.search(r"\{.*\}", content, re.S)
    if not match:
        raise RuntimeError("OpenRouter response did not contain a JSON object.")
    draft = json.loads(match.group(0))
    if not all(isinstance(draft.get(k), str) and draft[k].strip() for k in ("title", "slug", "html")):
        raise RuntimeError("Draft JSON is missing title, slug, or html.")
    return draft

def validate(draft: dict) -> None:
    body = draft["html"]
    lower = body.lower()
    h2_count = len(re.findall(r"<h2\b", lower))
    if h2_count < 6:
        raise RuntimeError(f"Draft needs five main sections plus FAQ; found {h2_count} h2 headings.")
    if "787950" not in body:
        raise RuntimeError("Required TRTT marker 787950 is missing.")
    if SITE_URL not in body:
        raise RuntimeError("Required TRTT Voyage website link is missing.")
    if not re.search(r"\bfaq\b|frequently asked questions", lower):
        raise RuntimeError("FAQ section is missing.")
    if re.search(r"<img\b", lower):
        raise RuntimeError("Refusing an AI-invented image URL; add a verified image manually.")
    if re.search(r"https?://(?!trttvoyage\.com)[^\s\"'<>]+", body):
        raise RuntimeError("Draft contains an external URL that requires editorial verification.")

def main() -> int:
    today = dt.datetime.now(dt.timezone.utc)
    topic = TOPICS[(today.timetuple().tm_yday - 1) % len(TOPICS)]
    draft = request_draft(topic)
    validate(draft)
    slug = re.sub(r"[^a-z0-9]+", "-", draft["slug"].lower()).strip("-")[:70]
    if not slug:
        raise RuntimeError("Draft slug is invalid.")
    stamp = today.strftime("%Y%m%d-%H%M%S")
    out = Path("blog/drafts") / f"{stamp}-trtt-{slug}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    safe_title = html.escape(draft["title"])
    document = f"""<!-- TRTT MAGIC - 787950 LOCKED -->
<!-- Generated with OpenRouter free-model routing. Editorial review required. -->
<!-- AI draft only: never auto-published. -->
<article class="trtt-voyage-article">
  <header>
    <p class="trtt-kicker">TRTT VOYAGE · TRAVEL GUIDE</p>
    <h1>{safe_title}</h1>
  </header>
  {draft["html"]}
  <footer>
    <p>Explore Beyond. Discover Everything. — <a href="{SITE_URL}">TRTT Voyage</a></p>
  </footer>
</article>
"""
    out.write_text(document, encoding="utf-8")
    print(f"Draft generated: {out}")
    print(f"Model requested: {MODEL}")
    print("Status: DRAFT ONLY — no Blogger publish, no Telegram send.")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
