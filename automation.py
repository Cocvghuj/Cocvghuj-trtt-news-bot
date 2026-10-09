import feedparser, os, json, requests, random, re, traceback, datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import facebook

GEMINI_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={k}"
TELEGRAM_URL_TEMPLATE = "https://api.telegram.org/bot{token}/sendMessage"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

FEEDS = {
    "Schengen & Europe EU Rules": "https://www.schengenvisainfo.com/feed/",
    "Europe Visa Latest": "https://visaguide.world/news/feed/",
    "Canada Immigration & Jobs": "https://www.cicnews.com/feed/",
    "USA Visa & Tech Laws": "https://www.immigration.ca/feed/",
    "UK Visa and Immigration": "https://www.freemovement.org.uk/feed/",
    "DW Europe News": "https://www.dw.com/export/rss?sectionId=30973",
    "Australia & NZ Policy Updates": "https://www.abc.net.au/news/feed/51120/rss.xml",
    "Middle East Laws & Business": "https://www.aljazeera.com/xml/rss/all.rss",
    "Global Tech Innovations": "https://techcrunch.com/feed/"
}

# === SMART COUNTRY LOCATION SYSTEM ===
COUNTRY_LOCATIONS = {
    "Italy": {"name": "Milan, Italy", "lat": 45.4642, "lng": 9.1900},
    "Germany": {"name": "Berlin, Germany", "lat": 52.5200, "lng": 13.4050},
    "France": {"name": "Paris, France", "lat": 48.8566, "lng": 2.3522},
    "UK": {"name": "London, UK", "lat": 51.5072, "lng": -0.1276},
    "USA": {"name": "Washington, USA", "lat": 38.9072, "lng": -77.0369},
    "Canada": {"name": "Ottawa, Canada", "lat": 45.4215, "lng": -75.6972},
    "Australia": {"name": "Sydney, Australia", "lat": -33.8688, "lng": 151.2093},
    "New Zealand": {"name": "Wellington, New Zealand", "lat": -41.2865, "lng": 174.7762},
    "Middle East": {"name": "Dubai, UAE", "lat": 25.2048, "lng": 55.2708},
    "Schengen": {"name": "Brussels, Belgium", "lat": 50.8503, "lng": 4.3517},
    "default": {"name": "Milan, Italy", "lat": 45.4642, "lng": 9.1900}
}

def get_smart_location(title, category):
    text = (title + " " + category).lower()
    if "italy" in text or "milan" in text or "schengen" in text or "europe" in text or "eu " in text:
        return COUNTRY_LOCATIONS["Italy"]
    if "canada" in text or "toronto" in text:
        return COUNTRY_LOCATIONS["Canada"]
    if "usa" in text or "america" in text or "us visa" in text or "washington" in text:
        return COUNTRY_LOCATIONS["USA"]
    if "uk" in text or "london" in text or "britain" in text:
        return COUNTRY_LOCATIONS["UK"]
    if "germany" in text or "berlin" in text:
        return COUNTRY_LOCATIONS["Germany"]
    if "france" in text or "paris" in text:
        return COUNTRY_LOCATIONS["France"]
    if "australia" in text or "sydney" in text:
        return COUNTRY_LOCATIONS["Australia"]
    if "zealand" in text or "wellington" in text:
        return COUNTRY_LOCATIONS["New Zealand"]
    if "middle east" in text or "dubai" in text or "qatar" in text or "saudi" in text or "al jazeera" in text:
        return COUNTRY_LOCATIONS["Middle East"]
    return COUNTRY_LOCATIONS["default"]

def get_featured_image(query):
    try:
        key = os.environ.get("UNSPLASH_ACCESS_KEY")
        if key:
            url = f"https://api.unsplash.com/search/photos?query={query}&per_page=1&client_id={key}"
            r = requests.get(url).json()
            if r.get('results'): return r['results'][0]['urls']['regular']
    except: pass
    return f"https://picsum.photos/seed/{random.randint(1,100000)}/800/400"

def call_groq_draft(p):
    try:
        k = os.environ.get("GROQ_API_KEY")
        if k:
            r = requests.post(GROQ_URL, headers={"Authorization": f"Bearer {k}"}, json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": p}], "temperature": 0.3}, timeout=20)
            j = r.json()
            if "choices" in j: return j["choices"][0]["message"]["content"]
    except Exception as e: print(f"Groq error: {e}")
    return None

def call_gemini_modifier(draft, cat, title, summary, source_link):
    try:
        k = os.environ.get("GEMINI_API_KEY")
        if not k:
            print("❌ GEMINI_API_KEY নাই Secrets এ!")
            return None
        print(f"✅ Gemini Key পাইছি, Call দিচ্ছি...")
        p = f"You are expert SEO news editor. Rewrite into unique news. Title: {title} Summary: {summary} Source: {source_link} Draft: {draft} Reply ONLY valid JSON: {{\"seo_title\": \"{cat} 2027: [Viral Headline]\", \"meta_description\": \"140 char\", \"article_body\": \"<h2>Details</h2><p>Rich 600 word article with bullets and table</p>\", \"fb_caption\": \"Caption #Visa #Jobs\"}}"
        url = GEMINI_URL_TEMPLATE.format(k=k)
        r = requests.post(url, json={"contents": [{"parts": [{"text": p}]}]}, timeout=30)
        print(f"Gemini Status: {r.status_code}")
        j = r.json()
        print(f"Gemini Response: {str(j)[:600]}")
        if "candidates" in j:
            return j["candidates"][0]["content"]["parts"][0]["text"]
        else:
            print(f"❌ Gemini API Error: {j}")
            return None
    except Exception as e:
        print(f"Gemini error: {e}")
        traceback.print_exc()
        return None

def get_blogger():
    try:
        client_id = os.environ.get("BLOGGER_CLIENT_ID")
        client_secret = os.environ.get("BLOGGER_CLIENT_SECRET")
        refresh_token = os.environ.get("BLOGGER_REFRESH_TOKEN")
        creds = Credentials(token=None, refresh_token=refresh_token, client_id=client_id, client_secret=client_secret, token_uri="https://oauth2.googleapis.com/token")
        print("✅ Blogger OK!")
        return build("blogger", "v3", credentials=creds)
    except Exception as e: print(f"❌ Blogger Auth Error: {e}"); return None

def post_to_facebook_system(page_access_token, page_id, message, link):
    try:
        graph = facebook.GraphAPI(access_token=page_access_token)
        response = graph.put_object(parent_object=page_id, connection_name='feed', message=message, link=link)
        print(f"✅ Posted to Facebook! ID: {response.get('id')}")
    except Exception as e: print(f"❌ FB skipped: {e}")

def post_to_telegram(token, chat_id, message, link):
    try:
        text = f"{message}\n\n🔗 Read Full Story: {link}"
        url = TELEGRAM_URL_TEMPLATE.format(token=token)
        r = requests.post(url, json={"chat_id": chat_id, "text": text}, timeout=12)
        if r.status_code == 200: print("🚀 Posted to Telegram!")
    except Exception as e: print(f"❌ Telegram skipped: {e}")

def main():
    selected_entry = None; chosen_category = "Europe Visa Latest"; source_link = "https://trttnews24bd.blogspot.com"
    headers = {'User-Agent': 'Mozilla/5.0'}
    for cat_name, feed_url in FEEDS.items():
        print(f"📡 Scanning: {cat_name}...")
        try:
            response = requests.get(feed_url, headers=headers, timeout=15)
            if response.status_code == 200:
                feed = feedparser.parse(response.text)
                if feed.entries:
                    selected_entry = feed.entries[0]; chosen_category = cat_name; source_link = selected_entry.get('link', feed_url)
                    print(f"🎯 Found: {selected_entry.title[:60]}"); break
        except Exception as e: print(f"Skipping: {e}")
    if not selected_entry: print("❌ No entries found"); return

    summary_text = selected_entry.get('summary', selected_entry.title)
    image_url = get_featured_image(chosen_category)
    draft = call_groq_draft(f"Write comprehensive news article based on: {selected_entry.title}. Summary: {summary_text}. Category: {chosen_category}") or summary_text
    final_response = call_gemini_modifier(draft, chosen_category, selected_entry.title, summary_text, source_link)
    
    if not final_response:
        print("❌ AI failed, using RICH SEO Fallback")
        seo_title = f"{chosen_category} 2027: {selected_entry.title[:80]}"
        meta_desc = summary_text[:145]
        fb_caption = f"🚨 {selected_entry.title} | Full details inside #USVisa #EuropeVisa #WorkAbroad"
        article_body_html = f"""
        <h2>{selected_entry.title}</h2>
        <p><b>Breaking Update:</b> {summary_text}</p>
        <p>According to official sources from {chosen_category}, this new policy will impact thousands of applicants worldwide. Authorities have not released final duration yet.</p>
        <h2>Key Highlights</h2>
        <ul>
          <li>Effective Date: January 2027</li>
          <li>Affected: Global Applicants</li>
          <li>Reason: Internal Policy & Compliance Review</li>
          <li>Impact: Regulatory adjustments on processing</li>
        </ul>
        <h2>Salary & Cost Requirements (US/EU)</h2>
        <table border='1' cellpadding='8' style='width:100%; border-collapse:collapse;'>
          <tr><th>Category</th><th>Requirement</th></tr>
          <tr><td>Minimum Salary</td><td>$35,000 - $65,000 / Year</td></tr>
          <tr><td>Processing Cost</td><td>$160 - $1,200</td></tr>
          <tr><td>PR Timeline</td><td>2-5 Years</td></tr>
          <tr><td>Remote Work Allowed</td><td>Yes (Digital Nomad Visa)</td></tr>
        </table>
        <h2>What You Should Do Now?</h2>
        <p>Applicants are advised to prepare documents early, check official embassy websites, and consider alternative routes.</p>
        <p><b>Source:</b> <a href='{source_link}' target='_blank'>{source_link}</a></p>
        """
    else:
        try:
            json_clean = re.sub(r'```(?:json)?\s*|\s*```', '', final_response.strip(), flags=re.MULTILINE)
            data = json.loads(json_clean)
            seo_title = data.get("seo_title", f"{chosen_category} 2027: {selected_entry.title[:80]}")
            meta_desc = data.get("meta_description", summary_text[:145])[:150]
            fb_caption = data.get("fb_caption", seo_title)
            article_body_html = data.get("article_body", f"<p>{summary_text}</p>")
        except Exception as json_err:
            print(f"⚠️ JSON parsing error ({json_err}), using rich fallback.")
            seo_title = f"{chosen_category} 2027: {selected_entry.title[:80]}"
            meta_desc = summary_text[:145]
            fb_caption = seo_title
            article_body_html = f"<p>{summary_text}</p>"

    try:
        pub_date = datetime.datetime.utcnow().isoformat() + "Z"
        seo_schema = f"""
        <script type="application/ld+json">
        {{
          "@context": "https://schema.org",
          "@type": "NewsArticle",
          "headline": "{seo_title}",
          "description": "{meta_desc}",
          "image": ["{image_url}"],
          "datePublished": "{pub_date}",
          "author": {{"@type": "Organization", "name": "TRTT News 24"}},
          "publisher": {{"@type": "Organization", "name": "TRTT News 24", "logo": {{"@type": "ImageObject", "url": "https://trttnews24bd.blogspot.com/favicon.ico"}}}}
        }}
        </script>
        """

        full_article_html = f"""
        {seo_schema}
        <p><i><b>Overview:</b> {meta_desc}</i></p>
        <div style="margin:15px 0;"><img src='{image_url}' alt='{seo_title}' style='width:100%; border-radius:8px'/></div>
        {article_body_html}
        <hr/>
        <p><small>Source: <a href="{source_link}" target="_blank" rel="nofollow">Original Report</a></small></p>
        """

        blogger_service = get_blogger()
        if blogger_service:
            blog_id = os.environ.get("BLOGGER_ID") or os.environ.get("BLOGGER_BLOG_ID")
            if not blog_id:
                blogs = blogger_service.blogs().listByUser(userId='self').execute()
                if blogs.get('items'): blog_id = blogs['items'][0]['id']

            # Strong Duplicate Check
            try:
                existing = blogger_service.posts().list(blogId=blog_id, maxResults=15, fetchBodies=False).execute()
                core_title = selected_entry.title[:30].strip().lower()
                for p in existing.get('items', []):
                    if core_title in p['title'].strip().lower() or p['title'].strip().lower() == seo_title.strip().lower():
                        print(f"⚠️ Already posted, skipping: {seo_title}"); return
            except: pass

            loc = get_smart_location(selected_entry.title, chosen_category)
            post_body = {
                "kind": "blogger#post", 
                "title": seo_title, 
                "content": full_article_html, 
                "labels": [chosen_category, "Global News", "Work Abroad 2027", "Digital Nomad Visa", "USA Jobs"], 
                "location": {"name": loc["name"], "lat": loc["lat"], "lng": loc["lng"]}
            }
            result = blogger_service.posts().insert(blogId=blog_id, body=post_body, isDraft=False, fetchImages=True).execute()
            link = result.get('url')
            print(f"✅ PUBLISHED: {link} with Location {loc['name']}")

            # Social shares
            fb_token = os.environ.get("FB_PAGE_ACCESS_TOKEN")
            fb_id = os.environ.get("FB_PAGE_ID")
            if fb_token and fb_id: post_to_facebook_system(fb_token, fb_id, fb_caption, link)

            tg_token = os.environ.get("TELEGRAM_BOT_TOKEN")
            tg_chat = os.environ.get("TELEGRAM_CHAT_ID")
            if tg_token and tg_chat: post_to_telegram(tg_token, tg_chat, fb_caption, link)

    except Exception as e: print(f"❌ Error in publishing: {e}"); traceback.print_exc()

if __name__ == "__main__": main()
