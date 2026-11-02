#!/usr/bin/env python3
"""Safe Blogger admin audit and explicit comment moderation actions."""
from __future__ import annotations

import os
import sys
from collections import Counter

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

BLOG_ID = os.environ.get("BLOGGER_BLOG_ID", "").strip()


def service():
    required = ("BLOGGER_BLOG_ID", "BLOGGER_CLIENT_ID",
                "BLOGGER_CLIENT_SECRET", "BLOGGER_REFRESH_TOKEN")
    missing = [key for key in required if not os.environ.get(key, "").strip()]
    if missing:
        raise RuntimeError("Missing required GitHub Actions secret(s): " + ", ".join(missing))
    creds = Credentials(
        token=None,
        refresh_token=os.environ["BLOGGER_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["BLOGGER_CLIENT_ID"],
        client_secret=os.environ["BLOGGER_CLIENT_SECRET"],
        scopes=["https://www.googleapis.com/auth/blogger"],
    )
    return build("blogger", "v3", credentials=creds, cache_discovery=False)


def collect_all(request_factory):
    results = []
    token = None
    while True:
        kwargs = {"maxResults": 500}
        if token:
            kwargs["pageToken"] = token
        response = request_factory(**kwargs).execute(num_retries=7)
        results.extend(response.get("items", []))
        token = response.get("nextPageToken")
        if not token:
            return results


def audit(api):
    blog = api.blogs().get(blogId=BLOG_ID).execute(num_retries=7)
    posts = collect_all(lambda **kw: api.posts().list(blogId=BLOG_ID, fetchBodies=False, **kw))
    pages = collect_all(lambda **kw: api.pages().list(blogId=BLOG_ID, **kw))
    comments = collect_all(
        lambda **kw: api.comments().listByBlog(
            blogId=BLOG_ID, fetchBodies=False, **kw
        )
    )
    statuses = Counter((item.get("status") or "unknown").lower() for item in comments)
    views_30d = api.pageViews().get(blogId=BLOG_ID, range="30DAYS").execute(num_retries=7)
    views_all = api.pageViews().get(blogId=BLOG_ID, range="all").execute(num_retries=7)
    print("BLOGGER ADMIN AUDIT — READ ONLY")
    print(f"Blog: {blog.get('name')}")
    print(f"URL: {blog.get('url')}")
    print(f"Blog ID configured: yes")
    print(f"Posts visible to API: {len(posts)}")
    print(f"Pages visible to API: {len(pages)}")
    print(f"Comments visible to API: {len(comments)}")
    print(f"Page views (30 days): {sum(int(x.get('count', 0)) for x in views_30d.get('counts', []))}")
    print(f"Page views (all time): {sum(int(x.get('count', 0)) for x in views_all.get('counts', []))}")
    for status, count in sorted(statuses.items()):
        print(f"Comments [{status}]: {count}")
    print("No Blogger data was changed.")


def list_comments(api):
    comments = collect_all(
        lambda **kw: api.comments().listByBlog(
            blogId=BLOG_ID, fetchBodies=False, **kw
        )
    )
    comments.sort(key=lambda x: x.get("published", ""), reverse=True)
    print(f"COMMENTS: {len(comments)} total; content and author details are not logged.")
    for item in comments[:50]:
        post = item.get("post") or {}
        print(
            f"comment_id={item.get('id')} post_id={post.get('id')} "
            f"status={item.get('status', 'unknown')} published={item.get('published', '')}"
        )


def moderate(api, operation: str) -> None:
    post_id = os.environ.get("BLOGGER_POST_ID", "").strip()
    comment_id = os.environ.get("BLOGGER_COMMENT_ID", "").strip()
    if not post_id or not comment_id:
        raise ValueError("BLOGGER_POST_ID and BLOGGER_COMMENT_ID are required.")
    comments = api.comments()
    if operation == "approve":
        result = comments.approve(
            blogId=BLOG_ID, postId=post_id, commentId=comment_id
        ).execute(num_retries=7)
        print(f"Comment {comment_id} restored from spam. Status: {result.get('status', 'unknown')}")
    elif operation == "mark_spam":
        result = comments.markAsSpam(
            blogId=BLOG_ID, postId=post_id, commentId=comment_id
        ).execute(num_retries=7)
        print(f"Comment {comment_id} marked as spam. Status: {result.get('status', 'unknown')}")
    elif operation == "delete":
        confirmation = os.environ.get("BLOGGER_CONFIRM_DELETE", "").strip()
        if confirmation != f"DELETE:{comment_id}":
            raise ValueError("Deletion blocked. Confirmation must exactly equal DELETE:<comment_id>.")
        comments.delete(
            blogId=BLOG_ID, postId=post_id, commentId=comment_id
        ).execute(num_retries=7)
        print(f"Comment {comment_id} permanently deleted.")
    else:
        raise ValueError(f"Unsupported operation: {operation}")


def main() -> int:
    operation = os.environ.get("BLOGGER_OPERATION", "audit").strip().lower()
    api = service()
    if operation == "audit":
        audit(api)
    elif operation == "list_comments":
        list_comments(api)
    elif operation in {"approve", "mark_spam", "delete"}:
        moderate(api, operation)
    else:
        raise ValueError("Operation must be audit, list_comments, approve, mark_spam, or delete.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except HttpError as exc:
        status = getattr(exc.resp, "status", "unknown")
        print(f"BLOGGER API ERROR: HTTP {status}: {str(exc)[:1200]}", file=sys.stderr)
        raise SystemExit(1)
    except Exception as exc:
        print(f"BLOGGER ADMIN FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(1)
