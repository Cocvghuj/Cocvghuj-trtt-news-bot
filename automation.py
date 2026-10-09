import feedparser
import os
import json
import requests
import random
import re
import traceback
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import facebook

GEMINI_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={k}"
TELEGRAM_URL_TEMPLATE = "https://api.telegram.org/bot{token}/sendMessage"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

FEEDS = {
    "Schengen & Europe EU Rules": "https://www.schengenvisainfo.com/feed/",
    "Schengen News Update": "https://www.schengenvisainfo.com/news/feed/",
    "Europe Visa Latest": "https://visaguide.world/news/feed/",
    "Canada Immigration & Jobs": "https://www.cicnews.com/feed/",
    "USA Visa & Tech Laws": "https://www.immigration.ca/feed/",
    "UK Visa and Immigration": "https://www.freemovement.org.uk/feed/",
    "EUobserver Migration": "https://euobserver.com/rss/migration",
    "DW Europe News": "https://www.dw.com/export/rss?sectionId=30973",
    "Australia & NZ Policy Updates": "https://www.abc.net.au/news/feed/51120/rss.xml",
    "Middle East Laws & Business": "https://www.aljazeera.com/xml/rss/all.rss",
    "Global Tech & Dev Innovations": "https://techcrunch.com/feed/",
    "Global Finance & Investment": "http://feeds.bbci.co.uk/news/business/rss.xml"
}

LOCATION_MAP = {
    "Schengen & Europe EU Rules": {"name": "Milan, Italy", "lat": 45.4642, "lng": 9.1900},
    "Schengen News Update": {"name": "Milan, Italy", "lat": 45.4642, "lng": 9.1900},
    "Europe Visa Latest": {"name": "Milan, Italy", "lat": 45.4642, "lng": 9.1900},
    "Canada Immigration & Jobs": {"name": "Milan, Italy", "lat": 45.4642, "lng": 9.1900},
    "USA Visa & Tech Laws": {"name": "Milan, Italy", "lat": 45.4642, "lng": 9.1900},
    "UK Visa and Immigration": {"name": "Milan, Italy", "lat": 45.4642, "lng": 9.1900},
    "default": {"name": "Milan, Italy", "lat": 45.4642, "lng": 9.1900}
}

def get_featured_image(query):
    try:
        key = os.environ.get("UNSPLASH_ACCESS_KEY")
        if key:
            url = f"https://api.unsplash.com/search/photos?query={query}&per_page=1&client_id={key}"
            r = requests.get(url).json()
            if r.get('results'):
                return r['results'][0]['urls']['regular']
    except: pass
    return f"https://picsum.photos/seed/{random.randint(1,100000)}/800/400"

def call_groq_draft(p):
    try:
        k = os.environ.get("GROQ_API_KEY")
        if k:
            r = requests.post(GROQ_URL, headers={"Authorization": f"Bearer {k}"}, json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": p}], "temperature": 0.3})
            j = r.json()
            if "choices" in j and len(j["choices"]) > 0:
                return j["choices"][0]["message"]["content"]
    except Exception as e: print(f"Groq error: {e}")
    return None

def call_gemini_modifier(draft, cat, title, summary, source_link):
    try:
        k = os.environ.get("GEMINI_API_KEY")
        if k:
            p = f"You are an expert SEO news editor. Rewrite draft into rich, detailed, 100% unique English news. Title: {title} Summary: {summary} Source: {source_link} Draft: {draft} Reply ONLY valid JSON: {{\"seo_title\": \"Catchy SEO Headline with {cat} 2027\", \"meta_description\": \"Compelling 140-150 char search description\", \"article_body\": \"Detailed HTML with <h2>, paragraphs, bullets\", \"fb_caption\": \"Engaging caption with hashtags\"}}"
            url = GEMINI_URL_TEMPLATE.format(k=k)
            r = requests.post(url, json={"contents": [{"parts": [{"text": p}]}]}, timeout=30)
            j = r.json()
            if "candidates" in j and len(j["candidates"]) > 0:
                parts = j["candidates"][0].get("content", {}).get("parts", [])
                if parts: return parts[0].get("text", "")
    except Exception as e: print(f"Gemini error: {e}")
    return None

def get_blogger():
    try:
        client_id = os.environ.get("BLOGGER_CLIENT_ID")
        client_secret = os.environ.get("BLOGGER_CLIENT_SECRET")
        refresh_token = os.environ.get("BLOGGER_REFRESH_TOKEN")
        creds = Credentials(token=None, refresh_token=refresh_token, client_id=client_id, client_secret=client_secret, token_uri="https://oauth2.googleapis.com/token")
        print("✅ Blogger Credentials initialized successfully!")
        return build("blogger", "v3", credentials=creds)
    except Exception as e:
        print(f"❌ Blogger Auth Error: {e}"); traceback.print_exc(); return None

def post_to_facebook_system(page_access_token, page_id, message, link):
    try:
        graph = facebook.GraphAPI(access_token=page_access_token)
        graph.put_object(parent_object=page_id, connection_name='feed', message=message, link=link)
        print("✅ Posted to Facebook!")
    except Exception as e: print(f"FB skipped: {e}")

def post_to_telegram(token, chat_id, message, link):
    try:
        text = f"{message}\n\n🔗 Read Full Story: {link}"
        url = TELEGRAM_URL_TEMPLATE.format(token=token)
        r = requests.post(url, json={"chat_id": chat_id, "text": text}, timeout=12)
        if r.status_code == 200: print("🚀 Posted to Telegram!")
    except Exception as e: print(f"Telegram skipped: {e}")

def main():
    selected_entry = None
    chosen_category = "Schengen & Europe EU Rules"
    source_link = "https://trttnews24bd.blogspot.com"
    headers = {'User-Agent': 'Mozilla/5.0'}
    for cat_name, feed_url in FEEDS.items():
        print(f"📡 Scanning: {cat_name}...")
        try:
            response = requests.get(feed_url, headers=headers, timeout=15)
            if response.status_code == 200:
                feed = feedparser.parse(response.text)
                if feed.entries:
                    selected_entry = feed.entries[0]
                    chosen_category = cat_name
                    source_link = selected_entry.get('link', feed_url)
                    print(f"🎯 Found: {selected_entry.title[:60]}")
                    break
        except Exception as e: print(f"Skipping: {e}")
    if not selected_entry: print("❌ No entries found"); exit(0)

    summary_text = selected_entry.get('summary', selected_entry.title)
    image_url = get_featured_image(chosen_category)
    draft = call_groq_draft(f"Write comprehensive news article based on: {selected_entry.title}. Summary: {summary_text}. Category: {chosen_category}") or summary_text
    final_response = call_gemini_modifier(draft, chosen_category, selected_entry.title, summary_text, source_link)

    try:
        if final_response:
            json_clean = re.sub(r'```(?:json)?\s*|\s*```', '', final_response.strip(), flags=re.MULTILINE)
            data = json.loads(json_clean)
            seo_title = data.get("seo_title", f"{chosen_category} 2027: {selected_entry.title[:80]}")
            meta_desc = data.get("meta_description", summary_text[:145])[:150]
            fb_caption = data.get("fb_caption", seo_title)

            article_body_html = f"""
            <p><i><b>Overview:</b> {meta_desc}</i></p>
            <div style="margin:15px 0;"><img src='{image_url}' alt='{seo_title}' style='width:100%; border-radius:8px'/></div>
            {data.get("article_body", f"<p>{summary_text}</p>")}
            <hr/>
            <p><small>Source & Reference: <a href="{source_link}" target="_blank" rel="nofollow">Original Report</a> | Category: {chosen_category}</small></p>
            """

            blogger_service = get_blogger()
            if blogger_service:
                blog_id = os.environ.get("BLOGGER_BLOG_ID") or os.environ.get("BLOGGER_ID")
                if not blog_id:
                    blogs = blogger_service.blogs().listByUser(userId='self').execute()
                    if blogs.get('items'): blog_id = blogs['items'][0]['id']

                loc = LOCATION_MAP.get(chosen_category, LOCATION_MAP["default"])

                post_body = {
                    "kind": "blogger#post",
                    "title": seo_title,
                    "content": article_body_html,
                    "labels": [chosen_category, "Official Updates", "Schengen Visa 2027"],
                    "location": {
                        "name": loc["name"],
                        "lat": loc["lat"],
                        "lng": loc["lng"]
                    }
                }

                result = blogger_service.posts().insert(blogId=blog_id, body=post_body, isDraft=False, fetchImages=True).execute()
                link = result.get('url')
                print(f"✅ PUBLISHED: {link} with Location {loc['name']}")

                fb_token = os.environ.get("FB_PAGE_ACCESS_TOKEN")
                fb_id = os.environ.get("FB_PAGE_ID")
                if fb_token and fb_id: post_to_facebook_system(fb_token, fb_id, fb_caption, link)

                tg_token = os.environ.get("TELEGRAM_BOT_TOKEN")
                tg_chat = os.environ.get("TELEGRAM_CHAT_ID")
                if tg_token and tg_chat: post_to_telegram(tg_token, tg_chat, fb_caption, link)

    except Exception as e:
        print(f"❌ Error: {e}"); traceback.print_exc()

if __name__ == "__main__":
    main()
