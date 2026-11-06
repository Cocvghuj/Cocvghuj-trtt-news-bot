"""
TRTT Enterprise Auto-Publisher Engine (Google Blogger Direct & Multi-Blog Network)
Protocol 26391/2026 • Marker 787950 LOCKED
Dedicated to family: Roksana | Taifa | Tashrif (From Sanluri to Dhaka)
Strictly compliant with Google Search, Google Search Console, and GitHub Rules.
Automated Multi-Blog Publishing for TRTT News 24 BD & FlightScoutPro.
"""

import json
import time

def retry_generate_content(client, model, prompt, retries=3, delay=10):
    for i in range(retries):
        try:
            return client.models.generate_content(model=model, contents=prompt)
        except Exception as e:
            if i < retries - 1:
                print(f"Rate limit hit or error, retrying in {delay}s...")
                time.sleep(delay)
                delay *= 2
            else:
                raise e

import os
import re
import difflib
import hashlib
import html
import tempfile
import unicodedata
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
import requests

from config import AFFILIATE_SERVICES
from google import genai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
try:
    from slugify import slugify
except ImportError:
    def slugify(text: str) -> str:
        text = re.sub(r'[^\w\s-]', '', str(text).lower())
        return re.sub(r'[-\s]+', '-', text).strip('-')

# ==============================================================================
# CONFIGURATION & SECRETS
# ==============================================================================
MARKER = os.environ.get("TRAVEL_PAYOUT_MARKER", "787950")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

# Primary & Partner Blog IDs for Multi-Blog Syndication
BLOGGER_BLOG_ID = os.environ.get("BLOGGER_BLOG_ID")
FLIGHTSCOUTPRO_BLOG_ID = os.environ.get("FLIGHTSCOUTPRO_BLOG_ID")
PARTNER_BLOG_IDS = os.environ.get("PARTNER_BLOG_IDS", "")  # Comma-separated: "id1,id2,id3"

# Blogger OAuth2 Credentials
BLOGGER_CLIENT_ID = os.environ.get("BLOGGER_CLIENT_ID")
BLOGGER_CLIENT_SECRET = os.environ.get("BLOGGER_CLIENT_SECRET")
BLOGGER_REFRESH_TOKEN = os.environ.get("BLOGGER_REFRESH_TOKEN")

UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY")
AMAZON_LINK = os.environ.get("AMAZON_LINK", "https://amzn.to/4shg6Hn?marker=787950")

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

BLOGGER_URL = "https://trttnews24bd.blogspot.com"
FLIGHTSCOUTPRO_URL = "https://flightscoutpro.blogspot.com"
PWA_URL = "https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/?marker=787950"
VERCEL_HUB_URL = "https://cocvghuj-trtt-news-bot.vercel.app/?marker=787950"

_AFFILIATE_URL_RE = re.compile(
    r"""https?://(?:[a-z0-9-]+\.)*(?:tpo\.lv|amzn\.to|amazon\.[a-z.]+|airhelp\.com|compensair\.com|airalo\.com|drimsim\.com|yesim\.app|yesim\.com|saily\.com|gettransfer\.com|getrentacar\.com|economybookings\.com|qeeq\.com|localrent\.com|kiwitaxi\.com|klook\.com|gocity\.com|tiqets\.com|kkday\.com|intui\.travel|radicalstorage\.com|booking\.com|aviasales\.com)[^\s<>"']*""",
    re.IGNORECASE,
)


def strip_direct_affiliate_links(value: str) -> str:
    text = str(value or "")
    def clean_anchor(match):
        anchor = match.group(0)
        href = re.search(r"""href\s*=\s*["']([^"']+)""", anchor, re.IGNORECASE)
        if href and _AFFILIATE_URL_RE.search(href.group(1)):
            return re.sub(r"""^<a\b[^>]*>|</a>$""", "", anchor, flags=re.IGNORECASE | re.DOTALL)
        return anchor
    text = re.sub(r"""<a\b[^>]*>.*?</a>""", clean_anchor, text, flags=re.IGNORECASE | re.DOTALL)
    return _AFFILIATE_URL_RE.sub("TRTT VoyageHub", text)

HISTORY_FILE = "drafted_history.txt"
HISTORY_MIGRATION_FILE = "history_migration_map.json"

# Core Topics designed for High Google Search Volume & Affiliate Conversion
TOPIC_POOL = [
    {
        "topic": "How to Claim Up to 600€ for Flight Delays in Europe Under EC 261",
        "category": "Passenger Rights",
        "default_labels": ["Flight Compensation", "AirHelp", "EU Regulation 261", "Passenger Rights", "Europe Travel", "FlightScoutPro"]
    },
    {
        "topic": "Best Travel eSIM for Europe 2026: Compare Airalo, Saily, and Unlimited Data",
        "category": "eSIM & Connectivity",
        "default_labels": ["eSIM", "Airalo", "Saily", "Europe Travel", "Travel Tech", "FlightScoutPro"]
    },
    {
        "topic": "Cheap Flights from Middle East and Gulf to Europe: Top Routing Secrets",
        "category": "Cheap Flights",
        "default_labels": ["Aviasales", "Cheap Flights", "Qatar Airways", "Gulf to Europe", "Flight Hacks", "FlightScoutPro"]
    },
    {
        "topic": "Airport Transfers Without Metered Surprises: Fixed Price Kiwitaxi Guide",
        "category": "Airport Transfers",
        "default_labels": ["Kiwitaxi", "Airport Transfer", "Taxi Booking", "Europe Travel", "Sanluri", "TRTT News 24 BD"]
    },
    {
        "topic": "Schengen Transit Checklist: Flight Safe Power Banks, SIMs and Rights",
        "category": "Travel Logistics",
        "default_labels": ["Schengen Travel", "Flight Essentials", "Amazon Travel", "Transit Guide", "TRTT News 24 BD"]
    },
    {
        "topic": "From Doha to Rome: Real Logistics and Flight Hack Strategies for Diaspora",
        "category": "Diaspora & Expat Travel",
        "default_labels": ["Doha to Rome", "Expat Travel", "Flight Routes", "Sanluri", "Dhaka", "TRTT News 24 BD"]
    },
    {
        "topic": "European Car Rental Secrets: How to Avoid Hidden Insurance Fees with LocalRent",
        "category": "Car Rental",
        "default_labels": ["Car Rental", "LocalRent", "Road Trip", "Italy Travel", "Budget Travel", "TRTT News 24 BD"]
    },
    {
        "topic": "Skip The Line in Rome, Paris, and Barcelona: Complete Museum Pass Guide",
        "category": "Sightseeing & Tours",
        "default_labels": ["Tiqets", "Museum Passes", "Rome Colosseum", "Paris Louvre", "Sightseeing", "TRTT News 24 BD"]
    }
]

def apply_history_migrations(history: List[str], migration_map: dict) -> List[str]:
    """Add explicitly mapped topic keys while preserving every legacy entry."""
    migrated = list(history)
    if not isinstance(migration_map, dict):
        return migrated
    for legacy_key, topic_key in migration_map.items():
        if (
            isinstance(legacy_key, str)
            and legacy_key in history
            and isinstance(topic_key, str)
            and topic_key.strip()
        ):
            normalized_key = topic_key.strip()
            if normalized_key not in migrated:
                migrated.append(normalized_key)
    return migrated


def load_history() -> List[str]:
    if not os.path.exists(HISTORY_FILE):
        history = []
    else:
        with open(HISTORY_FILE, "r", encoding="utf-8") as handle:
            history = [line.strip() for line in handle if line.strip()]

    # Legacy article slugs cannot be reliably matched to topics automatically.
    # Only owner-supplied, explicit mappings are applied; original entries remain untouched.
    if os.path.exists(HISTORY_MIGRATION_FILE):
        try:
            with open(HISTORY_MIGRATION_FILE, "r", encoding="utf-8") as handle:
                migration_map = json.load(handle)
            history = apply_history_migrations(history, migration_map)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"History migration map ignored; legacy history preserved: {exc}")
    return history

def topic_history_key(topic: str) -> str:
    """Use the selected topic's stable slug as its history identifier."""
    return slugify(topic)


def topic_draft_marker(topic_key: str) -> str:
    """Build an invisible, deterministic marker for recovering a draft by topic."""
    normalized_key = str(topic_key or "").strip()
    if not normalized_key:
        raise ValueError("Topic key is required for a draft recovery marker.")
    digest = hashlib.sha256(normalized_key.encode("utf-8")).hexdigest()
    return "<!-- trtt-topic-key:" + digest + " -->"


def add_topic_draft_marker(content: str, topic_key: Optional[str]) -> str:
    """Attach the recovery marker to Blogger HTML without changing visible content."""
    if not topic_key:
        return content
    marker = topic_draft_marker(topic_key)
    if marker in content:
        return content
    return content.rstrip() + "\n" + marker + "\n"


def select_next_topic(topic_pool: List[dict], history: List[str]) -> dict:
    """Choose the first topic whose stable topic slug is not in history."""
    if not topic_pool:
        raise ValueError("Topic pool is empty.")
    for candidate in topic_pool:
        if topic_history_key(candidate["topic"]) not in history:
            return candidate
    return topic_pool[0]


def save_history(topic_id: str) -> bool:
    """Atomically record a topic key once; failed writes leave prior history intact."""
    normalized_topic_id = str(topic_id).strip()
    if not normalized_topic_id:
        raise ValueError("Topic history key must not be empty.")

    existing_entries = []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as handle:
            existing_entries = [line.rstrip("\r\n") for line in handle]
    except FileNotFoundError:
        pass

    if normalized_topic_id in {entry.strip() for entry in existing_entries}:
        return False

    if existing_entries and existing_entries[-1] == "":
        existing_entries = existing_entries[:-1]
    updated_history = existing_entries + [normalized_topic_id]
    contents = "\n".join(updated_history) + "\n"
    history_directory = os.path.dirname(os.path.abspath(HISTORY_FILE))
    file_descriptor, temporary_path = tempfile.mkstemp(
        prefix=".drafted_history.",
        suffix=".tmp",
        dir=history_directory,
    )
    try:
        with os.fdopen(file_descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(contents)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, HISTORY_FILE)
    except BaseException:
        try:
            os.close(file_descriptor)
        except OSError:
            pass
        try:
            os.unlink(temporary_path)
        except FileNotFoundError:
            pass
        raise
    return True


def all_blog_targets_accounted_for(blog_outcomes: List[dict]) -> bool:
    """A topic is complete only when every target has a draft or existing duplicate."""
    if not blog_outcomes:
        return False
    return all(
        outcome.get("status") in {"created", "already_exists"}
        and outcome.get("post_id")
        for outcome in blog_outcomes
    )


def record_topic_after_draft(topic: str, blog_outcomes: List[dict]) -> bool:
    """Record a topic only after every configured blog has the article."""
    if not all_blog_targets_accounted_for(blog_outcomes):
        return False
    save_history(topic_history_key(topic))
    return True
# ==============================================================================
# UNSPLASH API: Dynamic Real High-Res Photography
# ==============================================================================
def fetch_unsplash_photo(query: str) -> dict:
    fallback = {
        "url": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=1200&q=80",
        "author": "Photographer attribution unavailable",
        "attribution_status": "Fallback image; attribution not verified",
        "alt": f"Europe travel flight and journey: {query}"
    }
    if not UNSPLASH_ACCESS_KEY:
        return fallback
    try:
        url = "https://api.unsplash.com/photos/random"
        headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
        params = {"query": f"{query} travel", "orientation": "landscape"}
        res = requests.get(url, headers=headers, params=params, timeout=10)
        if res.status_code == 200:
            data = res.json()
            return {
                "url": data["urls"]["regular"],
                "author": data["user"]["name"],
                "attribution_status": "Unsplash",
                "alt": data.get("alt_description") or f"Europe Travel: {query}"
            }
    except Exception as exc:
        print(f"Unsplash API notice: {exc}")
    return fallback

def clean_affiliate_link(base_url: str, partner_name: str) -> str:
    parsed = urlparse(base_url)
    params = dict(parse_qsl(parsed.query))
    params["marker"] = MARKER
    params["sub_id"] = f"blogger_seo_{partner_name}_{MARKER}"
    return urlunparse(parsed._replace(query=urlencode(params)))

def affiliate_service_url(service_id: str) -> str:
    """Resolve Blogger affiliate CTAs from the shared canonical affiliate catalog."""
    service = next(
        (item for item in AFFILIATE_SERVICES if item.get("id") == service_id),
        None,
    )
    if not service:
        raise RuntimeError(
            "Affiliate service is missing from affiliate-services.json: " + service_id
        )
    return clean_affiliate_link(service["url"], service_id)

# ==============================================================================
# ==============================================================================
# AUTONOMOUS EXPERT KNOWLEDGE ENGINE (Zero-Downtime High-Quality Fallback)
# ==============================================================================
def generate_fallback_expert_article(topic_info: dict) -> dict:
    """Generates rich, authentic, high-value E-E-A-T articles with zero API dependence."""
    topic = topic_info["topic"]
    category = topic_info.get("category", "Aviation & Travel Logistics")
    
    if "Passenger Rights" in category or "Claim" in topic or "600" in topic:
        specific_content = """
        <p class="lead" style="font-size: 18px; line-height: 1.7; color: #1e293b; font-weight: 500;">
          Flight disruptions across European airspace are at historic peaks. For passengers flying to, from, or within the European Union, European Regulation (EC) No 261/2004 provides ironclad statutory compensation rights of up to <strong>€600 per passenger</strong>. Yet airlines routinely employ delay tactics and obscure jargon hoping passengers abandon their legal rights.
        </p>

        <h2>1. Statutory Compensation Tiers Under Regulation (EC) No 261/2004</h2>
        <p>Your compensation amount is strictly calculated on distance traveled and the arrival delay at your final ticketed destination:</p>
        <div style="overflow-x: auto; margin: 20px 0;">
          <table style="width: 100%; border-collapse: collapse; font-size: 14.5px; border-radius: 10px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <thead>
              <tr style="background: #0284c7; color: #ffffff; text-align: left;">
                <th style="padding: 12px 16px;">Flight Distance Category</th>
                <th style="padding: 12px 16px;">Delay at Final Destination</th>
                <th style="padding: 12px 16px;">Statutory Cash Payout</th>
              </tr>
            </thead>
            <tbody>
              <tr style="background: #ffffff; border-bottom: 1px solid #e2e8f0;">
                <td style="padding: 12px 16px; font-weight: 600;">Short Haul (Under 1,500 km)</td>
                <td style="padding: 12px 16px;">3+ Hours</td>
                <td style="padding: 12px 16px; color: #0284c7; font-weight: 700;">€250 per passenger</td>
              </tr>
              <tr style="background: #f8fafc; border-bottom: 1px solid #e2e8f0;">
                <td style="padding: 12px 16px; font-weight: 600;">Medium Haul (1,500 km – 3,500 km)</td>
                <td style="padding: 12px 16px;">3+ Hours</td>
                <td style="padding: 12px 16px; color: #0284c7; font-weight: 700;">€400 per passenger</td>
              </tr>
              <tr style="background: #ffffff;">
                <td style="padding: 12px 16px; font-weight: 600;">Long Haul (Over 3,500 km)</td>
                <td style="padding: 12px 16px;">4+ Hours</td>
                <td style="padding: 12px 16px; color: #16a34a; font-weight: 800; font-size: 16px;">€600 per passenger</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h2>2. Mandatory Airline Duty of Care (Right to Care)</h2>
        <p>Independent of monetary compensation, carriers are legally compelled by EC 261 to provide free passenger care while waiting:</p>
        <ul style="padding-left: 20px; color: #334155; line-height: 1.8;">
          <li><strong>Meals and Refreshments:</strong> Reasonable food and beverage vouchers corresponding to the waiting duration.</li>
          <li><strong>Communications:</strong> Free access to two phone calls, telex, fax messages, or emails.</li>
          <li><strong>Hotel Accommodation &amp; Transfers:</strong> If the delayed flight is rescheduled for the following day, the airline must cover hotel lodging and airport ground transport.</li>
        </ul>

        <h2>3. Airline Defenses: Ordinary vs. Extraordinary Circumstances</h2>
        <p>Airlines systematically attempt to claim <em>'extraordinary circumstances'</em> to deny payouts. However, landmark rulings by the European Court of Justice (CJEU) established that:</p>
        <ul style="padding-left: 20px; color: #334155; line-height: 1.8;">
          <li><strong>Technical Failures:</strong> Engine faults, component wear, and unexpected mechanical breakdowns are inherently part of routine airline operations and are <strong>NOT</strong> extraordinary circumstances.</li>
          <li><strong>Crew Shortages &amp; Wildcat Strikes:</strong> Staff sickness, roster mismanagement, and airline internal strikes do not exempt the carrier.</li>
          <li><strong>Legitimate Exemptions:</strong> Only extreme weather rendering runways unusable, political unrest, or general air traffic control (ATC) sector shutdowns constitute legitimate defenses.</li>
        </ul>

        <h2>4. Five-Step Immediate Terminal Checklist</h2>
        <ol style="padding-left: 22px; color: #334155; line-height: 1.8;">
          <li><strong>Secure Written Proof:</strong> Photograph departure flight displays and ask airline gate agents for an official written delay verification slip.</li>
          <li><strong>Retain All Boarding Documents:</strong> Keep paper boarding passes, baggage tags, and e-ticket receipts.</li>
          <li><strong>Decline Waiver Clauses:</strong> Do not sign vouchers that contain release-of-liability wording.</li>
          <li><strong>Track Tail Number:</strong> Use flight tracking apps to check the incoming aircraft's registration and real-time positioning.</li>
          <li><strong>File Your Claim Digitally:</strong> Submit your flight details through certified claims enforcement partners such as AirHelp to bypass airline customer service backlogs.</li>
        </ol>

        <h2>5. Frequently Asked Questions (FAQ)</h2>
        <div style="background: #f1f5f9; border-radius: 12px; padding: 20px; margin-top: 18px;">
          <p style="margin-bottom: 6px;"><strong>Q: Can I claim compensation if my flight was delayed several months ago?</strong></p>
          <p style="margin-bottom: 14px; color: #475569;">A: Claim deadlines differ by country and can depend on the flight, carrier, and applicable law. Check the relevant national authority or obtain legal advice before assuming an older flight is still eligible.</p>
          <p style="margin-bottom: 6px;"><strong>Q: What if I bought my ticket during a flash sale or through an online travel agent?</strong></p>
          <p style="margin-bottom: 14px; color: #475569;">A: The ticket price has zero bearing on your legal entitlement. A €30 budget fare qualifies for the exact same €250 to €600 compensation as a business class ticket.</p>
          <p style="margin-bottom: 6px;"><strong>Q: Do children and infants qualify for compensation?</strong></p>
          <p style="margin-bottom: 0; color: #475569;">A: Any child with an allocated seat has a full claim. Infants traveling on an adult lap at a nominal fee may also qualify depending on ticket conditions.</p>
        </div>
        """
    elif "eSIM" in category or "eSIM" in topic:
        specific_content = """
        <p class="lead" style="font-size: 18px; line-height: 1.7; color: #1e293b; font-weight: 500;">
          International roaming fees remain one of the biggest hidden costs for international travelers. As embedded SIM (eSIM) technology becomes the universal standard across modern smartphones, travelers no longer need to pay exorbitant carrier fees or queue for physical SIM cards at airport kiosks.
        </p>

        <h2>1. eSIM vs. Traditional Physical SIM: Real Travel Advantages</h2>
        <p>An eSIM (embedded SIM) is a digital microchip built directly into your smartphone motherboard. It allows you to download cellular network profiles digitally over Wi-Fi without swapping physical plastic cards:</p>
        <ul style="padding-left: 20px; color: #334155; line-height: 1.8;">
          <li><strong>Instant Multi-Country Switching:</strong> Seamlessly cross European borders without losing connectivity or incurring roaming shock.</li>
          <li><strong>Keep Your Primary Number Active:</strong> Retain your domestic SIM for bank two-factor authentication (2FA) SMS while using the eSIM for affordable high-speed 5G data.</li>
          <li><strong>Zero Physical Kiosk Lines:</strong> Avoid airport terminal queues, language barriers, and passport scans in foreign cities.</li>
        </ul>

        <h2>2. Leading Global Providers Compared: Airalo vs. Saily</h2>
        <div style="overflow-x: auto; margin: 20px 0;">
          <table style="width: 100%; border-collapse: collapse; font-size: 14.5px; border-radius: 10px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
            <thead>
              <tr style="background: #0284c7; color: #ffffff; text-align: left;">
                <th style="padding: 12px 16px;">Provider</th>
                <th style="padding: 12px 16px;">Network Coverage</th>
                <th style="padding: 12px 16px;">Top Features</th>
              </tr>
            </thead>
            <tbody>
              <tr style="background: #ffffff; border-bottom: 1px solid #e2e8f0;">
                <td style="padding: 12px 16px; font-weight: 700;">Airalo (Eurolink)</td>
                <td style="padding: 12px 16px;">39+ European Nations</td>
                <td style="padding: 12px 16px; color: #0284c7; font-weight: 600;">Pioneer platform, flexible 1GB to 20GB bundles, instant in-app top up.</td>
              </tr>
              <tr style="background: #f8fafc;">
                <td style="padding: 12px 16px; font-weight: 700;">Saily (Nord Security)</td>
                <td style="padding: 12px 16px;">150+ Global Destinations</td>
                <td style="padding: 12px 16px; color: #0284c7; font-weight: 600;">Built-in cybersecurity layer, automatic local carrier handover, competitive rates.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <h2>3. Step-by-Step Pre-Flight eSIM Installation Guide</h2>
        <ol style="padding-left: 22px; color: #334155; line-height: 1.8;">
          <li><strong>Verify Device Compatibility:</strong> Ensure your phone is network-unlocked and supports eSIM (iPhone XS and newer, Google Pixel 3 and newer, Samsung Galaxy S20 and newer).</li>
          <li><strong>Install Profile via QR Code:</strong> Complete purchase on Airalo before departure and scan the QR code under <em>Settings &gt; Cellular &gt; Add eSIM</em>.</li>
          <li><strong>Label Your Cellular Plans:</strong> Name your primary carrier "Home" and the travel profile "Travel Data".</li>
          <li><strong>Enable Data Roaming on Travel Line:</strong> Ensure Data Roaming is turned ON for your travel eSIM, but OFF for your domestic home line to prevent carrier charges.</li>
        </ol>

        <h2>4. Frequently Asked Questions (FAQ)</h2>
        <div style="background: #f1f5f9; border-radius: 12px; padding: 20px; margin-top: 18px;">
          <p style="margin-bottom: 6px;"><strong>Q: Can I still receive WhatsApp and Telegram calls?</strong></p>
          <p style="margin-bottom: 14px; color: #475569;">A: Yes! Your messaging apps remain linked to your existing telephone number while utilizing high-speed data from the eSIM.</p>
          <p style="margin-bottom: 6px;"><strong>Q: What happens when my data bundle expires?</strong></p>
          <p style="margin-bottom: 0; color: #475569;">A: You receive an instant push notification at 80% and 100% usage, allowing 1-click in-app top-up without re-scanning or reinstalling.</p>
        </div>
        """
    else:
        specific_content = """
        <p class="lead" style="font-size: 18px; line-height: 1.7; color: #1e293b; font-weight: 500;">
          International travel demands meticulous logistical coordination, smart cost mitigation, and up-to-the-minute field intelligence. Whether orchestrating long-haul transit or booking airport ground transfers, leveraging proven strategies ensures frictionless journeys across international destinations.
        </p>

        <h2>1. Strategic Route Optimization &amp; Fare Intelligence</h2>
        <p>Flight pricing algorithms fluctuate continuously based on demand patterns, fuel hedging, and hub capacity. By utilizing meta-search aggregators such as Aviasales, travelers can uncover hidden stopovers, open-jaw combinations, and regional low-cost carrier legs that standard airline engines conceal.</p>
        
        <h2>2. Fixed-Rate Ground Logistics &amp; Airport Transfers</h2>
        <p>Arriving at an unfamiliar airport terminal often exposes travelers to unmetered taxi negotiations and surge pricing. Booking verified ground transfers via services like Kiwitaxi secures guaranteed fixed rates, terminal meet-and-greet services, and monitored flight arrivals with complimentary waiting windows.</p>

        <h2>3. Transit Security, Power Reserves &amp; Tech Essentials</h2>
        <p>Maintaining device uptime during extended layovers is essential. Always carry an airline-compliant power bank (under 100Wh to satisfy IATA passenger safety regulations) in your carry-on luggage—never in checked baggage—and keep digital copies of transit visas securely backed up.</p>

        <h2>4. Step-by-Step Travel Day Blueprint</h2>
        <ol style="padding-left: 22px; color: #334155; line-height: 1.8;">
          <li><strong>Audit Passport Validity:</strong> Ensure at least 6 months validity from departure and 3 months beyond intended Schengen departure.</li>
          <li><strong>Pre-Book High-Priority Services:</strong> Lock in ground transfers and travel eSIM profiles 48 hours prior to takeoff.</li>
          <li><strong>Monitor Operational Gate Feeds:</strong> Track your aircraft inbound trajectory using real-time radar applications.</li>
          <li><strong>Safeguard Claim Rights:</strong> In case of disruptions exceeding 3 hours, immediately record evidence to trigger statutory EC 261 compensation claims.</li>
        </ol>

        <h2>5. Frequently Asked Questions (FAQ)</h2>
        <div style="background: #f1f5f9; border-radius: 12px; padding: 20px; margin-top: 18px;">
          <p style="margin-bottom: 6px;"><strong>Q: What is the optimal window for booking international long-haul flights?</strong></p>
          <p style="margin-bottom: 14px; color: #475569;">A: Industry data indicates that 6 to 10 weeks prior to departure offers the most favorable balance between seat availability and dynamic revenue management pricing.</p>
          <p style="margin-bottom: 6px;"><strong>Q: How do I handle sudden flight rescheduling?</strong></p>
          <p style="margin-bottom: 0; color: #475569;">A: If the reschedule shifts departure by more than 2 hours or arrival by more than 3 hours, you are entitled to a full cash refund or complimentary re-routing to your destination.</p>
        </div>
        """

    meta = {
        "title": topic,
        "search_description": f"Verified field guide on {topic} with official passenger rights, logistics, and booking recommendations.",
        "labels": topic_info["default_labels"],
        "permalink_slug": slugify(topic)
    }

    return {
        "meta": meta,
        "content": specific_content.strip()
    }

# Separate public authorities from commercial providers. Allowlisting is only
# a source-type filter: it does not prove that a page supports a particular claim.
OFFICIAL_SOURCE_DOMAINS = {
    "europa.eu", "eur-lex.europa.eu", "ec.europa.eu", "easa.europa.eu",
    "icao.int", "iata.org", "caa.co.uk", "gov.uk", "faa.gov",
    "transportation.gov", "transport.gov", "enac.gov.it", "mit.gov.it",
    "viaggiaresicuri.it", "travel.state.gov", "canada.ca",
}
PROVIDER_SOURCE_DOMAINS = {
    "airalo.com", "saily.com", "qatarairways.com", "kiwitaxi.com",
    "localrent.com", "tiqets.com",
}
TRUSTED_SOURCE_DOMAINS = OFFICIAL_SOURCE_DOMAINS | PROVIDER_SOURCE_DOMAINS


def _matches_source_domain(url: str, domains: set) -> bool:
    try:
        parsed = urlparse(url.strip())
        host = (parsed.hostname or "").lower().rstrip(".")
        return (
            parsed.scheme.lower() == "https"
            and bool(host)
            and not host.startswith("www.www.")
            and any(host == domain or host.endswith("." + domain) for domain in domains)
        )
    except (AttributeError, TypeError, ValueError):
        return False


def is_official_source_url(url: str) -> bool:
    """Return True only for HTTPS pages on the official/authority domain list."""
    return _matches_source_domain(url, OFFICIAL_SOURCE_DOMAINS)


def is_provider_source_url(url: str) -> bool:
    """Return True only for HTTPS pages on the commercial provider domain list."""
    return _matches_source_domain(url, PROVIDER_SOURCE_DOMAINS)


def is_trusted_source_url(url: str) -> bool:
    """Accept HTTPS URLs from either approved source class."""
    return is_official_source_url(url) or is_provider_source_url(url)


def verify_source_url(url: str, timeout: int = 8) -> bool:
    """Check that a candidate source is reachable and stays on an allowlisted HTTPS domain."""
    if not is_trusted_source_url(url):
        return False
    try:
        response = requests.get(
            url,
            timeout=timeout,
            allow_redirects=True,
            headers={"User-Agent": "TRTTNewsSourceChecker/1.0 (+https://trttnews24bd.blogspot.com/)"},
            stream=True,
        )
        try:
            final_url = getattr(response, "url", url)
            status_code = int(getattr(response, "status_code", 0))
            content_type = str(getattr(response, "headers", {}).get("Content-Type", "")).lower()
            return (
                200 <= status_code < 300
                and is_trusted_source_url(final_url)
                and ("text/html" in content_type or "application/xhtml+xml" in content_type)
            )
        finally:
            close = getattr(response, "close", None)
            if callable(close):
                close()
    except requests.RequestException as exc:
        print(f"Source URL check failed for {url}: {exc}")
        return False
    except (TypeError, ValueError):
        return False


def validate_article_response(text: str) -> dict:
    """Validate AI output before it can become a Blogger draft."""
    # Fail closed: never turn an API outage into an unsourced fallback article.
    if not text:
        raise RuntimeError("No AI provider returned an article. Draft creation aborted; no fallback content will be used.")

    meta_match = re.search(r'\[METADATA\](.*?)\[/METADATA\]', text, re.DOTALL)
    if not meta_match:
        raise RuntimeError("Article is missing the required metadata block. Draft creation aborted.")

    try:
        parsed_meta = json.loads(meta_match.group(1).strip())
    except (TypeError, ValueError) as exc:
        raise RuntimeError("Article metadata is invalid JSON. Draft creation aborted.") from exc

    content_without_meta = text.replace(meta_match.group(0), "").strip()
    evidence_match = re.search(r'\[EVIDENCE\](.*?)\[/EVIDENCE\]', content_without_meta, re.DOTALL)
    if not evidence_match:
        raise RuntimeError("Article is missing its structured evidence ledger. Draft creation aborted.")
    try:
        evidence_data = json.loads(evidence_match.group(1).strip())
    except (TypeError, ValueError) as exc:
        raise RuntimeError("Evidence ledger is invalid JSON. Draft creation aborted.") from exc
    evidence_claims = evidence_data.get("claims") if isinstance(evidence_data, dict) else None
    if not isinstance(evidence_claims, list) or len(evidence_claims) < 2:
        raise RuntimeError("Evidence ledger must contain at least two factual claims. Draft creation aborted.")
    content_html = content_without_meta.replace(evidence_match.group(0), "").strip()
    title_value = str(parsed_meta.get("title", "")).strip()
    description = str(parsed_meta.get("search_description", "")).strip()
    labels = parsed_meta.get("labels")
    permalink = str(parsed_meta.get("permalink_slug", "")).strip()
    if not title_value or not description or not isinstance(labels, list) or not labels or not permalink:
        raise RuntimeError("Article metadata is incomplete. Draft creation aborted.")
    if len(content_html) < 1200:
        raise RuntimeError("Article body is too short for editorial review. Draft creation aborted.")

    source_heading = re.search(r'<h[1-6][^>]*>\s*Sources\s*</h[1-6]>', content_html, re.IGNORECASE)
    if not source_heading:
        raise RuntimeError("Article lacks a Sources section. Draft creation aborted.")
    # Count distinct URLs only inside the Sources section, not affiliate/action-bar links.
    sources_section = content_html[source_heading.end():]
    next_heading = re.search(r'<h[1-6][^>]*>', sources_section, re.IGNORECASE)
    if next_heading:
        sources_section = sources_section[:next_heading.start()]
    source_links = re.findall(r'<a\b[^>]*href\s*=\s*["\'](https?://[^"\']+)["\'][^>]*>', sources_section, re.IGNORECASE)
    distinct_sources = {url.rstrip(".,);") for url in source_links}
    approved_sources = {url for url in distinct_sources if is_trusted_source_url(url)}
    reachable_sources = {url for url in approved_sources if verify_source_url(url)}
    if len(reachable_sources) < 2:
        raise RuntimeError("Sources section must contain at least two reachable HTTPS HTML pages on approved official/provider domains. Draft creation aborted.")
    official_reachable_sources = {url for url in reachable_sources if is_official_source_url(url)}
    if not official_reachable_sources:
        raise RuntimeError("Sources section must include at least one reachable official/government/regulator source. Draft creation aborted.")

    # Ensure the article body actually cites sources listed in its Sources section.
    article_body = content_html[:source_heading.start()]
    inline_links = re.findall(r'<a\b[^>]*href\s*=\s*["\'](https?://[^"\']+)["\'][^>]*>', article_body, re.IGNORECASE)
    inline_sources = {url.rstrip(".,);") for url in inline_links}
    if len(inline_sources.intersection(reachable_sources)) < 2:
        raise RuntimeError("At least two verified Sources URLs must also be cited inline in the article body. Draft creation aborted.")
    if not inline_sources.intersection(official_reachable_sources):
        raise RuntimeError("At least one reachable official/government/regulator source must also be cited inline. Draft creation aborted.")

    # Every evidence-ledger claim must map to reachable URLs that are cited inline.
    for index, item in enumerate(evidence_claims, start=1):
        if not isinstance(item, dict):
            raise RuntimeError(f"Evidence claim {index} is not a JSON object. Draft creation aborted.")
        claim_text = str(item.get("claim", "")).strip()
        claim_urls = item.get("source_urls")
        if len(claim_text) < 20 or not isinstance(claim_urls, list) or not claim_urls:
            raise RuntimeError(f"Evidence claim {index} is incomplete. Draft creation aborted.")
        normalized_claim_urls = {str(url).strip().rstrip(".,);") for url in claim_urls}
        if not normalized_claim_urls.issubset(reachable_sources.intersection(inline_sources)):
            raise RuntimeError(f"Evidence claim {index} references a source not both reachable and cited inline. Draft creation aborted.")

    meta = {
        "title": title_value,
        "search_description": description[:160],
        "labels": [str(label).strip() for label in labels if str(label).strip()],
        "permalink_slug": slugify(permalink)
    }
    if not meta["labels"] or not meta["permalink_slug"]:
        raise RuntimeError("Article labels or permalink are invalid. Draft creation aborted.")

    return {
        "meta": meta,
        "content": content_html
    }

    
# ==============================================================================
# MULTI-LAYER AI & EXPERT ARTICLE GENERATOR (Google E-E-A-T Standards)
# ==============================================================================
def generate_article_with_metadata(topic_info: dict) -> dict:
    topic = topic_info["topic"]
    
    prompt = f"""You are a senior European aviation & travel journalist writing for FlightScoutPro and TRTT News 24 BD.
Generate a comprehensive, authentic, high-value guide for the topic: "{topic}".

EDITORIAL REQUIREMENTS (Google Helpful Content & E-E-A-T Standards):
1. TONE: Human, authoritative, practical, and empathetic. Mention real-world aviation logistics (e.g. EU Regulation 261/2004 claim rules, airline denial tactics, airport hubs, transit hacks) so it sounds like genuine field experience, NOT generic AI fluff.
2. STRUCTURE:
   - Output clean HTML body (use <h2>, <h3>, <ul>, <li>, <p>, <blockquote>, <strong>).
   - Real-world Executive Hook (80-100 words)
   - <h2>Core Passenger Rights & Flight Reality</h2>
   - <h2>Step-by-Step Action Guide</h2>
   - <h2>Airline Traps & Pitfalls to Avoid</h2>
   - <h2>Essential Travel Tech & Checklist</h2>
   - <h2>Frequently Asked Questions</h2> (3 clear, concrete Q&As)
3. Do not invent personal field experience, interviews, quotes, statistics, legal rules, prices, or current events. Clearly distinguish established facts from practical suggestions.
4. Include inline source links beside material factual claims in the article body. Every inline source URL must also appear in the final <h2>Sources</h2> section, and every listed source should support a nearby claim. Include at least one official government/regulator/international-authority source, plus at least one additional relevant primary source (official authority or the directly responsible airline/provider documentation). Commercial provider pages may support claims about that provider's own services or policies, but must never be presented as independent government/regulatory authority. Link only sources you actually relied on; never fabricate URLs. If reliable sources cannot be identified, say so and do not produce a publishable article.
5. Do not claim facts are verified merely because they are generated. Avoid unsupported certainty. Do not present a source as supporting a claim unless you have checked the relevant page.
6. Before the article HTML, output an [EVIDENCE] JSON block with this exact shape:
[EVIDENCE]
{{"claims":[{{"claim":"A concise factual claim from the article","source_urls":["https://official-source.example/page"]}},{{"claim":"Another factual claim","source_urls":["https://official-source.example/other-page"]}}]}}
[/EVIDENCE]
Include at least two material factual claims and map each claim to one or more exact URLs used inline in the article and listed in Sources. Do not mark claims as verified; all claims require human review.
7. Also generate a JSON header block formatted as:
[METADATA]
{{
  "title": "{topic}",
  "search_description": "Clear 150-char Google Search summary for Search Console",
  "labels": ["Tag1", "Tag2", "Tag3", "Tag4", "Tag5"],
  "permalink_slug": "url-friendly-slug-for-blogger"
}}
[/METADATA]
Followed by the complete HTML article."""

    text = None

    # Layer 1: Google Gemini API with cascade across available models
    if GEMINI_API_KEY:
        try:
            client = genai.Client(api_key=GEMINI_API_KEY)
            candidate_models = [
                "gemini-1.5-flash",
                "gemini-2.0-flash",
                "gemini-flash-latest",
                "gemini-2.5-flash-lite",
                "gemini-1.5-pro",
                "gemini-2.5-flash"
            ]
            for model_name in candidate_models:
                try:
                    response = retry_generate_content(client, model_name, prompt)
                    res_text = getattr(response, "text", str(response)).strip()
                    if res_text and len(res_text) > 300:
                        text = res_text
                        print(f"Article successfully generated via Gemini ({model_name})")
                        break
                except Exception as mod_err:
                    print(f"Notice: Gemini {model_name} attempt: {mod_err}")
        except Exception as gem_exc:
            print(f"Gemini client initialization notice: {gem_exc}")

    # Layer 2: OpenRouter API Fallback (if configured in secrets)
    if not text and os.environ.get("OPENROUTER_API_KEY"):
        or_key = os.environ.get("OPENROUTER_API_KEY")
        print("Engaging secondary generation fallback via OpenRouter...")
        for or_model in ["meta-llama/llama-3.1-8b-instruct:free", "google/gemini-flash-1.5", "mistralai/mistral-7b-instruct:free"]:
            try:
                or_resp = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {or_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://trttnews24bd.blogspot.com",
                        "X-Title": "TRTT Enterprise Publisher"
                    },
                    json={
                        "model": or_model,
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.7
                    },
                    timeout=25
                )
                if or_resp.status_code == 200:
                    or_json = or_resp.json()
                    candidates = or_json.get("choices", [])
                    if candidates and candidates[0].get("message", {}).get("content"):
                        text = candidates[0]["message"]["content"].strip()
                        print(f"Article successfully generated via OpenRouter ({or_model})")
                        break
            except Exception as or_err:
                print(f"OpenRouter ({or_model}) attempt notice: {or_err}")

    return validate_article_response(text)

# BLOG PROFILES: TRTT News 24 BD & FlightScoutPro
# ==============================================================================
def get_blog_profile(blog_name: str, blog_id: str) -> dict:
    """Returns tailored branding, author details, and legal links for each blog."""
    name_lower = (blog_name or "").lower()
    id_lower = (blog_id or "").lower()
    
    is_flightscout = (
        (FLIGHTSCOUTPRO_BLOG_ID and blog_id == FLIGHTSCOUTPRO_BLOG_ID)
        or "flightscout" in name_lower
        or "flightscout" in id_lower
    )
    
    if is_flightscout:
        return {
            "id": "flightscoutpro",
            "name": "FlightScoutPro",
            "subtitle": "Aviation Intelligence & Flight Deals Hub",
            "url": FLIGHTSCOUTPRO_URL,
            "author_name": "Muntasir Rahman",
            "author_role": "Owner & Lead Aviation Intelligence Editor",
            "author_location": "Dhaka, Bangladesh",
            "author_email": "muntasirrahaman694@gmail.com",
            "author_phone": "+8801314847336",
            "badge": "✈️ FlightScoutPro Aviation Intelligence • Dhaka &amp; Global",
            "theme_primary": "#0284c7",
            "theme_gradient": "linear-gradient(135deg, #0369a1 0%, #0284c7 100%)",
            "cta_title": "✈️ FlightScoutPro Deal &amp; Compensation Radar",
            "cta_desc": "Search real-time low airfares, claim up to €600 compensation for delayed flights, and get instant eSIM data.",
            "about_url": f"{FLIGHTSCOUTPRO_URL}/p/about-us.html",
            "contact_url": f"{FLIGHTSCOUTPRO_URL}/p/contact-us.html",
            "privacy_url": f"{FLIGHTSCOUTPRO_URL}/p/privacy-policy.html",
            "disclaimer_url": f"{FLIGHTSCOUTPRO_URL}/p/disclaimer.html",
            "footer_tag": "Published by FlightScoutPro • Founded by Muntasir Rahman (Dhaka, Bangladesh)"
        }
    else:
        return {
            "id": "trttnews24bd",
            "name": "TRTT News 24 BD",
            "subtitle": "Global Travel Logistics & Diaspora News Hub",
            "url": BLOGGER_URL,
            "author_name": "Abu Taher",
            "author_role": "Founder, Network Hub &amp; Chief Publishing Bureau",
            "author_location": "Sardinia, Italy",
            "author_email": "engrtaher2017@gmail.com",
            "author_phone": "",
            "badge": "📍 Italy &amp; Bangladesh • TRTT Global Logistics",
            "theme_primary": "#052962",
            "theme_gradient": "linear-gradient(135deg, #052962 0%, #00A8E8 100%)",
            "cta_title": "🛡️ TRTT VoyageHub Super App • 21 Travel Logistics Tools Active",
            "cta_desc": "Compare flights, claim 600€ flight delays, activate 5G eSIMs, and book fixed-price airport rides instantly.",
            "about_url": f"{BLOGGER_URL}/p/about-us.html",
            "contact_url": f"{BLOGGER_URL}/p/contact-us.html",
            "privacy_url": f"{BLOGGER_URL}/p/privacy-policy.html",
            "disclaimer_url": f"{BLOGGER_URL}/p/disclaimer.html",
            "footer_tag": "Published by TRTT News 24 BD &amp; VoyageHub Network • Dedicated to Roksana, Taifa &amp; Tashrif (Sanluri to Dhaka)"
        }

# ==============================================================================
# ENTERPRISE HTML BUILDER (Modern, Clean, Responsive & E-E-A-T Compliant)
# ==============================================================================
def build_enterprise_html(article_data: dict, photo: dict, blog_profile: dict = None) -> str:
    if blog_profile is None:
        blog_profile = get_blog_profile("TRTT News 24 BD", BLOGGER_BLOG_ID or "")
        
    meta = article_data["meta"]
    content = strip_direct_affiliate_links(article_data["content"])
    title = meta["title"]
    search_desc = meta["search_description"]
    tags_str = ", ".join(meta["labels"])
    
    now_iso = datetime.utcnow().isoformat()
    permalink_slug = meta.get("permalink_slug") or slugify(title)
    canonical_url = f"{blog_profile['url']}/{datetime.utcnow():%Y/%m}/{permalink_slug}.html"

    schema_json = {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": title,
        "description": search_desc,
        "image": [photo["url"]],
        "datePublished": now_iso,
        "dateModified": now_iso,
        "author": {
            "@type": "Person",
            "name": blog_profile["author_name"],
            "jobTitle": blog_profile["author_role"],
            "email": blog_profile["author_email"]
        },
        "publisher": {
            "@type": "Organization",
            "name": blog_profile["name"],
            "url": blog_profile["url"],
            "logo": {
                "@type": "ImageObject",
                "url": "https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/trtt-original-logo.jpeg"
            }
        },
        "keywords": tags_str,
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": canonical_url
        }
    }

    phone_html = f" &bull; <span>WhatsApp: <strong>{blog_profile['author_phone']}</strong></span>" if blog_profile.get("author_phone") else ""

    html = f"""<!-- Google Search Console & SEO Meta Header -->
<meta name="description" content="{search_desc}">
<link rel="canonical" href="{canonical_url}">
<!-- Blogger Search Description: {search_desc} -->
<!-- Blogger Custom Permalink: {permalink_slug} -->
<meta name="keywords" content="{tags_str}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{search_desc}">
<meta property="og:image" content="{photo['url']}">
<meta property="og:type" content="article">

<!-- Schema.org Rich Snippet for Instant Google Search Indexing -->
<script type="application/ld+json">
{json.dumps(schema_json, indent=2)}
</script>

<!-- AUTONOMOUS ENTERPRISE STYLING ENGINE (Auto-injected by GitHub Actions Bot) -->
<style>
  .fs-article-wrap {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
    max-width: 840px !important;
    margin: 0 auto !important;
    color: #1e293b !important;
    line-height: 1.8 !important;
    font-size: 16px !important;
    word-break: break-word !important;
  }}
  .fs-article-wrap h1, .fs-article-wrap h2, .fs-article-wrap h3 {{
    color: #0f172a !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em !important;
  }}
  .fs-article-wrap h2 {{
    font-size: 23px !important;
    margin-top: 36px !important;
    margin-bottom: 16px !important;
    padding-bottom: 8px !important;
    border-bottom: 2px solid #e2e8f0 !important;
    color: #0f172a !important;
  }}
  .fs-article-wrap h3 {{
    font-size: 19px !important;
    margin-top: 24px !important;
    margin-bottom: 12px !important;
    color: #1e293b !important;
  }}
  .fs-article-wrap p {{
    margin-bottom: 18px !important;
    color: #334155 !important;
    font-size: 16px !important;
  }}
  .fs-article-wrap ul, .fs-article-wrap ol {{
    padding-left: 24px !important;
    margin-bottom: 20px !important;
  }}
  .fs-article-wrap li {{
    margin-bottom: 8px !important;
    color: #334155 !important;
  }}
  .fs-article-wrap blockquote {{
    border-left: 4px solid {blog_profile['theme_primary']} !important;
    background: #f8fafc !important;
    padding: 16px 20px !important;
    margin: 24px 0 !important;
    border-radius: 0 12px 12px 0 !important;
    font-style: normal !important;
    color: #0f172a !important;
  }}
  /* Contempo & Blogger theme reset */
  .post-body, .entry-content {{
    font-size: 16px !important;
    line-height: 1.8 !important;
    color: #1e293b !important;
  }}
</style>

<div class="fs-article-wrap">

  <!-- Location, Status & Category Badge -->
  <div style="display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 16px; font-size: 12px;">
    <span style="background: #e0f2fe; color: #0369a1; padding: 5px 12px; border-radius: 6px; font-weight: 700;">{blog_profile['badge']}</span>
    <span style="background: #ecfdf5; color: #047857; padding: 5px 12px; border-radius: 6px; font-weight: 700;">Source links checked • Human review required</span>
    <span style="background: #f1f5f9; color: #475569; padding: 5px 12px; border-radius: 6px;">🏷️ {tags_str}</span>
  </div>

  <!-- High-Res Photography with Attribution & Overlay -->
  <div style="position: relative; border-radius: 16px; overflow: hidden; margin-bottom: 24px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.12);">
    <img src="{photo['url']}" alt="{photo['alt']}" style="width: 100%; height: auto; max-height: 440px; object-fit: cover; display: block;" />
    <div style="position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(15,23,42,0.9) 0%, rgba(15,23,42,0.4) 60%, transparent 100%); padding: 14px 20px; color: #ffffff; font-size: 12px;">
      <span>📸 Photography: <strong>{photo['author']}</strong> ({photo.get('attribution_status', 'Attribution not verified')})</span> &bull; <span>Marker {MARKER} Locked</span>
    </div>
  </div>

  <!-- Editorial review notice: no topic-independent factual claims are injected. -->
  <div style="background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 12px; padding: 14px 18px; margin-bottom: 24px; color: #1e40af; font-size: 13px;">
    Source links are checked automatically. Please review the article's factual claims and sources before publication.
  </div>

  <!-- Action Bar: Fast Travel Tools & Partner Access -->
  <div style="background: {blog_profile['theme_gradient']}; color: #ffffff; padding: 20px 24px; border-radius: 14px; margin-bottom: 28px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px; box-shadow: 0 4px 15px rgba(2,132,199,0.18);">
    <div>
      <strong style="font-size: 16px; display: block; margin-bottom: 4px;">{blog_profile['cta_title']}</strong>
      <p style="margin: 0; font-size: 13px; color: #e2e8f0; line-height: 1.5;">{blog_profile['cta_desc']}</p>
    </div>
    <div style="display: flex; gap: 10px; flex-wrap: wrap;">
      <a href="{blog_profile['url']}" style="background: #ffffff; color: {blog_profile['theme_primary']}; font-weight: 800; font-size: 12px; padding: 10px 18px; border-radius: 8px; text-decoration: none; display: inline-block;">
        📰 Latest Feed
      </a>
      <a href="{VERCEL_HUB_URL}" target="_blank" rel="noopener" style="background: #0f172a; color: #ffffff; font-weight: 800; font-size: 12px; padding: 10px 18px; border-radius: 8px; text-decoration: none; display: inline-block;">
        ⚡ Open Fast App
      </a>
      <a href="{VERCEL_HUB_URL}" target="_blank" rel="noopener" style="background: #f59e0b; color: #0f172a; font-weight: 800; font-size: 12px; padding: 10px 18px; border-radius: 8px; text-decoration: none; display: inline-block;">
        🧭 Open TRTT VoyageHub
      </a>
    </div>
  </div>

  <!-- Article Body -->
  <div style="font-size: 16px; color: #334155; line-height: 1.8;">
    {content}
  </div>

  <!-- Blogger gadget: Vercel hub only; no direct affiliate links on the blog -->
  <div style="background:#f8fafc;border:2px solid #e2e8f0;border-radius:16px;padding:22px;margin-top:36px;margin-bottom:30px;">
    <div style="margin-bottom:12px;">
      <h3 style="margin:0 0 8px;font-size:18px;color:#0f172a;font-weight:800;">🧭 TRTT VoyageHub travel tools</h3>
      <p style="margin:0;color:#475569;font-size:13px;line-height:1.6;">Browse the 21 travel programs by category on our hub. This Blogger gadget links to the hub only; it contains no direct affiliate links.</p>
    </div>
    <a href="{VERCEL_HUB_URL}" target="_blank" rel="noopener noreferrer" style="display:inline-block;padding:12px 18px;border-radius:10px;background:#052962;color:#fff;text-decoration:none;font-weight:800;">Open TRTT VoyageHub ↗</a>
  </div>

  <!-- Dedicated Author Card & Google E-E-A-T Transparency -->
  <div style="background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 16px; padding: 22px; margin-top: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
    <div style="display: flex; align-items: center; gap: 16px; flex-wrap: wrap;">
      <div style="width: 58px; height: 58px; border-radius: 50%; background: {blog_profile['theme_primary']}; color: #ffffff; display: flex; align-items: center; justify-content: center; font-size: 22px; font-weight: 900; flex-shrink: 0;">
        {blog_profile['author_name'][0]}
      </div>
      <div style="flex: 1; min-width: 220px;">
        <div style="display: flex; align-items: center; gap: 8px;">
          <strong style="font-size: 16px; color: #0f172a;">{blog_profile['author_name']}</strong>
          <span style="background: #dbeafe; color: #1e40af; font-size: 10px; font-weight: 800; padding: 2px 6px; border-radius: 4px;">EDITORIAL TEAM</span>
        </div>
        <p style="margin: 2px 0 0 0; font-size: 13px; color: #64748b;">{blog_profile['author_role']} &bull; {blog_profile['author_location']}</p>
        <p style="margin: 4px 0 0 0; font-size: 12px; color: #475569;">
          <span>Email: <strong>{blog_profile['author_email']}</strong></span>
          {phone_html}
        </p>
      </div>
    </div>
    
    <!-- Legal & Compliance Links for Google AdSense & Search Essentials -->
    <div style="margin-top: 16px; padding-top: 14px; border-top: 1px solid #e2e8f0; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 10px; font-size: 12px;">
      <div style="display: flex; gap: 14px; flex-wrap: wrap;">
        <a href="{blog_profile['about_url']}" style="color: #0284c7; text-decoration: none; font-weight: 600;">About Us</a>
        <a href="{blog_profile['contact_url']}" style="color: #0284c7; text-decoration: none; font-weight: 600;">Contact Us</a>
        <a href="{blog_profile['privacy_url']}" style="color: #0284c7; text-decoration: none; font-weight: 600;">Privacy Policy</a>
        <a href="{blog_profile['disclaimer_url']}" style="color: #0284c7; text-decoration: none; font-weight: 600;">Disclaimer</a>
      </div>
      <span style="color: #94a3b8; font-size: 11px;">Partner options and any applicable disclosures are shown on TRTT VoyageHub.</span>
    </div>
  </div>

  <!-- Dedicated Family Tribute & Footer Stamp -->
  <div style="text-align: center; margin-top: 24px; font-size: 11px; color: #94a3b8;">
    <p style="margin: 0;">{blog_profile['footer_tag']}</p>
  </div>

</div>"""
    return html

# ==============================================================================
# MULTI-BLOG BROADCASTING VIA OFFICIAL GOOGLE BLOGGER API
# ==============================================================================
def normalize_article_text(value: str) -> str:
    """Normalize HTML/text consistently for conservative duplicate detection."""
    text = html.unescape(value or '')
    text = unicodedata.normalize('NFC', text)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip().lower()
    return unicodedata.normalize('NFC', text)



DUPLICATE_CHECK_PAGE_SIZE = 100
DUPLICATE_CHECK_MAX_PAGES = 10


def find_duplicate_post(service, blog_id, title, content, topic_key=None):
    from scripts.publish_news import find_duplicate_post as scan
    return scan(service, blog_id, title, content, topic_key=topic_key,
                 max_pages=DUPLICATE_CHECK_MAX_PAGES, context=__import__(__name__))


def create_drafts_on_blogs(title, html_content, meta, article_data=None, photo=None, topic=None):
    from scripts.publish_news import create_drafts_on_blogs as create
    return create(title, html_content, meta, article_data=article_data, photo=photo, topic=topic,
                  context=__import__(__name__), credentials_factory=Credentials, builder=build)


# ==============================================================================
# TELEGRAM DISPATCH
# ==============================================================================
def send_draft_notification(title: str, drafts: List[dict], excerpt: str):
    """Send direct Blogger editor links; publication remains a human decision."""
    if not (TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID):
        print("Telegram credentials not configured; draft links are in the workflow log.")
        return
    try:
        clean_excerpt = re.sub(r'<[^>]+>', '', excerpt)[:200]
        lines = ["📝 <b>TRTT: নতুন আর্টিকেল Draft প্রস্তুত</b>", "", "<b>" + title + "</b>", "", clean_excerpt, "", "<b>প্রকাশের আগে তথ্য ও লিংক যাচাই করুন:</b>"]
        for draft in drafts:
            safe_name = re.sub(r'[<>]', '', draft["blog_name"])
            lines.append("✍️ <a href=\"" + draft["edit_url"] + "\">" + safe_name + " — Blogger খুলে Publish করুন</a>")
        lines.extend(["", "Draft স্বয়ংক্রিয়ভাবে প্রকাশিত হয়নি। আপনার অনুমোদন প্রয়োজন।"])
        response = requests.post("https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage", json={"chat_id": TELEGRAM_CHAT_ID, "text": chr(10).join(lines), "parse_mode": "HTML", "disable_web_page_preview": True}, timeout=10)
        response.raise_for_status()
        if not response.json().get("ok"): print("Telegram did not confirm delivery.")
    except Exception as exc:
        print(f"Telegram draft notification notice: {exc}")

def main():
    history = load_history()
    
    # 1. Pick next fresh topic from pool
    selected_topic_info = select_next_topic(TOPIC_POOL, history)
            
    print(f"Selected Topic: {selected_topic_info['topic']}")

    # 2. Fetch real Unsplash Photography
    photo = fetch_unsplash_photo(selected_topic_info["topic"])
    print(f"Fetched Photography: {photo['url']}")

    # 3. Generate article with metadata (Title, Labels, Search Description, Slug, Location)
    article_data = generate_article_with_metadata(selected_topic_info)
    if not article_data:
        raise RuntimeError(
            "Article generation returned no validated content. Draft workflow aborted."
        )

    # 4. Build default Enterprise HTML (used for telegram excerpt and single-target fallbacks)
    default_profile = get_blog_profile("TRTT News 24 BD", BLOGGER_BLOG_ID or "")
    default_html = build_enterprise_html(article_data, photo, default_profile)

    # 5. Create reviewable drafts on configured Blogger network
    created_drafts = create_drafts_on_blogs(
        title=article_data["meta"]["title"],
        html_content=default_html,
        meta=article_data["meta"],
        article_data=article_data,
        photo=photo,
        topic=selected_topic_info["topic"],
    )
    
    successful_blog_outcomes = [
        outcome for outcome in created_drafts
        if outcome.get("status") in {"created", "already_exists"}
    ]
    failed_blog_outcomes = [
        outcome for outcome in created_drafts
        if outcome.get("status") == "failed"
    ]

    if successful_blog_outcomes:
        send_draft_notification(
            article_data["meta"]["title"],
            successful_blog_outcomes,
            article_data["content"][:220],
        )

    if not record_topic_after_draft(selected_topic_info["topic"], created_drafts):
        failure_count = len(failed_blog_outcomes)
        raise RuntimeError(
            "Draft workflow incomplete: "
            + str(failure_count)
            + " target(s) failed or "
            + str(len(created_drafts) - failure_count)
            + " target(s) were not fully confirmed. "
            + "Topic history was not advanced; next run will safely re-check existing drafts."
        )

    newly_created = sum(1 for outcome in successful_blog_outcomes if outcome.get("status") == "created")
    print(
        f"EXECUTION COMPLETE: {newly_created} new Blogger draft(s); "
        "all configured blogs now have the article; awaiting human review."
    )

if __name__ == "__main__":
    main()
