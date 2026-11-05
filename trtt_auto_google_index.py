"""Notify discovery services only for HTTPS URLs explicitly supplied after human review.

This notification is not a Google indexing guarantee. Draft/dashboard URLs are rejected.
"""
from __future__ import annotations
import os
from urllib.parse import urlparse
import requests

def reviewed_urls() -> list[str]:
    urls = [item.strip() for item in os.environ.get("REVIEWED_POST_URLS", "").splitlines() if item.strip()]
    for url in urls:
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError(f"Expected an absolute HTTPS URL: {url!r}")
        if "blogger.com/blog/posts" in url or "/draft" in parsed.path.casefold():
            raise ValueError("Blogger dashboard and draft URLs cannot be submitted.")
    return urls

def main() -> int:
    urls = reviewed_urls()
    if not urls:
        raise RuntimeError("No reviewed published URLs supplied; refusing indexing notification.")
    for url in urls:
        response = requests.post("https://pubsubhubbub.appspot.com/publish",
                                 data={"hub.url": url, "hub.mode": "publish"}, timeout=15)
        response.raise_for_status()
        print(f"Discovery notification sent for reviewed URL: {url} (HTTP {response.status_code})")
    print("Notifications sent; Google indexing is not guaranteed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
