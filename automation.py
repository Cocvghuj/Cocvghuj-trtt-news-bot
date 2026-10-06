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
BLOGGER_ID = os.getenv("BLOGGER_ID")

BLOGGER_CLIENT_ID = os.getenv("BLOGGER_CLIENT_ID")
BLOGGER_CLIENT_SECRET = os.getenv("BLOGGER_CLIENT_SECRET")
BLOGGER_REFRESH_TOKEN = os.getenv("BLOGGER_REFRESH_TOKEN")

bot = telebot.TeleBot(TOKEN) if TOKEN else None

# আপনার রিকোয়েস্ট অনুযায়ী শুধুমাত্র এইキーワードগুলো শিরোনামে থাকলে পোস্ট হবে
JOB_KEYWORDS = ["চাকরি", "নিয়োগ", "বিজ্ঞপ্তি", "পদ", "कर्मসংস্থান", "পরীক্ষা"]
BLOCKED_KEYWORDS = ["অভিযান ছাড়া", "নিরাপত্তা"]

# সবগুলো প্রধান পত্রিকা ও বিডিজবস হাবের সম্পূর্ণ আরএসএস ফিড তালিকা
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
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    
    for url in RSS_FEEDS:
        try:
            response = requests.get(url, headers=headers, timeout=12)
            if response.status_code == 200:
                feed = feedparser.parse(response.content)
                for entry in feed.entries:
                    title = entry.get('title', '')
                    link = entry.get('link', '')
                    
                    if title and link and not any(word in title for word in BLOCKED_KEYWORDS):
                        # সবগুলো পত্রিকার খবরের মধ্যে শুধুমাত্র চাকরির খবর ফিল্টার করা হচ্ছে
                        if any(job_word in title.lower() for job_word in JOB_KEYWORDS):
                            articles.append({'title': title, 'link': link})
        except Exception as e:
            print(f"Feed Fetching Error ({url}): {e}")
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
        print("Blogger Error: Missing operational credentials in Environment Secrets.")
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
        print("Successfully posted to Blogger site.")
        return True
    except Exception as e:
        print(f"Blogger Error Details: {e}")
        return False

def load_posted_data():
    if os.path.exists("posted.json"):
        try:
            with open("posted.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"date": "", "count": 0, "links": []}

def save_posted_data(data):
    try:
        with open("posted.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except:
        pass

if __name__ == '__main__':
    self_heal()
    
    today_str = datetime.now(ZoneInfo("Asia/Dhaka")).strftime("%Y-%m-%d")
    posted_data = load_posted_data()
    
    if posted_data.get("date") != today_str:
        posted_data["date"] = today_str
        posted_data["count"] = 0
    
    if posted_data["count"] >= 6:
        print(f"Daily limit reached! Already posted {posted_data['count']} job articles today ({today_str}). Exiting.")
    else:
        articles = READ_RSS_FEEDS()
        slot = get_slot()
        
        if articles:
            print(f"Total matching job articles fetched across all sources: {len(articles)}")
            
            valid_item = None
            random.shuffle(articles)
            
            for item in articles:
                if item['link'] not in posted_data.get("links", []):
                    valid_item = item
                    break
            
            if valid_item:
                post_text = f"{valid_item['title']}\n\nবিস্তারিত পড়ুন: {valid_item['link']}"
                img_path = make_image(valid_item['title'], slot)
                
                # ফেসবুক সম্পূর্ণ বাদ, শুধু টেলিগ্রামে নিউজ পাঠানো হচ্ছে
                send_telegram_msg(post_text, img_path)
                
                # ব্লগারে অটোমেটিক নিউজ পাঠানো হচ্ছে
                html_content = f"<p>{valid_item['title']}</p><br><a href='{valid_item['link']}'>এখানে ক্লিক করে বিস্তারিত পড়ুন</a>"
                post_to_blogger(valid_item['title'], html_content)
                
                posted_data["links"].append(valid_item['link'])
                posted_data["count"] += 1
                save_posted_data(posted_data)
                print(f"Successfully processed job post #{posted_data['count']} for today.")
            else:
                print("All fetched job articles have already been posted previously.")
        else:
            print("No new job/recruitment articles found in any of the feeds at this moment.")
