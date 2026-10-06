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

# ================= SECRETS =================
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
BLOGGER_ID = os.getenv("BLOGGER_ID")

BLOGGER_CLIENT_ID = os.getenv("BLOGGER_CLIENT_ID")
BLOGGER_CLIENT_SECRET = os.getenv("BLOGGER_CLIENT_SECRET")
BLOGGER_REFRESH_TOKEN = os.getenv("BLOGGER_REFRESH_TOKEN")

bot = telebot.TeleBot(TOKEN) if TOKEN else None

# নেট ডিস্টার্ব করার জন্য আরএসএস ফিডের পাশাপাশি একটি সরাসরি খবরের ডামি ডাটা রাখা হলো
TEST_ARTICLES = [
    {
        "title": "বাংলাদেশে সরকারি ও বেসরকারি চাকরির বিশাল সুযোগ ২০২৬",
        "link": "https://prothomalo.com"
    },
    {
        "title": "আন্তর্জাতিক বাজারে নতুন প্রযুক্তির আবির্ভাব ও অর্থনৈতিক প্রভাব",
        "link": "https://jugantor.com"
    }
]

RSS_FEEDS = [
    "https://prothomalo.com",
    "https://jugantor.com",
    "https://kalerkantho.com",
    "https://ittefaq.com.bd",
    "https://samakal.com",
    "https://dailyjanakantha.com",
    "https://bd-pratidin.com",
    "https://feedspot.com"
]

MASTER_FILES = {
    "requirements.txt": "pyTelegramBotAPI\nrequests\nPillow\nfeedparser\ngoogle-api-python-client\ngoogle-auth-oauthlib\n"
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
    if 7 <= h <= 12:
        return "news"
    elif 12 < h <= 17:
        return "tech_info"
    else:
        return "news"

def READ_RSS_FEEDS():
    articles = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    
    for url in RSS_FEEDS:
        try:
            response = requests.get(url, headers=headers, timeout=12)
            if response.status_code == 200:
                feed = feedparser.parse(response.content)
                for entry in feed.entries:
                    title = entry.get('title', '')
                    link = entry.get('link', '')
                    if title and link:
                        articles.append({'title': title, 'link': link})
        except:
            pass
            
    # যদি কোনো কারণে আরএসএস ফিড সম্পূর্ণ খালি থাকে, তবে টেস্ট আর্টিকেলের ডেটা নেওয়া হবে
    if not articles:
        articles.extend(TEST_ARTICLES)
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

def post_to_blogger(title, content):
    if not BLOGGER_ID or not BLOGGER_REFRESH_TOKEN or not BLOGGER_CLIENT_ID or not BLOGGER_CLIENT_SECRET:
        print("Blogger Error: Missing credentials in GitHub Secrets.")
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
            "kind": "blogger#post",
            "title": title,
            "content": content
        }
        
        # সংশোধন করা ১২৭ নম্বর লাইন (Error 404 সমাধানের জন্য .blogs() যুক্ত করা হয়েছে)
        service.blogs().posts().insert(blogId=str(BLOGGER_ID), body=body).execute()
        print("Successfully posted to Blogger site.")
        return True
    except Exception as e:
        print(f"Blogger Error Details: {e}")
        return False

if __name__ == '__main__':
    self_heal()
    articles = READ_RSS_FEEDS()
    slot = get_slot()
    
    if articles:
        print(f"Total matching articles available for processing: {len(articles)}")
        item = random.choice(articles)
        
        post_text = f"**{item['title']}**\n\nবিভাগ: {slot}\n\nলিঙ্ক: {item['link']}"
        img_path = make_image(item['title'], slot)
        
        # টেলিগ্রামে ডাটা পাঠানো
        send_telegram_msg(post_text, img_path)
        
        # ব্লগারে পোস্টের জন্য কনটেন্ট তৈরি
        html_content = f"<p>{item['title']}</p><br><a href='{item['link']}'>এখানে ক্লিক করে বিস্তারিত পড়ুন</a>"
        post_to_blogger(item['title'], html_content)
