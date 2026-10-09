import feedparser, os, json, requests, datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import facebook

# ১. বিবিসি, সিএনএন, রয়টার্স ও আলজাজিরা সহ সকল গ্লোবাল হাই-ট্রাফিক আরএসএস সোর্স
FEEDS = {
    "Schengen & Europe EU Rules": "https://schengenvisainfo.com",
    "Canada Immigration & Jobs": "https://cicnews.com",
    "USA Visa & Tech Laws": "https://immigration.ca",
    "BBC World & Europe News": "https://bbci.co.uk",
    "CNN International News": "http://cnn.com",
    "Reuters Agency Global": "https://immigration.ca",  # বিকল্প অ্যান্টি-ব্লক সোর্স
    "Al Jazeera English Hub": "https://aljazeera.com"
}

# ২. ২৪ ঘণ্টা হাই-ট্রাফিক নিশ্চিত করার বৈশ্বিক সাপ্তাহিক রুটিন
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
        client_id = os.environ.get("UNSPLASH_ACCESS_KEY")
        if client_id:
            url = f"https://unsplash.com{query},global,news&client_id={client_id}"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            r = requests.get(url, headers=headers, timeout=12)
            if r.status_code == 200:
                return r.json()['urls']['regular']
    except: pass
    return "https://unsplash.com"

# প্রথম ফিল্টার: Groq (Llama 3.3) দিয়ে নিউজের খসড়া ও ডেটা অ্যানালাইসিস তৈরি
def call_groq_draft(p):
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
    return None

# দ্বিতীয় ফিল্টার (মডিফায়ার): Gemini 2.0 দিয়ে সম্পূর্ণ রিরাইট, প্রুফরিড ও ফাইনাল এসইও অপ্টিমাইজেশন
def call_gemini_modifier(draft, cat, title, summary):
    try:
        k = os.environ.get("GEMINI_API_KEY")
        if k:
            p = f"""
            You are a senior native English Chief Editor. Review and heavily rewrite the draft article below to ensure 100% uniqueness (no plagiarism) and elite British/American English quality.
            Fix any subtle grammar or spelling mistakes.

            Source Reference Title: {title}
            Source Reference Summary: {summary}
            Draft Article to Polish: {draft}

            Strict Rules:
            - Reply ONLY in valid JSON format. Do not use markdown tags like ```json outside the object.
            - Keywords to integrate seamlessly: "{cat} 2027", "global immigration requirements", "step-by-step application guidelines", "official regulatory policy".

            Expected JSON structure:
            {{
              "seo_title": "A high-CTR unique headline including {cat} 2027",
              "meta_description": "A powerful 150-character meta description for search engines without quotes.",
              "article_body": "HTML content starting with <h2>. Deep analysis, implications for 2027, and actionable advice with subheadings <h2>/<h3> and bullet points.",
              "fb_caption": "An engaging social caption with relevant global hashtags and emojis."
            }}
            """
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

#   Groq-কে দিয়ে খবরের মূল ড্রাফট তৈরি করানো
draft_prompt = f"Analyze and write a detailed professional news report based on this data: Title: {selected_entry.title}. Summary: {summary_text}. Category: {chosen_category}. Focus on structural data and factual background."
draft_content = call_groq_draft(draft_prompt)

if not draft_content:
    draft_content = f"Official update regarding {selected_entry.title}. {summary_text}"

#   Gemini দিয়ে সেই ড্রাফটটিকে মডিফাই, রিরাইট এবং প্রফেশনাল এসইও-তে রূপান্তর
final_response = call_gemini_modifier(draft_content, chosen_category, selected_entry.title, summary_text)

try:
    clean_json = final_response.strip().replace("```json", "").replace("```", "")
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

labels = [chosen_category, "Global Visa 2027", "Official Law Updates", "International NewsHub"]

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
