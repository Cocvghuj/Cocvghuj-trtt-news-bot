import os
import json
import feedparser
import requests
from datetime import datetime
import pytz

print("TRTT News Blogger & Social Bot Starting...")

# --- Configuration & Secrets ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
WHATSAPP_PHONE = os.environ.get("WHATSAPP_PHONE")
WA_API_KEY = os.environ.get("WA_API_KEY")

BLOGGER_BLOG_ID = os.environ.get("BLOGGER_BLOG_ID")
BLOGGER_CLIENT_ID = os.environ.get("BLOGGER_CLIENT_ID")
BLOGGER_CLIENT_SECRET = os.environ.get("BLOGGER_CLIENT_SECRET")
BLOGGER_REFRESH_TOKEN = os.environ.get("BLOGGER_REFRESH_TOKEN")
BLOGGER_ACCESS_TOKEN_OLD = os.environ.get("BLOGGER_ACCESS_TOKEN")

if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY পাওয়া যায়নি!")
    exit()

# --- Blogger Fresh Token Function (NEW FIX) ---
def get_fresh_blogger_token():
    print("Blogger Token Refresh করছি...")
    if not BLOGGER_CLIENT_ID or not BLOGGER_CLIENT_SECRET or not BLOGGER_REFRESH_TOKEN:
        print("Warning: CLIENT_ID/SECRET/REFRESH_TOKEN পাওয়া যায়নি, পুরানো টোকেন ব্যবহার করছি")
        return BLOGGER_ACCESS_TOKEN_OLD
    try:
        url = "https://oauth2.googleapis.com/token"
        data = {
            "client_id": BLOGGER_CLIENT_ID,
            "client_secret": BLOGGER_CLIENT_SECRET,
            "refresh_token": BLOGGER_REFRESH_TOKEN,
            "grant_type": "refresh_token"
        }
        res = requests.post(url, data=data, timeout=20)
        if res.status_code == 200:
            new_token = res.json().get("access_token")
            print("Blogger Token Refresh Successful!")
            return new_token
        else:
            print(f"Token Refresh Fail: {res.text}")
    except Exception as e:
        print(f"Token Error: {e}")
    return BLOGGER_ACCESS_TOKEN_OLD

BLOGGER_ACCESS_TOKEN = get_fresh_blogger_token()

# --- Night Time Check ---
def is_night_time():
    bd_tz = pytz.timezone('Asia/Dhaka')
    current_hour = datetime.now(bd_tz).hour
    if 0 <= current_hour < 6:
        return True
    return False

# --- Posted Log Setup ---
POSTED_LOG_FILE = "posted.json"
if os.path.exists(POSTED_LOG_FILE):
    try:
        with open(POSTED_LOG_FILE, "r", encoding="utf-8") as f:
            posted_items = json.load(f)
    except:
        posted_items = []
else:
    posted_items = []

# --- RSS Feed Sources ---
RSS_URLS = [
    "https://rss.app/feeds/_W6uNGIAKwKPBn602.xml",
    "https://www.prothomalo.com/feed/bangladesh",
    "https://www.jugantor.com/feed/rss.xml",
    "https://www.dhakapost.com/rss.xml",
    "https://www.jagonews24.com/rss/technology.xml"
]

# --- Category Detection ---
def detect_category(text):
    text_lower = text.lower()
    if any(k in text_lower for k in ["খেলা", "ক্রিকেট", "football", "cricket", "sports"]):
        return "Sports"
    elif any(k in text_lower for k in ["টেক", "প্রযুক্তি", "ai", "technology", "mobile"]):
        return "Technology"
    elif any(k in text_lower for k in ["বিনোদেন", "সিনেমা", "actor", "movie", "entertainment"]):
        return "Entertainment"
    else:
        return "Bangladesh"

# --- Gemini AI Rewriting Function ---
def generate_with_gemini(prompt):
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{ "parts": [{"text": prompt}] }]
        }
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            res_json = response.json()
            return res_json['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print(f"Gemini API Error: {e}")
    return None

# --- Blogger Posting Function ---
def post_to_blogger(title, content, category, original_link):
    if not BLOGGER_BLOG_ID or not BLOGGER_ACCESS_TOKEN:
        print("Blogger credentials missing!")
        return False
    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOGGER_BLOG_ID}/posts/"
    headers = {
        "Authorization": f"Bearer {BLOGGER_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    html_content = f"""
    <p>{content}</p>
    <br>
    <p><em>মূল সংবাদ: <a href="{original_link}" target="_blank" rel="nofollow">এখানে পড়ুন</a></em></p>
    """
    payload = {
        "title": title,
        "content": html_content,
        "labels": [category, "TRTT NEWS 24 BD"]
    }
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=20)
        if res.status_code == 200:
            print("Blogger Post Successful!")
            return True
        else:
            print(f"Blogger Post Failed: {res.text}")
    except Exception as e:
        print(f"Blogger Error: {e}")
    return False

# --- Telegram Notification ---
def send_telegram_update(title, link):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    msg = f"🚨 *TRTT NEWS 24 BD Update*\n\n*{title}*\n\n🔗 {link}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}, timeout=15)
    except Exception as e:
        print(f"Telegram error: {e}")

# --- WhatsApp Notification ---
def send_whatsapp_update(title, link):
    if not WHATSAPP_PHONE or not WA_API_KEY:
        return
    msg = f"🚨 *TRTT NEWS 24 BD Update*\n\n*{title}*\n\n🔗 {link}"
    wa_url = f"https://api.callmebot.com/whatsapp.php?phone={WHATSAPP_PHONE}&text={requests.utils.quote(msg)}&apikey={WA_API_KEY}"
    try:
        requests.get(wa_url, timeout=15)
    except Exception as e:
        print(f"WhatsApp error: {e}")

# --- Main Logic ---
target_news = None
for rss_url in RSS_URLS:
    try:
        feed = feedparser.parse(rss_url)
        if feed.entries:
            for entry in feed.entries:
                if entry.link not in posted_items:
                    target_news = entry
                    break
            if target_news:
                break
    except Exception as e:
        print(f"Skip RSS {rss_url}: {e}")

if not target_news:
    print("কোনো নতুন খবর পাওয়া যায়নি!")
    exit()

detected_tag = detect_category(target_news.title)
print(f"Found News: {target_news.title} [Tag: {detected_tag}]")

prompt_news = f"তুমি TRTT NEWS 24 BD এর চিফ নিউজ এডিটর। নিচের খবরটি সুন্দর ও আকর্ষণীয়ভাবে বাংলায় রিরাইট করো, SEO ফ্রেন্ডলি করো:\nTitle: {target_news.title}\nSummary: {target_news.get('summary', target_news.title)}"

ai_output = generate_with_gemini(prompt_news) or f"<p>{target_news.get('summary', target_news.title)}</p>"

# লগ সেভ করা
posted_items.append(target_news.link)
with open(POSTED_LOG_FILE, "w", encoding="utf-8") as f:
    json.dump(posted_items[-500:], f, ensure_ascii=False, indent=2)

# ব্লগে এবং সোশ্যাল মিডিয়ায় আপডেট পাঠানো
post_to_blogger(target_news.title, ai_output, detected_tag, target_news.link)
send_telegram_update(target_news.title, target_news.link)
send_whatsapp_update(target_news.title, target_news.link)

print("Process Completed Successfully!")
