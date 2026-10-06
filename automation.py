import os, random, json, requests, feedparser
from datetime import datetime
from zoneinfo import ZoneInfo
import telebot
from PIL import Image, ImageDraw

# ===== SECRETS =====
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
FB_PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")# গিটহাব সিক্রেটের সাথে মেলানো হলো
FB_PAGE_ID = os.getenv("FB_PAGE_ID")
BLOGGER_ID = os.getenv("BLOGGER_ID")
bot = telebot.TeleBot(TOKEN) if TOKEN else None

BLOCKED_KEYWORDS = ["সরকারি চাকরি", "নিয়োগ", "NID", "পাসপোর্ট", "অভিজ্ঞতা ছাড়া", "নিয়োগ বিজ্ঞপ্তি সরকারি", "অনলাইন", "police", "সরাসরি"]
RSS_FEEDS = ["https://prothomalo.com", "https://jugantor.com", "https://kalerkantho.com"]
MASTER_FILES = {
    "requirements.txt": "pyTelegramBotAPI\nrequests\nPillow\nfeedparser\nbeautifulsoup4\ngoogle-api-python-client\ngoogle-auth-httplib2\ngoogle-auth-oauthlib\nlxml\n"
}
def self_heal():
    for path, content in MASTER_FILES.items():
        d = os.path.dirname(path)
        if d and not os.path.exists(d): os.makedirs(d, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f: f.write(content.strip()+"\n")
def get_slot():
    h = datetime.now(ZoneInfo("Asia/Dhaka")).hour
    if 7 <= h < 12: return "news"
    elif 12 <= h < 17: return "tech_info"
    else: return "news"

def READ_RSS_FEEDS():
    articles = []
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                title = entry.get('title', '')
                link = entry.get('link', '')
                if title and link and not any(word in title for word in BLOCKED_KEYWORDS):
                    articles.append({'title': title, 'link': link})
        except:
            pass
    return articles

def make_image(title, category):
    try:
        img = Image.new('RGB', (800, 450), color=(28, 28, 30))
        d = ImageDraw.Draw(img)
        d.text((50, 200), title[:50], fill=(255, 255, 255))
        img.save("final_post.jpg")
        return "final_post.jpg"
    except:
        return None

def post_to_facebook(text, image_path=None):
    if not FB_PAGE_ACCESS_TOKEN or not FB_PAGE_ID: return
    url = f"https://facebook.com{FB_PAGE_ID}/photos" if image_path else f"https://facebook.com{FB_PAGE_ID}/feed"
    payload = {'message': text, 'access_token': FB_PAGE_ACCESS_TOKEN}
    try:
        if image_path and os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                requests.post(url, data=payload, files={'source': f})
        else:
            requests.post(url, data=payload)
    except:
        pass

def send_telegram(text, image_path=None):
    if not bot or not ADMIN_CHAT_ID: return
    try:
        if image_path and os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                bot.send_photo(ADMIN_CHAT_ID, f, caption=text)
        else:
            bot.send_message(ADMIN_CHAT_ID, text)
    except:
        pass

def post_to_blogger(title, content):
    if not BLOGGER_ID or not FB_PAGE_ACCESS_TOKEN: return
    # ব্লগারের জন্য পেজ টোকেন বা গুগল ক্লাউড টোকেন ব্যবহার করা হয়
    url = f"https://googleapis.com{BLOGGER_ID}/posts/"
    headers = {"Authorization": f"Bearer {FB_PAGE_ACCESS_TOKEN}"}
    payload = {
        "kind": "blogger#post",
        "title": title,
        "content": content
    }
    try:
        requests.post(url, json=payload, headers=headers)
    except:
        pass

def check_history(url):
    if not os.path.exists("history.txt"): return False
    with open("history.txt", "r", encoding="utf-8") as f:
        return url in f.read()

def save_history(url):
    with open("history.txt", "a", encoding="utf-8") as f:
        f.write(url + "\n")

if __name__ == "__main__":
    self_heal()
    slot = get_slot()
    news_items = READ_RSS_FEEDS()
    
    if news_items:
        for item in news_items:
            if not check_history(item['link']):
                image_path = make_image(item['title'], slot)
                post_text = f"🚨 {item['title']}\n\nবিস্তারিত পড়ুন: {item['link']}"
                
                send_telegram(post_text, image_path)
                post_to_facebook(post_text, image_path)
                
                blogger_content = f"<p>{item['title']}</p><br><a href='{item['link']}'>মূল নিউজ লিংক এখানে</a>"
                post_to_blogger(item['title'], blogger_content)
                
                save_history(item['link'])
                break
