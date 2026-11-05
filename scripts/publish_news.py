#!/usr/bin/env python3
"""Create verified, draft-only Blogger posts for both TRTT sites.

No live publishing endpoint is called. History is written only after both
Blogger records have been independently confirmed as DRAFT.
"""
from __future__ import annotations

import html
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import trtt_787950_master as engine

QUEUE_FILE = ROOT / "news" / "queue" / "latest.json"
HISTORY_FILE = ROOT / "drafted_history.txt"
ITALY = ZoneInfo("Europe/Rome")
BATCH_SIZE = 1
MARKER = "787950 LOCKED"
VERCEL_LINK = "https://cocvghuj-trtt-news-bot.vercel.app"
AFFILIATE = "https://amzn.to/4shg6Hn?marker=787950"
FALLBACK_ROUTE = {
    "from": "Cagliari",
    "to": "Bergamo",
    "iata_from": "CAG",
    "iata_to": "BGY",
    "price": "Check live fare",
    "airline": "Verify operating carrier",
    "isDraft": True,
}


def italy_now() -> datetime:
    return datetime.now(ITALY)


def load_route() -> tuple[dict, dict]:
    """Load one route, or create today's Cagliari–Bergamo fallback if empty."""
    if not QUEUE_FILE.is_file():
        queue = {"version": italy_now().date().isoformat(), "routes": []}
    else:
        try:
            queue = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Queue is unreadable; refusing to guess a route: {exc}") from exc

    if not isinstance(queue, dict):
        raise RuntimeError("Queue must be a JSON object.")
    if queue.get("isDraft", True) is not True:
        raise RuntimeError("Queue is not marked isDraft=true.")
    if queue.get("batch_size", BATCH_SIZE) != BATCH_SIZE:
        raise RuntimeError("Queue batch_size must be exactly 1.")

    routes = queue.get("routes", [])
    if routes is None:
        routes = []
    if not isinstance(routes, list):
        raise RuntimeError("Queue routes must be a list.")

    if not routes:
        fallback = dict(FALLBACK_ROUTE)
        fallback["date"] = italy_now().date().isoformat()
        route = fallback
        print("Queue empty - generated today's Cagliari to Bergamo fallback route.")
    else:
        if len(routes) != 1 or not isinstance(routes[0], dict):
            raise RuntimeError(f"Expected exactly one route for batch 1; found {len(routes)}.")
        route = dict(routes[0])

    required = ("from", "to", "iata_from", "iata_to", "date", "price", "airline")
    missing = [key for key in required if not str(route.get(key, "")).strip()]
    if missing:
        raise RuntimeError("Route missing required fields: " + ", ".join(missing))
    if route.get("isDraft") is not True:
        raise RuntimeError("Route must explicitly set isDraft=true.")

    today = italy_now().date().isoformat()
    if route["date"] != today:
        raise RuntimeError(
            f"Date guard blocked run: queue date {route['date']} != Italy today {today}. "
            "Run after 00:00 Europe/Rome on the queued date."
        )
    return queue, route


def route_key(route: dict) -> str:
    return f"{route['from']} to {route['to']} | {route['date']}"


def read_history() -> list[str]:
    if not HISTORY_FILE.exists():
        return []
    return [
        line.strip()
        for line in HISTORY_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def update_history_after_both_verified(key: str) -> None:
    """Append only after both sites have verified DRAFT IDs; retain 12 entries."""
    history = [item for item in read_history() if item != key]
    history = (history + [key])[-12:]
    temporary = HISTORY_FILE.with_suffix(".txt.tmp")
    temporary.write_text("\n".join(history) + "\n", encoding="utf-8")
    temporary.replace(HISTORY_FILE)


def count_words(content: str) -> int:
    plain = re.sub(r"<[^>]*>", " ", content)
    plain = html.unescape(plain)
    return len(re.findall(r"\b[\w€'-]+\b", plain, flags=re.UNICODE))


def build_article(route: dict) -> str:
    """Use the master engine, then add route-specific practical detail to reach 800+ words."""
    content = engine.build_content(route)
    origin = html.escape(str(route["from"]))
    destination = html.escape(str(route["to"]))
    travel_date = html.escape(str(route["date"]))
    iata_from = html.escape(str(route["iata_from"]))
    iata_to = html.escape(str(route["iata_to"]))

    extra = f"""
<section>
<h2>Before leaving for Cagliari Elmas Airport</h2>
<p>For a departure from {origin}, build the airport journey around the check-in deadline shown by the airline, not simply the scheduled take-off time. Check the airport's official transport and parking information close to departure because timetables, roadworks and service arrangements can change. If travelling by bus or train, confirm the first service that realistically gets you to the terminal with a useful buffer. If someone is driving you, agree on a meeting point and allow for traffic around the airport access roads. Travellers with reduced mobility, pushchairs, musical instruments or sports equipment should arrange any assistance or special handling through the carrier before travel and keep the confirmation available.</p>
<p>At online check-in, compare the passenger name with the travel document and review every segment of the itinerary. A small spelling difference can become a problem at the airport. Keep the booking reference, boarding pass and airline contact details available offline as well as in email. If the airline changes the schedule, read the notice carefully and check whether the revised time affects the ground transfer or any onward reservation. Do not rely on an old screenshot when the carrier has issued a newer itinerary.</p>
<h2>Confirm the arrival airport and onward journey</h2>
<p>The destination airport code for this route is {iata_to}; the departure code is {iata_from}. Confirm both codes on the final ticket and on the airport's own website. The phrase “Milan area” can refer to more than one airport, and a booking to a different airport can change the transfer cost and journey time substantially. For an arrival at {destination}, check the official bus, rail and taxi information for the actual arrival time. Late-night and early-morning services may be less frequent than daytime services. If the onward connection is important, identify a backup option and save its details before leaving home.</p>
<p>When comparing a flight with another travel option, include the time spent reaching the airport, waiting before departure, collecting baggage and travelling from the arrival airport to the final address. A headline fare is only one part of the total trip. A slightly more expensive departure may be better value if it avoids an expensive overnight stay or an impractical transfer. These are planning comparisons, not a claim that any particular service will be operating on {travel_date}; confirm the timetable with the transport provider.</p>
<h2>Baggage, seating and booking conditions</h2>
<p>Airline baggage rules can depend on the fare family, route, booking channel and date of purchase. Check the dimensions as well as the weight allowance, because a bag that fits one carrier's policy may not fit another's. Read the rule for a personal item separately from the rule for a cabin trolley. If checked baggage is needed, compare its price when selecting the fare rather than adding it later without checking the difference. Families and groups should also review seat allocation: sitting together may require a paid selection, and an automatically assigned seat is not necessarily next to another passenger.</p>
<p>Before paying, inspect the change, cancellation and refund conditions. A low-cost ticket may have limited flexibility, while optional products can have separate terms. Make sure the passenger details, dates, airports and currency are correct on the payment screen. Save the receipt and the full terms supplied at checkout. If a third-party booking service is involved, establish whether the airline or the intermediary will handle changes and disruption support. This practical check can save time if the itinerary later needs attention.</p>
<h2>Prepare for disruption without assuming compensation</h2>
<p>Keep evidence if a flight is delayed, cancelled or significantly changed. Save messages from the airline, screenshots of the departure board, boarding passes and reasonable receipts for necessary expenses. Ask the carrier what assistance it is providing and keep a record of the time and channel used. EC 261/2004 has specific eligibility rules and does not mean every delay automatically results in compensation. The route, operating carrier, arrival delay and cause of disruption can all matter. Use official European Union guidance and the airline's written response when assessing a claim. Avoid services that promise a guaranteed payout before the facts have been reviewed.</p>
<p>For this {origin}–{destination} itinerary, the most useful preparation is to verify the live schedule, identify the correct airport codes, price the complete door-to-door journey and keep the booking evidence together. Recheck the details shortly before departure because operational information can change. This guide is general planning information, not a live availability statement or legal advice. Editorial review should confirm every time-sensitive detail before the draft is approved for publication.</p>
</section>
"""
    content = content.replace("</article>", extra + "\n</article>")
    required = {
        "image": "<img src=\"https://images.unsplash.com/",
        "EC 261/2004": "EC 261/2004",
        "marker": MARKER,
        "Vercel link": VERCEL_LINK,
        "affiliate": AFFILIATE,
    }
    missing = [name for name, needle in required.items() if needle not in content]
    if missing:
        raise RuntimeError("Article validation failed: " + ", ".join(missing))
    words = count_words(content)
    if words < 800:
        raise RuntimeError(f"Article has {words} words; minimum required is 800.")
    return content


def require_blog_configuration() -> tuple[str, str]:
    names = (
        "BLOGGER_BLOG_ID",
        "FLIGHTSCOUTPRO_BLOG_ID",
        "BLOGGER_CLIENT_ID",
        "BLOGGER_CLIENT_SECRET",
        "BLOGGER_REFRESH_TOKEN",
    )
    missing = [name for name in names if not os.environ.get(name, "").strip()]
    if missing:
        raise RuntimeError("Missing Blogger settings: " + ", ".join(missing))
    main_id = os.environ["BLOGGER_BLOG_ID"].strip()
    second_id = os.environ["FLIGHTSCOUTPRO_BLOG_ID"].strip()
    if main_id == second_id:
        raise RuntimeError("The two Blogger Blog IDs must be different.")
    print(f"Blog ID verified - trttnews24bd: {main_id}")
    print(f"Blog ID verified - flightscoutpro: {second_id}")
    return main_id, second_id


def confirmed_status(service, blog_id: str, response: dict) -> str:
    post_id = response.get("id")
    if not post_id:
        raise RuntimeError("Blogger API response did not include response['id'].")
    status = str(response.get("status", "")).upper()
    if status != "DRAFT":
        fetched = service.posts().get(blogId=blog_id, postId=post_id).execute()
        status = str(fetched.get("status", "")).upper()
    if status != "DRAFT":
        raise RuntimeError(f"Post {post_id} was not confirmed as DRAFT (status={status or 'missing'}).")
    return str(post_id)


def find_existing_draft(service, blog_id: str, title: str) -> dict | None:
    page_token = None
    while True:
        args = {
            "blogId": blog_id,
            "fetchBodies": False,
            "maxResults": 100,
            "status": ["DRAFT"],
        }
        if page_token:
            args["pageToken"] = page_token
        result = service.posts().list(**args).execute()
        for post in result.get("items", []):
            if str(post.get("title", "")).strip().casefold() == title.casefold():
                return post
        page_token = result.get("nextPageToken")
        if not page_token:
            return None


def create_verified_draft(service, blog_id: str, blog_name: str, title: str, content: str,
                          route: dict) -> tuple[str, bool]:
    existing = find_existing_draft(service, blog_id, title)
    if existing:
        post_id = confirmed_status(service, blog_id, existing)
        print(f"CONFIRMED: Existing Blogger draft - {blog_name} - Post ID: {post_id}")
        return post_id, False

    post_body = {
        "kind": "blogger#post",
        "title": title,
        "content": content,
        "labels": ["TRTT", "Flight Guide", "Sardinia", "787950"],
    }
    response = service.posts().insert(
        blogId=blog_id,
        body=post_body,
        isDraft=True,
    ).execute()
    post_id = confirmed_status(service, blog_id, response)
    print(
        f"SUCCESS: Draft created - {blog_name} - "
        f"{route['from']} to {route['to']} - isDraft=True - Post ID: {post_id}"
    )
    return post_id, True


def main() -> int:
    queue, route = load_route()
    main_blog_id, second_blog_id = require_blog_configuration()
    key = route_key(route)
    if key in read_history():
        print("Republish allowed - today's date override")

    content = build_article(route)
    checks = [
        ("Image", "<img src=\"https://images.unsplash.com/" in content),
        ("EC 261/2004", "EC 261/2004" in content),
        (MARKER, MARKER in content),
        ("Vercel Link", VERCEL_LINK in content),
        (f"Affiliate {AFFILIATE}", AFFILIATE in content),
    ]
    for label, passed in checks:
        print(f"{label}: {'YES' if passed else 'NO'}")
        if not passed:
            raise RuntimeError(f"Required article element missing: {label}")
    print(f"Article word count: {count_words(content)} (minimum 800)")
    print(f"Queue batch: {queue.get('batch_size', BATCH_SIZE)} | isDraft=True")

    title_date = datetime.strptime(route["date"], "%Y-%m-%d").strftime("%-d %B %Y")
    title = f"{route['from']} to {route['to']} flight guide - {title_date} - TRTT"
    service = engine.build()

    targets = [
        (main_blog_id, "trttnews24bd"),
        (second_blog_id, "flightscoutpro"),
    ]
    confirmed = []
    newly_created = 0
    for blog_id, blog_name in targets:
        post_id, created = create_verified_draft(
            service, blog_id, blog_name, title, content, route
        )
        confirmed.append((blog_name, post_id))
        newly_created += int(created)

    if len(confirmed) != 2:
        raise RuntimeError("Both Blogger draft responses were not confirmed.")
    if newly_created == 0:
        print("Both dated drafts already existed; history remains unchanged.")
        return 0

    # Critical ordering: history is updated only after both IDs and DRAFT statuses pass.
    update_history_after_both_verified(key)
    print(f"History updated after both Blogger drafts were verified: {key}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
