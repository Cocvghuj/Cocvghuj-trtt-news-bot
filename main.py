import os
import json
import feedparser
import requests
from datetime import datetime
import pytz

print("TRTT News Blogger & Social Bot Starting...")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
WHATSAPP_PHONE = os.environ.get("WHATSAPP_PHONE")
WA_API_KEY = os.environ.get("WA_API_KEY")
BLOGGER_BLOG_ID = os.environ.get("BLOGGER_BLOG_ID")
BLOGGER_ACCESS_TOKEN = os.environ.get("BLOGGER_ACCESS_TOKEN")

if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY পাওয়া যায়নি!")
    exit()

def is_night_time():
    bd_tz = pytz.timezone('Asia/Dhaka')
    current_hour = datetime.now(bd_tz).hour
    if 0 <= current_hour < 6:
        return True
    return False

POSTED_LOG_FILE = "posted.json"
if os.path.exists(POSTED_LOG_FILE):
    try:
        with open(POSTED_LOG_FILE, "r", encoding="utf-8") as f:
            posted_items = json.load(f)
    except:
        posted_items = []
else:
    posted_items = []

RSS_URLS = [
    "https://www.jagonews24.com/rss/technology.xml",
    "https://www.prothomalo.com/feed/bangladesh",
    "https://www.jugantor.com/feed/rss.xml",
    "https://www.dhakapost.com/rss.xml",
    "https://feeds.feedburner.com/bdnews24",
]

BLOCKED_KEYWORDS = ["ধর্ষণ", "ধর্ষিতা", "হত্যা", "খুন", "আত্মহত্যা", "ফাঁসি", "jail", "murder", "rape", "killed", "suicide"]

CATEGORIES_KEYWORDS = {
    "টেক ও গ্যাজেট": ["প্রযুক্তি", "টেক", "মোবাইল", "এআই", "ai", "smartphone", "technology", "tech", "facebook", "google", "apple"],
    "চাকরি": ["চাকরি", "নিয়োগ", "job", "career"],
    "বগুড়া": ["বগুড়া", "bogura", "bogra"],
    "ঢাকা": ["ঢাকা", "dhaka"],
}

def is_blocked(text):
    text_lower = text.lower()
    return any(word.lower() in text_lower for word in BLOCKED_KEYWORDS)

def detect_category(text):
    text_lower = text.lower()
    for cat_name, keywords in CATEGORIES_KEYWORDS.items():
        if any(kw.lower() in text_lower for kw in keywords):
            return cat_name
    return "সাধারণ খবর"

def generate_with_gemini(prompt_text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt_text}]}]}
    try:
        response = requests.post(url, json=payload, timeout=30)
        res_json = response.json()
        if "candidates" in res_json and len(res_json["candidates"]) > 0:
            return res_json["candidates"][0]["content"]["parts"][0]["text"].strip()
        return None
    except Exception as e:
        print(f"Gemini API Exception: {e}")
        return None

def post_to_blogger(title, content, label, original_link):
    if not BLOGGER_BLOG_ID or not BLOGGER_ACCESS_TOKEN:
        print("Blogger credentials missing!")
        return

    url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOGGER_BLOG_ID}/posts"
    headers = {
        "Authorization": f"Bearer {BLOGGER_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    full_html_content = f"{content}<p><br></p><p><b>মূল খবর সূত্র:</b> <a href='{original_link}' target='_blank'>এখানে পড়ুন</a></p>"
    
    payload = {
        "title": title,
        "content": full_html_content,
        "labels": [label, "TRTT NEWS 24 BD"]
    }
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=20)
        if res.status_code == 200:
            print("Blogger post published successfully!")
        else:
            print(f"Blogger posting failed: {res.text}")
    except Exception as e:
        print(f"Blogger exception: {e}")

def send_telegram_update(title, ai_text, link):
    if is_night_time():
        print("Night time (12 AM - 6 AM BD Time): Telegram update skipped.")
        return

    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    
    next_news_link = posted_items[-1] if len(posted_items) >= 1 else "https://trttnews24.blogspot.com"
    message = f"<b>🚨 {title}</b>\n\n{ai_text}\n\n🔗 <b>বিস্তারিত:</b> <a href='{link}'>এখানে পড়ুন</a>\n\n👉 <b>পরবর্তী খবর:</b> <a href='{next_news_link}'>লিংক দেখুন</a>\n\n🌐 <b>TRTT NEWS 24 BD</b>"
    
    tg_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    try:
        res = requests.post(tg_url, json=payload, timeout=15)
        print("Telegram sent successfully!" if res.status_code == 200 else f"Telegram failed: {res.text}")
    except Exception as e:
        print(f"Telegram exception: {e}")

def send_whatsapp_update(title, link):
    if is_night_time():
        print("Night time (12 AM - 6 AM BD Time): WhatsApp update skipped.")
        return

    if not WHATSAPP_PHONE or not WA_API_KEY:
        return
    
    channel_link = "https://whatsapp.com/channel/0029Vb8co9VDeONEz0B5e51M"
    message = f"🔔 *TRTT NEWS 24 BD Update*\n\n📰 *{title}*\n\n🔗 পড়ুন বিস্তারিত: {link}\n\n👉 আমাদের অফিশিয়াল চ্যানেলে যুক্ত থাকুন:\n{channel_link}"
    
    wa_url = f"https://api.callmebot.com/whatsapp.php?phone={WHATSAPP_PHONE}&text={requests.utils.quote(message)}&apikey={WA_API_KEY}"
    try:
        res = requests.get(wa_url, timeout=15)
        if res.status_code == 200:
            print("WhatsApp update sent successfully!")
        else:
            print(f"WhatsApp sending returned status code: {res.status_code}")
    except Exception as e:
        print(f"WhatsApp sending failed: {e}")

# --- Main Logic ---
target_news = None
for rss_url in RSS_URLS:
    try:
        feed = feedparser.parse(rss_url)
        if feed.entries:
            for entry in feed.entries:
                if entry.link not in posted_items:
                    full_text = entry.title + " " + entry.get('summary', '')
                    if not is_blocked(full_text):
                        target_news = entry
                        break
        if target_news:
            break
    except Exception as e:
        print(f"Skip RSS {rss_url}: {e}")

if not target_news:
    print("কোনো নতুন ইতিবাচক খবর পাওয়া যায়নি!")
    exit()

detected_tag = detect_category(target_news.title + " " + target_news.get('summary', ''))
print(f"Found News: {target_news.title} [Tag: {detected_tag}]")

prompt_news = f"""তুমি TRTT NEWS 24 BD এর চিফ নিউজ এডিটর। নিচের খবরটি ১০০% বস্তুনিষ্ঠ এবং সুন্দর ভাষায় ৩ প্যারাগ্রাফে (HTML <p> ট্যাগ ব্যবহার করে) সাজাও। ইতিবাচক ও আকর্ষণীয় করো। ক্যাটাগরি: '{detected_tag}'
Title: {target_news.title}
Summary: {target_news.get('summary', target_news.title)}"""

ai_output = generate_with_gemini(prompt_news) or f"<p>{target_news.get('summary', '')}</p>"

# লগে নতুন লিংক সেভ করা
posted_items.append(target_news.link)
with open(POSTED_LOG_FILE, "w", encoding="utf-8") as f:
    json.dump(posted_items[-500:], f, ensure_ascii=False, indent=2)

# ব্লগে এবং সোশ্যাল মিডিয়ায় আপডেট পাঠানো
post_to_blogger(target_news.title, ai_output, detected_tag, target_news.link)
send_telegram_update(target_news.title, ai_output, target_news.link)
send_whatsapp_update(target_news.title, target_news.link)

print("Process Completed Successfully!")
