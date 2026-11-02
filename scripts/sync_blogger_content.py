#!/usr/bin/env python3
"""Publish the GitHub-managed TRTT posts and pages to Blogger.

Managed sources:
  posts/*.md                 -> published Blogger posts
  pages/trttnews24bd/*.html  -> published Blogger pages

A stable source marker makes sync idempotent. Changed source files update the
matching Blogger item; deleted source files delete only items carrying a
TRTT GitHub source marker. Unmanaged Blogger content is never touched.
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
PAGES_DIR = Path("pages/trttnews24bd")
SKIP_POSTS = {"news_guideline.md"}


def require_secrets() -> None:
    names = ("BLOGGER_BLOG_ID", "BLOGGER_CLIENT_ID",
             "BLOGGER_CLIENT_SECRET", "BLOGGER_REFRESH_TOKEN")
    missing = [name for name in names if not os.environ.get(name, "").strip()]
    if missing:
        raise RuntimeError("Missing GitHub Actions secret(s): " + ", ".join(missing))


def make_service():
    credentials = Credentials(
        token=None,
        refresh_token=os.environ["BLOGGER_REFRESH_TOKEN"],
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
    value = re.sub(r"<[^>]+>", "", value)
    return html.unescape(re.sub(r"\s+", " ", value)).strip()


def title_from_markdown(source: str, fallback: str) -> str:
    match = re.search(r"(?m)^#\s+(.+?)\s*$", source)
    return plain_title(match.group(1)) if match else fallback


def title_from_html(source: str, fallback: str) -> str:
    match = re.search(r"<h1\b[^>]*>(.*?)</h1\s*>", source, re.I | re.S)
    if match:
        return plain_title(match.group(1))
    match = re.search(r"<title\b[^>]*>(.*?)</title\s*>", source, re.I | re.S)
    return plain_title(match.group(1)) if match else fallback


def remove_first_h1(content: str) -> str:
    return re.sub(r"<h1\b[^>]*>.*?</h1\s*>", "", content, count=1, flags=re.I | re.S)


def marker_for(path: str) -> str:
    return SOURCE_MARKER_PREFIX + path + " -->"


def sha_marker_for(digest: str) -> str:
    return SHA_MARKER_PREFIX + digest + " -->"


def build_content(path: Path) -> dict[str, Any]:
    source = path.read_text(encoding="utf-8")
    relative = path.as_posix()
    digest = hashlib.sha256(source.encode("utf-8")).hexdigest()
    fallback = path.stem.replace("-", " ").replace("_", " ").title()

    if relative.startswith("posts/"):
        metadata, markdown_source = split_front_matter(source)
        title = str(metadata.get("title") or title_from_markdown(markdown_source, fallback)).strip()
        if not title:
            raise ValueError(f"{relative}: a non-empty title is required.")
        content = markdown.markdown(
            markdown_source,
            extensions=["extra", "sane_lists", "toc"],
            output_format="html5",
        )
        content = remove_first_h1(content)
        labels = metadata.get("labels", ["TRTT News 24 BD"])
        if isinstance(labels, str):
            labels = [labels]
        if not isinstance(labels, list) or not all(isinstance(x, str) for x in labels):
            raise ValueError(f"{relative}: labels must be a list of strings.")
        body = {
            "kind": "blogger#post",
            "title": title,
            "content": content,
            "labels": labels,
        }
        kind = "post"
    else:
        title = title_from_html(source, fallback)
        content = remove_first_h1(source)
        body = {
            "kind": "blogger#page",
            "title": title,
            "content": content,
        }
        kind = "page"

    body["content"] = (
        body["content"].rstrip()
        + "\n"
        + marker_for(relative)
        + "\n"
        + sha_marker_for(digest)
    )
    return {"path": relative, "sha": digest, "kind": kind, "body": body}


def list_all(resource):
    items = []
    token = None
    while True:
        kwargs = {"blogId": BLOG_ID, "maxResults": 500}
        if token:
            kwargs["pageToken"] = token
        response = resource.list(**kwargs).execute(num_retries=7)
        items.extend(response.get("items", []))
        token = response.get("nextPageToken")
        if not token:
            return items


def marker_path(item: dict[str, Any]) -> str | None:
    content = item.get("content") or ""
    match = re.search(r"<!--\s*trtt-github-source:(.*?)\s*-->", content)
    return match.group(1).strip() if match else None


def marker_sha(item: dict[str, Any]) -> str | None:
    content = item.get("content") or ""
    match = re.search(r"<!--\s*trtt-github-sha:(.*?)\s*-->", content)
    return match.group(1).strip() if match else None


def sync_resource(resource, kind: str, desired: dict[str, dict[str, Any]]) -> tuple[int, int, int]:
    existing = list_all(resource)
    by_source = {
        marker_path(item): item
        for item in existing
        if marker_path(item) and marker_path(item).startswith(
            "posts/" if kind == "post" else "pages/trttnews24bd/"
        )
    }
    created = updated = deleted = 0

    for source_path, record in desired.items():
        if record["kind"] != kind:
            continue
        old = by_source.get(source_path)
        if old and marker_sha(old) == record["sha"]:
            print(f"UNCHANGED {source_path}: Blogger ID {old.get('id')}")
            continue

        body = dict(record["body"])
        if old:
            body["id"] = old["id"]
            if kind == "post":
                result = resource.update(
                    blogId=BLOG_ID, postId=old["id"], body=body, publish=True
                ).execute(num_retries=7)
                time.sleep(1.25)
            else:
                result = resource.update(
                    blogId=BLOG_ID, pageId=old["id"], body=body
                ).execute(num_retries=7)
                time.sleep(1.25)
            updated += 1
            print(f"UPDATED {source_path}: Blogger ID {result.get('id', old['id'])}")
        else:
            if kind == "post":
                result = resource.insert(
                    blogId=BLOG_ID, body=body, isDraft=False
                ).execute(num_retries=7)
                time.sleep(1.25)
            else:
                result = resource.insert(
                    blogId=BLOG_ID, body=body, isDraft=False
                ).execute()
            created += 1
            print(f"PUBLISHED {source_path}: Blogger ID {result.get('id')}")

    managed_prefix = "posts/" if kind == "post" else "pages/trttnews24bd/"
    for source_path, old in by_source.items():
        if source_path not in desired:
            if kind == "post":
                resource.delete(blogId=BLOG_ID, postId=old["id"]).execute(num_retries=7)
                time.sleep(1.25)
            else:
                resource.delete(blogId=BLOG_ID, pageId=old["id"]).execute(num_retries=7)
                time.sleep(1.25)
            deleted += 1
            print(f"DELETED Blogger-managed {kind}: {source_path} (source file removed)")

    return created, updated, deleted


def collect_sources() -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    if POSTS_DIR.exists():
        for path in sorted(POSTS_DIR.glob("*.md")):
            if path.name in SKIP_POSTS:
                print(f"SKIPPED documentation file: {path}")
                continue
            record = build_content(path)
            records[record["path"]] = record
    if PAGES_DIR.exists():
        for path in sorted(PAGES_DIR.glob("*.html")):
            record = build_content(path)
            records[record["path"]] = record
    return records


def main() -> int:
    require_secrets()
    records = collect_sources()
    print(f"GitHub source files discovered: {len(records)}")
    service = make_service()
    blog = service.blogs().get(blogId=BLOG_ID).execute(num_retries=7)
    print(f"Connected Blogger blog: {blog.get('name')} ({blog.get('url')})")

    post_counts = sync_resource(service.posts(), "post", records)
    page_counts = sync_resource(service.pages(), "page", records)
    print(
        "SYNC COMPLETE — "
        f"posts created/updated/deleted={post_counts}; "
        f"pages created/updated/deleted={page_counts}"
    )
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
