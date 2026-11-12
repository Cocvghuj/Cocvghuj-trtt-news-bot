#!/usr/bin/env python3
"""Create one verified TRTT Blogger DRAFT from a location-news GitHub issue.

The assistant researches and writes the article before opening the issue.
This script only transfers that reviewed payload to Blogger. It never publishes LIVE.
"""
from __future__ import annotations

import json
import os
import re
import sys
from typing import Any
from urllib.parse import urlparse


def required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required GitHub Actions secret: {name}")
    return value


def read_payload() -> dict[str, Any]:
    event_path = required("GITHUB_EVENT_PATH")
    with open(event_path, "r", encoding="utf-8") as handle:
        event = json.load(handle)

    issue = event.get("issue") or {}
    title = str(issue.get("title", ""))
    author = str((issue.get("user") or {}).get("login", ""))
    if not title.startswith("[TRTT-LOCATION-NEWS]"):
        raise RuntimeError("Safety stop: issue title is not a TRTT location-news request.")
    if author != "Cocvghuj":
        raise RuntimeError("Safety stop: only the repository owner may submit a TRTT draft payload.")

    body = str(issue.get("body") or "")
    match = re.search(r"```json\s*(\{.*?\})\s*```", body, flags=re.S)
    if not match:
        raise RuntimeError("Issue body must contain one fenced JSON article payload.")
    payload = json.loads(match.group(1))
    if not isinstance(payload, dict):
        raise RuntimeError("Article payload must be a JSON object.")
    return payload


def validate(payload: dict[str, Any]) -> tuple[str, str, list[str]]:
    title = str(payload.get("title", "")).strip()
    content = str(payload.get("html", "")).strip()
    labels = payload.get("labels")
    if not title or len(title) > 300:
        raise RuntimeError("Article title is missing or exceeds 300 characters.")
    if not isinstance(content, str) or len(content) < 2000:
        raise RuntimeError("Article HTML is too short; refusing a thin or empty post.")
    if not isinstance(labels, list) or not labels:
        raise RuntimeError("At least one Blogger label is required.")
    labels = [str(item).strip() for item in labels if str(item).strip()]
    if not labels:
        raise RuntimeError("Blogger labels are empty.")

    image_url = str(payload.get("image_url", "")).strip()
    image_alt = str(payload.get("image_alt", "")).strip()
    image_credit_url = str(payload.get("image_credit_url", "")).strip()
    image_rights = str(payload.get("image_rights", "")).strip()
    for label, url in (("image", image_url), ("image credit", image_credit_url)):
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.netloc:
            raise RuntimeError(f"Invalid HTTPS {label} URL.")
    if len(image_alt) < 12 or len(image_rights) < 12:
        raise RuntimeError("Image alt text and documented usage-rights note are required.")
    if image_url not in content or image_alt not in content or image_credit_url not in content:
        raise RuntimeError("The HTML must include the declared image, alt text and image credit link.")

    sources = payload.get("sources")
    if not isinstance(sources, list) or len(sources) < 5:
        raise RuntimeError("Five or more independently listed source URLs are required.")
    for source in sources:
        if not isinstance(source, dict):
            raise RuntimeError("Each source must be an object.")
        url = str(source.get("url", "")).strip()
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.netloc or url not in content:
            raise RuntimeError("Every listed source must be an HTTPS link included in the article HTML.")

    description = str(payload.get("search_description", "")).strip()
    if not description or len(description) > 160:
        raise RuntimeError("SEO search_description is required and must be at most 160 characters.")
    if description not in content:
        raise RuntimeError("The search description must appear as the article's opening summary.")

    if "affiliate disclosure" not in content.lower() and "affiliate links" not in content.lower():
        raise RuntimeError("Affiliate disclosure is required.")
    if "rel=\"sponsored\"" not in content.lower():
        raise RuntimeError("Affiliate links must carry rel=sponsored.")
    return title, content, labels


def find_existing(service: Any, blog_id: str, title: str) -> dict[str, Any] | None:
    page_token = None
    for _ in range(20):
        args: dict[str, Any] = {
            "blogId": blog_id,
            "maxResults": 100,
            "status": ["LIVE", "DRAFT"],
            "view": "ADMIN",
        }
        if page_token:
            args["pageToken"] = page_token
        page = service.posts().list(**args).execute()
        for post in page.get("items", []):
            if post.get("title") == title:
                status = str(post.get("status", "")).upper()
                if status == "LIVE":
                    raise RuntimeError("Safety stop: matching title already exists as LIVE; nothing changed.")
                if status != "DRAFT":
                    raise RuntimeError(f"Safety stop: matching post has unexpected status {status!r}.")
                return post
        page_token = page.get("nextPageToken")
        if not page_token:
            return None
    raise RuntimeError("Duplicate scan exceeded 20 pages; refusing to create a post.")


def main() -> int:
    payload = read_payload()
    title, content, labels = validate(payload)
    blog_id = required("BLOGGER_BLOG_ID")
    client_id = required("BLOGGER_CLIENT_ID")
    client_secret = required("BLOGGER_CLIENT_SECRET")
    refresh_token = required("BLOGGER_REFRESH_TOKEN")

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

    existing = find_existing(service, blog_id, title)
    if existing:
        post_id = str(existing.get("id", "")).strip()
        print(f"Existing matching DRAFT found; no duplicate created. post_id={post_id}")
    else:
        created = service.posts().insert(
            blogId=blog_id,
            isDraft=True,
            body={
                "kind": "blogger#post",
                "title": title,
                "content": content,
                "labels": labels,
            },
        ).execute()
        post_id = str(created.get("id", "")).strip()
        if not post_id:
            raise RuntimeError("Blogger returned no post ID.")

    verified = service.posts().get(blogId=blog_id, postId=post_id, view="ADMIN").execute()
    if str(verified.get("id", "")) != post_id:
        raise RuntimeError("Read-back post ID mismatch.")
    if str(verified.get("status", "")).upper() != "DRAFT":
        raise RuntimeError("Safety stop: read-back status is not DRAFT.")
    if verified.get("title") != title:
        raise RuntimeError("Read-back title mismatch.")
    if str(payload.get("image_url", "")) not in str(verified.get("content", "")):
        raise RuntimeError("Read-back image verification failed.")

    print(
        "VERIFIED TRTT NEWS DRAFT"
        f" | post_id={post_id}"
        " | status=DRAFT"
        f" | location={payload.get('location', 'not supplied')}"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
