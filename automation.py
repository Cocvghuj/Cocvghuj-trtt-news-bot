import feedparser, os, json, requests, random, re, datetime, time, subprocess, sys
from gtts import gTTS
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

HISTORY_FILE = "posted_history.json"
TELEGRAM_URL_TEMPLATE = "https://api.telegram.org/bot{token}/sendMessage"

HIGH_CPC_TOPICS = [
    "USA H2B Work Permit Visa 2027 for Bangladesh - Salary $3500 + Free Visa",
    "Canada LMIA Work Permit 2027 - Direct Company Apply Link (No Agent)",
    "Italy Seasonal Work Visa 2027 (Decreto Flussi) - Application from Sanluri, Italy",
    "Portugal Work Visa for Bangladeshi 2027 - 90 Days Processing Time",
    "Romania Work Permit for Bangladesh - How to Check Real vs Fake Visa 2027",
    "Malta Work Visa 2027 for Bangladeshi - Hotel Jobs with Free Accommodation",
    "Croatia Work Permit for Bangladeshis 2027 - New Salary Update",
    "How to Apply for Morocco E-Visa for AFCON 2027 from Bangladesh (AEVM Pass)",
    "Mali Suspends US Work Visas - What Bangladeshi Workers Must Know 2027",
    "USA DV Lottery 2027 for Bangladesh - Last Date and Photo Size Guide"
]

FEEDS = {
    "Wall Street & Global Markets": "https://feeds.feedburner.com/reuters/businessNews",
    "Bloomberg Global Business": "https://www.cnbc.com/id/10001147/device/rss/rss.html",
    "European Central Bank & Trade": "https://politico.eu/feed/",
    "Global Geopolitics & EU": "https://www.euronews.com/rss?format=mrss",
    "BBC World Intelligence": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "Schengen & European Visa Hub": "https://www.schengenvisainfo.com/feed/",
    "Global Work Permits & Immigration": "https://visaguide.world/news/feed/",
    "Artificial Intelligence & Future Tech": "https://techcrunch.com/feed/",
    "Silicon Valley Deep Tech": "https://www.wired.com/feed/rss",
    "Global Cyber Security & Defense": "https://thehackernews.com/feeds/posts/default",
    "Global Energy & Green Transition": "https://www.euronews.com/tag/climate-change/rss",
    "International Aviation & Supply Chain": "https://simpleflying.com/feed/"
}

BREAKING_CATEGORIES = [
    "Global Geopolitics & EU", 
    "BBC World Intelligence", 
    "Wall Street & Global Markets",
    "Global Cyber Security & Defense"
]

COUNTRY_LOCATIONS = {
    "italy": {"name": "Milan, Italy", "lat": 45.4642, "lng": 9.1900},
    "germany": {"name": "Berlin, Germany", "lat": 52.5200, "lng": 13.4050},
    "uk": {"name": "London, UK", "lat": 51.5072, "lng": -0.1276},
    "usa": {"name": "New York, USA", "lat": 40.7128, "lng": -74.0060},
    "europe": {"name": "Brussels, Belgium", "lat": 50.8503, "lng": 4.3517},
    "default": {"name": "Milan, Italy", "lat": 45.4642, "lng": 9.1900}
}

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            cleaned_history = []
            for item in raw_data:
                if isinstance(item, dict):
                    cleaned_history.append(item)
                elif isinstance(item, str):
                    cleaned_history.append({"link": "", "title": item.strip().lower(), "date": "", "category": "", "post_url": ""})
            return cleaned_history
        except:
            return []
    return []

def commit_history_to_github():
    try:
        subprocess.run(["git", "config", "--global", "user.name", "GitHub Action Bot"], check=True)
        subprocess.run(["git", "config", "--global", "user.email", "action@github.com"], check=True)
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
        if not status.stdout.strip():
            return
        subprocess.run(["git", "add", HISTORY_FILE], check=True)
        subprocess.run(["git", "commit", "-m", "Auto-update posted history & URLs [skip ci]"], check=True)
        subprocess.run(["git", "push"], check=True)
    except Exception as e:
        print(f"⚠️ Git commit warning: {e}")

def save_history(link, title, category, url=""):
    hist = load_history()
    today_str = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    hist.append({"link": link, "title": title.strip().lower(), "date": today_str, "category": category, "post_url": url})
    hist = hist[-1000:]
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(hist, f, ensure_ascii=False, indent=2)
        commit_history_to_github()
    except Exception as e:
        print(f"⚠️ History save error: {e}")

def is_duplicate(entry_link, entry_title):
    hist = load_history()
    clean_entry_link = entry_link.strip().lower()
    clean_entry_title = re.sub(r'[^a-zA-Z0-9\s]', '', entry_title).strip().lower()
    
    for item in hist:
        if isinstance(item, dict):
            item_link = item.get("link", "").strip().lower()
            item_title = re.sub(r'[^a-zA-Z0-9\s]', '', item.get("title", "")).strip().lower()
            
            if item_link and clean_entry_link and item_link == clean_entry_link:
                return True
            if item_title and clean_entry_title and item_title == clean_entry_title:
                return True
    return False

def get_today_breaking_count():
    hist = load_history()
    today_str = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    count = 0
    for item in hist:
        if isinstance(item, dict):
            if item.get("date") == today_str and item.get("category") in BREAKING_CATEGORIES:
                count += 1
    return count

def get_smart_location(title, category):
    text = (title + " " + category).lower()
    for key, loc in COUNTRY_LOCATIONS.items():
        if key in text and key != "default":
            return loc
    return COUNTRY_LOCATIONS["default"]

def get_featured_image(title, category=""):
    fallback_img = f"https://picsum.photos/seed/{random.randint(1, 10000000)}/800/600"
    fallback_alt = f"{title} - Global News Wire"
    try:
        key = os.environ.get("UNSPLASH_ACCESS_KEY")
        if not key: return fallback_img, fallback_alt
        
        lower_title
