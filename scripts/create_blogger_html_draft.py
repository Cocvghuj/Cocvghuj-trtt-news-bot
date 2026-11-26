#!/usr/bin/env python3
"""Create a verified TRTT Blogger DRAFT from one merged HTML article.

This script never publishes a post and never sends Telegram messages.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


SITE_URL = "https://trttvoyage.com"
ALLOWED_TAGS = {
    "article", "header", "footer", "main", "section", "div", "span", "p",
    "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "li", "strong",
    "em", "b", "i", "blockquote", "a", "img", "figure", "figcaption",
    "br", "hr", "table", "thead", "tbody", "tr", "th", "td", "caption",
    "sup", "sub", "small", "code", "pre", "dl", "dt", "dd",
}
ALLOWED_ATTRIBUTES = {
    "class", "id", "href", "src", "alt", "title", "rel", "target",
    "width", "height", "loading", "aria-label", "role",
}


class ArticleInspector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.h1_parts: list[str] = []
        self.in_h1 = False
        self.h1_count = 0
        self.h2_count = 0
        self.has_image = False
        self.errors: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag not in ALLOWED_TAGS:
            self.errors.append(f"Disallowed HTML tag: {tag}")
            return
        if tag == "h1":
            self.h1_count += 1
            self.in_h1 = True
        if tag == "h2":
            self.h2_count += 1
        attr_map = {str(k).lower(): (v or "") for k, v in attrs}
        for name, value in attr_map.items():
            if name.startswith("on") or name not in ALLOWED_ATTRIBUTES:
                self.errors.append(f"Disallowed HTML attribute: {name}")
            if name in {"href", "src"}:
                parsed = urlparse(value.strip())
                if parsed.scheme != "https" or not parsed.netloc:
                    self.errors.append(f"Only absolute HTTPS {name} URLs are allowed.")
        if tag == "img":
            self.has_image = True
            if not attr_map.get("alt", "").strip():
                self.errors.append("Every article image must have descriptive alt text.")
            if not attr_map.get("src", "").strip():
                self.errors.append("Every article image must have an HTTPS source URL.")

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "h1":
            self.in_h1 = False

    def handle_data(self, data: str) -> None:
        if self.in_h1:
            self.h1_parts.append(data)


def validate_article(path: str) -> tuple[str, str]:
    candidate = Path(path)
    if candidate.suffix.lower() != ".html" or candidate.parent.as_posix() != "blog/drafts":
        raise RuntimeError("Only HTML files directly inside blog/drafts/ can be sent to Blogger.")
    if not candidate.is_file():
        raise RuntimeError(f"Draft file does not exist: {candidate}")
    content = candidate.read_text(encoding="utf-8")
    if len(content) < 1500:
        raise RuntimeError("Article HTML is too short; refusing an empty or thin draft.")
    if "787950" not in content:
        raise RuntimeError("Required TRTT marker 787950 is missing.")
    if SITE_URL not in content:
        raise RuntimeError("Required TRTT Voyage website link is missing.")
    lowered = content.lower()
    if not re.search(r"affiliate disclosure|affiliate links", lowered):
        raise RuntimeError("A transparent affiliate disclosure is required.")
    if not re.search(r"\bfaq\b|frequently asked questions", lowered):
        raise RuntimeError("An FAQ section is required.")
    inspector = ArticleInspector()
    inspector.feed(content)
    inspector.close()
    if inspector.errors:
        raise RuntimeError("; ".join(inspector.errors[:8]))
    title = " ".join("".join(inspector.h1_parts).split())
    if inspector.h1_count != 1 or not title or len(title) > 300:
        raise RuntimeError("Article must contain exactly one non-empty H1 title (maximum 300 characters).")
    if inspector.h2_count < 6:
        raise RuntimeError("Article must contain five main sections plus an FAQ heading.")
    return title, content


def blogger_service():
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    names = ("BLOGGER_BLOG_ID", "BLOGGER_CLIENT_ID", "BLOGGER_CLIENT_SECRET", "BLOGGER_REFRESH_TOKEN")
    missing = [name for name in names if not os.environ.get(name, "").strip()]
    if missing:
        raise RuntimeError("Missing required GitHub Actions Secret(s): " + ", ".join(missing))
    credentials = Credentials(
        token=None,
        refresh_token=os.environ["BLOGGER_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["BLOGGER_CLIENT_ID"],
        client_secret=os.environ["BLOGGER_CLIENT_SECRET"],
        scopes=["https://www.googleapis.com/auth/blogger"],
    )
    return build("blogger", "v3", credentials=credentials, cache_discovery=False)


def find_same_title(service, blog_id: str, title: str):
    token = None
    for _ in range(20):
        args = {"blogId": blog_id, "maxResults": 100, "status": ["LIVE", "DRAFT"], "view": "ADMIN"}
        if token:
            args["pageToken"] = token
        page = service.posts().list(**args).execute(num_retries=5)
        for post in page.get("items", []):
            if post.get("title") == title:
                return post
        token = page.get("nextPageToken")
        if not token:
            return None
    raise RuntimeError("Duplicate scan exceeded 20 pages; refusing to create a post.")


def create_or_verify_draft(path: str) -> str:
    title, content = validate_article(path)
    blog_id = os.environ["BLOGGER_BLOG_ID"].strip()
    service = blogger_service()
    blog = service.blogs().get(blogId=blog_id).execute(num_retries=5)
    blog_host = urlparse(str(blog.get("url", ""))).hostname
    allowed_hosts = {"trttvoyage.blogspot.com", "trttvoyage.com", "www.trttvoyage.com"}
    if blog_host not in allowed_hosts:
        raise RuntimeError("Configured Blogger blog is not an approved TRTT Voyage destination; no write performed.")
    existing = find_same_title(service, blog_id, title)
    if existing:
        status = str(existing.get("status", "")).upper()
        if status != "DRAFT":
            raise RuntimeError("A matching title already exists but is not a Blogger DRAFT; no changes made.")
        if existing.get("content") != content:
            raise RuntimeError("A matching Blogger DRAFT has different content; refusing to overwrite it.")
        post_id = str(existing.get("id", "")).strip()
        if not post_id:
            raise RuntimeError("Existing draft has no Blogger post ID.")
    else:
        created = service.posts().insert(
            blogId=blog_id,
            isDraft=True,
            body={"kind": "blogger#post", "title": title, "content": content},
        ).execute(num_retries=5)
        post_id = str(created.get("id", "")).strip()
        if not post_id:
            raise RuntimeError("Blogger returned no post ID.")
    verified = service.posts().get(blogId=blog_id, postId=post_id, view="ADMIN").execute(num_retries=5)
    if str(verified.get("id", "")) != post_id:
        raise RuntimeError("Blogger read-back post ID mismatch.")
    if str(verified.get("status", "")).upper() != "DRAFT":
        raise RuntimeError("Blogger read-back status is not DRAFT.")
    if verified.get("title") != title or verified.get("content") != content:
        raise RuntimeError("Blogger read-back title/content mismatch.")
    return post_id


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate-only", action="store_true", help="Validate HTML without calling Blogger.")
    parser.add_argument("path", help="HTML article directly under blog/drafts/")
    args = parser.parse_args()
    if args.validate_only:
        title, _ = validate_article(args.path)
        print(f"PASS: Blogger HTML validated; title={title}; blogger_write=NO")
        return 0
    post_id = create_or_verify_draft(args.path)
    print(f"PASS: Blogger DRAFT verified; post_id={post_id}; source={args.path}; publish=NO; telegram=NO")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FAIL: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(1)
