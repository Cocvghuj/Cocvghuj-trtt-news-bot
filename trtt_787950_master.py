#!/usr/bin/env python3
"""TRTT daily Blogger draft engine. Draft-only; never publishes posts live."""
from __future__ import annotations

import html
import json
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
QUEUE_FILE = ROOT / "news" / "queue" / "latest.json"
HISTORY_FILE = ROOT / "drafted_history.txt"
TIME_ZONE = ZoneInfo("Europe/Rome")
BATCH_SIZE = 1
MARKER = "787950 LOCKED"
LIVE_APP = "https://cocvghuj-trtt-news-bot.vercel.app"
AFFILIATES = {
    "amazon": "https://amzn.to/4shg6Hn?marker=787950",
    "aviasales": "https://aviasales.tpo.lv/Fb8U9yav?marker=787950",
    "klook": "https://klook.tpo.lv/TWKnemhz?marker=787950",
    "airalo": "https://airalo.tpo.lv/ZZoQC7Mz?marker=787950",
    "gettransfer": "https://gettransfer.tpo.lv/1u8zRU5s?marker=787950",
}


def publish_date() -> datetime:
    return datetime.now(TIME_ZONE)


def daily_focus(day: int) -> tuple[str, str]:
    focuses = [
        ("Compare the complete fare", "Include baggage, seat selection, payment fees and airport transfers before comparing the final price."),
        ("Plan the airport transfer", "Check the first and last practical ground connections and leave time for queues, road traffic and terminal access."),
        ("Review baggage rules", "Check the operating carrier's current cabin and checked-bag limits for the exact fare class before checkout."),
        ("Keep disruption records", "Save the booking confirmation, boarding pass, airline notices and receipts if the journey is disrupted."),
        ("Protect connections", "Allow time for baggage collection, check-in and security when separate tickets are involved."),
    ]
    return focuses[day % len(focuses)]


def route_key(route: dict[str, Any]) -> str:
    return f"{route['from']} to {route['to']} | {route['date']}"


def load_history() -> list[str]:
    if not HISTORY_FILE.exists():
        return []
    return [line.strip() for line in HISTORY_FILE.read_text(encoding="utf-8").splitlines() if line.strip()]


def append_history(key: str) -> None:
    """Atomically retain the latest 12 verified route keys; oldest entry shifts out."""
    history = [item for item in load_history() if item != key]
    history.append(key)
    history = history[-12:]
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    temporary = HISTORY_FILE.with_suffix(HISTORY_FILE.suffix + ".tmp")
    temporary.write_text("\n".join(history) + "\n", encoding="utf-8")
    temporary.replace(HISTORY_FILE)


def _load_today_route() -> tuple[dict[str, Any], dict[str, Any]]:
    today = publish_date().date().isoformat()
    fallback_template = {
        "from": "Cagliari", "to": "Bergamo", "iata_from": "CAG", "iata_to": "BGY",
        "price": "€19 (unverified queue lead)", "airline": "Verify operating carrier",
        "image_url": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=800&h=600&fit=crop&q=80", "isDraft": True,
    }
    if not QUEUE_FILE.is_file() or QUEUE_FILE.stat().st_size == 0:
        queue: dict[str, Any] = {
            "version": today, "batch_size": BATCH_SIZE, "isDraft": True,
            "require_image": True, "require_marker": MARKER, "routes": [],
            "fallback_route": fallback_template,
        }
    else:
        try:
            queue = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise AssertionError(f"Daily queue is unreadable; refusing to guess: {exc}") from exc
    if not isinstance(queue, dict):
        raise AssertionError("Queue must be a JSON object, not a bare route list.")
    if queue.get("isDraft") is not True:
        raise AssertionError("Queue policy violation: isDraft must be true.")
    if queue.get("batch_size") != BATCH_SIZE:
        raise AssertionError("Queue policy violation: batch_size must equal 1.")
    if queue.get("require_image") is not True:
        raise AssertionError("Queue policy violation: require_image must be true.")
    if queue.get("require_marker") != MARKER:
        raise AssertionError("Queue policy violation: marker must be 787950 LOCKED.")
    routes = queue.get("routes", [])
    if routes is None:
        routes = []
    if not isinstance(routes, list):
        raise AssertionError("Queue routes must be a list.")
    if len(routes) == 0:
        fallback = queue.get("fallback_route")
        route = dict(fallback) if isinstance(fallback, dict) else dict(fallback_template)
        route.setdefault("date", today)
        route.setdefault("isDraft", True)
        print("Queue empty - generated today's Cagliari to Bergamo fallback route.")
    else:
        if len(routes) != BATCH_SIZE or not isinstance(routes[0], dict):
            raise AssertionError(f"Exactly one route object is required; found {len(routes)}.")
        route = dict(routes[0])
    required = ("from", "to", "iata_from", "iata_to", "date", "price", "airline")
    missing = [field for field in required if not str(route.get(field, "")).strip()]
    if missing:
        raise AssertionError("Queue route is missing: " + ", ".join(missing))
    if route.get("isDraft") is not True:
        raise AssertionError("Route policy violation: route.isDraft must be true.")
    if route["date"] != today:
        raise AssertionError(
            f"Queue date {route['date']} is not today's Europe/Rome date {today}; "
            "refusing to create a draft for the wrong day."
        )
    return queue, route

def _plain_word_count(content: str) -> int:
    plain = re.sub(r"<[^>]+>", " ", content)
    plain = html.unescape(plain)
    return len(re.findall(r"\b[\w€'-]+\b", plain, flags=re.UNICODE))


def _affiliate_list() -> str:
    items = [
        ("Amazon travel gear", AFFILIATES["amazon"]),
        ("Aviasales flight comparison", AFFILIATES["aviasales"]),
        ("Klook activities and experiences", AFFILIATES["klook"]),
        ("Airalo travel eSIM options", AFFILIATES["airalo"]),
        ("GetTransfer airport transfers", AFFILIATES["gettransfer"]),
    ]
    return "<ul>" + "".join(
        f'<li><a href="{html.escape(url, quote=True)}" rel="sponsored nofollow noopener" target="_blank">{label}</a></li>'
        for label, url in items
    ) + "</ul>"


def build_content(route: dict[str, Any] | str, date_label: str | None = None) -> str:
    """Build a researched-style planning draft; queue prices are explicitly unverified leads."""
    if isinstance(route, str):
        parts = route.split(" to ", 1)
        if len(parts) != 2:
            raise ValueError("Route string must use 'Origin to Destination'.")
        route = {
            "from": parts[0].strip(), "to": parts[1].strip(),
            "iata_from": "CAG", "iata_to": "BGY",
            "date": publish_date().date().isoformat(), "price": "Not supplied",
            "airline": "Not supplied", "isDraft": True,
        }
    origin = html.escape(str(route["from"]))
    destination = html.escape(str(route["to"]))
    iata_from = html.escape(str(route["iata_from"]))
    iata_to = html.escape(str(route["iata_to"]))
    travel_date = html.escape(str(route["date"]))
    fare = html.escape(str(route["price"]))
    airline = html.escape(str(route["airline"]))
    published = date_label or publish_date().strftime("%-d %B %Y")
    image_url = str(route.get("image_url") or "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=800&h=600&fit=crop&q=80")
    content = f"""<!-- 787950 LOCKED -->
<article class="trtt-daily-route" data-marker="787950 LOCKED" data-is-draft="true">
<h1>{origin} to {destination}: flight planning guide for {travel_date}</h1>
<figure>
<img src="{image_url}" alt="Mountain and lake landscape in Sardinia travel scenery" loading="lazy" />
<figcaption>Travel-planning image. Confirm image licensing and attribution requirements before publication.</figcaption>
</figure>
<p><strong>Route:</strong> {origin} ({iata_from}) to {destination} ({iata_to}). <strong>Scheduled date:</strong> {travel_date}. The queue currently lists a fare lead of {fare} with {airline}. This is not a live fare guarantee or an independently verified quotation. Airline inventory, taxes, baggage charges and payment fees can change, so check the final price directly with the operating carrier before buying.</p>
<p>A useful flight plan begins before the airport. Travellers starting in Cagliari should allow time to reach Cagliari Elmas Airport, confirm the terminal shown on the booking and check the airline's current check-in deadline. The journey to the airport can vary with the time of day, local road conditions and the transport option selected. People travelling from Sanluri or elsewhere in Sardinia should compare the full door-to-terminal journey rather than looking only at the flight departure time. Keep a practical buffer for parking, public transport changes, security queues and any mobility or family needs.</p>
<p>For the destination side, confirm that the ticket names Bergamo Orio al Serio (BGY), not another airport serving the wider Milan area. Airport names can look similar in search results, but the ground transfer may be very different. Before choosing a fare, check the arrival time, onward bus or rail options, the location of your accommodation and the cost of reaching the final address. A low fare can become an expensive journey when a late arrival requires a taxi or an overnight stay. Do not assume a transfer is included unless it appears in the booking conditions.</p>
<h2>Compare the complete price, not just the headline fare</h2>
<p>Use the same passenger count, travel dates and baggage requirements when comparing options. Review the cabin-bag dimensions, checked-bag allowance, seat-selection charge and payment conditions for the exact fare class. If you are travelling with children, carrying equipment or need extra time at the airport, check those details before checkout. Save a copy of the fare rules and confirmation email. If the price shown in the queue is no longer available, do not describe it as a current offer; update the article only after checking a live booking page and recording when that check was made.</p>
<p>Travellers comparing schedules should look at the whole day. An early departure may require transport before normal public services begin, while a late arrival may reduce the available transfer choices. Check the first and last practical connections for the actual travel date. If you are using separate tickets, leave enough time to collect baggage, check in again and pass security. Separate tickets generally do not provide the same missed-connection protection as a single through-ticket, so understand the risk before paying.</p>
<h2>Travel connectivity: Ghost-SIM = eSIM</h2>
<p>Ghost-SIM = eSIM. A compatible eSIM can help a traveller access mobile data after arrival without searching for a physical SIM shop. Check that the phone is unlocked, supports eSIM and is compatible with the provider's network in Italy and the destination country. Compare data allowance, validity period, hotspot rules and activation instructions. Install the profile using a reliable internet connection before departure when the provider recommends it, but follow the provider's own activation timing so that the plan does not start earlier than intended. Keep offline copies of tickets, hotel details and transfer instructions in case mobile coverage is temporarily unavailable.</p>
<h2>Passenger rights and disruption records</h2>
<p>EC 261/2004 may provide assistance, rerouting, reimbursement or compensation for eligible passengers when a flight is cancelled, denied boarding or delayed on arrival. The outcome depends on the journey, the length of the delay, the reason for the disruption and the applicable legal conditions. Compensation is not automatic, and extraordinary circumstances can affect eligibility. Read the official passenger-rights information and the airline's notice carefully rather than relying on a generic promise. Keep the booking reference, boarding pass, receipts, written airline messages and a note of the actual arrival time. Those records make it easier to describe what happened accurately if you later contact the airline or seek advice.</p>
<p>For a Cagliari-based traveller, the practical checklist is straightforward: verify CAG and BGY on the ticket, confirm the operating carrier, compare the complete fare, plan the Sardinian airport transfer and save the booking documents. Sanluri residents should add the road journey to the calculation. Anyone continuing beyond Bergamo should check the onward connection before choosing a flight. These steps are useful whether the trip is for work, a family visit or a short break, and they reduce the chance of overlooking a cost that appears only after checkout.</p>
<h2>Useful travel tools</h2>
{_affiliate_list()}
<p><strong>Editorial note:</strong> This is a route-planning draft based on the supplied queue record. It does not claim first-hand travel experience, a real-time fare check or a guarantee of flight operation. Confirm every time-sensitive detail with the airline, airport and transport operator. Human editorial review is required before publication.</p>
<p><strong>Published:</strong> {html.escape(published)} · <strong>Updated:</strong> {html.escape(published)}</p>
<p>Marker 787950 LOCKED · Make every journey feel effortless.</p>
<p><a href="https://europa.eu/youreurope/citizens/travel/passenger-rights/air/index_en.htm" rel="noopener">Official EU air passenger rights guidance</a></p>
<p><a href="{LIVE_APP}">TRTT VoyageHub Showroom</a></p>
</article>"""
    content = content.replace("</article>", """
<h2>Check the complete journey before booking</h2>
<p>Use the date on the final booking screen as the source of truth and compare the departure and arrival airport codes before payment. A city label can cover several airports, and choosing the wrong one can add a long transfer or an unexpected overnight stay. For this route, check that the ticket shows CAG at departure and BGY at arrival. If the carrier changes an airport or schedule, compare the revised itinerary with your ground transport, accommodation check-in time and any onward reservation. Save the updated confirmation rather than relying on an earlier search result.</p>
<p>Compare the total cost for the same number of passengers and the same baggage needs. Include cabin baggage, checked baggage, seat selection, payment charges and transport to and from each airport. Optional products may be cheaper when selected during the initial booking, but only add them if they are useful. Read the fare conditions before payment and note whether changes, cancellations or refunds are permitted. A low headline price is not a meaningful comparison if one option excludes a bag that you already know you need.</p>
<h2>Plan the airport day with a realistic time buffer</h2>
<p>Check the official airport and transport operator information close to departure. Timetables can change for weekends, public holidays, maintenance or seasonal demand. Work backwards from the airline's check-in and bag-drop deadlines, then allow time for the journey to the terminal, parking or public transport, security and walking to the gate. If the first available bus or train leaves little margin, identify a backup before travel day. Travellers who need mobility assistance should request it from the airline in advance and keep the confirmation with their booking documents.</p>
<p>For the arrival at Bergamo, check the onward connection using the actual landing time, not just the scheduled departure time. Allow for taxiing, baggage collection and possible delays before choosing a coach or train. If the next leg is on a separate ticket, understand that the second provider may not protect you when the first flight is late. Keep the address of your accommodation offline and check the final public transport departure. When no practical connection remains, compare the cost of a licensed taxi with the cost of changing the flight.</p>
<h2>Prepare documents and baggage before leaving</h2>
<p>Check that every passenger name matches the travel document and that the document is valid for the complete journey. Review entry and transit requirements using official government information for the passenger's nationality and destination. Keep the booking reference, boarding pass, travel insurance details and carrier contact information available offline. Photographing a document can be useful as a backup, but it does not replace carrying the original document when required. If a booking was made through an intermediary, note whether the airline or the agent must handle a change or refund request.</p>
<p>Measure cabin baggage and check the operating carrier's current size and weight limits for the exact fare. A personal item and a cabin trolley may have different allowances. Put medication and essential items in the bag that stays with you, subject to applicable security rules. If travelling with sports equipment, musical instruments, a pushchair or other unusual baggage, obtain written confirmation of the handling rules before going to the airport. Do not assume that an allowance from a previous trip applies to a new fare or a different airline.</p>
<h2>Understand disruption support and passenger rights</h2>
<p>If a flight is cancelled, delayed or changed, save the airline's messages and take a note of the time the information was received. Keep boarding passes, booking confirmations, receipts for necessary expenses and evidence of the actual arrival time. Ask the carrier what care, rerouting or refund options are available and keep the response. EC 261/2004 can apply to eligible journeys, but compensation is not automatic for every delay. The route, operating carrier, length of delay and cause of disruption all matter. Read official European Union guidance and the carrier's written decision before deciding whether a claim is appropriate.</p>
<p>When requesting help, describe the events in chronological order and attach copies of relevant records. Keep original receipts and avoid sending sensitive payment details in an ordinary email. If the airline rejects a request, read the reason and check the official national enforcement body or consumer advice route that applies to the journey. A claims company cannot guarantee an outcome. This guide is general travel information, not legal advice; the facts of the individual disruption determine which rights and remedies may be available.</p>
<h2>Final checks for this Cagliari–Bergamo itinerary</h2>
<p>Before departure, verify the live operating schedule with the airline, confirm CAG and BGY on the ticket, review the baggage allowance and calculate the complete door-to-door cost. Recheck the airport transfer on the day because road conditions and public transport services can change. Confirm the destination address and save a backup route from the airport. If the fare or operating carrier differs from the queue information, update the draft after checking a reliable source rather than presenting old details as current facts.</p>
<p>The route record is a starting point for a human-reviewed travel guide, not proof that a seat or fare is currently available. Prices, flight times, baggage rules and ground connections are time-sensitive. The editor should confirm each item against the airline, airport and transport operator before approving the post. Keep affiliate disclosures clear wherever a tracked link appears, and make sure the reader can distinguish editorial guidance from a commercial link. The article should remain useful even if a displayed fare changes or a particular service is no longer offered.</p>

</article>""")
    if _plain_word_count(content) < 800:
        raise AssertionError(f"Draft content is too short: {_plain_word_count(content)} words; minimum is 800.")
    required = [
        '<img src="https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=800&h=600&fit=crop&q=80"',
        "<img src=\"https://images.unsplash.com/",
        "EC 261/2004",
        "Ghost-SIM = eSIM",
        "787950 LOCKED",
        LIVE_APP,
        "amzn.to/4shg6Hn?marker=787950",
        "Sanluri",
        "Sardinia",
        "Cagliari",
    ]
    missing = [item for item in required if item not in content]
    if missing:
        raise AssertionError("Draft content missing required fields: " + ", ".join(missing))
    return content


def build():
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


def find_duplicate_post(service: Any, blog_id: str, title: str) -> dict[str, Any] | None:
    page_token = None
    while True:
        params: dict[str, Any] = {
            "blogId": blog_id,
            "fetchBodies": False,
            "maxResults": 100,
            "status": ["LIVE", "DRAFT"],
        }
        if page_token:
            params["pageToken"] = page_token
        response = service.posts().list(**params).execute()
        for post in response.get("items", []):
            if str(post.get("title", "")).strip().casefold() == title.strip().casefold():
                return post
        page_token = response.get("nextPageToken")
        if not page_token:
            return None


def _confirmed_status(service: Any, blog_id: str, post: dict[str, Any]) -> str:
    """Read the saved Blogger resource back; do not trust a local flag or insert log."""
    post_id = post.get("id")
    if not post_id:
        return ""
    fetched = service.posts().get(blogId=blog_id, postId=post_id).execute()
    return str(fetched.get("status", "")).upper()


def _create_or_recover_draft(service: Any, blog_id: str, title: str, content: str) -> tuple[dict[str, Any], bool]:
    last_error: Exception | None = None
    for attempt in range(1, 4):
        existing = find_duplicate_post(service, blog_id, title)
        if existing:
            status = _confirmed_status(service, blog_id, existing)
            if status == "DRAFT":
                return existing, False
            raise AssertionError(f"Matching Blogger post exists with status {status or 'UNKNOWN'}; refusing unsafe action.")
        try:
            response = service.posts().insert(
                blogId=blog_id,
                body={
                    "kind": "blogger#post",
                    "title": title,
                    "content": content,
                    "labels": ["TRTT", "Flight Guide", "Sardinia", "787950"],
                },
                isDraft=True,
            ).execute()
            if not response.get("id"):
                raise AssertionError("Blogger insert response did not include a post id.")
            status = _confirmed_status(service, blog_id, response)
            if status != "DRAFT":
                raise AssertionError(f"Blogger did not confirm DRAFT status; returned {status or 'UNKNOWN'}.")
            return response, True
        except AssertionError:
            raise
        except Exception as error:
            last_error = error
            print(f"Blogger insert attempt {attempt}/3 failed for blog {blog_id}: {error}")
            if attempt < 3:
                time.sleep(attempt)
    raise AssertionError(f"Unable to create or verify Blogger draft for blog {blog_id}: {last_error}")


def _require_configuration() -> tuple[str, str]:
    required = (
        "BLOGGER_BLOG_ID",
        "FLIGHTSCOUTPRO_BLOG_ID",
        "BLOGGER_CLIENT_ID",
        "BLOGGER_CLIENT_SECRET",
        "BLOGGER_REFRESH_TOKEN",
    )
    missing = [name for name in required if not os.environ.get(name, "").strip()]
    if missing:
        raise AssertionError("Missing required Blogger configuration: " + ", ".join(missing))
    main_id = os.environ["BLOGGER_BLOG_ID"].strip()
    partner_id = os.environ["FLIGHTSCOUTPRO_BLOG_ID"].strip()
    if main_id == partner_id:
        raise AssertionError("The two Blogger blog IDs must be different.")
    return main_id, partner_id


def main() -> int:
    run_started = time.monotonic()
    main_blog_id, partner_blog_id = _require_configuration()
    queue, route = _load_today_route()
    key = route_key(route)
    history = load_history()
    print("Republish allowed - today's date override")
    title = (
        f"{route['from']} to {route['to']} flight guide - "
        f"{datetime.strptime(route['date'], '%Y-%m-%d').strftime('%-d %B %Y')} - TRTT"
    )
    content = build_content(route)
    checks = {
        "Image": "<img src=\"https://images.unsplash.com/" in content,
        "EC 261/2004": "EC 261/2004" in content,
        "787950 LOCKED": MARKER in content,
        "Vercel Link": LIVE_APP in content,
        "Affiliate": AFFILIATES["amazon"] in content,
    }
    for label, passed in checks.items():
        print(f"{label}: {'YES' if passed else 'NO'}")
        if not passed:
            raise AssertionError(f"Required draft content check failed: {label}")
    word_count = _plain_word_count(content)
    print(f"Article word count: {word_count}")
    if word_count < 800:
        raise AssertionError(f"Draft content must contain at least 800 words; got {word_count}.")
    print(f"Queue: {queue.get('version', route['date'])} | Batch size: {BATCH_SIZE} | isDraft=True")

    service = build()
    targets = [
        (main_blog_id, "trttnews24bd"),
        (partner_blog_id, "flightscoutpro"),
    ]
    results = []
    newly_created = 0
    for blog_id, blog_name in targets:
        post, created = _create_or_recover_draft(service, blog_id, title, content)
        if not post.get("id"):
            raise AssertionError(f"Blogger returned no post ID for {blog_name}.")
        if _confirmed_status(service, blog_id, post) != "DRAFT":
            raise AssertionError(f"Blogger DRAFT status could not be verified for {blog_name}.")
        if created:
            newly_created += 1
            print(f"SUCCESS: Draft created - {blog_name} - Post ID: {post['id']}")
        else:
            print(f"CONFIRMED: Existing Blogger DRAFT - {blog_name} - Post ID: {post['id']}")
        results.append((blog_name, str(post["id"])))

    if len(results) != 2:
        raise AssertionError("Draft creation failed: both Blogger sites were not verified.")
    # History is written only after both real Blogger post IDs and DRAFT statuses are confirmed.
    append_history(key)
    elapsed = time.monotonic() - run_started
    print(f"Draft run elapsed: {elapsed:.2f}s")
    print(
        f"CONFIRMED: {len(results)} Blogger DRAFT records; "
        f"newly created this run: {newly_created}; route: {key}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
