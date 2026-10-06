import os
import random
import json
import requests
import feedparser
from datetime import datetime
from zoneinfo import ZoneInfo
import telebot
from PIL import Image, ImageDraw
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# ===== SECRETS =====
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
FB_PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")
FB_PAGE_ID = os.getenv("FB_PAGE_ID")
BLOGGER_ID = os.getenv("BLOGGER_ID")

# ব্লগার অটোমেটিক টোকেন রিনিউ করার জন্য নতুন ৩টি সিক্রেট
BLOGGER_CLIENT_ID = os.getenv("BLOGGER_CLIENT_ID")
BLOGGER_CLIENT_SECRET = os.getenv("BLOGGER_CLIENT_SECRET")
BLOGGER_REFRESH_TOKEN = os.getenv("BLOGGER_REFRESH_TOKEN")

bot = telebot.TeleBot(TOKEN) if TOKEN else None

BLOCKED_KEYWORDS = ["সরকারি চাকরি", "নিয়োগ", "NID", "পাসপোর্ট", "অভিযান ছাড়া", "নিরাপত্তা"]
RSS_FEEDS = ["https://prothomalo.com", "https://jugantor.com", "https://kalerkantho.com"]
MASTER_FILES = {
    "requirements.txt": "pyTelegramBotAPI\nrequests\nPillow\nfeedparser\ngoogle-api-python-client\ngoogle-auth-oauthlib\ngoogle-auth-httplib2"
}

def self_heal():
    for path, content in MASTER_FILES.items():
        d = os.path.dirname(path)
        if d and not os.path.exists(d): 
            os.makedirs(d, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f: 
            f.write(content.strip() + "\n")

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
    if not FB_PAGE_ACCESS_TOKEN or not FB_PAGE_ID: 
        return
    url = f"https://facebook.com{FB_PAGE_ID}/feed" if not image_path else f"https://facebook.com{FB_PAGE_ID}/photos"
    payload = {'message': text, 'access_token': FB_PAGE_ACCESS_TOKEN}
    try:
        if image_path:
            with open(image_path, 'rb') as img:
                requests.post(url, data=payload, files={'source': img})
        else:
            requests.post(url, data=payload)
    except:
        pass

def send_telegram_msg(text, image_path=None):
    if not bot or not ADMIN_CHAT_ID: 
        return
    try:
        if image_path:
            with open(image_path, 'rb') as img:
                bot.send_photo(ADMIN_CHAT_ID, img, caption=text)
        else:
            bot.send_message(ADMIN_CHAT_ID, text)
    except:
        pass

# রিফ্রেশ টোকেন দিয়ে ব্লগারে পোস্ট করার নতুন ফাংশন
def post_to_blogger(title, content):
    if not BLOGGER_ID or not BLOGGER_REFRESH_TOKEN or not BLOGGER_CLIENT_ID or not BLOGGER_CLIENT_SECRET:
        return False
    try:
        creds = Credentials(
            token=None,
            refresh_token=BLOGGER_REFRESH_TOKEN,
            token_uri="https://googleapis.com",
            client_id=BLOGGER_CLIENT_ID,
            client_secret=BLOGGER_CLIENT_SECRET
        )
        service = build('blogger', 'v3', credentials=creds)
        body = {
            'kind': 'blogger#post',
            'title': title,
            'content': content
        }
        service.posts().insert(blogId=BLOGGER_ID, body=body).execute()
        return True
    except Exception as e:
        print(f"Blogger Error: {e}")
        return False

def check_history(url):
    try:
        if path.exists('history.txt'): 
            return False
        with open('history.txt', 'r', encoding='utf-8') as f:
            return url in f.read()
    except:
        return False

def save_history(url):
    try:
        with open('history.txt', 'a', encoding='utf-8') as f:
            f.write(url + '\n')
    except:
        pass

if __name__ == '__main__':
    self_heal()
    articles = READ_RSS_FEEDS()
    slot = get_slot()
    
    if articles:
        item = random.choice(articles)
        if not check_history(item['link']):
            post_text = f"{item['title']}\n\nবিস্তারিত পড়ুন: {item['link']}"
            img_path = make_image(item['title'], slot)
            
            # ফেসবুক ও টেলিগ্রামে পোস্ট
            post_to_facebook(post_text, img_path)
            send_telegram_msg(post_text, img_path)
            
            # আপনার ব্লগারে অটোমেটিক পোস্ট করার লজিক
            html_content = f"<p>{item['title']}</p><br><a href='{item['link']}'>এখানে ক্লিক করে বিস্তারিত পড়ুন</a>"
            post_to_blogger(item['title'], html_content)
            
            save_history(item['link'])
