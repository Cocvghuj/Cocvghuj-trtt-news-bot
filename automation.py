import feedparser, os, json, requests, random, re, traceback, datetime, time
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import facebook

GEMINI_MODELS = ["gemini-3.8-flash", "gemini-flash-latest"]
GROQ_MODELS = ["openai/gpt-oss-20b", "openai/gpt-oss-120b"]

TELEGRAM_URL_TEMPLATE = "https://api.telegram.org/bot{token}/sendMessage"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

HISTORY_FILE = "posted_history.json"

FEEDS = {
    "Schengen & EU Rules": "https://www.schengenvisainfo.com/feed/",
    "Europe Visa Latest": "https://visaguide.world/news/feed/",
    "Italy & Schengen Updates": "https://www.thelocal.it/feed/",
    "Germany Work Visa": "https://www.dw.com/export/rss?sectionId=30973",
    "UK Visa and Immigration": "https://www.freemovement.org.uk/feed/",
    "France Visa News": "https://visaguide.world/europe/france/visa/feed/",
    "Europe Breaking News": "https://www.euronews.com/rss?format=mrss",
    "Global Tech & AI": "https://techcrunch.com/feed/"
}

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
    "Europe": {"name": "Brussels, Belgium", "lat": 50.8503, "lng": 4.3517},
    "default": {"name": "Milan, Italy", "lat": 45.4642, "lng": 9.1900}
}

def load_history():
    if os.path.exists(HISTORY_FILE):
        try: return json.load(open(HISTORY_FILE))
        except: return []
    return []

def save_history(link):
    hist = load_history()
    if link not in hist:
        hist.append(link)
        hist = hist[-100:]
        open(HISTORY_FILE, "w").write(json.dumps(hist))

def get_smart_location(title, category):
    text = (title + " " + category).lower()
    if "italy" in text or "milan" in text:
        return COUNTRY_LOCATIONS["Italy"]
    if "germany" in text or "berlin" in text:
        return COUNTRY_LOCATIONS["Germany"]
    if "france" in text or "paris" in text:
        return COUNTRY_LOCATIONS["France"]
    if "uk" in text or "london" in text or "britain" in text:
        return COUNTRY_LOCATIONS["UK"]
    if "europe" in text or "schengen" in text or "eu " in text:
        return COUNTRY_LOCATIONS["Europe"]
    return COUNTRY_LOCATIONS["default"]

def get_featured_image(title, category=""):
    try:
        key = os.environ.get("UNSPLASH_ACCESS_KEY")
        text = (title + " " + category).lower()

        if "tech" in text or "ai" in text or "ram" in text: q = "technology innovation computer laptop"
        elif "france" in text: q = "Paris France landmark"
        elif "germany" in text: q = "Berlin Germany city"
        elif "italy" in text: q = "Italy landscape city"
        elif "uk" in text or "britain" in text or "london" in text: q = "London Big Ben UK"
        elif "schengen" in text or "europe" in text: q = "Europe travel architecture"
        else: q = "visa passport travel"

        if key:
            url = f"https://api.unsplash.com/search/photos?query={q}&per_page=1&orientation=landscape&client_id={key}"
            r = requests.get(url, timeout=15).json()
            if r.get('results'):
                img = r['results'][0]['urls']['regular']
                print(f"✅ Image found for {q}")
                return img
    except Exception as e:
        print(f"Image error: {e}")

    return f"https://picsum.photos/seed/{random.randint(1,1000000)}/800/600"

def call_gemini(cat, title, summary, source_link):
    k = os.environ.get("GEMINI_API_KEY")
    if not k: return None
    p = f"""Write a detailed SEO news article in English, 700+ words.
Title: {title}
Summary: {summary}
Category: {cat}
Must include: h2 headings, bullet points, a comparison table, and FAQ.
Return ONLY valid JSON without line breaks inside values.
Keys: seo_title, meta_description (max 148 chars, no double quotes), article_body (HTML with h2, p, ul, table), fb_caption
"""
    for model in GEMINI_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={k}"
        try:
            print(f"🔄 Trying Gemini {model}...")
            r = requests.post(url, json={"contents": [{"parts": [{"text": p}]}]}, timeout=90)
            if r.status_code == 200 and "candidates" in r.json():
                txt = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                match = re.search(r'\{.*\}', txt, re.DOTALL)
                if match:
                    cleaned = match.group(0).replace('\n', ' ').replace('\r', '')
                    json.loads(cleaned)
                    return cleaned
        except Exception as e:
            print(f"⚠️ {model} error: {e}")
            time.sleep(3)
    return None

def call_groq_backup(cat, title, summary, source_link):
    k = os.environ.get("GROQ_API_KEY")
    if not k: return None
    p = f"""Write a detailed SEO news article in English, 700+ words.
Title: {title}
Summary: {summary}
Category: {cat}
Must include: h2 headings, bullet points, a comparison table, and FAQ.
Return ONLY valid JSON without line breaks inside values.
Keys: seo_title, meta_description (max 148 chars, no double quotes), article_body (HTML with h2, p, ul, table), fb_caption
"""
    for model in GROQ_MODELS:
        try:
            print(f"🔄 Trying Groq {model}...")
            r = requests.post(GROQ_URL, headers={"Authorization": f"Bearer {k}"}, json={"model": model, "messages": [{"role": "user", "content": p}], "temperature": 0.2}, timeout=60)
            if r.status_code == 200:
                txt = r.json()["choices"][0]["message"]["content"]
                match = re.search(r'\{.*\}', txt, re.DOTALL)
                if match:
                    cleaned = match.group(0).replace('\n', ' ').replace('\r', '')
                    json.loads(cleaned)
                    return cleaned
        except Exception as e:
            print(f"Groq error: {e}")
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
        r = requests.post(url, json={"chat_id": chat_id, "text": text}, timeout=15)
        if r.status_code == 200: print("🚀 Posted to Telegram!")
    except Exception as e: print(f"❌ Telegram skipped: {e}")

def main():
    history = load_history()
    selected_entry = None; chosen_category = "Europe Breaking News"; source_link = "https://trttnews24bd.blogspot.com"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    feed_items = list(FEEDS.items())
    random.shuffle(feed_items)

    for cat_name, feed_url in feed_items:
        print(f"📡 Scanning: {cat_name}...")
        try:
            response = requests.get(feed_url, headers=headers, timeout=15)
            if response.status_code == 200:
                feed = feedparser.parse(response.text)
                for entry in feed.entries[:5]:
                    link = entry.get('link')
                    if link and link not in history:
                        selected_entry = entry
                        chosen_category = cat_name
                        source_link = link
                        print(f"🎯 Found new entry from [{cat_name}]: {selected_entry.title[:60]}")
                        break
                if selected_entry: break
        except Exception as e: print(f"Skipping feed error: {e}")
        
    if not selected_entry: 
        print("❌ No new unposted entries found")
        return

    summary_text = selected_entry.get('summary', selected_entry.title)
    image_url = get_featured_image(selected_entry.title, chosen_category)
    
    final_response = call_gemini(chosen_category, selected_entry.title, summary_text, source_link)
    if not final_response:
        print("⚠️ Gemini failed, trying Groq Backup...")
        final_response = call_groq_backup(chosen_category, selected_entry.title, summary_text, source_link)
    
    current_date_tag = f" ({datetime.datetime.utcnow().strftime('%b %d, %Y')})"
    
    if not final_response:
        print("❌ All AI failed, using RICH SEO Fallback")
        seo_title = f"{chosen_category}: {selected_entry.title[:70]}{current_date_tag}"
        
        raw_desc = summary_text
        clean = re.sub(r'[^a-zA-Z0-9,.\-:\(\)$]', ' ', raw_desc)
        meta_desc = ' '.join(clean.split())[:148].strip()
        if len(meta_desc) < 20:
            meta_desc = re.sub(r'[^a-zA-Z0-9,.\-]', ' ', summary_text)[:148].strip()

        fb_caption = f"🚨 {selected_entry.title} | Full details inside #{chosen_category.replace(' ', '')} #EuropeNews"
        article_body_html = f"""
        <h2>{selected_entry.title}</h2>
        <p><b>Overview & Editorial Insight:</b> {summary_text}</p>
        <p>This comprehensive report outlines essential regional and international updates.</p>
        <h2>Key Highlights</h2>
        <ul>
          <li>Core Policy Changes & Impact</li>
          <li>Official Directives and Timelines</li>
          <li>Global Expert Analysis</li>
        </ul>
        <h2>Overview & Comparison Table</h2>
        <table border='1' cellpadding='8' style='width:100%; border-collapse:collapse;'>
          <tr><th>Parameter</th><th>Details</th></tr>
          <tr><td>Impact Level</td><td>High Significance</td></tr>
          <tr><td>Analysis Standard</td><td>Comprehensive Review</td></tr>
          <tr><td>Status</td><td>Active Development</td></tr>
        </table>
        <p><b>Reference Source:</b> <a href='{source_link}' target='_blank' rel='nofollow'>Official News Network</a></p>
        """
    else:
        try:
            data = json.loads(final_response)
            seo_title = data.get("seo_title", f"{chosen_category}: {selected_entry.title[:70]}")
            if not current_date_tag in seo_title:
                seo_title += current_date_tag
            
            raw_desc = data.get("meta_description") or data.get("seo_title") or summary_text
            clean = re.sub(r'[^a-zA-Z0-9,.\-:\(\)$]', ' ', raw_desc)
            meta_desc = ' '.join(clean.split())[:148].strip()
            if len(meta_desc) < 20:
                meta_desc = re.sub(r'[^a-zA-Z0-9,.\-]', ' ', summary_text)[:148].strip()
            print(f"DEBUG SearchDesc OK: {meta_desc}")

            fb_caption = data.get("fb_caption", seo_title)
            article_body_html = data.get("article_body", f"<p>{summary_text}</p>")
        except Exception as json_err:
            print(f"⚠️ JSON parsing error ({json_err}), using rich fallback.")
            seo_title = f"{chosen_category}: {selected_entry.title[:70]}{current_date_tag}"
            
            raw_desc = summary_text
            clean = re.sub(r'[^a-zA-Z0-9,.\-:\(\)$]', ' ', raw_desc)
            meta_desc = ' '.join(clean.split())[:148].strip()
            if len(meta_desc) < 20:
                meta_desc = re.sub(r'[^a-zA-Z0-9,.\-]', ' ', summary_text)[:148].strip()

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
          "author": {{"@type": "Organization", "name": "TRTT News 24 Editorial Team"}},
          "publisher": {{"@type": "Organization", "name": "TRTT News 24", "logo": {{"@type": "ImageObject", "url": "https://trttnews24bd.blogspot.com/favicon.ico"}}}}
        }}
        </script>
        """

        full_article_html = f"""
        {seo_schema}
        <p><i><b>Editorial Note:</b> {meta_desc}</i></p>
        <div style="margin:15px 0;"><img src='{image_url}' alt='{seo_title}' style='width:100%; border-radius:8px'/></div>
        {article_body_html}
        <hr/>
        <p><small>Original Source & Reference: <a href="{source_link}" target="_blank" rel="nofollow noopener">Verified News Wire</a></small></p>
        """

        blogger_service = get_blogger()
        if blogger_service:
            blog_id = os.environ.get("BLOGGER_ID") or os.environ.get("BLOGGER_BLOG_ID")
            if not blog_id:
                blogs = blogger_service.blogs().listByUser(userId='self').execute()
                if blogs.get('items'): blog_id = blogs['items'][0]['id']

            loc = get_smart_location(selected_entry.title, chosen_category)
            
            post_body = {
                "kind": "blogger#post", 
                "title": seo_title, 
                "content": full_article_html, 
                "searchDescription": meta_desc,
                "labels": [chosen_category, "Europe News", "Global Updates", "Breaking News"], 
                "location": {"name": loc["name"], "lat": loc["lat"], "lng": loc["lng"]}
            }
            
            # পোস্ট ইনসার্ট করো
            result = blogger_service.posts().insert(blogId=blog_id, body=post_body, isDraft=False, fetchImages=True).execute()
            link = result.get('url')
            post_id = result.get('id')
            print(f"✅ PUBLISHED: {link} under [{chosen_category}] with Location {loc['name']}")

            # গ্যারান্টিড ফিক্স: আলাদাভাবে Search Description প্যাচ করে দাও যাতে বক্সে লেখা ১০০% বসে যায়
            try:
                patch_body = {"searchDescription": meta_desc}
                blogger_service.posts().patch(blogId=blog_id, postId=post_id, body=patch_body).execute()
                print(f"✅ Search Description successfully patched: {meta_desc}")
            except Exception as patch_err:
                print(f"⚠️ Patch warning: {patch_err}")

            save_history(source_link)

            fb_token = os.environ.get("FB_PAGE_ACCESS_TOKEN")
            fb_id = os.environ.get("FB_PAGE_ID")
            if fb_token and fb_id: post_to_facebook_system(fb_token, fb_id, fb_caption, link)

            tg_token = os.environ.get("TELEGRAM_BOT_TOKEN")
            tg_chat = os.environ.get("TELEGRAM_CHAT_ID")
            if tg_token and tg_chat: post_to_telegram(tg_token, tg_chat, fb_caption, link)

    except Exception as e: print(f"❌ Error in publishing: {e}"); traceback.print_exc()

if __name__ == "__main__": main()
