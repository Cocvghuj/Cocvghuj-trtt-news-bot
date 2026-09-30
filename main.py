import os
import json
import feedparser
import requests
import datetime
import google.generativeai as genai

print("TRTT Bot Started...")

# 1. API Key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("GEMINI_API_KEY নাই!")
    exit()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# 2. History / Duplicate Check
POSTED_LOG_FILE = "posted.json"
if os.path.exists(POSTED_LOG_FILE):
    try:
        with open(POSTED_LOG_FILE, "r", encoding="utf-8") as f:
            posted_items = json.load(f)
    except:
        posted_items = []
else:
    posted_items = []

# 3. RSS URLs (সব ফিড একসাথে)
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

today_str = datetime.datetime.now().strftime("%Y-%m-%d")
day_of_week = datetime.datetime.now().weekday()
special_content_text = None
special_title = ""

# 4. Special Content Logic (ইতিহাস, বঙ্গবন্ধু ও প্রচ্ছদ)
if today_str + "-special" not in posted_items:
    if day_of_week == 4: # শুক্রবার
        prompt_special = """তুমি TRTT NEWS 24 BD এর ইসলামি সেকশনের এডিটর। ইসলামের ইতিহাসের একটি গুরুত্বপূর্ণ ও শিক্ষণীয় ঘটনা নিয়ে সুন্দর একটি আর্টিকেল লেখো। তথ্য ১০০% নির্ভুল রাখবে। ফরম্যাট: 🌙 ইসলামের ইতিহাস: [শিরোনাম] বিস্তারিত... #TRTT #IslamicHistory"""
        special_title = "ইসলামের ইতিহাস"
    elif day_of_week == 1: # মঙ্গলবার
        prompt_special = """তুমি TRTT NEWS 24 BD এর ফিচার এডিটর। বঙ্গবন্ধু শেখ মুজিবুর রহমানের জীবন নিয়ে একটি ফিচার লেখো। তথ্য ১০০% সত্য হতে হবে। ফরম্যাট: 🇧🇩 ঐতিহাসিক কথা: [শিরোনাম] বিস্তারিত... #TRTT #Bangabandhu"""
        special_title = "বঙ্গবন্ধুর জীবনী"
    else:
        prompt_special = """তুমি TRTT NEWS 24 BD এর সিনিয়র এডিটর। সমাজ বা বর্তমান সময়ের গুরুত্বপূর্ণ বিষয় নিয়ে সাপ্তাহিক প্রচ্ছদ লেখো। ফরম্যাট: ✨ সাপ্তাহিক প্রচ্ছদ: [শিরোনাম] বিস্তারিত... #TRTT #Feature"""
        special_title = "সাপ্তাহিক প্রচ্ছদ"
    
    try:
        res_spec = model.generate_content(prompt_special)
        special_content_text = res_spec.text.strip()
    except Exception as e:
        print(f"Special Content Gen Error: {e}")

if special_content_text:
    final_text = special_content_text
    news_link = "https://trttnews24.blogspot.com"
    print(f"Generated Special Content: {special_title}")
    posted_items.append(today_str + "-special")
else:
    # RSS থেকে খবর
    all_entries = []
    for url in RSS_URLS:
        try:
            feed = feedparser.parse(url)
            if feed.entries:
                all_entries.extend(feed.entries)
        except:
            print(f"Skip {url}")

    target_news = None
    if all_entries:
        for entry in all_entries:
            if entry.link not in posted_items:
                target_news = entry
                break
    
    if target_news:
        original_title = target_news.title
        original_summary = target_news.get('summary', original_title)
        news_link = target_news.link
        print(f"Found RSS News: {original_title}")

        prompt_news = f"""তুমি TRTT NEWS 24 BD এর চিফ নিউজ এডিটর। নিচের খবরটাকে ১০০% সত্য রেখে সুন্দর করে সাজাও। কোনো মিথ্যা যোগ করবে না।
Title: {original_title}
Summary: {original_summary}
Link: {news_link}
ফরম্যাট: 📰 শিরোনাম বিস্তারিত... #TRTT #News"""

        try:
            response = model.generate_content(prompt_news)
            final_text = response.text.strip()
            posted_items.append(news_link)
        except Exception as e:
            print(f"Gemini Error: {e}")
            exit()
    else:
        print("কোনো নতুন খবর নাই")
        exit()

# 5. Post to FB & TG
FB_PAGE_ID = os.environ.get("FB_PAGE_ID")
FB_ACCESS_TOKEN = os.environ.get("FB_ACCESS_TOKEN")
if FB_PAGE_ID and FB_ACCESS_TOKEN:
    try:
        fb_url = f"https://graph.facebook.com/{FB_PAGE_ID}/feed"
        r = requests.post(fb_url, data={"message": final_text, "link": news_link, "access_token": FB_ACCESS_TOKEN}, timeout=20)
        print(f"FB: {r.status_code}")
    except Exception as e:
        print(f"FB Error: {e}")

TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID")
if TG_BOT_TOKEN and TG_CHAT_ID:
    try:
        tg_url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
        r = requests.post(tg_url, json={"chat_id": TG_CHAT_ID, "text": final_text + f"\n\n{news_link}"}, timeout=20)
        print(f"TG: {r.status_code}")
    except Exception as e:
        print(f"TG Error: {e}")

with open(POSTED_LOG_FILE, "w", encoding="utf-8") as f:
    json.dump(posted_items[-500:], f, ensure_ascii=False, indent=2)

print("Done - সফলভাবে পোস্ট সম্পন্ন হলো!")
