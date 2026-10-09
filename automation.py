import feedparser, os, json, requests, datetime, random, re
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import facebook

# ১. বৈশ্বিক হাই-সিপিসি ১০০% লাইভ আরএসএস ফিড নেটওয়ার্ক
FEEDS = {
    "Schengen & Europe EU Rules": "https://schengenvisainfo.com",
    "Canada Immigration & Jobs": "https://cicnews.com",
    "USA Visa & Tech Laws": "https://uscis.gov",
    "BBC World & Europe News": "http://bbci.co.uk",
    "CNN International News": "http://cnn.com",
    "Reuters Agency Global": "https://immigration.ca",  
    "Al Jazeera English Hub": "https://aljazeera.com"
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
            url = f"https://unsplash.com{query}&per_page=1&client_id={key}"
            r = requests.get(url, timeout=10).json()
            if r.get('results'): return r['results'][0]['urls']['regular']
    except: pass
    return f"https://picsum.photos{random.randint(1,1000)}/800/400"

def call_groq_draft(p):
    try:
        k = os.environ.get("GROQ_API_KEY")
        if k:
            r = requests.post("https://groq.com",
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
            p = f"""You are a senior native English Chief Editor. Rewrite draft to 100% unique elite English. Source Title: {title} Summary: {summary} Draft: {draft} Strict Rules: Reply ONLY valid JSON. Keywords: "{cat} 2027". JSON: {{"seo_title": "headline with {cat} 2027", "meta_description": "150 char meta", "article_body": "HTML starting with <h2> with deep analysis", "fb_caption": "social caption with hashtags"}}"""
            for m in ["gemini-2.0-flash", "gemini-1.5-flash"]:
                url = f"https://googleapis.com{m}:generateContent?key={k}"
                r = requests.post(url, json={"contents":[{"parts":[{"text":p}]}]}, timeout=30)
                j = r.json()
                if "candidates" in j: return j["candidates"][0]['content']['parts'][0]['text']
    except: pass
    return None

# ৩. আপনার গতকালের টোকেনকে এরর-মুক্ত করার স্পেশাল অটো-ক্লিন মেকানিজম
def get_blogger():
    try:
        s = os.environ.get("BLOGGER_TOKEN_JSON")
        if not s:
            print("❌ Error: BLOGGER_TOKEN_JSON খুঁজে পাওয়া যায়নি।")
            return None
            
        # গিটহাব সিক্রেটে পেস্ট হওয়া ভাঙা ক্যারেক্টার বা অদৃশ্য ময়লা স্পেস স্বয়ংক্রিয়ভাবে ক্লিন করা হচ্ছে
        s_clean = s.strip()
        s_clean = re.sub(r'^[^{]*', '', s_clean) # বন্ধনীর আগের অদৃশ্য ময়লা কাটা
        s_clean = re.sub(r'[^}]*$', '', s_clean) # বন্ধনীর শেষের অদৃশ্য ময়লা কাটা
        s_clean = s_clean.replace("'", '"')
        
        token_data = json.loads(s_clean)
        creds = Credentials.from_authorized_user_info(token_data)
        return build("blogger", "v3", credentials=creds)
    except Exception as e:
        print(f"⚠️ Blogger Fallguard active (Token clean bypass): {str(e)}")
        return None

def post_to_facebook_system(page_access_token, page_id, message, link):
    try:
        graph = facebook.GraphAPI(access_token=page_access_token)
        graph.put_object(parent_object=page_id, connection_name='feed', message=message, link=link)
        print("🎉 Successfully posted to Facebook Page!")
    except Exception as e:
        print(f"Facebook skipped: {str(e)}")

def post_to_telegram(token, chat_id, message, link):
    try:
        text = f"{message}\n\n🔗 Read Full Story: {link}"
        url = f"https://telegram.org{token}/sendMessage"
        r = requests.post(url, json={"chat_id": chat_id, "text": text}, timeout=12)
        if r.status_code == 200: print("🎉 Successfully posted to Telegram!")
    except Exception as e:
        print(f"Telegram skipped: {str(e)}")

# --- Main Runtime ---
selected_entry = None
chosen_category = get_cat()
categories_to_try = [chosen_category] + [cat for cat in FEEDS.keys() if cat != chosen_category]

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
    print("❌ No entries found.")
    exit(0)

summary_text = selected_entry.get('summary', selected_entry.title)
image_url = get_featured_image(chosen_category)

draft_prompt = f"Write news report: Title: {selected_entry.title}. Summary: {summary_text}. Category: {chosen_category}."
draft_content = call_groq_draft(draft_prompt) or f"Update regarding {selected_entry.title}. {summary_text}"
final_response = call_gemini_modifier(draft_content, chosen_category, selected_entry.title, summary_text)

try:
    clean_json = final_response.strip().replace("```json", "").replace("```", "")
    data = json.loads(clean_json)
    seo_title, article_body, meta_desc, fb_caption = data["seo_title"], f'<div><img src="{image_url}" style="width:100%; border-radius:8px;"/></div>' + data["article_body"], data["meta_description"], data["fb_caption"]
except:
    seo_title = f"{chosen_category}: {selected_entry.title[:80]}"
    article_body = f'<div><img src="{image_url}" style="width:100%; border-radius:8px;"/></div><h2>{seo_title}</h2><p>{summary_text}</p>'
    meta_desc = f"Latest updates on {chosen_category}."
    fb_caption = f"📢 Global Update: {seo_title}."

labels = [chosen_category, "Global Visa 2027"]
service = get_blogger()

if service:
    try:
        body = {"kind": "blogger#post", "blog": {"id": os.environ["BLOGGER_ID"]}, "title": seo_title, "content": article_body, "labels": labels, "searchDescription": meta_desc}
        post = service.posts().insert(blogId=os.environ["BLOGGER_ID"], body=body, isDraft=False).execute()
        post_url = post['url']
        print(f"🚀 GLOBAL HUB AUTOMATION PUBLISHED: {post_url}")

        FB_TOKEN = os.environ.get("FB_PAGE_ACCESS_TOKEN")
        FB_PAGE_ID = os.environ.get("FB_PAGE_ID")
        if FB_TOKEN and FB_PAGE_ID: post_to_facebook_system(FB_TOKEN, FB_PAGE_ID, fb_caption, post_url)

        TG_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
        TG_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
        if TG_TOKEN and TG_CHAT_ID: post_to_telegram(TG_TOKEN, TG_CHAT_ID, fb_caption, post_url)
    except Exception as e:
        print(f"Execution Error: {str(e)}")
        exit(1)
else:
    print("❌ Token Clean limit bypassed. Google API still rejects string. Fix your Secret format.")
    exit(1)
