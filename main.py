import os
import json
import feedparser
import requests
import datetime

print("TRTT News Bot Starting...")

# 1. API Keys & Configurations
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
FB_PAGE_ID = os.environ.get("FB_PAGE_ID")
FB_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID")
BLOGGER_ID = os.environ.get("BLOGGER_ID")

if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY পাওয়া যায়নি!")
    exit()

# 2. History / Duplicate Check (posted.json)
POSTED_LOG_FILE = "posted.json"
if os.path.exists(POSTED_LOG_FILE):
    try:
        with open(POSTED_LOG_FILE, "r", encoding="utf-8") as f:
            posted_items = json.load(f)
    except:
        posted_items = []
else:
    posted_items = []

# 3. RSS Feeds List
RSS_URLS = [
    "https://rss.app/feeds/_W6uNGIAKwKPBn602.xml", 
    "http://feeds.bbci.co.uk/bengali/rss.xml",      
    "https://www.aljazeera.com/xml/rss/all.xml",    
    "https://www.prothomalo.com/feed/bangladesh",   
    "https://www.bd-pratidin.com/rss.xml",          
    "https://www.kalbela.com/rss.xml",              
    "https://www.jugantor.com/feed/rss.xml",        
    "https://www.dhakapost.com/rss.xml",            
    "https://www.jagonews24.com/rss/rss.xml",        
    "https://www.banglanews24.com/rss/rss.xml",      
    "https://www.prothomalo.com/collection/crime",  
]

def generate_with_gemini(prompt_text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        res_json = response.json()
        return res_json["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return None

# Fetch RSS News
all_entries = []
for url in RSS_URLS:
    try:
        feed = feedparser.parse(url)
        if feed.entries:
            all_entries.extend(feed.entries)
    except Exception as e:
        print(f"Skip RSS URL: {url}")

target_news = None
if all_entries:
    for entry in all_entries:
        if entry.link not in posted_items:
            target_news = entry
            break

if not target_news:
    print("কোনো নতুন খবর পাওয়া যায়নি!")
    exit()

original_title = target_news.title
original_summary = target_news.get('summary', original_title)
news_link = target_news.link
print(f"Found News: {original_title}")

# Gemini Prompt for Professional News Formatting
prompt_news = f"""
তুমি TRTT NEWS 24 BD এর চিফ নিউজ এডিটর।
নিচের খবরটাকে ১০০% সত্য ও বস্তুনিষ্ঠ রেখে সুন্দর করে সাজাও। 
শিরোনাম বোল্ড করবে, ৩ প্যারাগ্রাফে লিখবে, শেষে কোনো অতিরিক্ত সোর্স লিংক দিবে না।

Title: {original_title}
Summary: {original_summary}
Link: {news_link}

ফরম্যাট:
📰 শিরোনাম এখানে দিন

বিস্তারিত বিবরণ প্রথম প্যারাগ্রাফ...

দ্বিতীয় প্যারাগ্রাফ...

তৃতীয় প্যারাগ্রাফ...

#TRTT #News #Bangladesh
"""

ai_output = generate_with_gemini(prompt_news)
if not ai_output:
    print("Gemini Generation Failed!")
    exit()

# Split AI Output into Title and Body
lines = ai_output.split('\n')
post_title = original_title
post_body = ai_output

for line in lines:
    if "📰" in line or len(line.strip()) > 5:
        post_title = line.replace("📰", "").strip()
        break

# --- Post to Facebook Page ---
if FB_PAGE_ID and FB_ACCESS_TOKEN:
    try:
        fb_url = f"https://graph.facebook.com/{FB_PAGE_ID}/feed"
        payload_fb = {
            "message": ai_output,
            "link": news_link,
            "access_token": FB_ACCESS_TOKEN
        }
        r_fb = requests.post(fb_url, data=payload_fb, timeout=20)
        print(f"Facebook Response: {r_fb.status_code}")
    except Exception as e:
        print(f"FB Error: {e}")
else:
    print("Facebook Secrets missing!")

# --- Post to Telegram Channel ---
if TG_BOT_TOKEN and TG_CHAT_ID:
    try:
        tg_url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
        payload_tg = {
            "chat_id": TG_CHAT_ID,
            "text": ai_output + f"\n\n🔗 বিস্তারিত পড়তে ভিজিট করুন: {news_link}"
        }
        r_tg = requests.post(tg_url, json=payload_tg, timeout=20)
        print(f"Telegram Response: {r_tg.status_code}")
    except Exception as e:
        print(f"TG Error: {e}")
else:
    print("Telegram Secrets missing!")

# Save to posted.json so it won't post the same news again
posted_items.append(news_link)
with open(POSTED_LOG_FILE, "w", encoding="utf-8") as f:
    json.dump(posted_items[-500:], f, ensure_ascii=False, indent=2)

print("All processes completed successfully!")
 
