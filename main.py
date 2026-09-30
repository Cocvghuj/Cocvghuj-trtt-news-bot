import os
import json
import random
import time
import feedparser
import google.generativeai as genai
import requests

# ==========================================
# ০. গুগলের প্যাটার্ন এড়াতে র‍্যান্ডম ডিলে (০ থেকে ৩০ মিনিট)
# ==========================================
delay_seconds = random.randint(0, 1800)
print(f"গুগল স্প্যাম এড়াতে {delay_seconds // 60} মিনিট অপেক্ষা করা হচ্ছে...")
time.sleep(delay_seconds)

# ==========================================
# ১. GEMINI AI সেটআপ
# ==========================================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("GEMINI_API_KEY পাওয়া যায়নি!")
    exit()

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ==========================================
# ২. ডুপ্লিকেট চেক ফাইল লোড করা
# ==========================================
POSTED_LOG_FILE = "posted.json"

if os.path.exists(POSTED_LOG_FILE):
    with open(POSTED_LOG_FILE, "r") as f:
        try:
            posted_urls = json.load(f)
        except:
            posted_urls = []
else:
    posted_urls = []

# ==========================================
# ৩. ১০টি RSS ফিড থেকে খবর সংগ্রহ ও ফিল্টার
# ==========================================
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
        print(f"ফিড লোড করতে সমস্যা: {url} -> {e}")

if not all_entries:
    print("কোনো নতুন খবর পাওয়া যায়নি।")
    exit()

# ডুপ্লিকেট বাদ দিয়ে প্রথম ইউনিক খবরটি বেছে নেওয়া
target_news = None
for entry in all_entries:
    if entry.link not in posted_urls:
        target_news = entry
        break

if not target_news:
    print("সবগুলো খবর আগেই প্রকাশিত হয়েছে। নতুন কোনো খবর নেই।")
    exit()

original_title = target_news.title
original_summary = target_news.get('summary', original_title)
news_link = target_news.link

# ==========================================
# ৪. স্পেশাল ক্যাটাগরি ফিল্টার
# ==========================================
special_instruction = ""
full_text = f"{original_title} {original_summary}".lower()

if any(k in full_text for k in ["বঙ্গবন্ধু", "শেখ মুজিব", "জাতির পিতা", "১৫ আগস্ট"]):
    special_instruction = "ধরণ: 'বঙ্গবন্ধু বা ইতিহাস ভিত্তিক'। সর্বোচ্চ শ্রদ্ধা, নিরপেক্ষতা ও ঐতিহাসিক সঠিকতা বজায় রেখে রিপোর্ট তৈরি করো।"
elif any(k in full_text for k in ["ইসলাম", "রমজান", "হজ", "কোরআন", "হাদিস", "মসজিদ"]):
    special_instruction = "ধরণ: 'ইসলামিক সংবাদ'। সঠিক ও শালীন ইসলামিক পরিভাষা ব্যবহার করো এবং যেকোনো বিতর্কিত বক্তব্য এড়িয়ে চলো।"
elif any(k in full_text for k in ["তদন্ত", "অনুসন্ধান", "দুর্নীতি", "রিপোর্ট", "ইনভেস্টিগেশন"]):
    special_instruction = "ধরণ: 'ইনভেস্টিগেটিভ / অনুসন্ধানী সংবাদ'। ডিপ ইনভেস্টিগেটিভ স্টাইলে লিখবে এবং খবরের প্রেক্ষাপটসহ গত ৫ দিনের ঘটনার সংক্ষিপ্ত সারসংক্ষেপ বিশ্লেষণ করবে।"
else:
    special_instruction = "ধরণ: 'সাধারণ আন্তর্জাতিক/জাতীয় সংবাদ'। আধুনিক ও বস্তুনিষ্ঠ সংবাদের ভাষায় রিপোর্ট তৈরি করো।"

# ==========================================
# ৫. মাস্টার প্রম্পট
# ==========================================
prompt = f"""
তুমি TRTT NEWS 24 BD-এর প্রধান আন্তর্জাতিক বার্তা সম্পাদক।
নিচের সংবাদের তথ্য বিশ্লেষণ করে সম্পূর্ণ নিজস্ব ভাষায় একটি প্রফেশনাল ও আকর্ষণীয় বাংলা নিউজ রিপোর্ট তৈরি করো।

[বিশেষ নির্দেশনা]:
১. {special_instruction}
২. মূল লেখার কোনো বাক্য হুবহু কপি করবে না, সম্পূর্ণ ইউনিক বাংলা ভাষায় রূপান্তর করবে।

[আউটপুট ফরম্যাট]:
- একটি আকর্ষনীয় হেডলাইন (শিরোনাম)
- মূল খবর নিয়ে ৩ থেকে ৪টি স্পষ্ট প্যারাগ্রাফ
- ইনভেস্টিগেশনের ক্ষেত্রে ৫ দিনের পেছনের ঘটনাবলীর সংক্ষিপ্ত রূপরেখা
- ৪-৫টি অত্যন্ত ট্রেন্ডিং হ্যাশট্যাগ

সংবাদের তথ্য:
শিরোনাম: {original_title}
বিস্তারিত: {original_summary}
"""

try:
    print(f"AI প্রসেস করছে: {original_title}")
    response = model.generate_content(prompt)
    rewritten_content = response.text
    post_message = f"{rewritten_content}\n\n📌 বিস্তারিত ও মূল খবর পড়তে ক্লিক করুন: {news_link}"

    # ==========================================
    # ৬. ফেসবুক পেজে পোস্ট
    # ==========================================
    fb_page_id = os.environ.get("FB_PAGE_ID")
    fb_token = os.environ.get("FB_ACCESS_TOKEN")

    if fb_page_id and fb_token:
        post_url = f"https://graph.facebook.com/v19.0/{fb_page_id}/feed"
        payload = {'message': post_message, 'access_token': fb_token}
        requests.post(post_url, data=payload)
        print("ফেসবুকে পোস্ট সফল হয়েছে!")

    # ==========================================
    # ৭. টেলিগ্রাম চ্যানেলে পোস্ট
    # ==========================================
    tg_bot_token = os.environ.get("TG_BOT_TOKEN")
    tg_chat_id = os.environ.get("TG_CHAT_ID")

    if tg_bot_token and tg_chat_id:
        tg_url = f"https://api.telegram.org/bot{tg_bot_token}/sendMessage"
        payload = {'chat_id': tg_chat_id, 'text': post_message}
        requests.post(tg_url, data=payload)
        print("টেলিগ্রাম চ্যানেলে পোস্ট সফল হয়েছে!")

    # ==========================================
    # ৮. হোয়াটসঅ্যাপে পোস্ট
    # ==========================================
    wa_instance_id = os.environ.get("WA_INSTANCE_ID")
    wa_token = os.environ.get("WA_TOKEN")
    wa_to = os.environ.get("WA_TO")

    if wa_instance_id and wa_token and wa_to:
        wa_url = f"https://api.ultramsg.com/{wa_instance_id}/messages/chat"
        payload = {'token': wa_token, 'to': wa_to, 'body': post_message}
        requests.post(wa_url, data=payload)
        print("হোয়াটসঅ্যাপে পোস্ট সফল হয়েছে!")

    # ==========================================
    # ৮.৫. BLOGSPOT এ DRAFT হিসেবে পোস্ট (Google Safe)
    # ==========================================
    blogger_blog_id = os.environ.get("BLOGGER_BLOG_ID")
    blogger_token = os.environ.get("BLOGGER_TOKEN")

    if blogger_blog_id and blogger_token:
        blog_url = f"https://www.googleapis.com/blogger/v3/blogs/{blogger_blog_id}/posts/"
        headers = {
            "Authorization": f"Bearer {blogger_token}",
            "Content-Type": "application/json"
        }
        blog_payload = {
            "kind": "blogger#post",
            "title": original_title,
            "content": f"{rewritten_content}<br><br><a href='{news_link}' target='_blank'>মূল খবর পড়ুন</a>",
            "isDraft": True
        }
        try:
            res = requests.post(blog_url, headers=headers, json=blog_payload)
            if res.status_code == 200:
                print("Blogspot এ Draft হিসেবে সেভ হয়েছে!")
            else:
                print(f"Blogger Error: {res.text}")
        except Exception as e:
            print(f"Blogger Error: {e}")

    # ==========================================
    # ৯. ইতিহাস সেভ করা (যেন ২ বার না যায়)
    # ==========================================
    posted_urls.append(news_link)
    with open(POSTED_LOG_FILE, "w") as f:
        json.dump(posted_urls, f)

except Exception as e:
    print(f"এরর: {e}")
