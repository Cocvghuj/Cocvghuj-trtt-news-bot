#!/usr/bin/env python3
"""Create two Blogger drafts and verify both remain DRAFT. Never publish."""
import os
import re
import sys
from pathlib import Path

import markdown
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parents[1]
ARTICLES = [
    ("drafts/trtt/leadership-framework-en.md", ["TRTT UNIVERSE", "Leadership", "AI Collaboration"]),
    ("drafts/trtt/leadership-framework-bn.md", ["TRTT UNIVERSE", "Leadership", "AI Collaboration"]),
]

def main():
    names = ("BLOGGER_BLOG_ID", "BLOGGER_CLIENT_ID", "BLOGGER_CLIENT_SECRET", "BLOGGER_REFRESH_TOKEN")
    missing = [name for name in names if not os.environ.get(name, "").strip()]
    if missing:
        sys.exit("Missing GitHub Actions secret(s): " + ", ".join(missing))

    credentials = Credentials(
        None,
        refresh_token=os.environ["BLOGGER_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["BLOGGER_CLIENT_ID"],
        client_secret=os.environ["BLOGGER_CLIENT_SECRET"],
        scopes=["https://www.googleapis.com/auth/blogger"],
    )
    api = build("blogger", "v3", credentials=credentials, cache_discovery=False)
    blog_id = os.environ["BLOGGER_BLOG_ID"].strip()

    for relative_path, labels in ARTICLES:
        source_path = ROOT / relative_path
        source = source_path.read_text(encoding="utf-8")
        match = re.search(r"^#\s+(.+?)\s*$", source, flags=re.MULTILINE)
        if not match:
            raise RuntimeError(f"No H1 title found in {relative_path}")
        title = match.group(1).strip()
        existing = api.posts().list(blogId=blog_id, fetchBodies=False, status=["LIVE", "DRAFT"], maxResults=100).execute()
        same = [p for p in existing.get("items", []) if p.get("title", "").strip().casefold() == title.casefold()]
        if same:
            post_id = same[0].get("id")
            saved = api.posts().get(blogId=blog_id, postId=post_id, view="AUTHOR").execute()
            if saved.get("status") == "DRAFT":
                print(f"ALREADY VERIFIED DRAFT: {title} | post ID {post_id}")
                continue
            raise RuntimeError(f"Matching post exists but is not a DRAFT; refusing to alter it: {title}")

        html = markdown.markdown(source, extensions=["extra", "sane_lists"])
        response = api.posts().insert(
            blogId=blog_id,
            body={"kind": "blogger#post", "title": title, "content": html, "labels": labels},
            isDraft=True,
        ).execute()
        post_id = response.get("id")
        if not post_id:
            raise RuntimeError(f"Blogger returned no post ID for {title}")
        saved = api.posts().get(blogId=blog_id, postId=post_id, view="AUTHOR").execute()
        if saved.get("status") != "DRAFT":
            raise RuntimeError(f"Blogger did not confirm DRAFT status for {title}: {saved.get('status')}")
        print(f"CONFIRMED DRAFT: {title} | post ID {post_id} | status DRAFT")

    print("SUCCESS: English and Bengali Blogger drafts are verified. No post was published.")

if __name__ == "__main__":
    main()
