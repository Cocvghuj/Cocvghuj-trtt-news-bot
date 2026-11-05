#!/usr/bin/env python3
"""Publish the generated article to both configured Blogger blogs.

This entry point is intentionally separate from scripts/draft_news.py, which
remains a review-first draft workflow. Publishing requires explicit Blogger
configuration and verifies Blogger's LIVE status before reporting success.
"""
from __future__ import annotations

import os
import sys


def require_configuration() -> None:
    required = (
        "BLOGGER_BLOG_ID",
        "FLIGHTSCOUTPRO_BLOG_ID",
        "BLOGGER_CLIENT_ID",
        "BLOGGER_CLIENT_SECRET",
        "BLOGGER_REFRESH_TOKEN",
    )
    missing = [name for name in required if not os.environ.get(name, "").strip()]
    if missing:
        raise RuntimeError(
            "Automatic publishing requires both Blogger blog IDs and OAuth secrets. "
            "Missing: " + ", ".join(missing)
        )
    if os.environ["BLOGGER_BLOG_ID"].strip() == os.environ["FLIGHTSCOUTPRO_BLOG_ID"].strip():
        raise RuntimeError("BLOGGER_BLOG_ID and FLIGHTSCOUTPRO_BLOG_ID must identify different blogs.")
    if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("OPENROUTER_API_KEY")):
        raise RuntimeError("Configure GEMINI_API_KEY or OPENROUTER_API_KEY to generate the article.")


class _PostsProxy:
    def __init__(self, posts):
        self._posts = posts

    def list(self, **kwargs):
        return self._posts.list(**kwargs)

    def insert(self, **kwargs):
        # Blogger creates a LIVE post when isDraft is false.
        kwargs["isDraft"] = False
        response = self._posts.insert(**kwargs).execute()
        if str(response.get("status", "")).upper() != "LIVE":
            raise RuntimeError("Blogger did not confirm the new post is LIVE.")
        return _ImmediateResult(response)

    def publish(self, **kwargs):
        return self._posts.publish(**kwargs)


class _ImmediateResult:
    def __init__(self, value):
        self._value = value

    def execute(self):
        return self._value


class _BloggerServiceProxy:
    def __init__(self, service):
        self._service = service

    def posts(self):
        return _PostsProxy(self._service.posts())


def main() -> int:
    require_configuration()

    import main as engine

    original_build = engine.build
    original_find_duplicate = engine.find_duplicate_post

    def publishing_build(*args, **kwargs):
        return _BloggerServiceProxy(original_build(*args, **kwargs))

    def publish_or_confirm_live(service, blog_id, title, content, topic_key=None):
        existing = original_find_duplicate(
            service, blog_id, title, content, topic_key=topic_key
        )
        if not existing:
            return None

        status = str(existing.get("status", "")).upper()
        if status == "LIVE":
            return existing
        if status != "DRAFT":
            raise RuntimeError(
                "Matching Blogger post has no confirmed LIVE or DRAFT status; refusing success."
            )

        post_id = existing.get("id")
        if not post_id:
            raise RuntimeError("Matching Blogger draft has no post ID; refusing success.")
        published = service.posts().publish(
            blogId=blog_id, postId=str(post_id)
        ).execute()
        if str(published.get("status", "")).upper() != "LIVE":
            raise RuntimeError("Blogger did not confirm the existing draft is LIVE.")
        return published

    def report_published(title, outcomes, excerpt):
        print("Blogger publication confirmed for: " + title)
        for outcome in outcomes:
            print(
                "- " + str(outcome.get("blog_name", "Blogger blog")) + ": "
                + str(outcome.get("edit_url", "no editor URL returned"))
            )

    engine.build = publishing_build
    engine.find_duplicate_post = publish_or_confirm_live
    engine.send_draft_notification = report_published
    try:
        engine.main()
    finally:
        engine.build = original_build
        engine.find_duplicate_post = original_find_duplicate
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("Scheduled Blogger publication failed: " + str(exc), file=sys.stderr)
        raise
