#!/usr/bin/env python3
"""Create one Blogger draft on each configured blog. Never publish."""
import os
import re
import sys
from pathlib import Path

import markdown
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TARGETS = {
    "TRTT": {
        "path": Path("drafts/trtt/essential-travel-planning-tips-en.md"),
        "blog_id_env": "BLOGGER_BLOG_ID",
        "labels": ["TRTT Voyage", "Travel Tips", "Travel Planning"],
    },
    "FlightScoutPro": {
        "path": Path("drafts/flightscoutpro/choosing-the-right-flight-en.md"),
        "blog_id_env": "FLIGHTSCOUTPRO_BLOG_ID",
        "labels": ["FlightScoutPro", "Flights", "Travel Tips"],
    },
}


def main():
    client_id = os.environ.get("BLOGGER_CLIENT_ID")
    client_secret = os.environ.get("BLOGGER_CLIENT_SECRET")
    refresh_token = os.environ.get("BLOGGER_REFRESH_TOKEN")
    if not all([client_id, client_secret, refresh_token]):
        sys.exit("ERROR: Missing BLOGGER_CLIENT_ID, BLOGGER_CLIENT_SECRET or BLOGGER_REFRESH_TOKEN GitHub secret.")

    failures = []
    for target, config in TARGETS.items():
        blog_id = os.environ.get(config["blog_id_env"])
        if not blog_id:
            print(f"ERROR: {target}: missing {config['blog_id_env']} secret.")
            failures.append(target)
            continue

        md_file = config["path"]
        if not md_file.is_file():
            print(f"ERROR: {target}: article file not found: {md_file}")
            failures.append(target)
            continue

        source = md_file.read_text(encoding="utf-8")
        match = re.search(r"^#\s+(.+?)\s*$", source, flags=re.MULTILINE)
        if not match:
            print(f"ERROR: {target}: article has no H1 title.")
            failures.append(target)
            continue

        title = match.group(1).strip()
        html = markdown.markdown(source, extensions=["extra", "sane_lists"])
        credentials = Credentials(
            None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret,
        )
        try:
            blogger = build("blogger", "v3", credentials=credentials, cache_discovery=False)
            body = {
                "kind": "blogger#post",
                "title": title,
                "content": html,
                "labels": config["labels"],
            }
            print(f"Creating DRAFT only: {target} — {title}")
            post = blogger.posts().insert(blogId=blog_id, body=body, isDraft=True).execute()
            post_id = post.get("id")
            if not post_id:
                raise RuntimeError(f"Blogger returned no post ID: {post}")
            print(f"CONFIRMED DRAFT: {target}; post ID: {post_id}; status: {post.get('status', 'not supplied')}")
        except Exception as exc:
            print(f"ERROR: {target}: {type(exc).__name__}: {exc}")
            failures.append(target)

    if failures:
        sys.exit("Draft creation incomplete for: " + ", ".join(failures))
    print("SUCCESS: Blogger API confirmed draft creation on both blogs. No post was published.")


if __name__ == "__main__":
    main()
