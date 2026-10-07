import os
import random
import json
import sqlite3
import requests
import feedparser
from datetime import datetime
from zoneinfo import ZoneInfo
import telebot
from PIL import Image, ImageDraw, ImageFont
from google import genai

# ================= SECRETS & CONFIG =================
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
BLOGGER_ID = os.getenv("BLOGGER_ID")

BLOGGER_CLIENT_ID = os.getenv("BLOGGER_CLIENT_ID")
BLOGGER_CLIENT_SECRET = os.getenv("BLOGGER_CLIENT_SECRET")
BLOGGER_REFRESH_TOKEN = os.getenv("BLOGGER_REFRESH_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

bot = telebot.TeleBot(TOKEN) if TOKEN else None
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

# ================= DATABASE SETUP (ডুপ্লিকেট রোধ করতে) =================
def init_db():
    conn = sqlite3.connect("posts_history.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posted_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            link TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def is_already_posted(title):
    conn = sqlite3.connect("posts_history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM posted_articles WHERE title = ?", (title,))
    row = cursor.fetchone()
    conn.close()
    return row is not None

def mark_as_posted(title, link):
    try:
        conn = sqlite3.connect("posts_history.db")
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO posted_articles (title, link) VALUES (?, ?)", (title, link))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB Error: {e}")

# ব্যাকআপ ডামি ডাটা
TEST_ARTICLES = [
    {
        "title": "Schengen Work Visa & Tech Career Opportunities in Europe 2026",
        "link": "https://www.euronews.com",
        "summary": "Essential updates regarding European Union work permits, tech careers, and high-demand job sectors for international aspirants."
    }
]

# সব ক্যাটাগরির আরএসএস ফিড
RSS_FEEDS = [
    "https://www.euronews.com/rss",
    "https://feeds.bbci.co.uk/news/world/europe/rss.xml",
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "https://www.euronews.com/travel/rss",
    "https://www.euronews.com/green/rss",
    "https://www.skysports.com/rss/12118"
]

MASTER_FILES = {
    "requirements.txt": "pyTelegramBotAPI\nrequests\nPillow\nfeedparser\ngoogle-genai\n"
}

def self_heal():
    for path, content in MASTER_FILES.items():
        d = os.path.dirname(path)
        if d and not os.path.exists(d):
            os.makedirs(d, exist_ok=True)
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(content.strip() + "\n")

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
                    summary = entry.get('summary', '') or entry.get('description', '') or title
                    # ডাটাবেজ চেক করে ডুপ্লিকেট বাদ দেওয়া হচ্ছে
                    if title and link and not is_already_posted(title):
                        articles.append({'title': title, 'link': link, 'summary': summary})
        except Exception as e:
            print(f"RSS Fetch Error for {url}: {e}")
            
    if not articles:
        articles.extend(TEST_ARTICLES)
    return articles

def enhance_with_gemini(title, original_summary, category):
    if not client:
        return {
            "content": original_summary[:220],
            "focus_keywords": f"{category.lower()}, europe updates, international trends",
            "meta_desc": original_summary[:150]
        }
    try:
        prompt = f"""
        Act as an expert international journalist and career/lifestyle editor focusing on Europe, Schengen aspirants, and global expats.
        Category: {category}
        Task:
        1. Rewrite and expand the following topic into an engaging, professional blog post (180-250 words) in English, tailored for youth, job seekers, expats, and global readers.
        2. Generate 3-4 high-value SEO Focus Keywords.
        3. Write a compelling SEO Meta Description (under 150 characters).
        
        Output format strictly as JSON with keys: "content", "focus_keywords", "meta_desc".
        
        Title: {title}
        Original Content: {original_summary}
        """
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        if response and response.text:
            text = response.text.strip().replace("```json", "").replace("```", "")
            return json.loads(text)
    except Exception as e:
        print(f"Gemini AI Error: {e}")
        
    return {
        "content": original_summary[:220],
        "focus_keywords": "europe updates, global trends, live news",
        "meta_desc": original_summary[:150]
    }

def make_image(title, category):
    try:
        width, height = 1200, 630
        img = Image.new('RGB', (width, height), color=(15, 23, 42))
        d = ImageDraw.Draw(img)
        
        # প্রিমিয়াম ডিজাইন ও বর্ডার
        d.rectangle([(15, 15), (width-15, height-15)], outline=(14, 165, 233), width=6)
        d.rectangle([(50, 50), (480, 105)], fill=(14, 165, 233))
        d.text((70, 68), f"Category: {category}", fill=(255, 255, 255))
        
        display_title = title[:65] + "..." if len(title) > 65 else title
        d.text((60, 260), display_title, fill=(255, 255, 255))
        
        # ব্র্যান্ডিং ওয়াটারমার্ক বা ট্যাগলাইন
        d.text((60, 540), "EUROPE EXPATS & GLOBAL INSIDER | Verified Live Updates", fill=(148, 163, 184))
        
        img.save("final_post.jpg")
        return "final_post.jpg"
    except Exception as e:
        print(f"Image Creation Error: {e}")
        return None

def post_to_blogger(title, content, labels, meta_desc):
    if not BLOGGER_ID or not BLOGGER_REFRESH_TOKEN or not BLOGGER_CLIENT_ID or not BLOGGER_CLIENT_SECRET:
        print("Blogger Error: Missing credentials.")
        return False
        
    try:
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "client_id": BLOGGER_CLIENT_ID,
            "client_secret": BLOGGER_CLIENT_SECRET,
            "refresh_token": BLOGGER_REFRESH_TOKEN,
            "grant_type": "refresh_token"
        }
        token_res = requests.post(token_url, data=token_data, timeout=10)
        access_token = token_res.json().get("access_token")
        
        if not access_token:
            print("Blogger Error: Access token failed.")
            return False

        api_url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOGGER_ID}/posts"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "kind": "blogger#post",
            "title": title,
            "content": content,
            "labels": labels,
            "searchDescription": meta_desc
        }
        
        post_res = requests.post(api_url, headers=headers, json=payload, timeout=10)
        
        if post_res.status_code in [200, 201]:
            print("Successfully posted update to Blogger.")
            return True
        else:
            print(f"Blogger API Error: {post_res.text}")
            return False
            
    except Exception as e:
        print(f"Blogger Error Details: {e}")
        return False

if __name__ == '__main__':
    self_heal()
    init_db()  # ডাটাবেজ ইনিশিয়ালাইজেশন
    
    articles = READ_RSS_FEEDS()
    slot = get_slot()
    
    if articles:
        item = random.choice(articles)
        
        # ডুপ্লিকেট সুরক্ষা ডাবল চেক
        if not is_already_posted(item['title']):
            ai_data = enhance_with_gemini(item['title'], item.get('summary', ''), slot)
            
            clean_desc = ai_data.get("content")
            seo_meta = ai_data.get("meta_desc")
            focus_keys = ai_data.get("focus_keywords")
                
            post_text = f"**{item['title']}**\n\nCategory: {slot}\n\nLink: {item['link']}"
            img_path = make_image(item['title'], slot)
            
            # টেলিগ্রামে নোটিফিকেশন পাঠানো
            if bot and ADMIN_CHAT_ID:
                try:
                    if img_path and os.path.exists(img_path):
                        with open(img_path, 'rb') as img:
                            bot.send_photo(ADMIN_CHAT_ID, img, caption=post_text, parse_mode="Markdown")
                    else:
                        bot.send_message(ADMIN_CHAT_ID, post_text, parse_mode="Markdown")
                except Exception as e:
                    print(f"Telegram Send Error: {e}")
            
            seo_title = item['title']
            seo_labels = [slot, "Schengen Jobs", "Europe Expats", "Crypto", "Tech", "Travel", "Weather", "Football Scores"] + [k.strip() for k in focus_keys.split(',')]
            
            html_content = f"""
            <div style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.8; color: #1e293b; max-width: 800px; margin: 0 auto; padding: 20px; border: 1px solid #e2e8f0; border-radius: 10px; background-color: #ffffff;">
                <h1 style="color: #0f172a; font-size: 28px; font-weight: 700; margin-bottom: 15px; line-height: 1.3;">{seo_title}</h1>
                
                <p style="font-size: 14px; margin-bottom: 25px; color: #64748b; border-bottom: 1px solid #e2e8f0; padding-bottom: 10px;">
                    <em>Category: <b>{slot}</b> | Published: {datetime.now(ZoneInfo("UTC")).strftime('%d %B, %Y, %H:%M UTC')} | Live Editorial Desk</em>
                </p>
                
                <p style="font-size: 16px; margin-bottom: 25px; text-align: justify; color: #334155; background-color: #f8fafc; padding: 20px; border-left: 5px solid #0284c7; border-radius: 0 6px 6px 0;">
                    <strong>Insights & Live Update:</strong> {clean_desc}
                </p>
                
                <div style="margin: 40px 0; text-align: center;">
                    <p style="font-size: 15px; color: #475569; margin-bottom: 15px;">Access complete official data, scores, and verified guidelines via the source link below:</p>
                    <a href="{item['link']}" rel="noopener noreferrer" target="_blank" style="background-color: #0284c7; color: #ffffff; padding: 15px 40px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 17px; display: inline-block; box-shadow: 0 4px 12px rgba(2,132,199,0.25);">
                        Read Full Story on Official Portal ➜
                    </a>
                </div>
                
                <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 30px 0;">
                <p style="font-size: 12px; color: #94a3b8; text-align: center;">
                    Notice: Curated for European residents, expats, and global trending searches. Tags: {', '.join(seo_labels)}
                </p>
            </div>
            """
            
            # ব্লগস্পটে পোস্ট করা এবং ডাটাবেজে এন্ট্রি সেভ করা
            success = post_to_blogger(seo_title, html_content, seo_labels, seo_meta)
            if success:
                mark_as_posted(item['title'], item['link'])
