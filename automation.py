import feedparser, os, json, requests, datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import facebook

# ১. বৈশ্বিক হাই-সিপিসি ও ১০০% লাইভ আসল আরএসএস ফিড নেটওয়ার্ক
FEEDS = {
    "Schengen & Europe EU Rules": "https://schengenvisainfo.com",
    "USA Visa & Tech Laws": "https://commonwealthfund.org",
    "Canada Immigration & Jobs": "https://cicnews.com",
    "Australia & NZ Policy Updates": "https://smartraveller.gov.au",
    "Middle East Laws & Business": "https://arabianbusiness.com",
    "Global Tech & Dev Innovations": "https://bbci.co.uk",
    "Global Finance & Investment": "https://ft.com"
}

# ২. ২৪ ঘণ্টা গ্লোবাল কভারেজ নিশ্চিত করার শিডিউল রুটিন (২০২৭ রেডি)
WEEK = {
    0: ["Schengen & Europe EU Rules", "Global Tech & Dev Innovations"],
    1: ["Canada Immigration & Jobs", "Global Finance & Investment"],
    2: ["USA Visa & Tech Laws", "Middle East Laws & Business"],
    3: ["Australia & NZ Policy Updates", "Schengen & Europe EU Rules"],
    4: ["Canada Immigration & Jobs", "Global Tech & Dev Innovations"],
    5: ["USA Visa & Tech Laws", "Middle East Laws & Business"],
    6: ["Australia & NZ Policy Updates", "Global Finance & Investment"]
}

def get_cat():
    now = datetime.datetime.now()
    return WEEK[now.weekday()][0 if now.hour < 12 else 1]

def get_featured_image(query):
    try:
        client_id = os.environ.get("UNSPLASH_ACCESS_KEY")
        if client_id:
            url = f"https://unsplash.com{query},global,news&client_id={client_id}"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            r = requests.get(url, headers=headers, timeout=12)
            if r.status_code == 200:
                return r.json()['urls']['regular']
    except: pass
    return "https://unsplash.com"

def ai_seo_generator(p):
    try:
        k = os.environ.get("GROQ_API_KEY")
        if k:
            r = requests.post("https://groq.com", 
                              headers={"Authorization": f"Bearer {k}"}, 
                              json={"model":"llama-3.3-70b-versatile", "messages":[{"role":"user","content":p}], "temperature": 0.2}, timeout=40)
            j = r.json()
            if "choices" in j and len(j["choices"]) > 0: 
                return j["choices"]["message"]["content"]
    except: pass

    try:
        k = os.environ.get("GEMINI_API_KEY")
        if k:
            for m in ["gemini-2.0-flash", "gemini-2.0-flash-lite"]:
                url = f"https://googleapis.com{m}:generateContent?key={k}"
                r = requests.post(url, json={"contents":[{"parts":[{"text":p}]}]}, timeout=30)
                j = r.json()
                if "candidates" in j and len(j["candidates"]) > 0: 
                    return j["candidates"]['content']['parts']['text']
    except: pass
    return None

def get_blogger():
    s = os.environ.get("BLOGGER_TOKEN_JSON")
    creds = Credentials.from_authorized_user_info(json.loads(s))
    return build("blogger", "v3", credentials=creds)

def post_to_facebook_system(app_id, app_secret, page_id, message, link):
    try:
        graph = facebook.GraphAPI()
        app_token = graph.get_app_access_token(app_id=app_id, app_secret=app_secret)
        page_graph = facebook.GraphAPI(access_token=app_token)
        page_graph.put_object(parent_object=page_id, connection_name='feed', message=message, link=link)
        print("🎉 Successfully posted to Facebook Page!")
    except Exception as e:
        print(f"Facebook skipped: {str(e)}")

def post_to_telegram(token, chat_id, message, link):
    try:
        text = f"{message}\n\n🔗 Read Full Story: {link}"
        url = f"https://telegram.org{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        r = requests.post(url, json=payload, timeout=12)
        if r.status_code == 200:
            print("🎉 Successfully posted to Telegram Channel!")
    except Exception as e:
        print(f"Telegram skipped: {str(e)}")

# --- স্মার্ট লুপ অ্যান্ড সিকিউর হেডার (অ্যান্টি-ব্লক প্রটেকশন) ---
selected_entry = None
chosen_category = get_cat()
categories_to_try = [chosen_category] + [cat for cat in FEEDS.keys() if cat != chosen_category]

browser_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

for current_cat in categories_to_try:
    print(f"Scanning Global Network: {current_cat}...")
    try:
        response = requests.get(FEEDS[current_cat], headers=browser_headers, timeout=15)
        if response.status_code == 200:
            feed = feedparser.parse(response.text)
            if feed.entries and len(feed.entries) > 0:
                selected_entry = feed.entries[0]
                chosen_category = current_cat
                print(f"🎯 Premium Breaking News found in: {chosen_category}!")
                break
    except Exception as feed_err:
        print(f"Skipping {current_cat}: {str(feed_err)}")
        continue

if not selected_entry:
    print("❌ Critical: No entries found across global feeds.")
    exit(0)

summary_text = selected_entry.get('summary', 'Latest official regulatory updates and global insights.')
image_url = get_featured_image(chosen_category)

# গ্লোবাল অডিয়েন্স এবং অটো-ইনডেক্সিং এর জন্য আল্ট্রা-এসইও প্রম্পট
prompt = f"""
You are a senior native English international journalist and elite SEO architect.
Write a 100% unique, deep-dive, professional news article in flawless, advanced native English based on the source data below. Eliminate any grammar or spelling issues.

Category: {chosen_category}
Source Title: {selected_entry.title}
Source Summary: {summary_text}

Strict Structural Rules:
- Language: Flawless, highly advanced native British/American English only.
- Format: Reply ONLY in valid JSON format without markdown ticks outside the object.
- Elements: Use <h2> and <h3> tags for subheadings. Use clean bullet points (<ul>/<li>) to present data with deep clarity.
- Keywords to Integrate Naturally: "{chosen_category} 2027", "global immigration requirements", "step-by-step application guidelines", "official regulatory policy", "international technical innovations".

Expected JSON structure:
{{
  "seo_title": "A high-CTR unique headline including {chosen_category} 2027",
  "meta_description": "A powerful 150-character meta description for search engines without quotes.",
  "article_body": "HTML content starting with <h2>. Deep analysis of the news, background information, implications for 2027, and actionable advice.",
  "fb_caption": "Write an engaging social caption with relevant global hashtags and emojis."
}}
"""

response_raw = ai_seo_generator(prompt)

try:
    clean_json = response_raw.strip().replace("```json", "").replace("```", "")
    data = json.loads(clean_json)
    seo_title = data["seo_title"]
    article_body = f'<div style="margin-bottom:20px;"><img src="{image_url}" alt="{seo_title}" style="width:100%; max-height:420px; object-fit:cover; border-radius:8px;"/></div>' + data["article_body"]
    meta_desc = data["meta_description"]
    fb_caption = data["fb_caption"]
except Exception as parse_error:
    print(f"JSON Guard triggered: {str(parse_error)}")
    seo_title = f"{chosen_category}: {selected_entry.title[:80]}"
    article_body = f'<div style="margin-bottom:20px;"><img src="{image_url}" alt="{seo_title}" style="width:100%; border-radius:8px;"/></div><h2>{seo_title}</h2><p>{summary_text}</p>'
    meta_desc = f"Latest official updates and global insights on {chosen_category}."
    fb_caption = f"📢 Global Update: {seo_title}. Read details on our portal!"

# ক্যাটাগরি ও দেশের ওপর ভিত্তি করে গুগলের গ্লোবাল ট্যাগ
labels = [chosen_category, "Global Immigration 2027", "Official Law Updates", "International NewsHub"]

service = get_blogger()
body = {
    "kind": "blogger#post",
    "blog": {"id": os.environ["BLOGGER_ID"]},
    "title": seo_title,
    "content": article_body,
    "labels": labels,
    "searchDescription": meta_desc # এটি মেটা ডেসক্রিপশন বক্সে ডেটা পুশ করবে যা গুগলে অটো-ইনডেক্স করবে
}

try:
    post = service.posts().insert(blogId=os.environ["BLOGGER_ID"], body=body, isDraft=False).execute()
    post_url = post['url']
    print(f"🚀 GLOBAL HUB AUTOMATION PUBLISHED: {post_url}")
    
    APP_ID = os.environ.get("FB_APP_ID")
    APP_SECRET = os.environ.get("FB_APP_SECRET")
    FB_PAGE_ID = os.environ.get("FB_PAGE_ID")
    if APP_ID and APP_SECRET and FB_PAGE_ID:
        post_to_facebook_system(APP_ID, APP_SECRET, FB_PAGE_ID, fb_caption, post_url)

    TG_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    TG_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
    if TG_TOKEN and TG_CHAT_ID:
        post_to_telegram(TG_TOKEN, TG_CHAT_ID, fb_caption, post_url)

except Exception as blogger_error:
    print(f"Automation execution break: {str(blogger_error)}")
    exit(1)
