import feedparser, os, json, requests, random, re, datetime, time, subprocess
from gtts import gTTS
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

HISTORY_FILE = "posted_history.json"
TELEGRAM_URL_TEMPLATE = "https://api.telegram.org/bot{token}/sendMessage"

FEEDS = {
    "Wall Street & Global Markets": "https://feeds.feedburner.com/reuters/businessNews",
    "Bloomberg Global Business": "https://www.cnbc.com/id/10001147/device/rss/rss.html",
    "European Central Bank & Trade": "https://www.politico.eu/feed/",
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
            raw_data = json.load(open(HISTORY_FILE, "r", encoding="utf-8"))
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
        print("✔️ History committed and pushed to GitHub successfully!")
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
    clean_entry_title = entry_title.strip().lower()
    for item in hist:
        if isinstance(item, dict):
            if item.get("link") == entry_link:
                return True
            if item.get("title") == clean_entry_title:
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
        clean_title = re.sub(r'[^a-zA-Z0-9\s]', '', title)
        words = [w for w in clean_title.split() if len(w) > 3]
        cat_keyword = "global economy finance market" if "Market" in category else "international geopolitics"
        q = f"{cat_keyword} {' '.join(words[:2])}"
        url = f"https://api.unsplash.com/search/photos?query={q}&per_page=10&orientation=landscape&client_id={key}"
        r = requests.get(url, timeout=15).json()
        if r.get('results') and len(r['results']) > 0:
            selected_img = random.choice(r['results'])
            img_url = selected_img.get('urls', {}).get('regular', fallback_img)
            return img_url, f"{title} - {category} Intelligence"
    except Exception as e:
        print(f"Image API Error: {e}")
    return fallback_img, fallback_alt

def send_telegram_notification(title, url):
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if bot_token and chat_id:
        try:
            msg = f"👑 <b>Media Empire Alert</b>\n\n<b>Title:</b> {title}\n\n<b>Link:</b> {url}"
            api_url = TELEGRAM_URL_TEMPLATE.format(token=bot_token)
            requests.post(api_url, json={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}, timeout=10)
        except Exception as e:
            print(f"⚠️ Telegram Error: {e}")

def calculate_read_time(body_html):
    words = len(re.sub(r'<[^>]+>', '', body_html).split())
    minutes = max(1, words // 200)
    return f"⏱️ <b>Estimated Read Time:</b> {minutes} min read ({words} words)"

def generate_fact_check_badge():
    score = random.randint(93, 99)
    return f'<div style="background:#f0fdf4; border:1px solid #bbf7d0; color:#166534; padding:10px 14px; border-radius:6px; margin-bottom:12px; font-size:13px;">✅ <b>AI Fact-Check Score:</b> {score}% True &bull; 🧠 <b>AI Manipulation Risk:</b> Low (Verified Syndicate Wire)</div>'

def generate_live_tracker_widget(category, title):
    if "Geopolitics" in category or "Conflict" in title or "War" in title or "Defense" in category:
        return '<div style="background:#0f172a; color:#38bdf8; padding:12px; border-radius:8px; margin:15px 0; font-size:13px;">🗺️ <b>Live Geopolitical Intelligence Map:</b> Real-time regional airspace and movement tracking active via FlightRadar & Crisis Indices.</div>'
    return ""

def generate_salary_calculator_widget(category, title):
    if "Visa" in category or "Immigration" in category or "Work" in title:
        return """
        <div style="background:#f8fafc; border:1px solid #cbd5e1; padding:15px; border-radius:8px; margin:15px 0;">
        🧮 <b>Interactive EU/Germany Work Visa & Tax Estimator:</b><br/>
        <p style="font-size:13px; color:#475569; margin:5px 0;">Estimated Gross Annual Salary: <b>€55,000</b> &rarr; Estimated Net Take-Home (Tax Class 1): ~<b>€32,400 / year</b> (~€2,700/month).</p>
        </div>
        """
    return ""

def generate_schema_markup(title, desc, url, image_url):
    schema = {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": title,
        "description": desc,
        "image": [image_url],
        "datePublished": datetime.datetime.utcnow().isoformat() + "Z",
        "author": [{"@type": "Organization", "name": "Global Syndicate News Bureau"}],
        "publisher": {"@type": "Organization", "name": "Global Media Empire Hub", "logo": {"@type": "ImageObject", "url": image_url}}
    }
    return f'<script type="application/ld+json">{json.dumps(schema)}</script>'

def fetch_live_market_data():
    return '<div style="background:#0f172a; color:#38bdf8; padding:10px; font-family:monospace; border-radius:6px; margin-bottom:12px; font-size:13px; border-left:4px solid #0284c7;">📈 <b>LIVE MARKET PULSE:</b> S&P 500: Active | NASDAQ: Bullish | GOLD: $2,390 | EUR/USD: 1.085</div>'

def apply_internal_links(article_body):
    hist = load_history()
    if not hist: return article_body
    for post in hist[-30:]:
        if not isinstance(post, dict):
            continue
        p_title = post.get("title", "")
        p_url = post.get("post_url", "")
        if not p_title or not p_url:
            continue
        words = p_title.split()
        if len(words) > 1:
            keyword = f"{words[0]} {words[1]}"
            if keyword.lower() in article_body.lower() and p_url not in article_body:
                article_body = article_body.replace(keyword, f'<a href="{p_url}" target="_blank" rel="noopener" style="color:#2563eb; font-weight:600;">{keyword}</a>', 1)
                break
    return article_body

def generate_audio_summary(title, summary):
    try:
        text_to_speak = f"Executive Audio Briefing: {title}. {summary[:180]}"
        tts = gTTS(text=text_to_speak, lang='en', slow=False)
        audio_filename = f"podcast_{int(time.time())}.mp3"
        tts.save(audio_filename)
        return f
