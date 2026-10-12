import feedparser, os, json, requests, random, re, datetime, time, subprocess, sys
from gtts import gTTS
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

HISTORY_FILE = "posted_history.json"
TELEGRAM_URL_TEMPLATE = "https://api.telegram.org/bot{token}/sendMessage"

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
        
        lower_title = title.lower()
        if "morocco" in lower_title or "afcon" in lower_title:
            q = "morocco flag stadium"
        elif "usa" in lower_title or "h2b" in lower_title:
            q = "usa passport travel work"
        elif "canada" in lower_title or "lmia" in lower_title:
            q = "canada flag passport travel"
        elif "italy" in lower_title or "sanluri" in lower_title:
            q = "italy visa passport travel"
        elif "windborne" in lower_title or "balloon" in lower_title:
            q = "weather balloon sky atmosphere"
        else:
            clean_title = re.sub(r'[^a-zA-Z0-9\s]', '', title)
            words = [w for w in clean_title.split() if len(w) > 3]
            q = f"{category} {' '.join(words[:2])}"

        url = f"https://api.unsplash.com/search/photos?query={q}&per_page=10&orientation=landscape&client_id={key}"
        r = requests.get(url, timeout=15).json()
        if r.get('results') and len(r['results']) > 0:
            selected_img = random.choice(r['results'])
            img_url = selected_img.get('urls', {}).get('regular', fallback_img)
            return img_url, f"{title} - {category} Intelligence"
    except Exception as e:
        print(f"Image API Error: {e}")
    return fallback_img, fallback_alt

def clean_post(content):
    content = content.replace("[...]", "")
    content = content.replace("[…]", "")
    return content

def validate_post(content, title):
    errors = []
    if "[...]" in content or "[…]" in content:
        errors.append("Found [...] - Incomplete content")
    if "actively coordinating responses" in content or "structural changes" in content:
        errors.append("Found banned filler phrase")
    if "critical juncture" in content or "Global Mobility Desk" in content:
        errors.append("Found banned filler phrase")
    if "operational stakeholders" in content or "Silicon Valley Tech Desk" in content:
        errors.append("Found banned filler phrase")
    if "US Passport" in content and "Morocco" in title:
        errors.append("Image Mismatch: Morocco title with US Passport")

    words = len(re.sub(r'<[^>]+>', '', content).split())
    if words < 300:
        errors.append(f"Post too short ({words} words). Minimum required: 300 words.")

    if errors:
        print("❌ POST REJECTED BY VALIDATOR:")
        for e in errors:
            print(f" - {e}")
        sys.exit(1)
    else:
        print("✅ Post is Clean - Ready for AdSense")
        return True

def send_telegram_notification(title, url):
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if bot_token and chat_id:
        try:
            msg = f"👑 <b>Media Empire Alert</b>\n\n<b>Title:</b> {title}\n\n<b>Link:</b> {url}"
            api_url = TELEGRAM_URL_TEMPLATE.format(token=bot_token)
            requests.post(api_url, json={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}, timeout=10)
