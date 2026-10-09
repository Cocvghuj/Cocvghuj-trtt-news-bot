import feedparser, os, json, requests, datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import facebook

# ১. হাই-সিপিসি (High CPC) এবং গুগল নিউজ অ্যাপ্রুভড আরএসএস ফিডস
FEEDS = {
    "Schengen Visa": "https://schengenvisainfo.com",
    "Europe Work Permit": "https://cicnews.com",
    "Europe Jobs": "https://schengenvisainfo.com",
    "Study in Europe": "https://scholarship-positions.com",
    "Europe Business": "https://bbci.co.uk",
    "Europe Investment": "https://ft.com",
    "Europe Tech": "https://bbci.co.uk",
    "Europe Politics": "https://bbci.co.uk"
}

WEEK = {
    0: ["Schengen Visa", "Europe Investment"],
    1: ["Europe Business", "Europe Work Permit"],
    2: ["Europe Tech", "Europe Jobs"],
    3: ["Europe Investment", "Schengen Visa"],
    4: ["Europe Work Permit", "Europe Politics"],
    5: ["Study in Europe", "Europe Business"],
    6: ["Europe Jobs", "Schengen Visa"]
}

def get_cat():
    now = datetime.datetime.now()
    return WEEK[now.weekday()][0 if now.hour < 12 else 1]

def get_featured_image(query):
    try:
        client_id = os.environ.get("UNSPLASH_ACCESS_KEY")
        if client_id:
            url = f"https://unsplash.com{query},europe&client_id={client_id}"
            r = requests.get(url, timeout=12)
            if r.status_code == 200:
                return r.json()['urls']['regular']
    except: pass
    return "https://unsplash.com"

def ai_seo_generator(p):
    # গিটহাব ফেল করা ঠেকাতে ডাবল ফলব্যাক মেকানিজম (Groq -> Gemini)
    try:
        k = os.environ.get("GROQ_API_KEY")
        if k:
            r = requests.post("https://groq.com", 
                              headers={"Authorization": f"Bearer {k}"}, 
                              json={"model":"llama-3.3-70b-versatile", "messages":[{"role":"user","content":p}], "temperature": 0.3}, timeout=40)
            j = r.json()
            if "choices" in j and len(j["choices"]) > 0: 
                return j["choices"][0]["message"]["content"]
    except: pass

    try:
        k = os.environ.get("GEMINI_API_KEY")
        if k:
            for m in ["gemini-2.0-flash", "gemini-2.0-flash-lite"]:
                url = f"https://googleapis.com{m}:generateContent?key={k}"
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

def post_to_facebook_system(app_id, app_secret, page_id, message, link):
    try:
        graph = facebook.GraphAPI()
        app_token = graph.get_app_access_token(app_id=app_id, app_secret=app_secret)
        page_graph = facebook.GraphAPI(access_token=app_token)
        page_graph.put_object(parent_object=page_id, connection_name='feed', message=message, link=link)
        print("🎉 Successfully posted to Facebook Page automatically!")
    except Exception as e:
        print(f"Facebook warning (Workflow skipped fail to prevent crash): {str(e)}")

# --- মূল রান টাইম ---
cat = get_cat()
feed = feedparser.parse(FEEDS[cat])

if not feed.entries:
    print(f"No active RSS entries found for {cat}. Exiting cleanly.")
    exit(0)

sel = feed.entries[0]
summary_text = sel.get('summary', 'Latest industry insight and detailed updates.')
image_url = get_featured_image(cat)

# বানান ভুল মুক্ত, প্রফেশনাল এবং গুগল ফ্রেন্ডলি আর্টিকেলের জন্য প্রম্পট
prompt = f"""
You are an elite native English financial journalist writing for a premium European News site.
Write a 100% unique, deep-dive, professional news article based on the source data below. Fix any grammar and spelling errors from the source.

Category: {cat}
Source Title: {sel.title}
Source Summary: {summary_text}

Strict Structural Rules:
- Language: Native, flawless, high-vocabulary British/American English only.
- Format: Reply ONLY in valid JSON format. Do not use Markdown blocks like ```json outside the object.
- Elements: Use <h2> and <h3> tags for subheadings. Use bullet points (<ul>/<li>) to present data clearly.
- Target Keywords to Naturally Integrate: "{cat} 2027", "Europe 2027", "step-by-step application guidelines", "financial legal requirements", "investment risk updates".

Expected JSON structure:
{{
  "seo_title": "A high-CTR unique headline including {cat} 2027",
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
    # গুগলের ব্লগে স্বয়ংক্রিয় ইমেজ সেটআপ
    article_body = f'<div style="margin-bottom:20px;"><img src="{image_url}" alt="{seo_title}" style="width:100%; max-height:420px; object-fit:cover; border-radius:8px;"/></div>' + data["article_body"]
    meta_desc = data["meta_description"]
    fb_caption = data["fb_caption"]
except Exception as parse_error:
    print(f"JSON Parsing failed, active failguard triggered: {str(parse_error)}")
    seo_title = f"{cat} 2027: {sel.title[:80]}"
    article_body = f'<div style="margin-bottom:20px;"><img src="{image_url}" alt="{seo_title}" style="width:100%; border-radius:8px;"/></div><h2>{seo_title}</h2><p>{summary_text}</p>'
    meta_desc = f"Latest premium updates on {cat} 2027 and legal regulations in Europe."
    fb_caption = f"📢 Latest Update: {seo_title}. Read more details on our blog!"

labels = [cat, "Europe 2027", "Premium Insights"]

# ব্লগারে স্বয়ংক্রিয়ভাবে টাইটেল, বডি, ট্যাগ এবং মেটা সার্চ ডেসক্রিপশন পুশ করা
service = get_blogger()
body = {
    "kind": "blogger#post",
    "blog": {"id": os.environ["BLOGGER_ID"]},
    "title": seo_title,
    "content": article_body,
    "labels": labels,
    "searchDescription": meta_desc # এটি সরাসরি ব্লগারের সার্চ ডেসক্রিপশন বক্সে মেটা ডেটা বসিয়ে দেবে (SEO-র জন্য সবচেয়ে জরুরি)
}

try:
    post = service.posts().insert(blogId=os.environ["BLOGGER_ID"], body=body, isDraft=False).execute()
    post_url = post['url']
    print(f"SUCCESSFULLY PUBLISHED BLOG: {post_url}")
    
    APP_ID = os.environ.get("FB_APP_ID")
    APP_SECRET = os.environ.get("FB_APP_SECRET")
    FB_PAGE_ID = os.environ.get("FB_PAGE_ID")

    if APP_ID and APP_SECRET and FB_PAGE_ID:
        post_to_facebook_system(APP_ID, APP_SECRET, FB_PAGE_ID, fb_caption, post_url)
    else:
        print("Facebook credentials missing in GitHub Secrets. Skipping Social share.")
except Exception as blogger_error:
    print(f"Blogger API critically failed: {str(blogger_error)}")
    exit(1)
