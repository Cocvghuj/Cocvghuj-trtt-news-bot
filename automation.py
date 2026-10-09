import feedparser
import os
import json
import requests
import datetime
import random
import re
import traceback
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import facebook

# URL Constants
TOKEN_URI = "https://oauth2.googleapis.com/token"
GEMINI_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={k}"
TELEGRAM_URL_TEMPLATE = "https://api.telegram.org/bot{token}/sendMessage"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

FEEDS = {
    "Schengen & Europe EU Rules": "https://www.schengenvisainfo.com/news/feed/",
    "Canada Immigration & Jobs": "https://www.cicnews.com/feed/",
    "USA Visa & Tech Laws": "https://www.immigration.ca/feed/",
    "Australia & NZ Policy Updates": "https://www.abc.net.au/news/feed/51120/rss.xml",
    "Middle East Laws & Business": "https://www.aljazeera.com/xml/rss/all.rss",
    "Global Tech & Dev Innovations": "https://techcrunch.com/feed/",
    "Global Finance & Investment": "http://feeds.bbci.co.uk/news/business/rss.xml"
}

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
        key = os.environ.get("UNSPLASH_ACCESS_KEY")
        if key:
            url = f"https://api.unsplash.com/search/photos?query={query}&per_page=1&client_id={key}"
            r = requests.get(url).json()
            if r.get('results') and len(r['results']) > 0:
                return r['results'][0]['urls']['regular']
    except Exception:
        pass
    return f"https://picsum.photos/seed/{random.randint(1, 100000)}/800/400"

def call_groq_draft(p):
    try:
        k = os.environ.get("GROQ_API_KEY")
        if k:
            r = requests.post(GROQ_URL,
                headers={"Authorization": f"Bearer {k}"},
                json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": p}], "temperature": 0.3}
            )
            j = r.json()
            if "choices" in j and len(j["choices"]) > 0:
                return j["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Groq error: {e}")
    return None

def call_gemini_modifier(draft, cat, title, summary):
    try:
        k = os.environ.get("GEMINI_API_KEY")
        if k:
            p = f"""You are a senior native English Chief Editor. Rewrite draft to 100% unique elite English optimized for AdSense and high search traffic.
Title: {title} Summary: {summary} Draft: {draft}
Reply ONLY valid JSON format. Do not add markdown blocks like ```json outside the raw object.
Keywords to integrate seamlessly: '{cat} 2027', 'global immigration requirements', 'official guidelines'.
JSON Structure: {{"seo_title": "SEO optimized catchy headline with {cat} 2027", "meta_description": "150 char high CTR meta description", "article_body": "HTML content starting with <h2> with deep analysis, formatting, and high readability", "fb_caption": "engaging social caption with hashtags"}}"""
            
            url = GEMINI_URL_TEMPLATE.format(k=k)
            r = requests.post(url, json={"contents": [{"parts": [{"text": p}]}]}, timeout=30)
            j = r.json()
            if "candidates" in j and len(j["candidates"]) > 0:
                return j["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print(f"Gemini error: {e}")
    return None

# সরাসরি தனி আলাদা সিক্রেটগুলো ব্যবহার করার জন্য ফাংশন
def get_blogger():
    try:
        client_id = os.environ.get("BLOGGER_CLIENT_ID")
        client_secret = os.environ.get("BLOGGER_CLIENT_SECRET")
        refresh_token = os.environ.get("BLOGGER_REFRESH_TOKEN")
        
        if not client_id or not client_secret or not refresh_token:
            print("❌ Missing Blogger OAuth Secrets!")
            return None

        creds = Credentials(
            token=None,
            refresh_token=refresh_token,
            client_id=client_id,
            client_secret=client_secret,
            token_uri=TOKEN_URI,
        )
        
        creds.refresh(Request())
        print("✅ Blogger token refreshed successfully!")

        return build("blogger", "v3", credentials=creds)
    except Exception as e:
        print(f"❌ Blogger Auth Error: {e}")
        traceback.print_exc()
        return None

def post_to_facebook_system(page_access_token, page_id, message, link):
    try:
        graph = facebook.GraphAPI(access_token=page_access_token)
        graph.put_object(parent_object=page_id, connection_name='feed', message=message, link=link)
        print("✅ Successfully posted to Facebook Page!")
    except Exception as e:
        print(f"🇫 Facebook skipped: {str(e)}")

def post_to_telegram(token, chat_id, message, link):
    try:
        text = f"{message}\n\n🔗 Read Full Story: {link}"
        url = TELEGRAM_URL_TEMPLATE.format(token=token)
        r = requests.post(url, json={"chat_id": chat_id, "text": text}, timeout=12)
        if r.status_code == 200:
            print("🚀 Successfully posted to Telegram!")
    except Exception as e:
        print(f"📱 Telegram skipped: {str(e)}")

def main():
    selected_entry = None
    chosen_category = get_cat()
    categories_to_try = [chosen_category] + [cat for cat in FEEDS.keys() if cat != chosen_category]
    browser_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    for current_cat in categories_to_try:
        print(f"📡 Scanning Network: {current_cat}...")
        try:
            response = requests.get(FEEDS[current_cat], headers=browser_headers, timeout=15)
            if response.status_code == 200:
                feed = feedparser.parse(response.text)
                if feed.entries and len(feed.entries) > 0:
                    selected_entry = feed.entries[0]
                    chosen_category = current_cat
                    print(f"🎯 Found in: {chosen_category}! Title: {selected_entry.title[:60]}")
                    break
        except Exception as e:
            print(f"Skipping {current_cat}: {e}")
            continue

    if not selected_entry:
        print("❌ No entries found across global networks.")
        exit(0)

    summary_text = selected_entry.get('summary', selected_entry.title)
    image_url = get_featured_image(chosen_category)
    
    draft_prompt = f"Write news report: Title: {selected_entry.title}. Summary: {summary_text}. Category: {chosen_category}"
    draft_content = call_groq_draft(draft_prompt) or f"Update regarding {selected_entry.title}. {summary_text}"
    final_response = call_gemini_modifier(draft_content, chosen_category, selected_entry.title, summary_text)

    try:
        json_clean = final_response.strip() if final_response else ""
        if json_clean.startswith("```"):
            json_clean = re.sub(r'```(?:json)?\s*|\s*```', '', json_clean, flags=re.MULTILINE)
        data = json.loads(json_clean)
        seo_title = data["seo_title"]
        article_body = f"<div ><img src='{image_url}' style='width:100%; border-radius:8px'/></div>" + data["article_body"]
        meta_desc = data["meta_description"]
        fb_caption = data["fb_caption"]
    except:
        print("Bypassing advanced JSON Parsing to Fallback Guard template")
        seo_title = f"{chosen_category} 2027: {selected_entry.title[:80]}"
        article_body = f"<div ><img src='{image_url}' style='width:100%; border-radius:8px'/></div><h2>{seo_title}</h2><p>{summary_text}</p>"
        meta_desc = f"Latest official updates and global insights on {chosen_category}."
        fb_caption = f"🌍 Global Update: {seo_title}. Read details on our portal!"

    labels = [chosen_category, "Global Visa 2027", "Official Updates"]
    service = get_blogger()

    if service:
        try:
            body = {"kind": "blogger#post", "blog": {"id": os.environ["BLOGGER_ID"]}, "title": seo_title, "content": article_body, "labels": labels}
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
            print(f"❌ Blogger Post Execution break: {str(e)}")
            exit(1)
    else:
        print("❌ Blogger Service could not be initialized.")
        exit(1)

if __name__ == "__main__":
    main()
