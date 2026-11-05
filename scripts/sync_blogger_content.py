#!/usr/bin/env python3
"""Safely sync Markdown article sources to Blogger DRAFTS only.

Published posts are never modified, pages are not synced, and no source deletion
is propagated to Blogger. Human review and manual publishing are separate steps.
"""
from __future__ import annotations
import hashlib
import html
import os
import re
import sys
import time
from pathlib import Path
from typing import Any
import markdown
import yaml
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

BLOG_ID = os.environ.get("BLOGGER_BLOG_ID", "").strip()
SOURCE_MARKER_PREFIX = "<!-- trtt-github-source:"
SHA_MARKER_PREFIX = "<!-- trtt-github-sha:"
POSTS_DIR = Path("posts")
SKIP_POSTS = {"news_guideline.md"}


def require_secrets() -> None:
    names = ("BLOGGER_BLOG_ID", "BLOGGER_CLIENT_ID", "BLOGGER_CLIENT_SECRET", "BLOGGER_REFRESH_TOKEN")
    missing = [name for name in names if not os.environ.get(name, "").strip()]
    if missing:
        raise RuntimeError("Missing Blogger secret(s): " + ", ".join(missing))


def make_service():
    credentials = Credentials(
        token=None, refresh_token=os.environ["BLOGGER_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["BLOGGER_CLIENT_ID"],
        client_secret=os.environ["BLOGGER_CLIENT_SECRET"],
        scopes=["https://www.googleapis.com/auth/blogger"],
    )
    return build("blogger", "v3", credentials=credentials, cache_discovery=False)


def split_front_matter(raw: str) -> tuple[dict[str, Any], str]:
    match = re.match(r"\A---\s*\r?\n(.*?)\r?\n---\s*\r?\n", raw, re.S)
    if not match:
        return {}, raw
    metadata = yaml.safe_load(match.group(1)) or {}
    if not isinstance(metadata, dict):
        raise ValueError("Markdown front matter must be a YAML mapping.")
    return metadata, raw[match.end():]


def plain_title(value: str) -> str:
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", value))).strip()


def title_from_markdown(source: str, fallback: str) -> str:
    match = re.search(r"(?m)^#\s+(.+?)\s*$", source)
    return plain_title(match.group(1)) if match else fallback


def marker_for(path: str) -> str:
    return SOURCE_MARKER_PREFIX + path + " -->"


def sha_marker_for(digest: str) -> str:
    return SHA_MARKER_PREFIX + digest + " -->"


def build_content(path: Path) -> dict[str, Any]:
    source = path.read_text(encoding="utf-8")
    relative = path.as_posix()
    digest = hashlib.sha256(source.encode("utf-8")).hexdigest()
    fallback = path.stem.replace("-", " ").replace("_", " ").title()
    metadata, markdown_source = split_front_matter(source)
    title = str(metadata.get("title") or title_from_markdown(markdown_source, fallback)).strip()
    if not title:
        raise ValueError(f"{relative}: a non-empty title is required.")
    content = markdown.markdown(markdown_source, extensions=["extra", "sane_lists", "toc"], output_format="html5")
    content = re.sub(r"<h1\b[^>]*>.*?</h1\s*>", "", content, count=1, flags=re.I | re.S)
    labels = metadata.get("labels", ["TRTT News 24 BD"])
    if isinstance(labels, str):
        labels = [labels]
    if not isinstance(labels, list) or not all(isinstance(x, str) for x in labels):
        raise ValueError(f"{relative}: labels must be a list of strings.")
    content = content.rstrip() + "\n" + marker_for(relative) + "\n" + sha_marker_for(digest)
    return {"path": relative, "sha": digest, "title": title, "content": content, "labels": labels}


def list_all_posts(resource):
    items, token = [], None
    while True:
        kwargs = {"blogId": BLOG_ID, "maxResults": 500, "status": ["LIVE", "DRAFT"]}
        if token:
            kwargs["pageToken"] = token
        response = resource.list(**kwargs).execute(num_retries=7)
        items.extend(response.get("items", []))
        token = response.get("nextPageToken")
        if not token:
            return items


def source_path(item: dict[str, Any]) -> str | None:
    match = re.search(r"<!--\s*trtt-github-source:(.*?)\s*-->", item.get("content") or "")
    return match.group(1).strip() if match else None


def source_sha(item: dict[str, Any]) -> str | None:
    match = re.search(r"<!--\s*trtt-github-sha:(.*?)\s*-->", item.get("content") or "")
    return match.group(1).strip() if match else None


def sync_drafts(resource, desired: dict[str, dict[str, Any]]) -> tuple[int, int]:
    existing = {source_path(item): item for item in list_all_posts(resource) if source_path(item)}
    created = updated = 0
    for path, record in desired.items():
        old = existing.get(path)
        if old and source_sha(old) == record["sha"]:
            if str(old.get("status", "")).upper() != "DRAFT":
                raise RuntimeError(f"{path}: managed post is LIVE; refusing to claim draft-only sync.")
            print(f"UNCHANGED DRAFT {path}: Blogger ID {old.get('id')}")
            continue
        if old:
            if str(old.get("status", "")).upper() != "DRAFT":
                raise RuntimeError(f"{path}: existing post is LIVE; refusing to modify or republish it.")
            result = resource.update(
                blogId=BLOG_ID, postId=old["id"],
                body={"kind": "blogger#post", "title": record["title"],
                      "content": record["content"], "labels": record["labels"]},
            ).execute(num_retries=7)
            if str(result.get("status", "")).upper() != "DRAFT":
                raise RuntimeError(f"{path}: Blogger did not retain DRAFT status after update.")
            updated += 1
            print(f"UPDATED DRAFT {path}: Blogger ID {result.get('id', old['id'])}")
        else:
            result = resource.insert(
                blogId=BLOG_ID,
                body={"kind": "blogger#post", "title": record["title"],
                      "content": record["content"], "labels": record["labels"]},
                isDraft=True,
            ).execute(num_retries=7)
            if str(result.get("status", "")).upper() != "DRAFT":
                raise RuntimeError(f"{path}: Blogger did not confirm DRAFT status.")
            created += 1
            print(f"CREATED DRAFT {path}: Blogger ID {result.get('id')}")
        time.sleep(1.0)
    return created, updated


def main() -> int:
    require_secrets()
    records = {}
    if POSTS_DIR.exists():
        for path in sorted(POSTS_DIR.glob("*.md")):
            if path.name in SKIP_POSTS:
                print(f"SKIPPED documentation file: {path}")
                continue
            record = build_content(path)
            records[record["path"]] = record
    print(f"Markdown article sources discovered: {len(records)}")
    service = make_service()
    blog = service.blogs().get(blogId=BLOG_ID).execute(num_retries=7)
    print(f"Connected Blogger blog: {blog.get('name')} ({blog.get('url')})")
    created, updated = sync_drafts(service.posts(), records)
    print(f"DRAFT SYNC COMPLETE — created={created}; updated={updated}; deleted=0; pages=skipped")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except HttpError as exc:
        status = getattr(exc.resp, "status", "unknown")
        print(f"BLOGGER API ERROR: HTTP {status}: {str(exc)[:1500]}", file=sys.stderr)
        raise SystemExit(1)
    except Exception as exc:
        print(f"SYNC FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(1)
