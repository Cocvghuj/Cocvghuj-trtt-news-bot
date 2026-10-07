import os
import sqlite3
import textwrap
import feedparser
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
from PIL import Image, ImageDraw, ImageFont
import telebot
from google import genai
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# --- CONFIG ---
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BLOGGER_ID = os.getenv("BLOGGER_ID")

bot = telebot.TeleBot(TOKEN) if TOKEN else None
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

RSS_FEEDS = [
    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "https://www.aljazeera.com/xml/rss/all.xml"
]

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect("posts_history.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS posted (link TEXT PRIMARY KEY)''')
    conn.commit()
    conn.close()

def is_posted(link):
    conn = sqlite3.connect("posts_history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM posted WHERE link = ?", (link,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def mark_as_posted(link):
    conn = sqlite3.connect("posts_history.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO posted (link) VALUES (?)", (link,))
    conn.commit()
    conn.close()

def get_slot():
    h = datetime.now(ZoneInfo("Europe/Berlin")).hour
    if 3 <= h < 6:
        return "Crypto & Market Trends"
    elif 6 <= h < 9:
        return "EU Job Market & Work Visas"
    elif 9 <= h < 12:
        return "Schengen Career & Youth Opportunities"
    elif 12 <= h < 15:
        return "Tech & Gadgets Innovation"
    elif 15 <= h < 18:
        return "European Travel & Tourism"
    elif 18 <= h < 21:
        return "Weather & Climate Reports"
    else:
        return "European Football Live Scores"

def READ_RSS_FEEDS():
    articles = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    for url in RSS_FEEDS:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                feed = feedparser.parse(response.content)
                for entry in feed.entries:
                    title = entry.get('title', '')
                    link = entry.get('link', '')
                    summary = entry.get('summary', '') or title
                    if title and link:
                        articles.append({'title': title, 'link': link, 'summary': summary})
        except Exception as e:
            print(f"Feed Read Error ({url}): {e}")
    return articles

def enhance_with_gemini(title, original_summary, category):
    if not client:
        return original_summary[:300]
    try:
        prompt = f"""
        Act as an expert international news editor.
        Category: {category}
        Task: Rewrite and expand the following news into an engaging, professional article (150-250 words) in English.
        
        Title: {title}
        Original Content: {original_summary}
        """
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        if response and response.text:
            return response.text.strip()
    except Exception as e:
        print(f"Gemini AI Error: {e}")
    return original_summary[:300]

def make_image(title, category):
    try:
        W, H = 1200, 630
        clean = title.encode('ascii', 'ignore').decode('ascii').strip()
        if len(clean) < 5: clean = "Breaking News Update From Europe"
        clean = clean[:90]

        img = Image.new('RGB', (W, H), color=(15, 23, 42))

        if os.path.exists("logo.jpeg"):
            try:
                logo = Image.open("logo.jpeg").convert("RGBA")
                logo = logo.resize((140, 140))
                bg = Image.new("RGBA", (W, H), (15, 23, 42, 255))
                bg.paste(logo, (55, 45), logo)
                img = bg.convert("RGB")
            except: pass

        d = ImageDraw.Draw(img)
        def load_font(sz):
            for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
                if os.path.exists(p):
                    try: return ImageFont.truetype(p, sz)
                    except: pass
            return ImageFont.load_default()

        title_font = load_font(42)
        cat_font = load_font(20)
        brand_font = load_font(18)

        d.rectangle([(215, 60), (550, 105)], fill=(14, 165, 233))
        d.text((230, 70), f"CATEGORY: {category}", fill=(255,255,255), font=cat_font)
        wrapped = textwrap.fill(clean, width=32)
        d.text((60, 220), wrapped, fill=(255,255,255), font=title_font, spacing=12)
        d.text((60, 550), "THIS MOMENT | Verified Live Updates", fill=(148, 163, 184), font=brand_font)
        d.rectangle([(15, 15), (W-15, H-15)], outline=(14, 165, 233), width=5)

        if os.path.exists("final_post.jpg"):
            os.remove("final_post.jpg")

        img.save("final_post.jpg", quality=95)
        return "final_post.jpg"
    except Exception as e:
        print(f"Image Error: {e}")
        return None

def post_to_blogger(title, content, link):
    try:
        creds = None
        token_json = os.getenv("BLOGGER_TOKEN_JSON")
        if token_json:
            creds_data = json.loads(token_json)
            creds = Credentials.from_authorized_user_info(creds_data)
        
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        if creds and BLOGGER_ID:
            service = build('blogger', 'v3', credentials=creds)
            body = {
                "title": title,
                "content": f"<p>{content}</p><p><a href='{link}'>Read original source</a></p>"
            }
            service.posts().insert(blogId=BLOGGER_ID, body=body).execute()
            print("Blogger Post OK")
    except Exception as e:
        print(f"Blogger Error: {e}")

def main():
    init_db()
    category = get_slot()
    print(f"Running for category slot: {category}")
    
    articles = READ_RSS_FEEDS()
    for article in articles:
        link = article['link']
        if is_posted(link):
            continue
        
        title = article['title']
        summary = article['summary']
        
        # Gemini দিয়ে সংবাদ রিরাইট করা
        rewritten_content = enhance_with_gemini(title, summary, category)
        print(f"Rewritten news: {title}")

        # থাম্বনেইল ইমেজ তৈরি
        img_path = make_image(title, category)

        # টেলিগ্রামে পাঠানো
        if bot and CHAT_ID and img_path:
            with open(img_path, 'rb') as photo:
                caption = f"*{category}*\n\n*{title}*\n\n{rewritten_content[:300]}...\n\nSource: {link}\n\n#ThisMoment #Europe"
                bot.send_photo(CHAT_ID, photo, caption=caption, parse_mode="Markdown")
            print("Telegram Sent OK")

        # ব্লগার এআই পোস্ট
        post_to_blogger(title, rewritten_content, link)

        mark_as_posted(link)
        break # প্রতি রান্নায় একটি নতুন আর্টিকেল প্রসেস করবে

if __name__ == "__main__":
    main()
