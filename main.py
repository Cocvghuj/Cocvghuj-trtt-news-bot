import os
import json
import feedparser
import requests
import datetime
import google.generativeai as genai

print("TRTT Bot Started with Complete Features...")

# 1. API Key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("GEMINI_API_KEY নাই!")
    exit()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# 2. History / Duplicate Check (৫০০ খবরের মেমোরি)
POSTED_LOG_FILE = "posted.json"
if os.path.exists(POSTED_LOG_FILE):
    try:
        with open(POSTED_LOG_FILE, "r", encoding="utf-8") as f:
            posted_items = json.load(f)
    except:
        posted_items = []
else:
    posted_items = []

# 3. RSS URLs (আপনার কাস্টম ফিড, দৈনিক পূর্বকোণ, রয়টার্স, বিবিসি, আল জাজিরা এবং জাতীয় মিডিয়া)
RSS_URLS = [
    "https://rss.app/feeds/_W6uNGIAKwKPBn602.xml", # আপনার মূল কাস্টম ফিড (যেখানে পূর্বকোণ ও অন্যান্য ফিড আছে)
    "http://feeds.bbci.co.uk/bengali/rss.xml",      # BBC Bangla
    "https://www.aljazeera.com/xml/rss/all.xml",    # Al Jazeera
    "https://www.reutersagency.com/feed/?best-regions=middle-east&post_type=best", # Reuters
    "https://www.prothomalo.com/feed/bangladesh",   # Prothom Alo
    "https://www.bd-pratidin.com/rss.xml",          # BD Pratidin
    "https://www.kalbela.com/rss.xml",              # Kalbela
    "https://www.jugantor.com/feed/rss.xml",        # Jugantor
    "https://www.dhakapost.com/rss.xml",            # Dhaka Post
    "https://www.jagonews24.com/rss/rss.xml",        # Jago News 24
    "https://www.banglanews24.com/rss/rss.xml",      # Bangla News 24
    "https://www.prothomalo.com/collection/crime",  # Crime News
]

# --- বিশেষ ফিচার ও ইতিহাস সংক্রান্ত লজিক (ইসলামের ইতিহাস, বঙ্গবন্ধু ও সাপ্তাহিক প্রচ্ছদ) ---
today_str = datetime.datetime.now().strftime("%Y-%m-%d")
day_of_week = datetime.datetime.now().weekday() # ০ = সোমবার, ৪ = শুক্রবার ইত্যাদি

special_content_text = None
special_title = ""

# যদি আজকের ডেটে এই স্পেশাল কন্টেন্ট পোস্ট না হয়ে থাকে
if today_str + "-special" not in posted_items:
    if day_of_week == 4: # শুক্রবার হলে ইসলামের ইতিহাস
        prompt_special = """
        তুমি TRTT NEWS 24 BD এর ইসলামি সেকশনের এডিটর।
        ইসলামের ইতিহাসের একটি গুরুত্বপূর্ণ ও শিক্ষণীয় ঘটনা বা সোনালী যুগের কোনো সত্য ঘটনা নিয়ে সুন্দর একটি আর্টিকেল লেখো।
        তথ্য ১০০% নির্ভুল রাখবে। শিরোনাম বোল্ড করবে, ৩ প্যারাগ্রাফে লিখবে, শেষে সোর্স লিংক দিবে না।
        
        ফরম্যাট:
        🌙 ইসলামের ইতিহাস: [এখানে শিরোনাম দিন]

        বিস্তারিত বিবরণ...

        #TRTT #IslamicHistory #Bangladesh #News
        """
        special_title = "ইসলামের ইতিহাস"
        
    elif day_of_week == 1: # মঙ্গলবার হলে বঙ্গবন্ধুর জীবনী ও ইতিহাস
        prompt_special = """
        তুমি TRTT NEWS 24 BD এর ফিচার এডিটর।
        জাতির পিতা বঙ্গবন্ধু শেখ মুজিবুর রহমানের বর্ণাঢ্য রাজনৈতিক জীবন, সংগ্রাম বা ঐতিহাসিক ভাষণের তাৎপর্য নিয়ে একটি চমৎকার ফিচার লেখো।
        তথ্য ১০০% সত্য ও প্রামাণিক হতে হবে। শিরোনাম বোল্ড করবে, ৩ প্যারাগ্রাফে লিখবে।
        
        ফরম্যাট:
        🇧🇩 ঐতিহাসিক কথা: [এখানে শিরোনাম দিন]

        বিস্তারিত বিবরণ...

        #TRTT #Bangabandhu #History #Bangladesh
        """
        special_title = "বঙ্গবন্ধুর জীবনী"
        
    else: # অন্য দিনগুলোতে সাপ্তাহিক প্রচ্ছদ বা বিশেষ ফিচার
        prompt_special = """
        তুমি TRTT NEWS 24 BD এর সিনিয়র এডিটর।
        সমাজ, সংস্কৃতি বা বর্তমান সময়ের একটি গুরুত্বপূর্ণ জীবনমুখী বিষয় নিয়ে একটি আকর্ষণীয় সাপ্তাহিক প্রচ্ছদ বা ফিচার আর্টিকেল লেখো। শিরোনাম বোল্ড করবে, ৩ প্যারাগ্রাফে লিখবে।
        
        ফরম্যাট:
        ✨ সাপ্তাহিক প্রচ্ছদ: [এখানে শিরোনাম দিন]

        বিস্তারিত বিবরণ...

        #TRTT #Feature #Bangladesh #News
        """
        special_title = "সাপ্তাহিক প্রচ্ছদ"

    try:
        res_spec = model.generate_content(prompt_special)
        special_content_text = res_spec.text.strip()
    except Exception as e:
        print(f"Special Content Gen Error: {e}")

# যদি স্পেশাল কন্টেন্ট জেনারেট হয়, তবে সেটি পোস্ট হবে; না হলে RSS থেকে সাধারণ বা ক্রাইম/আন্তর্জাতিক খবর পোস্ট হবে
if special_content_text:
    final_text = special_content_text
    news_link = "https://trttnews24.blogspot.com"
    print(f"Generated Special Content: {special_title}")
    posted_items.append(today_str + "-special")
else:
    # RSS থেকে সাধারণ খবর ফেচ করা
    all_entries = []
    for url in RSS_URLS:
        try:
            feed = feedparser.parse(url)
            if feed.entries:
                all_entries.extend(feed.entries)
        except Exception as e:
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

        prompt_news = f"""
        তুমি TRTT NEWS 24 BD এর চিফ নিউজ এডিটর।
        নিচের খবরটাকে (তা সে আন্তর্জাতিক, ক্রাইম বা জাতীয় যা-ই হোক) ১০০% সত্য ও বস্তুনিষ্ঠ রেখে সুন্দর করে সাজাও। কোনো অতিরিক্ত তথ্য যোগ করবে না।
        শিরোনাম বোল্ড করবে, ৩ প্যারাগ্রাফে লিখবে, শেষে সোর্স লিংক দিবে না।

        Title: {original_title}
        Summary: {original_summary}
        Link: {news_link}

        ফরম্যাট:
        📰 শিরোনাম

        বিস্তারিত...

        #TRTT #International #Crime #Bangladesh #News
        """
        try:
            response = model.generate_content(prompt_news)
            final_text = response.text.strip()
            posted_items.append(news_link)
        except Exception as e:
            print(f"Gemini Error: {e}")
            exit()
    else:
        print("কোনো নতুন খবর বা কন্টেন্ট নাই")
        exit()

# 4. Post to Facebook & Telegram
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

# Save posted log (৫০০ মেমোরি পর্যন্ত সেভ থাকবে)
with open(POSTED_LOG_FILE, "w", encoding="utf-8") as f:
    json.dump(posted_items[-500:], f, ensure_ascii=False, indent=2)

print("Done - সফলভাবে পোস্ট সম্পন্ন হলো!")
