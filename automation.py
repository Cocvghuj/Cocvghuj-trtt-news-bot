import feedparser, os, json, requests, datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import facebook

# ১. টেকনোলজি ও কোডিং সহ সকল সচল ও লাইভ আরএসএস ফিডস
FEEDS = {
    "Schengen Visa": "https://schengenvisainfo.com",
    "Europe Work Permit": "https://cicnews.com",
    "Europe Jobs": "https://schengenvisainfo.com",
    "Study in Europe": "https://scholarship-positions.com",
    "Europe Business": "https://bbci.co.uk",
    "Europe Investment": "https://ft.com",
    "Europe Tech & Coding": "https://bbci.co.uk",
    "Europe Politics": "https://bbci.co.uk"
}

# ২. আপনার রুটিনে টেকনোলজি ক্যাটাগরি যুক্ত করা হলো
WEEK = {
    0: ["Schengen Visa", "Europe Tech & Coding"],   # সোমবার
    1: ["Europe Business", "Europe Work Permit"],   # মঙ্গলবার
    2: ["Europe Tech & Coding", "Europe Jobs"],     # বুধবার
    3: ["Europe Investment", "Schengen Visa"],      # বৃহস্পতিবার
    4: ["Europe Work Permit", "Europe Politics"],   # শুক্রবার
    5: ["Study in Europe", "Europe Tech & Coding"], # শনিবার
    6: ["Europe Jobs", "Schengen Visa"]             # রবিবার
}

def get_cat():
    now = datetime.datetime.now()
    return WEEK[now.weekday()][0 if now.hour < 12 else 1]

def get_featured_image(query):
    try:
        client_id = os.environ.get("UNSPLASH_ACCESS_KEY")
        if client_id:
            url = f"https://unsplash.com{query},europe,coding&client_id={client_id}"
            r = requests.get(url, timeout=12)
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
                              json={"model":"llama-3.3-70b-versatile", "messages":[{"role":"user","content":p}], "temperature": 0.3}, timeout=40)
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
        print("🎉 Successfully posted to Facebook Page automatically!")
    except Exception as e:
        print(f"Facebook warning (Skipped to prevent crash): {str(e)}")

def post_to_telegram(token, chat_id, message, link):
    try:
        text = f"{message}\n\n🔗 Read Full Story: {link}"
        url = f"https://telegram.org{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        r = requests.post(url, json=payload, timeout=12)
        if r.status_code == 200:
            print("🎉 Successfully posted to Telegram Channel automatically!")
        else:
            print(f"Telegram API response error: {r.text}")
    except Exception as e:
        print(f"Telegram warning: {str(e)}")

# --- স্মার্ট লুপ মেকানিজম (কোনো রান খালি যাবে激活) ---
selected_entry = None
chosen_category = get_cat()

categories_to_try = [chosen_category] + [cat for cat in FEEDS.keys() if cat != chosen_category]

for current_cat in categories_to_try:
    print(f"Checking RSS source for category: {current_cat}...")
    feed = feedparser.parse(FEEDS[current_cat])
    
    if feed.entries and len(feed.entries) > 0:
        selected_entry = feed.entries[0]
        chosen_category = current_cat
        print(f"🎯 Target news found in category: {chosen_category}!")
        break

if not selected_entry:
    print("❌ No news entries found across all categories. Exiting cleanly.")
    exit(0)

summary_text = selected_entry.get('summary', 'Latest industry insight and detailed tech updates.')
image_url = get_featured_image(chosen_category)

prompt = f"""
You are an elite native English technology and financial journalist writing for a premium European News site.
Write a 100% unique, deep-dive, professional news article based on the source data below. Fix any grammar and spelling errors from the source.

Category: {chosen_category}
Source Title: {selected_entry.title}
Source Summary: {summary_text}

Strict Structural Rules:
- Language: Native, flawless, high-vocabulary British/American English only.
- Format: Reply ONLY in valid JSON format. Do not include markdown indicators outside the JSON object.
- Elements: Use <h2> and <h3> tags for subheadings. Use bullet points (<ul>/<li>) to present data clearly.
- Target Keywords to Naturally Integrate: "{chosen_category} 2027", "Europe 2027", "step-by-step application guidelines", "technical innovations", "development and coding trends".

Expected JSON structure:
{{
  "seo_title": "A high-CTR unique headline including {chosen_category} 2027",
  "meta_description": "A powerful 150-character meta description for search engines without quotes.",
  "article_body": "HTML content starting with <h2>. Deep analysis of the news, background information, implications for 2027, and actionable advice for readers.",
  "fb_caption": "Write an engaging Facebook post caption with relevant 2027 hashtags and emojis."
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
    print(f"JSON Parsing fallguard triggered: {str(parse_error)}")
    seo_title = f"{chosen_category} 2027: {selected_entry.title[:80]}"
    article_body = f'<div style="margin-bottom:20px;"><img src="{image_url}" alt="{seo_title}" style="width:100%; border-radius:8px;"/></div><h2>{seo_title}</h2><p>{summary_text}</p>'
    meta_desc = f"Latest premium updates on {chosen_category} 2027 and technical regulations in Europe."
    fb_caption = f"📢 Latest Update: {seo_title}. Read more details on our blog!"

labels = [chosen_category, "Europe 2027", "Premium Insights", "Tech News"]

service = get_blogger()
body = {
    "kind": "blogger#post",
    "blog": {"id": os.environ["BLOGGER_ID"]},
    "title": seo_title,
    "content": article_body,
    "labels": labels,
    "searchDescription": meta_desc
}

try:
    post = service.posts().insert(blogId=os.environ["BLOGGER_ID"], body=body, isDraft=False).execute()
    post_url = post['url']
    print(f"🚀 SUCCESSFULLY PUBLISHED BLOG: {post_url}")
    
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
    print(f"Automation critically failed: {str(blogger_error)}")
    exit(1)
