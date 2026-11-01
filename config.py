import json
import os
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

# --- API KEYS & SECRETS ---
MARKER = os.environ.get("TRAVEL_PAYOUT_MARKER", "787950")
AMAZON_LINK = os.environ.get("AMAZON_LINK", "https://amzn.to/4shg6Hn")

BLOGGER_BLOG_ID = os.environ.get("BLOGGER_BLOG_ID")
BLOGGER_CLIENT_ID = os.environ.get("BLOGGER_CLIENT_ID")
BLOGGER_CLIENT_SECRET = os.environ.get("BLOGGER_CLIENT_SECRET")
BLOGGER_REFRESH_TOKEN = os.environ.get("BLOGGER_REFRESH_TOKEN")

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

GMAIL_EMAIL = os.environ.get("GMAIL_EMAIL")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")
CUSTOMER_EMAILS = os.environ.get("CUSTOMER_EMAILS", "")

# --- Dynamic Topics ---
TOPICS = [
    {
        "title": "Building a Remote Travel Consulting Business in Europe",
        "cat": "Business & Entrepreneurship",
        "read_time": "6 min read",
        "summary": "Step-by-step framework to launch an EU-compliant consulting agency while traveling."
    },
    {
        "title": "Schengen Travel Blueprint: Low-Cost Routes & Smart Planning",
        "cat": "Destination Strategy",
        "read_time": "8 min read",
        "summary": "Hidden rail networks, budget flight corridors, and visa hacks for 2026."
    },
    {
        "title": "Digital Nomad Productivity: Essential Gadgets & Workflow",
        "cat": "Nomad Lifestyle",
        "read_time": "5 min read",
        "summary": "The ultra-light gear checklist that keeps top creators working seamlessly anywhere."
    }
]

# --- Affiliate Links: single source of truth in affiliate-services.json ---
_catalog_path = Path(__file__).with_name("affiliate-services.json")
with _catalog_path.open(encoding="utf-8") as _catalog_file:
    _affiliate_catalog = json.load(_catalog_file)

def _affiliate_url(service):
    if service["network"] == "amazon-associates":
        return AMAZON_LINK
    parsed = urlparse(service["url"])
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query["marker"] = MARKER
    return urlunparse(parsed._replace(query=urlencode(query)))

AFFILIATE_SERVICES = [
    {
        "id": service["id"],
        "name": service["name"],
        "network": service["network"],
        "category": service["category"],
        "url": _affiliate_url(service),
    }
    for service in _affiliate_catalog["services"]
]
