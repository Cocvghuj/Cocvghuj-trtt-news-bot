#!/usr/bin/env python3
"""Generate and publish verified travel articles to both configured Blogger blogs.

This entry point is intentionally separate from scripts/draft_news.py: scheduled
runs publish immediately, while review-first workflows can continue creating drafts.
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
        # Blogger publishes immediately unless isDraft is true.
        kwargs["isDraft"] = False
        return self._posts.insert(**kwargs)

    def publish(self, **kwargs):
        return self._posts.publish(**kwargs)


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

    def publish_matching_draft(service, blog_id, title, content, topic_key=None):
        existing = original_find_duplicate(
            service, blog_id, title, content, topic_key=topic_key
        )
        if existing and str(existing.get("status", "")).upper() == "DRAFT":
            post_id = existing.get("id")
            if not post_id:
                raise RuntimeError(
                    "A matching Blogger draft has no post ID; refusing to report publication success."
                )
            published = service.posts().publish(
                blogId=blog_id, postId=str(post_id)
            ).execute()
            if str(published.get("status", "")).upper() != "LIVE":
                raise RuntimeError(
                    "Blogger did not confirm the existing matching draft is LIVE."
                )
            existing.update(published)
        return existing

    def report_published(title, outcomes, excerpt):
        print("Blogger publication results for: " + title)
        for outcome in outcomes:
            print(
                "- " + str(outcome.get("blog_name", "Blogger blog")) + ": "
                + str(outcome.get("edit_url", "no editor URL returned"))
            )

    engine.build = publishing_build
    engine.find_duplicate_post = publish_matching_draft
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
