import os

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

# --- Affiliate Links Master Database ---
AFFILIATE_SERVICES = [
    {"name": "Aviasales", "url": f"https://aviasales.tpo.lv/Fb8U9ay?marker={MARKER}"},
    {"name": "Airalo eSIM", "url": f"https://airalo.tpo.lv/ZZoQC7Mz?marker={MARKER}"},
    {"name": "AirHelp", "url": f"https://airhelp.tpo.lv/3ItXSOE4?marker={MARKER}"},
    {"name": "Klook", "url": f"https://klook.tpo.lv/TWKnenhz?marker={MARKER}"},
    {"name": "GetTransfer", "url": f"https://gettransfer.tpo.lv/1u82RU5s?marker={MARKER}"},
    {"name": "Hotels", "url": f"https://economybookings.tpo.lv/pyHqIOo?marker={MARKER}"},
    {"name": "Amazon Travel Gear", "url": AMAZON_LINK},
]
