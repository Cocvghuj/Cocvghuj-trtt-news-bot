import os

# --- API KEYS & SECRETS ---
MARKER = os.environ.get("TRAVEL_PAYOUT_MARKER", "787950")
AMAZON = os.environ.get("AMAZON_LINK", "[https://amzn.to/4shg6Hn](https://amzn.to/4shg6Hn)")

BLOGGER_BLOG_ID = os.environ.get("BLOGGER_BLOG_ID")
BLOGGER_CLIENT_ID = os.environ.get("BLOGGER_CLIENT_ID")
BLOGGER_CLIENT_SECRET = os.environ.get("BLOGGER_CLIENT_SECRET")
BLOGGER_REFRESH_TOKEN = os.environ.get("BLOGGER_REFRESH_TOKEN")

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

GMAIL_EMAIL = os.environ.get("GMAIL_EMAIL")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")
CUSTOMER_EMAILS = os.environ.get("CUSTOMER_EMAILS", "")

# --- Dynamic Dynamic Topics ---
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
    {"name": "Aviasales", "url": f"[https://aviasales.tpo.lv/Fb8U9yav?marker=](https://aviasales.tpo.lv/Fb8U9yav?marker=){MARKER}", "type": "Flights", "tag": "Best Price"},
    {"name": "Airalo eSIM", "url": f"[https://airalo.tpo.lv/ZZoQC7Mz?marker=](https://airalo.tpo.lv/ZZoQC7Mz?marker=){MARKER}", "type": "eSIM", "tag": "Top Pick"},
    {"name": "AirHelp", "url": f"[https://airhelp.tpo.lv/3ItXS0E4?marker=](https://airhelp.tpo.lv/3ItXS0E4?marker=){MARKER}", "type": "Compensation", "tag": "Essential"},
    {"name": "Klook", "url": f"[https://klook.tpo.lv/TWKnemhz?marker=](https://klook.tpo.lv/TWKnemhz?marker=){MARKER}", "type": "Tours", "tag": "Discounts"},
    {"name": "GetTransfer", "url": f"[https://gettransfer.tpo.lv/1u8zRU5s?marker=](https://gettransfer.tpo.lv/1u8zRU5s?marker=){MARKER}", "type": "Taxi", "tag": "Fixed Rate"},
    {"name": "Hotels", "url": f"[https://economybookings.tpo.lv/pyHqRiOo?marker=](https://economybookings.tpo.lv/pyHqRiOo?marker=){MARKER}", "type": "Stays", "tag": "Verified"}
]
