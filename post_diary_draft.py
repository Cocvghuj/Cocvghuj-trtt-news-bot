#!/usr/bin/env python3
"""Create a reviewed Markdown diary as a Blogger draft (never publish)."""
import os
import re
import sys
from pathlib import Path

import markdown
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

DIARIES = {
    "trtt": {
        "path": Path("diary/2026-11-10-thinking-room-menu-diary-en.md"),
        "blog_id_env": "BLOGGER_BLOG_ID",
        "labels": ["TRTT Voyage", "Diary", "Thinking Room", "MAC-787950"],
    },
    "flightscoutpro": {
        "path": Path("drafts/flightscoutpro/2026-11-10-thinking-room-traveller-diary-en.md"),
        "blog_id_env": "FLIGHTSCOUTPRO_BLOG_ID",
        "labels": ["FlightScoutPro", "Travel Diary", "Thinking Room", "MAC-787950"],
    },
}


def main():
    target = os.environ.get("TARGET_BLOG", "").strip().lower()
    if target not in DIARIES:
        sys.exit("ERROR: TARGET_BLOG must be 'trtt' or 'flightscoutpro'.")

    config = DIARIES[target]
    blog_id = os.environ.get(config["blog_id_env"])
    client_id = os.environ.get("BLOGGER_CLIENT_ID")
    client_secret = os.environ.get("BLOGGER_CLIENT_SECRET")
    refresh_token = os.environ.get("BLOGGER_REFRESH_TOKEN")
    if not all([blog_id, client_id, client_secret, refresh_token]):
        sys.exit(
            "ERROR: Missing Blogger credentials. Required: "
            f"{config['blog_id_env']}, BLOGGER_CLIENT_ID, "
            "BLOGGER_CLIENT_SECRET, BLOGGER_REFRESH_TOKEN."
        )

    md_file = config["path"]
    if not md_file.is_file():
        sys.exit(f"ERROR: Diary file not found: {md_file}")

    source = md_file.read_text(encoding="utf-8")
    match = re.search(r"^#\\s+(.+?)\\s*$", source, flags=re.MULTILINE)
    if not match:
        sys.exit(f"ERROR: No Markdown H1 title found in {md_file}.")
    title = match.group(1).strip()
    html = markdown.markdown(source, extensions=["extra", "sane_lists"])

    credentials = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
    )
    blogger = build("blogger", "v3", credentials=credentials, cache_discovery=False)

    body = {
        "kind": "blogger#post",
        "title": title,
        "content": html,
        "labels": config["labels"],
    }

    print(f"Creating Blogger DRAFT for {target}: {title}")
    post = blogger.posts().insert(blogId=blog_id, body=body, isDraft=True).execute()
    post_id = post.get("id")
    status = post.get("status")
    if not post_id:
        sys.exit(f"ERROR: Blogger returned no post ID: {post}")
    print("CONFIRMED: Blogger API returned a post ID.")
    print(f"Post ID: {post_id}")
    print(f"Status: {status or 'not supplied by API'}")
    print(f"Target: {target}")
    print(f"Title: {title}")
    if status and status.upper() not in ("DRAFT", "SCHEDULED"):
        sys.exit(f"ERROR: Unexpected Blogger status: {status}")


if __name__ == "__main__":
    main()
