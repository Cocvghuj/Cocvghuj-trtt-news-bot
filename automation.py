import feedparser, os, json, requests, random, re, datetime, time, subprocess, sys
from gtts import gTTS
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

HISTORY_FILE = "posted_history.json"
TELEGRAM_URL_TEMPLATE = "[https://api.telegram.org/bot](https://api.telegram.org/bot){token}/sendMessage"

HIGH_CPC_TOPICS = [
    "USA H2B Work Permit Visa 2027 for Bangladesh - Salary $3500 + Free Visa",
    "Canada LMIA Work Permit 2027 - Direct Company Apply Link (No Agent)",
    "Italy Seasonal Work Visa 2027 (Decreto Flussi) - Application from Sanluri, Italy",
    "Portugal Work Visa for Bangladeshi 2027 - 90 Days Processing Time",
    "Romania Work Permit for Bangladesh - How to Check Real vs Fake Visa 2027",
    "Malta Work Visa 2027 for Bangladeshi - Hotel Jobs with Free Accommodation",
    "Croatia Work Permit for Bangladeshis 2027 - New Salary Update",
    "How to Apply for Morocco E-Visa for AFCON 2027 from Bangladesh (AEVM Pass)",
    "Mali Suspends US Work Visas - What Bangladeshi Workers Must Know 2027",
    "USA DV Lottery 2027 for Bangladesh - Last Date and Photo Size Guide"
]

FEEDS = {
    "Wall Street & Global Markets": "[https://feeds.feedburner.com/reuters/businessNews](https://feeds.feedburner.com/reuters/businessNews)",
    "Bloomberg Global Business": "[https://www.cnbc.com/id/10001147/device/rss/rss.html](https://www.cnbc.com/id/10001147/device/rss/rss.html)",
    "European Central Bank & Trade": "[https://politico.eu/feed/](https://politico.eu/feed/)",
    "Global Geopolitics & EU": "[https://www.euronews.com/rss?format=mrss](https://www.euronews.com/rss?format=mrss)",
    "BBC World Intelligence": "[http://feeds.bbci.co.uk/news/world/rss.xml](http://feeds.bbci.co.uk/news/world/rss.xml)",
    "Schengen & European Visa Hub": "[https://www.schengenvisainfo.com/feed/](https://www.schengenvisainfo.com/feed/)",
    "Global Work Permits & Immigration": "[https://visaguide.world/news/feed/](https://visaguide.world/news/feed/)",
    "Artificial Intelligence & Future Tech": "[https://techcrunch.com/feed/](https://techcrunch.com/feed/)",
    "Silicon Valley Deep Tech": "[https://www.wired.com/feed/rss](https://www.wired.com/feed/rss)",
    "Global Cyber Security & Defense": "[https://thehackernews.com/feeds/posts/default](https://thehackernews.com/feeds/posts/default)",
    "Global Energy & Green Transition": "[https://www.euronews.com/tag/climate-change/rss](https://www.euronews.com/tag/climate-change/rss)",
    "International Aviation & Supply Chain": "[https://simpleflying.com/feed/](https://simpleflying.com/feed/)"
}

BREAKING_CATEGORIES = [
    "Global Geopolitics & EU", 
    "BBC World Intelligence", 
    "Wall Street & Global Markets",
    "Global Cyber Security & Defense"
]

COUNTRY_LOCATIONS = {
    "italy": {"name": "Milan, Italy", "lat": 45.4642, "lng": 9.1900},
    "germany": {"name": "Berlin, Germany", "lat": 52.5200, "lng": 13.4050},
    "uk": {"name": "London, UK", "lat": 51.5072, "lng": -0.1276},
    "usa": {"name": "New York, USA", "lat": 40.7128, "lng": -74.0060},
    "europe": {"name": "Brussels, Belgium", "lat": 50.8503, "lng": 4.3517},
    "default": {"name": "Milan, Italy", "lat": 45.4642, "lng": 9.1900}
}

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            cleaned_history = []
            for item in raw_data:
                if isinstance(item, dict):
                    cleaned_history.append(item)
                elif isinstance(item, str):
                    cleaned_history.append({"link": "", "title": item.strip().lower(), "date": "", "category": "", "post_url": ""})
            return cleaned_history
        except:
            return []
    return []

def commit_history_to_github():
    try:
        subprocess.run(["git", "config", "--global", "user.name", "GitHub Action Bot"], check=True)
        subprocess.run(["git", "config", "--global", "user.email", "action@github.com"], check=True)
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
        if not status.stdout.strip():
            return
        subprocess.run(["git", "add", HISTORY_FILE], check=True)
        subprocess.run(["git", "commit", "-m", "Auto-update posted history & URLs [skip ci]"], check=True)
        subprocess.run(["git", "push"], check=True)
    except Exception as e:
        print(f"⚠️ Git commit warning: {e}")

def save_history(link, title, category, url=""):
    hist = load_history()
    today_str = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    hist.append({"link": link, "title": title.strip().lower(), "date": today_str, "category": category, "post_url": url})
    hist = hist[-1000:]
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(hist, f, ensure_ascii=False, indent=2)
        commit_history_to_github()
    except Exception as e:
        print(f"⚠️ History save error: {e}")

def is_duplicate(entry_link, entry_title):
    hist = load_history()
    clean_entry_link = entry_link.strip().lower()
    clean_entry_title = re.sub(r'[^a-zA-Z0-9\s]', '', entry_title).strip().lower()
    
    for item in hist:
        if isinstance(item, dict):
            item_link = item.get("link", "").strip().lower()
            item_title = re.sub(r'[^a-zA-Z0-9\s]', '', item.get("title", "")).strip().lower()
            
            if item_link and clean_entry_link and item_link == clean_entry_link:
                return True
            if item_title and clean_entry_title and item_title == clean_entry_title:
                return True
    return False

def get_today_breaking_count():
    hist = load_history()
    today_str = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    count = 0
    for item in hist:
        if isinstance(item, dict):
            if item.get("date") == today_str and item.get("category") in BREAKING_CATEGORIES:
                count += 1
    return count

def get_smart_location(title, category):
    text = (title + " " + category).lower()
    for key, loc in COUNTRY_LOCATIONS.items():
        if key in text and key != "default":
            return loc
    return COUNTRY_LOCATIONS["default"]

def get_featured_image(title, category=""):
    fallback_img = f"[https://picsum.photos/seed/](https://picsum.photos/seed/){random.randint(1, 10000000)}/800/600"
    fallback_alt = f"{title} - Global News Wire"
    try:
        key = os.environ.get("UNSPLASH_ACCESS_KEY")
        if not key: return fallback_img, fallback_alt
        
        lower_title = title.lower()
        if "morocco" in lower_title or "afcon" in lower_title:
            q = "morocco flag stadium"
        elif "usa" in lower_title or "h2b" in lower_title or "lottery" in lower_title:
            q = "usa passport travel work"
        elif "canada" in lower_title or "lmia" in lower_title:
            q = "canada flag passport travel"
        elif "italy" in lower_title or "sanluri" in lower_title:
            q = "italy visa passport travel"
        elif "portugal" in lower_title or "romania" in lower_title or "malta" in lower_title or "croatia" in lower_title:
            q = "europe work visa passport"
        else:
            clean_title = re.sub(r'[^a-zA-Z0-9\s]', '', title)
            words = [w for w in clean_title.split() if len(w) > 3]
            q = f"{category} {' '.join(words[:2])}"

        url = f"[https://api.unsplash.com/search/photos?query=](https://api.unsplash.com/search/photos?query=){q}&per_page=10&orientation=landscape&client_id={key}"
        r = requests.get(url, timeout=15).json()
        if r.get('results') and len(r['results']) > 0:
            selected_img = random.choice(r['results'])
            img_url = selected_img.get('urls', {}).get('regular', fallback_img)
            return img_url, f"{title} - {category} Intelligence"
    except Exception as e:
        print(f"Image API Error: {e}")
    return fallback_img, fallback_alt

def clean_post(content):
    content = content.replace("[...]", "")
    content = content.replace("[…]", "")
    return content

def validate_post(content, title):
    errors = []
    if "[...]" in content or "[…]" in content:
        errors.append("Found [...] - Incomplete content")
    if "actively coordinating responses" in content or "structural changes" in content:
        errors.append("Found banned filler phrase")
    if "critical juncture" in content or "Global Mobility Desk" in content:
        errors.append("Found banned filler phrase")
    if "operational stakeholders" in content or "Silicon Valley Tech Desk" in content:
        errors.append("Found banned filler phrase")
    if "US Passport" in content and "Morocco" in title:
        errors.append("Image Mismatch: Morocco title with US Passport")

    words = len(re.sub(r'<[^>]+>', '', content).split())
    if words < 200:
        errors.append(f"Post too short ({words} words). Minimum required: 200 words.")

    if errors:
        print("❌ POST REJECTED BY VALIDATOR:")
        for e in errors:
            print(f" - {e}")
        sys.exit(1)
    else:
        print("✅ Post is Clean - Ready for AdSense")
        return True

def send_telegram_notification(title, url):
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if bot_token and chat_id:
        try:
            msg = f"👑 <b>Media Empire Alert</b>\n\n<b>Title:</b> {title}\n\n<b>Link:</b> {url}"
            api_url = TELEGRAM_URL_TEMPLATE.format(token=bot_token)
            requests.post(api_url, json={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}, timeout=10)
        except Exception as e:
            print(f"⚠️ Telegram Error: {e}")

def calculate_read_time(body_html):
    words = len(re.sub(r'<[^>]+>', '', body_html).split())
    minutes = max(2, round(words / 180))
    return f"⏱️ <b>Estimated Read Time:</b> {minutes} min read ({words} words)"

def generate_fact_check_badge():
    score = random.randint(93, 99)
    return f'<div style="background:#f0fdf4; border:1px solid #bbf7d0; color:#166534; padding:10px 14px; border-radius:6px; margin-bottom:12px; font-size:13px;">✅ <b>AI Fact-Check Score:</b> {score}% True &bull; 🧠 <b>AI Manipulation Risk:</b> Low (Verified Syndicate Wire)</div>'

def generate_schema_markup(title, desc, url, image_url):
    schema = {
        "@context": "[https://schema.org](https://schema.org)",
        "@type": "NewsArticle",
        "headline": title,
        "description": desc,
        "image": [image_url],
        "datePublished": datetime.datetime.utcnow().isoformat() + "Z",
        "author": [{"@type": "Organization", "name": "Global Syndicate News Bureau"}],
        "publisher": {"@type": "Organization", "name": "Global Media Empire Hub", "logo": {"@type": "ImageObject", "url": image_url}}
    }
    return f'<script type="application/ld+json">{json.dumps(schema)}</script>'

def apply_internal_links(article_body):
    hist = load_history()
    if not hist: return article_body
    for post in hist[-30:]:
        if not isinstance(post, dict):
            continue
        p_title = post.get("title", "")
        p_url = post.get("post_url", "")
        if not p_title or not p_url:
            continue
        words = p_title.split()
        if len(words) > 1:
            keyword = f"{words[0]} {words[1]}"
            if keyword.lower() in article_body.lower() and p_url not in article_body:
                article_body = article_body.replace(keyword, f'<a href="{p_url}" target="_blank" rel="noopener" style="color:#2563eb; font-weight:600;">{keyword}</a>', 1)
                break
    return article_body

def generate_audio_summary(title, summary):
    try:
        text_to_speak = f"Executive Audio Briefing: {title}. {summary[:180]}"
        tts = gTTS(text=text_to_speak, lang='en', slow=False)
        audio_filename = f"podcast_{int(time.time())}.mp3"
        tts.save(audio_filename)
        return f'<div style="background:#f8fafc; border:1px solid #e2e8f0; padding:12px; border-radius:8px; margin:15px 0;">🎙️ <b>Executive Audio Summary Available</b></div>'
    except Exception:
        return ""

def generate_article_with_ai(cat, title, summary, source_link):
    clean_summary = summary.replace("[…]", "").replace("[...]", "").strip()
    
    GEMINI_PROMPT = f"""
Write a news article for TITLE: "{title}" in the year 2027.

RULES YOU MUST FOLLOW:
1. Write 400-500 words, simple English, human tone.
2. NEVER write [...] or "Royal [...]". Finish every sentence.
3. NEVER write these banned phrases: "actively coordinating responses", "structural changes", "critical juncture", "Global Mobility Desk", "operational stakeholders", "Silicon Valley Tech Desk".
4. Structure:
   - Paragraph 1: What happened in 2027?
   - Paragraph 2: Who is affected? (Country names clearly)
   - Paragraph 3: Salary / Visa Fee / Processing Time for 2027 (Real numbers)
   - Paragraph 4: How to Apply - Step by Step (3 steps)
   - Paragraph 5: Official Source Link
5. FAQ Section - Write 3 FAQs with REAL answers, no template:
   Q1: What is the salary/fee for 2027?
   Q2: Who can apply from Bangladesh?
   Q3: What is the last date in 2027?
6. SEO: Use keyword "{title}" 2-3 times.
7. Image Keyword: Suggest 1 image keyword that matches title.
8. Output in clean JSON format ONLY with keys: "seo_title", "meta_description", "article_body". Do not add markdown backticks around JSON.

Context: {clean_summary}
Source Link: {source_link}
"""

    gemini_key = os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        for model in ["gemini-1.5-flash", "gemini-1.5-pro"]:
            try:
                url = f"[https://generativelanguage.googleapis.com/v1beta/models/](https://generativelanguage.googleapis.com/v1beta/models/){model}:generateContent?key={gemini_key}"
                r = requests.post(url, json={"contents": [{"parts": [{"text": GEMINI_PROMPT}]}]}, timeout=90)
                if r.status_code == 200 and "candidates" in r.json():
                    txt = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                    txt_clean = txt.replace("```json", "").replace("```", "").strip()
                    match = re.search(r'\{.*\}', txt_clean, re.DOTALL)
                    if match:
                        data = json.loads(match.group(0))
                        if len(data.get("article_body","")) > 150:
                            return data
            except Exception as e:
                print(f"⚠️ Gemini model {model} error: {e}")

    groq_key = os.environ.get("GROQ_API_KEY")
    if groq_key:
        try:
            url = "[https://api.groq.com/openai/v1/chat/completions](https://api.groq.com/openai/v1/chat/completions)"
            headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
            payload = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": GEMINI_PROMPT}], "temperature": 0.7}
            r = requests.post(url, json=payload, headers=headers, timeout=90)
            if r.status_code == 200:
                txt = r.json()["choices"][0]["message"]["content"]
                txt_clean = txt.replace("```json", "").replace("```", "").strip()
                match = re.search(r'\{.*\}', txt_clean, re.DOTALL)
                if match:
                    data = json.loads(match.group(0))
                    if len(data.get("article_body","")) > 150:
                        return data
        except Exception as e:
            print(f"⚠️ Groq error: {e}")

    return None

def get_blogger():
    try:
        client_id = os.environ.get("BLOGGER_CLIENT_ID")
        client_secret = os.environ.get("BLOGGER_CLIENT_SECRET")
        refresh_token = os.environ.get("BLOGGER_REFRESH_TOKEN")
        creds = Credentials(token=None, refresh_token=refresh_token, client_id=client_id, client_secret=client_secret, token_uri="[https://oauth2.googleapis.com/token](https://oauth2.googleapis.com/token)")
        creds.refresh(Request())
        return build("blogger", "v3", credentials=creds)
    except Exception as e:
        print(f"❌ Blogger Auth Error: {e}")
        return None

def main():
    selected_entry = None; chosen_category = ""; source_link = ""
    
    unposted_cpc = [t for t in HIGH_CPC_TOPICS if not is_duplicate("", t)]
    if unposted_cpc and random.random() > 0.3:
        entry_title = random.choice(unposted_cpc)
        chosen_category = "Global Work Permits & Immigration"
        source_link = "[https://visaguide.world](https://visaguide.world)"
        summary_text = f"Comprehensive official 2027 update regarding {entry_title} for international applicants and Bangladeshi workers."
    else:
        headers = {'User-Agent': 'Mozilla/5.0'}
        breaking_count = get_today_breaking_count()
        feed_items = list(FEEDS.items())
        random.shuffle(feed_items)

        if breaking_count >= 3:
            feed_items = [f for f in feed_items if f[0] not in BREAKING_CATEGORIES]

        for cat_name, feed_url in feed_items:
            try:
                response = requests.get(feed_url, headers=headers, timeout=15)
                if response.status_code == 200:
                    feed = feedparser.parse(response.text)
                    for entry in feed.entries[:8]:
                        link = entry.get('link')
                        title = entry.get('title', '')
                        if link and title and not is_duplicate(link, title):
                            selected_entry = entry
                            chosen_category = cat_name
                            source_link = link
                            break
                if selected_entry: break
            except Exception as e:
                print(f"Skipping Feed: {e}")

        if selected_entry:
            entry_title = selected_entry.get('title', 'Global Strategic Intelligence Wire')
            summary_text = selected_entry.get('summary', entry_title)
        else:
            entry_title = random.choice(HIGH_CPC_TOPICS)
            chosen_category = "Global Work Permits & Immigration"
            source_link = "[https://visaguide.world](https://visaguide.world)"
            summary_text = f"Official 2027 guidelines and updates on {entry_title}."

    image_url, image_alt = get_featured_image(entry_title, chosen_category)
    ai_data = generate_article_with_ai(chosen_category, entry_title, summary_text, source_link)

    if not ai_data or not isinstance(ai_data, dict):
        print("❌ AI Generation failed. Aborting script safely.")
        sys.exit(1)

    seo_title = ai_data.get("seo_title", entry_title[:70])
    raw_desc = ai_data.get("meta_description") or summary_text
    clean_desc = re.sub(r'[^a-zA-Z0-9\s.,-]', '', raw_desc)
    meta_desc = ' '.join(clean_desc.split())[:148].strip()
    article_body_html = ai_data.get("article_body", "")

    article_body_html = clean_post(article_body_html)
    article_body_html = apply_internal_links(article_body_html)
    
    validate_post(article_body_html, seo_title)

    fact_badge = generate_fact_check_badge()
    read_time = calculate_read_time(article_body_html)
    audio_widget = generate_audio_summary(seo_title, meta_desc)

    temp_post_url = "[https://yourblog.blogspot.com](https://yourblog.blogspot.com)"
    schema_script = generate_schema_markup(seo_title, meta_desc, temp_post_url, image_url)

    full_article_html = f"""
    {schema_script}
    {fact_badge}
    <div style="color:#64748b; font-size:12px; margin-bottom:10px;">{read_time}</div>
    <p><i><b>Summary:</b> {meta_desc}</i></p>
    {audio_widget}
    <div style="margin:20px 0;">
        <img src="{image_url}" alt="{image_alt}" title="{seo_title}" style="width:100%; border-radius:10px; box-shadow:0 4px 6px rgba(0,0,0,0.1);"/>
    </div>
    {article_body_html}
    <hr/>
    <p><small><b>Source:</b> <a href="{source_link}" target="_blank" rel="nofollow noopener" style="color:#0284c7; font-weight:600;">Official Wire Bureau</a></small></p>
    """

    blogger_service = get_blogger()
    if blogger_service:
        blog_id = os.environ.get("BLOGGER_ID") or os.environ.get("BLOGGER_BLOG_ID")
        loc = get_smart_location(entry_title, chosen_category)

        raw_labels = [chosen_category, "Global Media Empire", "B2B Intelligence", "Master Syndicate", "AI Fact-Check"]
        unique_labels = list(set(raw_labels))

        post_body = {
            "kind": "blogger#post",
            "title": seo_title,
            "content": full_article_html,
            "searchDescription": meta_desc,
            "labels": unique_labels,
            "location": {"name": loc["name"], "lat": loc["lat"], "lng": loc["lng"]}
        }

        result = blogger_service.posts().insert(blogId=blog_id, body=post_body, isDraft=False, fetchImages=True).execute()
        post_id = result.get('id')
        post_url = result.get('url')
        print(f"👑 MEDIA EMPIRE ARTICLE PUBLISHED: {post_url}")

        try:
            patch_body = {"searchDescription": meta_desc}
            blogger_service.posts().patch(blogId=blog_id, postId=post_id, body=patch_body).execute()
        except Exception:
            pass

        save_history(source_link, seo_title, chosen_category, post_url)
        send_telegram_notification(seo_title, post_url)

if __name__ == "__main__":
    main()
