#!/usr/bin/env python3
"""TRTT one-route-per-day Blogger draft engine. Never publishes posts live."""
from __future__ import annotations
import html
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

MARKER = "787950"
QUEUE_FILE = "news/queue/latest.json"
HISTORY_FILE = "drafted_history.txt"
BATCH_SIZE = 1
LINKS = {
    "aviasales": "https://aviasales.tpo.lv/Fb8U9yav?marker=787950",
    "klook": "https://klook.tpo.lv/TWKnemhz?marker=787950",
    "airalo": "https://airalo.tpo.lv/ZZoQC7Mz?marker=787950",
    "gettransfer": "https://gettransfer.tpo.lv/1u8zRU5s?marker=787950",
    "amazon": "https://amzn.to/4shg6Hn",
}
LIVE_APP = "https://cocvghuj-trtt-news-bot.vercel.app"


def publish_date() -> datetime:
    return datetime.now(ZoneInfo("Europe/Rome"))


def history_key(city: str, date_label: str) -> str:
    return f"{city} | {date_label}"


def load_history() -> set[str]:
    path = Path(HISTORY_FILE)
    return {line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()} if path.exists() else set()


def route_context(city: str) -> tuple[str, str]:
    route = city.casefold()
    if "rome" in route and "cagliari" in route:
        return ("Sanluri to Cagliari-Elmas Airport (CAG)",
                "SS131 is the principal road connection from the Sanluri area towards Cagliari. Allow a practical buffer for road traffic, parking, check-in and security. Confirm the airport and terminal on the ticket.")
    if "milan" in route and "cagliari" in route:
        return ("Milan to Cagliari",
                "Compare the complete journey to each Milan airport before choosing a fare. Include airport transfers, baggage, seat selection and departure time in the total cost.")
    if "cagliari" in route and "rome" in route:
        return ("Cagliari-Elmas (CAG) to Rome",
                "Check whether the booking arrives at Fiumicino (FCO) or Ciampino (CIA), then compare the onward transfer cost and time. Confirm the airport shown by the airline before payment.")
    return ("Sanluri, Sardinia", "Confirm the airport codes, terminal, ground transport and airline check-in deadline. Compare the complete trip cost rather than the headline fare.")


def daily_focus(day: int) -> tuple[str, str]:
    focuses = [
        ("Compare the real fare", "Add baggage, seat selection, payment charges and airport transfers before comparing totals. A lower headline fare is not necessarily the lower-cost journey."),
        ("Plan the airport transfer", "Check the first and last practical ground-transport options, parking arrangements and the time needed to reach the terminal. Keep a buffer for traffic and queues."),
        ("Check baggage rules", "Read the operating airline's current cabin-bag dimensions and weight limits. If the trip uses more than one carrier, check each carrier's rules rather than assuming they match."),
        ("Keep passenger-rights records", "Save the booking confirmation, boarding pass, airline messages and receipts. These records help establish what happened if a delay or cancellation affects the journey."),
        ("Protect connection time", "For separate tickets, allow extra time to collect baggage, clear any required checks and re-check in. A self-transfer is not the same protection as a single through-ticket."),
    ]
    return focuses[day % len(focuses)]


def _tool_links(city: str) -> str:
    labels = [("Find cheapest flights", LINKS["aviasales"]), ("Plan activities with Klook", LINKS["klook"]),
              ("Compare travel eSIMs with Airalo", LINKS["airalo"]),
              ("Compare airport transfers", LINKS["gettransfer"]),
              ("Travel gear on Amazon", LINKS["amazon"])]
    links = "".join(
        f'<li><a href="{html.escape(url, quote=True)}" rel="sponsored nofollow noopener" target="_blank">{label}</a></li>'
        for label, url in labels
    )
    return f'<section class="trtt-tools" data-destination="{html.escape(city, quote=True)}"><h2>Useful travel tools</h2><ul>{links}</ul></section>'


def build_content(city: str, date_label: str | None = None) -> str:
    """Build a locally grounded editorial draft without invented first-person claims."""
    now = publish_date()
    published = date_label or now.strftime("%-d %B %Y")
    updated = now.strftime("%-d %B %Y")
    safe_city = html.escape(city)
    local_start, route_note = route_context(city)
    focus_title, focus_note = daily_focus(now.day)
    paragraph_one = (
        f"For {safe_city}, plan the ground journey as carefully as the flight. From {local_start}, "
        f"check the airport code and terminal printed on the booking. {route_note} Compare suitable "
        "departure times and calculate the full price after baggage, seat selection, airport transfers "
        "and any overnight stay. Search results are only a snapshot: recheck the airline's own schedule "
        "and fare conditions before paying, especially when a connection or separate ticket is involved."
    )
    paragraph_two = (
        f"This practical route note is prepared from Sanluri, Sardinia, Italy, for travellers comparing "
        f"{safe_city}. It is an editorial planning guide, not a claim of a personally completed journey "
        "or a live fare quotation. Keep the booking confirmation and receipts together. Under EC "
        "Regulation 261/2004, eligible passengers may have rights to care, rerouting or compensation "
        "of up to €600 in qualifying cases. Compensation depends on route distance, arrival delay, "
        "the cause of disruption and legal exceptions; extraordinary circumstances may affect eligibility. "
        "Check the official rules and the facts of your own flight before making a claim."
    )
    tips = (
        f"<h2>Today's planning focus: {html.escape(focus_title)}</h2><p>{html.escape(focus_note)}</p>"
        "<h2>Before you book</h2><ul>"
        "<li>Confirm departure and arrival airport codes and terminals.</li>"
        "<li>Compare the total fare after adding the baggage and seat options you need.</li>"
        "<li>Allow time for the airport transfer, check-in and security queue.</li>"
        "<li>Save airline notices, booking confirmations and receipts if disruption occurs.</li>"
        "<li>Read the <a href='https://europa.eu/youreurope/citizens/travel/passenger-rights/air/index_en.htm'>official EU air-passenger rights guidance</a>.</li>"
        "</ul>"
    )
    footer = (
        '<div class="trtt-editorial-footer">'
        '<p>Marker 787950 Locked - Live from TRTT - Daily update - One route per day - '
        'TRTT editorial planning notes; confirm live fares, schedules and eligibility with official sources.</p>'
        '<p><strong>Publisher:</strong> <a href="https://cocvghuj-trtt-news-bot.vercel.app/about.html">TRTT VoyageHub</a>. '
        'This draft was prepared with automated assistance and requires human fact-checking before publication; '
        'it is not a personal trip report.</p>'
        f'<p><strong>Published:</strong> {html.escape(published)} · <strong>Updated:</strong> {html.escape(updated)}</p>'
        '</div>'
    )
    live_app = (
        f'<p class="trtt-live-app">Live App: <a href="{LIVE_APP}">{LIVE_APP}</a> - '
        'TRTT VoyageHub - Make every journey feel effortless.</p>'
    )
    return (
        f'<article class="trtt-travel-article" data-marker="{MARKER}">'
        f'<h2>{safe_city}: a practical flight-planning guide</h2>'
        f'<img src="https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=800" '
        f'alt="{safe_city}" loading="lazy" />'
        f'<p>{html.escape(paragraph_one)}</p><p>{html.escape(paragraph_two)}</p>'
        + tips
        + '<div id="ghost-esim" data-service="Ghost-SIM" data-product="eSIM" hidden></div>'
        + _tool_links(city) + footer + live_app + '</article>'
    )


def ghost_sim_esim_logic(city: str) -> dict[str, str]:
    return {"service": "Ghost-SIM", "product": "eSIM", "destination": city, "marker": MARKER}


def require_configuration() -> None:
    required = ("BLOGGER_BLOG_ID", "FLIGHTSCOUTPRO_BLOG_ID", "BLOGGER_CLIENT_ID",
                "BLOGGER_CLIENT_SECRET", "BLOGGER_REFRESH_TOKEN")
    missing = [name for name in required if not os.environ.get(name, "").strip()]
    if missing:
        raise RuntimeError("Missing required Blogger configuration: " + ", ".join(missing))
    if os.environ["BLOGGER_BLOG_ID"].strip() == os.environ["FLIGHTSCOUTPRO_BLOG_ID"].strip():
        raise RuntimeError("BLOGGER_BLOG_ID and FLIGHTSCOUTPRO_BLOG_ID must be different.")


def build():
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build as google_build
    credentials = Credentials(
        token=None, refresh_token=os.environ["BLOGGER_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["BLOGGER_CLIENT_ID"],
        client_secret=os.environ["BLOGGER_CLIENT_SECRET"],
        scopes=["https://www.googleapis.com/auth/blogger"],
    )
    return google_build("blogger", "v3", credentials=credentials, cache_discovery=False)


def find_duplicate_post(service: Any, blog_id: str, title: str, content: str,
                        topic_key: str | None = None) -> dict[str, Any] | None:
    """Find matching LIVE or DRAFT posts; never publish an existing draft."""
    token = None
    while True:
        params = {"blogId": blog_id, "fetchBodies": True, "maxResults": 100, "status": ["LIVE", "DRAFT"]}
        if token:
            params["pageToken"] = token
        response = service.posts().list(**params).execute()
        for post in response.get("items", []):
            if str(post.get("title", "")).strip().casefold() == title.strip().casefold():
                return post
            if content.strip() and str(post.get("content", "")).strip() == content.strip():
                return post
        token = response.get("nextPageToken")
        if not token:
            return None


def publish_or_confirm_live(service: Any, blog_id: str, title: str, content: str,
                            topic_key: str | None = None) -> dict[str, Any]:
    """Legacy function name; it can ONLY create or confirm DRAFT posts."""
    existing = find_duplicate_post(service, blog_id, title, content, topic_key)
    if existing:
        status = str(existing.get("status", "")).upper()
        if status == "DRAFT":
            return existing
        raise RuntimeError(f"Matching post is not a draft (status={status}); refusing to publish.")
    post = service.posts().insert(
        blogId=blog_id,
        body={"kind": "blogger#post", "title": title, "content": content,
              "labels": ["TRTT", "Travel Guide", "787950"]},
        isDraft=True,
    ).execute()
    if str(post.get("status", "")).upper() != "DRAFT":
        raise RuntimeError(f"Blogger did not confirm DRAFT status for {title!r}.")
    return post


def run_batch() -> int:
    path = Path(QUEUE_FILE)
    if not path.exists():
        raise RuntimeError(f"Daily route queue missing: {QUEUE_FILE}")
    queue = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(queue, list) or len(queue) != BATCH_SIZE:
        raise ValueError(f"{QUEUE_FILE} must contain exactly {BATCH_SIZE} route.")
    item = queue[0]
    city = str(item.get("city") or item.get("route") or "").strip() if isinstance(item, dict) else str(item).strip()
    if not city:
        raise ValueError("The daily route queue contains an empty route.")
    today = publish_date()
    date_label = today.strftime("%-d %b %Y")
    key = history_key(city, date_label)
    if key in load_history():
        print(f"Draft already recorded for {key}; skipping this scheduled run.")
        return 0
    service = build()
    title = f"{city} Travel Guide: {today.strftime('%-d %B %Y')} - TRTT"
    content = build_content(city, date_label)
    ghost_sim_esim_logic(city)
    targets = [(os.environ["BLOGGER_BLOG_ID"].strip(), "TRTT News 24 BD"),
               (os.environ["FLIGHTSCOUTPRO_BLOG_ID"].strip(), "FlightScoutPro")]
    outcomes = []
    for blog_id, blog_name in targets:
        post = publish_or_confirm_live(service, blog_id, title, content, city)
        if str(post.get("status", "")).upper() != "DRAFT":
            raise RuntimeError(f"{blog_name} did not confirm DRAFT status.")
        outcomes.append((blog_name, post.get("id"), post.get("editUrl") or post.get("url")))
    if len(outcomes) != 2:
        raise RuntimeError("Both Blogger blogs must confirm DRAFT status.")
    for blog_name, post_id, editor in outcomes:
        print(f"{blog_name}: DRAFT id={post_id} editor={editor or 'Open Blogger Posts > Drafts'}")
    with Path(HISTORY_FILE).open("a", encoding="utf-8") as handle:
        handle.write(key + "\n")
    print(f"TRTT complete: 1 route; 2 Blogger DRAFT records confirmed for {city}.")
    return 1


def main() -> int:
    require_configuration()
    return run_batch()


if __name__ == "__main__":
    raise SystemExit(main())
