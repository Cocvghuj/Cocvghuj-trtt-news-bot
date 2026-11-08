#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def main():
    blog_id = os.environ.get("BLOGGER_BLOG_ID")
    client_id = os.environ.get("BLOGGER_CLIENT_ID")
    client_secret = os.environ.get("BLOGGER_CLIENT_SECRET")
    refresh_token = os.environ.get("BLOGGER_REFRESH_TOKEN")

    if not all([blog_id, client_id, client_secret, refresh_token]):
        print("ERROR: Missing Blogger secrets in environment.")
        sys.exit(1)

    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
    )

    service = build("blogger", "v3", credentials=creds)

    html_file = Path("content/diary/what-i-learned-in-3-days-blogger-theme-restore.html")
    if not html_file.exists():
        print(f"ERROR: {html_file} does not exist.")
        sys.exit(1)

    content = html_file.read_text(encoding="utf-8")
    title = 'What I Learned in 3 Days: Blogger Theme Restore Is Harder Than “PASS” — TRTT Voyage Diary'

    body = {
        "kind": "blogger#post",
        "title": title,
        "content": content,
        "labels": ["TRTT Voyage", "Diary", "Blogger Theme", "MAC-787950"],
    }

    print("Submitting draft to Blogger...")
    post = service.posts().insert(
        blogId=blog_id,
        body=body,
        isDraft=True
    ).execute()

    post_id = post.get("id")
    status = post.get("status")
    print(f"CONFIRMED: Blogger DRAFT successfully created!")
    print(f"Post ID: {post_id}")
    print(f"Status: {status}")
    print(f"Title: {title}")

if __name__ == "__main__":
    main()
