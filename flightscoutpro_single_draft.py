#!/usr/bin/env python3
"""Create or confirm exactly one FlightScoutPro Blogger DRAFT from a reviewed JSON payload.

This script intentionally knows only FLIGHTSCOUTPRO_BLOG_ID. It never targets
the TRTT main blog and never publishes LIVE posts.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any


def required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required GitHub Actions secret: {name}")
    return value


def main() -> int:
    payload_path = Path(os.environ.get("ARTICLE_PAYLOAD", "news/flightscoutpro-single-draft.json"))
    if not payload_path.is_file():
        raise RuntimeError(f"Article payload not found: {payload_path}")
    payload = json.loads(payload_path.read_text(encoding="utf-8"))

    title = str(payload.get("title", "")).strip()
    content = str(payload.get("html", "")).strip()
    labels = payload.get("labels", [])
    if not isinstance(labels, list):
        raise RuntimeError("Article labels must be a JSON array.")
    labels = [str(item).strip() for item in labels if str(item).strip()]

    if not title or len(title) > 300:
        raise RuntimeError("Article title is missing or too long (maximum 300 characters).")
    if len(content) < 80:
        raise RuntimeError("Article HTML is too short; refusing to create an empty/thin draft.")
    if not labels:
        raise RuntimeError("At least one Blogger label is required.")

    blog_id = required("FLIGHTSCOUTPRO_BLOG_ID")
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

    # Idempotency guard: never create a duplicate, and never modify a LIVE post.
    page_token = None
    existing = None
    for _ in range(20):
        params: dict[str, Any] = {
            "blogId": blog_id,
            "maxResults": 100,
            "status": ["LIVE", "DRAFT"],
            "view": "ADMIN",
        }
        if page_token:
            params["pageToken"] = page_token
        page = service.posts().list(**params).execute()
        for post in page.get("items", []):
            if post.get("title") == title:
                status = str(post.get("status", "")).upper()
                if status == "LIVE":
                    raise RuntimeError("Safety stop: a LIVE post already has this title; nothing changed.")
                if status != "DRAFT":
                    raise RuntimeError(f"Safety stop: matching post has unexpected status {status!r}.")
                existing = post
                break
        if existing:
            break
        page_token = page.get("nextPageToken")
        if not page_token:
            break
    else:
        raise RuntimeError("Duplicate scan exceeded 20 pages; refusing to continue.")

    if existing:
        post_id = str(existing.get("id", "")).strip()
        print(f"Found existing matching DRAFT; no duplicate created. post_id={post_id}")
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
            raise RuntimeError("Blogger returned no post ID; verification failed.")

    # Read back from Blogger ADMIN view and prove the status is DRAFT.
    verified = service.posts().get(blogId=blog_id, postId=post_id, view="ADMIN").execute()
    if str(verified.get("id", "")) != post_id:
        raise RuntimeError("Read-back post ID mismatch.")
    if str(verified.get("status", "")).upper() != "DRAFT":
        raise RuntimeError("Safety stop: Blogger read-back status is not DRAFT.")
    if verified.get("title") != title:
        raise RuntimeError("Read-back title mismatch.")

    print(f"VERIFIED FlightScoutPro DRAFT | post_id={post_id} | status=DRAFT")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
