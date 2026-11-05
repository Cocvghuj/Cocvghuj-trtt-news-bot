#!/usr/bin/env python3
"""TRTT Blogger publishing engine. The payout marker is kept in API configuration only."""
from __future__ import annotations
import json, os, time
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

MARKER = os.getenv("TRAVEL_PAYOUT_MARKER", "787950")
QUEUE_FILE = "news/queue/latest.json"
HISTORY_FILE = "drafted_history.txt"
BATCH_SIZE = 20
SLEEP_BETWEEN = 60
REAL_ROUTES = [
    "Dhaka to Rome", "Dhaka to Milan", "Chittagong to Rome",
    "Rome to Dhaka", "Milan to Dhaka", "Sanluri to Dhaka",
    "Cagliari to Rome", "Rome to Cagliari", "Milan to Cagliari",
    "Rome to Paris", "Paris to Rome", "Rome to London",
]

def publish_date() -> datetime:
    """Use the publisher's local market date, independent of the Actions runner timezone."""
    return datetime.now(ZoneInfo("Europe/Rome"))

def history_key(city: str, date_label: str) -> str:
    return f"{city} | {date_label}"

def load_history() -> set[str]:
    path = Path(HISTORY_FILE)
    if not path.exists():
        return set()
    return {line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()}

def build_content(city: str, date_label: str | None = None) -> str:
    date_label = date_label or publish_date().strftime("%-d %b %Y")
    return (
        f"<h2>Live Travel Guide: {city}</h2>"
        f"<div id='roksana-vault-flight' data-city='{city}'></div>"
        f"<div id='ghost-esim' data-city='{city}'></div>"
        f"<p>Daily route update: {date_label} - 4 times daily - Live from TRTT</p>"
    )

def ghost_sim_esim_logic(city: str) -> dict[str, str]:
    """Keep Ghost-SIM/eSIM API configuration separate from visible article HTML."""
    return {"service": "Ghost-SIM", "product": "eSIM", "destination": city, "marker": MARKER}

def require_configuration() -> None:
    required = ("BLOGGER_BLOG_ID", "FLIGHTSCOUTPRO_BLOG_ID", "BLOGGER_CLIENT_ID",
                "BLOGGER_CLIENT_SECRET", "BLOGGER_REFRESH_TOKEN")
    missing = [key for key in required if not os.environ.get(key, "").strip()]
    if missing:
        raise RuntimeError("Missing required Blogger configuration: " + ", ".join(missing))
    if os.environ["BLOGGER_BLOG_ID"].strip() == os.environ["FLIGHTSCOUTPRO_BLOG_ID"].strip():
        raise RuntimeError("BLOGGER_BLOG_ID and FLIGHTSCOUTPRO_BLOG_ID must be different.")
    if not (os.environ.get("GEMINI_API_KEY", "").strip() or os.environ.get("OPENROUTER_API_KEY", "").strip()):
        raise RuntimeError("Configure GEMINI_API_KEY or OPENROUTER_API_KEY.")
    os.environ.setdefault("TRAVEL_PAYOUT_MARKER", "787950")

def build():
    """Create an authenticated Blogger v3 service using the configured OAuth refresh token."""
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build as google_build
    credentials = Credentials(
        token=None,
        refresh_token=os.environ["BLOGGER_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["BLOGGER_CLIENT_ID"],
        client_secret=os.environ["BLOGGER_CLIENT_SECRET"],
        scopes=["https://www.googleapis.com/auth/blogger"],
    )
    return google_build("blogger", "v3", credentials=credentials, cache_discovery=False)

def find_duplicate_post(service: Any, blog_id: str, title: str, content: str,
                        topic_key: str | None = None) -> dict[str, Any] | None:
    """Find an existing post by title or exact content, following Blogger pagination."""
    page_token = None
    while True:
        params: dict[str, Any] = {"blogId": blog_id, "fetchBodies": True, "maxResults": 100,
                                  "status": ["LIVE", "DRAFT"]}
        if page_token:
            params["pageToken"] = page_token
        response = service.posts().list(**params).execute()
        for post in response.get("items", []):
            if str(post.get("title", "")).strip().casefold() == title.strip().casefold():
                return post
            if content.strip() and str(post.get("content", "")).strip() == content.strip():
                return post
        page_token = response.get("nextPageToken")
        if not page_token:
            return None

def send_draft_notification(title: str, outcomes: list[dict[str, Any]], excerpt: str) -> None:
    print("Blogger publication confirmed for: " + title)
    for outcome in outcomes:
        print("- " + str(outcome.get("blog_name", "Blogger blog")) + ": "
              + str(outcome.get("edit_url", "no editor URL returned")))

def _load_queue() -> list[str]:
    path = Path(QUEUE_FILE)
    if not path.exists():
        return list(REAL_ROUTES)
    payload = json.loads(path.read_text(encoding="utf-8"))
    items = payload if isinstance(payload, list) else payload.get("routes", payload.get("queue", [])) if isinstance(payload, dict) else None
    if items is None:
        raise ValueError(f"{QUEUE_FILE} must contain a JSON list or an object with routes/queue.")
    routes = [str(item.get("city") or item.get("route") or item) if isinstance(item, dict) else str(item)
              for item in items]
    return [route.strip() for route in routes if route and route.strip()]

def _ensure_live(service: Any, blog_id: str, title: str, content: str, city: str) -> dict[str, Any]:
    existing = find_duplicate_post(service, blog_id, title, content, topic_key=city)
    if existing:
        status = str(existing.get("status", "")).upper()
        if status == "LIVE":
            return existing
        if status == "DRAFT" and existing.get("id"):
            published = service.posts().publish(blogId=blog_id, postId=str(existing["id"])).execute()
            if str(published.get("status", "")).upper() == "LIVE":
                return published
        raise RuntimeError(f"Existing Blogger post for {title!r} was not confirmed LIVE.")
    result = service.posts().insert(
        blogId=blog_id,
        body={"kind": "blogger#post", "title": title, "content": content,
              "labels": ["TRTT", "Travel Guide"]},
        isDraft=False,
    ).execute()
    if str(result.get("status", "")).upper() != "LIVE":
        raise RuntimeError(f"Blogger did not confirm LIVE status for {title!r}.")
    return result

def run_batch() -> int:
    # Prefer today's explicit queue; use REAL_ROUTES only when no queue file exists.
    queue = _load_queue()
    history = load_history()
    today = publish_date()
    date_label = today.strftime("%-d %b %Y")
    title_date = today.strftime("%-d %b")
    dated_history = history
    blog_ids = [os.environ["BLOGGER_BLOG_ID"].strip(), os.environ["FLIGHTSCOUTPRO_BLOG_ID"].strip()]
    service = build()
    completed = 0
    for city in queue:
        city = city.strip()
        if not city or history_key(city, date_label) in dated_history:
            continue
        if completed >= BATCH_SIZE:
            break
        ghost_sim_esim_logic(city)
        title = f"{city} Cheap Flights Today: {title_date} Update - TRTT"
        content = build_content(city, date_label)
        outcomes = []
        for blog_id, blog_name in ((blog_ids[0], "TRTT News 24 BD"),
                                   (blog_ids[1], "FlightScoutPro")):
            post = _ensure_live(service, blog_id, title, content, city)
            outcomes.append({"blog_name": blog_name, "id": post.get("id"),
                             "status": post.get("status"),
                             "edit_url": post.get("url") or post.get("editUrl") or "no editor URL returned"})
        if len(outcomes) != 2 or any(str(item.get("status", "")).upper() != "LIVE" for item in outcomes):
            raise RuntimeError(f"Both Blogger sites were not confirmed LIVE for {title!r}.")
        send_draft_notification(title, outcomes, content[:240])
        with Path(HISTORY_FILE).open("a", encoding="utf-8") as history_file:
            history_file.write(history_key(city, date_label) + "\n")
        history.add(history_key(city, date_label))
        completed += 1
        print(f"[{completed}] Published and verified on both Blogger sites: {city}")
        if completed < BATCH_SIZE:
            time.sleep(SLEEP_BETWEEN)
    print(f"TRTT Blogger batch complete: {completed} route(s) published/verified.")
    return completed

def main() -> int:
    require_configuration()
    run_batch()
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
