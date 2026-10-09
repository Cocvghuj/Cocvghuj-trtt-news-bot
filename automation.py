import feedparser, os, json, requests, datetime, random, re
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# ১. ১০০% আসল ও লাইভ বৈশ্বিক আরএসএস ফিড নেটওয়ার্ক
FEEDS = {
    "Schengen & Europe EU Rules": "https://www.schengenvisainfo.com/feed/",
    "Canada Immigration & Jobs": "https://www.cicnews.com/feed/",
    "USA Visa & Tech Laws": "https://www.uscis.gov/rss.xml",
    "BBC World & Europe News": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "CNN International News": "http://rss.cnn.com/rss/edition.rss",
    "Reuters Agency Global": "http://feeds.reuters.com/reuters/topNews",
    "Al Jazeera English Hub": "https://www.aljazeera.com/xml/rss/all.xml"
}

WEEK = {
    0: ["Schengen & Europe EU Rules", "BBC World & Europe News"],
    1: ["Canada Immigration & Jobs", "CNN International News"],
    2: ["USA Visa & Tech Laws", "Al Jazeera English Hub"],
    3: ["BBC World & Europe News", "Schengen & Europe EU Rules"],
    4: ["Canada Immigration & Jobs", "CNN International News"],
    5: ["USA Visa & Tech Laws", "Al Jazeera English Hub"],
    6: ["CNN International News", "BBC World & Europe News"]
}

def get_cat():
    now = datetime.datetime.now()
    return WEEK[now.weekday()][0 if now.hour < 12 else 1]

def get_featured_image(query):
    try:
        key = os.environ.get("UNSPLASH_ACCESS_KEY")
        if key:
            url = f"https://api.unsplash.com/search/photos?query={query}&per_page=1&client_id={key}"
            r = requests.get(url, timeout=10).json()
            if r.get('results'): return r['results'][0]['urls']['regular']
    except: pass
    return f"https://picsum.photos/seed/{random.randint(1,1000)}/800/400"

def call_groq_draft(p):
    try:
        k = os.environ.get("GROQ_API_KEY")
        if k:
            r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {k}"},
                json={"model":"llama-3.3-70b-versatile", "messages":[{"role":"user","content":p}], "temperature": 0.3}, timeout=40)
            j = r.json()
            if "choices" in j: return j["choices"][0]["message"]["content"]
    except: pass
    return None

def call_gemini_modifier(draft, cat, title, summary):
    try:
        k = os.environ.get("GEMINI_API_KEY")
        if k:
            p = f"""You are a senior native English Chief Editor writing for a global audience. Rewrite the draft to 100% unique elite English. Source Title: {title} Summary: {summary} Draft: {draft} 
            Strict Rules: Reply ONLY in a valid JSON object. Do not include markdown code blocks like ```json outside the raw JSON. Keywords to integrate seamlessly: "{cat} 2027", "global immigration requirements", "official regulatory policy".
            JSON Structure: {{"seo_title": "headline with {cat} 2027", "meta_description": "150 char meta description without quotes", "article_body": "HTML starting with <h2> with deep analysis", "fb_caption": "social caption with hashtags"}}"""
            
            # মেটার আপ-টু-ডেট এবং হাই-স্পিড মডেল রুটিন সেট করা হলো
            for m in ["gemini-2.0-flash", "gemini-2.0-flash-lite"]:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={k}"
                r = requests.post(url, json={"contents":[{"parts":[{"text":p}]}]}, timeout=30)
                j = r.json()
                if "candidates" in j and len(j["candidates"]) > 0: 
                    return j["candidates"][0]['content']['parts'][0]['text']
    except: pass
    return None

def get_blogger():
    s = os.environ.get("BLOGGER_TOKEN_JSON")
    creds = Credentials.from_authorized_user_info(json.loads(s))
    return build("blogger", "v3", credentials=creds)

def post_to_facebook_system(page_access_token, page_id, message, link):
    try:
        import facebook
        graph = facebook.GraphAPI(access_token=page_access_token)
        graph.put_object(parent_object=page_id, connection_name='feed', message=message, link=link)
        print("🎉 Successfully posted to Facebook Page!")
    except Exception as e:
        print(f"Facebook skipped: {str(e)}")

def post_to_telegram(token, chat_id, message, link):
    try:
        text = f"{message}\n\n🔗 Read Full Story: {link}"
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        r = requests.post(url, json={"chat_id": chat_id, "text": text}, timeout=12)
        if r.status_code == 200: print("🎉 Successfully posted to Telegram!")
    except Exception as e:
        print(f"Telegram skipped: {str(e)}")

# --- Main Runtime ---
selected_entry = None
chosen_category = get_cat()
categories_to_try = [chosen_category] + [cat for cat in FEEDS.keys() if cat != chosen_category]
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

for current_cat in categories_to_try:
    print(f"Scanning: {current_cat}...")
    try:
        feed = feedparser.parse(FEEDS[current_cat])
        if feed.entries and len(feed.entries) > 0:
            selected_entry = feed.entries[0]
            chosen_category = current_cat
            print(f"🎯 Found in: {chosen_category}!")
            break
    except Exception as e:
        print(f"Skipping {current_cat}: {e}")
        continue

if not selected_entry:
    print("❌ No active entries found across any global feeds. Exiting safely.")
    exit(0)

summary_text = selected_entry.get('summary', selected_entry.title)
image_url = get_featured_image(chosen_category)

draft_prompt = f"Write a professional news report. Title: {selected_entry.title}. Summary: {summary_text}. Category: {chosen_category}."
draft_content = call_groq_draft(draft_prompt) or f"Update regarding {selected_entry.title}. {summary_text}"
final_response = call_gemini_modifier(draft_content, chosen_category, selected_entry.title, summary_text)

# এসইও এবং গুগল ইনডেক্সিং ১০০% নিশ্চিত করার জন্য উন্নত অবজেক্ট পার্সিং
try:
    # রেগুলার এক্সপ্রেশন দিয়ে ব্র্যাকেটের বাইরের সমস্ত ময়লা পরিষ্কার করা হচ্ছে
    json_clean = final_response.strip()
    if json_clean.startswith("```"):
        json_clean = re.sub(r'^```(?:json)?\s*|\s*```$', '', json_clean, flags=re.MULTILINE)
    
    data = json.loads(json_clean.strip())
    seo_title = data["seo_title"]
    article_body = f'<div><img src="{image_url}" style="width:100%; max-height:440px; object-fit:cover; border-radius:8px;"/></div>' + data["article_body"]
    meta_desc = data["meta_description"]
    fb_caption = data["fb_caption"]
except Exception as parse_err:
    print(f"Bypassing advanced JSON Parsing to Fallguard due to: {str(parse_err)}")
    seo_title = f"{chosen_category} 2027: {selected_entry.title[:80]}"
    article_body = f'<div><img src="{image_url}" style="width:100%; border-radius:8px;"/></div><h2>{seo_title}</h2><p>{summary_text}</p>'
    meta_desc = f"Latest official regulatory updates and premium insights on {chosen_category}."
    fb_caption = f"📢 Global Update: {seo_title}. Read details on our portal!"

labels = [chosen_category, "Global Visa 2027", "Official Updates"]
service = get_blogger()
body = {
    "kind": "blogger#post", 
    "blog": {"id": os.environ["BLOGGER_ID"]}, 
    "title": seo_title, 
    "content": article_body, 
    "labels": labels, 
    "searchDescription": meta_desc # এটি সরাসরি ব্লগারের সার্চ ডেসক্রিপশন বক্সে ডেটা পুশ করবে যা গুগলে অটো-ইনডেক্স করবে
}

try:
    post = service.posts().insert(blogId=os.environ["BLOGGER_ID"], body=body, isDraft=False).execute()
    post_url = post['url']
    print(f"🚀 GLOBAL HUB AUTOMATION PUBLISHED: {post_url}")

    FB_TOKEN = os.environ.get("FB_PAGE_ACCESS_TOKEN")
    FB_PAGE_ID = os.environ.get("FB_PAGE_ID")
    if FB_TOKEN and FB_PAGE_ID:
        post_to_facebook_system(FB_TOKEN, FB_PAGE_ID, fb_caption, post_url)

    TG_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    TG_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
    if TG_TOKEN and TG_CHAT_ID:
        post_to_telegram(TG_TOKEN, TG_CHAT_ID, fb_caption, post_url)
except Exception as e:
    print(f"Critical execution error: {str(e)}")
    exit(1)
