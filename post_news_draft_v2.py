#!/usr/bin/env python3
"""Create and verify one Reuters-sourced, 300-word Blogger DRAFT on both TRTT blogs.

Safety: this script only inserts with isDraft=True. It never publishes, edits, or deletes.
"""
from __future__ import annotations

import html
import os
import re
import sys
from typing import Any

TITLE = "Oil Prices Rise as Hormuz Shipping Risks Offset Hopes for Iran De-escalation"
SOURCE_URL = "https://www.reuters.com/business/energy/oil-rises-two-month-low-hormuz-shipping-attacks-offset-iran-truce-hopes-2026-11-11/"
LABELS = ["World News", "Energy", "Oil Markets", "Reuters"]

ARTICLE_PARAGRAPHS = [
    "Oil prices rose on Wednesday, November 11, after falling to two-month lows in the previous session. Traders balanced hopes for easing tensions with continuing attacks on commercial shipping near the Strait of Hormuz, a major route for global energy supplies.",
    "Brent crude futures gained 71 cents, or 0.78%, to $92.20 a barrel by 0119 GMT. US West Texas Intermediate rose 49 cents, or 0.57%, to $86.53, Reuters reported. Prices had initially fallen by more than $3 on Tuesday after US officials played down further military strikes against Iran.",
    "Shipping risks remained central. The Washington Institute for Near East Policy said 37 ships were attacked in the Strait of Hormuz and nearby waterways in October, the highest monthly total since the war began. Ten further attacks had been recorded in November at the time of the report.",
    "Reuters reported that video verified by the agency showed the Navig8 tanker on fire near Oman on Sunday. The United Kingdom Maritime Trade Operations agency separately reported that another tanker was struck northeast of Lima, Oman, on Tuesday. Iran’s Revolutionary Guards Navy said two tankers caught fire after hitting naval mines on a route it called unauthorised.",
    "Analysts cited by Reuters warned that even a diplomatic agreement might not quickly restore normal traffic. Mine clearance, insurance costs and shipowners’ willingness to accept risks could delay a recovery in shipping flows.",
    "Market sources citing the American Petroleum Institute said US crude inventories rose by 9 million barrels in the week ended November 6. Reuters also reported that Russian oil-refining capacity had fallen about 30% since late October following renewed Ukrainian drone attacks.",
    "The market’s next direction will depend on whether diplomacy reduces regional risks and whether commercial shipping can safely resume normal operations over the coming days and weeks."
]

def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))

def build_html() -> str:
    paragraphs = "\n".join(f"<p>{html.escape(p)}</p>" for p in ARTICLE_PARAGRAPHS)
    source = f'<p><strong>Source:</strong> <a href="{html.escape(SOURCE_URL, quote=True)}" rel="nofollow noopener">Reuters, November 11, 2026</a>.</p>'
    return paragraphs + "\n" + source

def require_env() -> tuple[str, str, str, str, str]:
    names = ("BLOGGER_BLOG_ID", "FLIGHTSCOUTPRO_BLOG_ID",
             "BLOGGER_CLIENT_ID", "BLOGGER_CLIENT_SECRET", "BLOGGER_REFRESH_TOKEN")
    missing = [name for name in names if not os.environ.get(name, "").strip()]
    if missing:
        raise RuntimeError("Missing required GitHub Actions secrets: " + ", ".join(missing))
    main_id = os.environ["BLOGGER_BLOG_ID"].strip()
    flight_id = os.environ["FLIGHTSCOUTPRO_BLOG_ID"].strip()
    if main_id == flight_id:
        raise RuntimeError("The two Blogger blog IDs must be different.")
    return (main_id, flight_id, os.environ["BLOGGER_CLIENT_ID"].strip(),
            os.environ["BLOGGER_CLIENT_SECRET"].strip(),
            os.environ["BLOGGER_REFRESH_TOKEN"].strip())

def verify_draft(service: Any, blog_id: str, post_id: str) -> dict:
    post = service.posts().get(blogId=blog_id, postId=post_id).execute()
    if str(post.get("id", "")) != str(post_id):
        raise RuntimeError(f"Read-back ID mismatch for blog {blog_id}.")
    status = str(post.get("status", "")).upper()
    if status != "DRAFT":
        raise RuntimeError(f"Safety stop: blog {blog_id}, post {post_id} returned {status or 'UNKNOWN'}, not DRAFT.")
    if post.get("title") != TITLE:
        raise RuntimeError(f"Read-back title mismatch for blog {blog_id}, post {post_id}.")
    return post

def find_existing(service: Any, blog_id: str) -> dict | None:
    token = None
    for _ in range(20):
        args = {"blogId": blog_id, "maxResults": 100, "status": ["LIVE", "DRAFT"]}
        if token:
            args["pageToken"] = token
        response = service.posts().list(**args).execute()
        for item in response.get("items", []):
            if item.get("title") == TITLE:
                status = str(item.get("status", "")).upper()
                if status == "LIVE":
                    raise RuntimeError(f"Matching article is already LIVE on blog {blog_id}; no changes made.")
                if status != "DRAFT":
                    raise RuntimeError(f"Matching article has unexpected status {status!r} on blog {blog_id}.")
                return item
        token = response.get("nextPageToken")
        if not token:
            return None
    raise RuntimeError(f"Duplicate scan exceeded 20 pages for blog {blog_id}; refusing to insert.")

def create_or_confirm(service: Any, blog_id: str, blog_name: str) -> str:
    existing = find_existing(service, blog_id)
    if existing:
        post_id = str(existing.get("id", "")).strip()
        if not post_id:
            raise RuntimeError(f"Matching draft on {blog_name} has no ID.")
        verify_draft(service, blog_id, post_id)
        print(f"CONFIRMED existing DRAFT: {blog_name} | post_id={post_id}")
        return post_id

    result = service.posts().insert(
        blogId=blog_id,
        isDraft=True,
        body={"kind": "blogger#post", "title": TITLE, "content": build_html(), "labels": LABELS},
    ).execute()
    post_id = str(result.get("id", "")).strip()
    if not post_id:
        raise RuntimeError(f"Blogger returned no post ID for {blog_name}.")
    verify_draft(service, blog_id, post_id)
    print(f"VERIFIED DRAFT: {blog_name} | post_id={post_id}")
    return post_id

def main() -> int:
    plain_text = "\n".join(ARTICLE_PARAGRAPHS)
    count = word_count(plain_text)
    if count != 300:
        raise RuntimeError(f"Article validation failed: expected 300 words, found {count}.")
    if "https://www.reuters.com/" not in SOURCE_URL:
        raise RuntimeError("Source validation failed.")
    main_id, flight_id, client_id, client_secret, refresh_token = require_env()

    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    credentials = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/blogger"],
    )
    service = build("blogger", "v3", credentials=credentials, cache_discovery=False)

    results = [
        create_or_confirm(service, main_id, "TRTT News 24 BD"),
        create_or_confirm(service, flight_id, "FlightScoutPro"),
    ]
    if len(results) != 2 or not all(results):
        raise RuntimeError("Both blog drafts must be verified before success.")
    print("SUCCESS: both Blogger posts were read back and verified as DRAFT. No LIVE post was created.")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
