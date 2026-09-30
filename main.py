import os
import json
import random
import time
import feedparser
import google.generativeai as genai
import requests

# ০. Google Safe Random Delay
delay_seconds = random.randint(0, 1800)
print(f"Google Spam এড়াতে {delay_seconds // 60} মিনিট অপেক্ষা...")
time.sleep(delay_seconds)

# ১. GEMINI AI
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("GEMINI_API_KEY পাওয়া যায়নি!")
    exit()
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ২. Duplicate Check
POSTED_LOG_FILE = "posted.json"
if os.path.exists(POSTED_LOG_FILE):
    with open(POSTED_LOG_FILE, "r", encoding="utf-8") as f:
        try:
            posted_urls = json.load(f)
        except:
            posted_urls = []
else:
    posted_urls = []

# ৩. 10 RSS
RSS_URLS = [
    "https://rss.app/feeds/_W6uNGIAKwKPBn602.xml",
    "https://www.prothomalo.com/feed/bangladesh",
    "https://www.bd-pratidin.com/rss.xml",
    "https://www.kalbela.com/rss.xml",
    "https://www.jugantor.com/feed/rss.xml",
    "https://bangla.bdnews24.com/rss.xml",
    "https://www.dhakapost.com/rss.xml",
    "https://www.jagonews24.com/rss/rss.xml",
    "https://www.banglanews24.com/rss/rss.xml",
    "https://www.ittefaq.com.bd/rss.xml"
]
all_entries = []
for url in RSS_URLS:
    try:
        feed = feedparser.parse(url)
        if feed.entries:
            all_entries.extend(feed.entries)
    except Exception as e:
        print(f"ফিড সমস্যা: {url} -> {e}")

if not all_entries:
    print("কোনো নতুন খবর নাই।")
    exit()

target_news = None
for entry in all_entries:
    if entry.link not in posted_urls:
        target_news = entry
        break

if not target_news:
    print("সব খবর আগেই পোস্ট হয়েছে।")
    exit()

original_title = target_news.title
original_summary = target_news.get('summary', original_title)
news_link = target_news.link

# ৪. Special Filter
special_instruction = ""
full_text = f"{original_title} {original_summary}".lower()
if any(k in full_text for k in ["বঙ্গবন্ধু", "শেখ মুজিব", "জাতির পিতা", "১৫ আগস্ট"]):
    special_instruction = "ধরণ: 'বঙ্গবন্ধু বা ইতিহাস ভিত্তিক'। সর্বোচ্চ শ্রদ্ধা ও নিরপেক্ষতা বজায় রেখে লিখো।"
elif any(k in full_text for k in ["ইসলাম", "রমজান", "হজ", "কোরআন", "হাদিস", "মসজিদ"]):
    special_instruction = "ধরণ: 'ইসলামিক সংবাদ'। সঠিক ও শালীন ইসলামিক পরিভাষা ব্যবহার করো।"
elif any(k in full_text for k in ["তদন্ত", "অনুসন্ধান", "দুর্নীতি", "রিপোর্ট"]):
    special_instruction = "ধরণ: 'ইনভেস্টিগেটিভ'। ডিপ ইনভেস্টিগেটিভ স্টাইলে ৫ দিনের প্রেক্ষাপট সহ লিখো।"
else:
    special_instruction = "ধরণ: 'সাধারণ সংবাদ'। আধুনিক ও বস্তুনিষ্ঠ ভাষায় লিখো।"

# ৫. Master Prompt
prompt = f"""
তুমি TRTT NEWS 24 BD-এর প্রধান বার্তা সম্পাদক। নিচের তথ্য থেকে সম্পূর্ণ নিজস্ব ভাষায় প্রফেশনাল বাংলা নিউজ বানাও।
[বিশেষ নির্দেশনা]: {special_instruction}
[ফরম্যাট]: একটি আকর্ষণীয় হেডলাইন + ৩-৪টি প্যারাগ্রাফ + ৪-৫টি ট্রেন্ডিং হ্যাশট্যাগ
সংবাদ: শিরোনাম: {original_title} বিস্তারিত: {original_summary}
"""

try:
    print(f"AI প্রসেস: {original_title}")
    response = model.generate_content(prompt)
    rewritten_content = response.text
    post_message = f"{rewritten_content}\n\n📌 বিস্তারিত: {news_link}"

    # ৬. Facebook
    fb_page_id = os.environ.get("FB_PAGE_ID")
    fb_token = os.environ.get("FB_ACCESS_TOKEN")
    if fb_page_id and fb_token:
        r = requests.post(f"https://graph.facebook.com/v19.0/{fb_page_id}/feed", data={'message': post_message, 'access_token': fb_token})
        print("Facebook Done!", r.json())

    # ৭. Telegram
    tg_token = os.environ.get("TG_BOT_TOKEN")
    tg_chat_id = os.environ.get("TG_CHAT_ID")
    if tg_token and tg_chat_id:
        r = requests.post(f"https://api.telegram.org/bot{tg_token}/sendMessage", data={'chat_id': tg_chat_id, 'text': post_message})
        print("Telegram Done!", r.json())

    # ৮. WhatsApp (UltraMsg)
    wa_instance_id = os.environ.get("WA_INSTANCE_ID")
    wa_token = os.environ.get("WA_TOKEN")
    wa_to = os.environ.get("WA_TO")
    if wa_instance_id and wa_token and wa_to:
        wa_url = f"https://api.ultramsg.com/{wa_instance_id}/messages/chat"
        payload = {'token': wa_token, 'to': wa_to, 'body': post_message}
        r = requests.post(wa_url, data=payload)
        print("WhatsApp Done!", r.json())

    # ৯. Blogger Draft
    blogger_id = os.environ.get("BLOGGER_BLOG_ID")
    blogger_token = os.environ.get("BLOGGER_TOKEN")
    if blogger_id and blogger_token:
        headers = {"Authorization": f"Bearer {blogger_token}", "Content-Type": "application/json"}
        payload = {
            "title": original_title,
            "content": f"<p>{rewritten_content}</p><p>সোর্স লিংক: <a href='{news_link}'>original source</a></p>",
            "isDraft": True
        }
        r = requests.post(f"https://www.googleapis.com/blogger/v3/blogs/{blogger_id}/posts/", headers=headers, json=payload)
        print("Blogger Done!", r.json())

    # ১০. History / Duplicate Save (try এর ভেতরে)
    posted_urls.append(news_link)
    with open(POSTED_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(posted_urls[-100:], f, ensure_ascii=False, indent=4)
    print("বট সফলভাবে কাজ সম্পন্ন করেছে!")

except Exception as e:
    print(f"এরর: {e}")
