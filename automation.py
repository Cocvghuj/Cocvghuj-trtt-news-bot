import feedparser, os, json, requests, random, re, datetime, time, subprocess, sys
from google import genai
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

HISTORY_FILE = "posted_history.json"
TELEGRAM_URL_TEMPLATE = "https://api.telegram.org/bot{token}/sendMessage"

# ডায়নামিক বছর নির্ধারণ (স্বয়ংক্রিয়ভাবে বর্তমান বছর নেবে)
CURRENT_YEAR = datetime.datetime.now().year

# ১. OFFICIAL & TRUSTED INTERNATIONAL DESKS (Brackets Removed)
OFFICIAL_DB = {
    "WORLD": {
        "desk": "Reuters World News Bureau", 
        "url": "https://www.reuters.com/world/", 
        "keyword": "World News International Politics Policy", 
        "label": "World News 24"
    },
    "BUSINESS": {
        "desk": "Global Business Intelligence Desk", 
        "url": "https://www.reuters.com/business/", 
        "keyword": "Global Business Enterprise Strategy Market", 
        "label": "Global Business Fix"
    },
    "VISA": {
        "desk": "Schengen Visa & Immigration Authority", 
        "url": "https://www.make-it-in-germany.com/en/", 
        "keyword": "Schengen Visa Immigration Regulation Policy", 
        "label": "Schengen Visa & Immigration"
    },
    "TECH": {
        "desk": "Global Technology Press Release", 
        "url": "https://www.reuters.com/technology/", 
        "keyword": "Global Technology AI Innovation Digital", 
        "label": "Technology & Education"
    },
    "STARTUP": {
        "desk": "European Business & Startup Desk", 
        "url": "https://vistos.mne.gov.pt/en/", 
        "keyword": "Europe Startup Business Investment Economy", 
        "label": "Europe Startup & Business"
    },
    "TOOLS": {
        "desk": "TRTT Developer & SEO Tools Desk", 
        "url": "https://www.google.com", 
        "keyword": "Free SEO Tools Digital Marketing Analytics", 
        "label": "Free Tools"
    }
}

def get_today_topics():
    today_weekday = datetime.datetime.utcnow().strftime('%A')
    
    # দৈনিক ৬টি অটো পোস্ট
    topics = [
        {"title": f"Global Geopolitical Shifts and International Policy Frameworks {CURRENT_YEAR}", "category": "WORLD"},
        {"title": f"Artificial Intelligence and Enterprise Technology Innovation Trends {CURRENT_YEAR}", "category": "TECH"},
        {"title": f"Global Cybersecurity and Digital Infrastructure Developments {CURRENT_YEAR}", "category": "TECH"},
        {"title": f"Global Business Growth Strategies and Market Adaptability {CURRENT_YEAR}", "category": "BUSINESS"},
        {"title": f"International Trade, Economic Policy and Market Analysis {CURRENT_YEAR}", "category": "BUSINESS"},
        {"title": f"Schengen Visa Regulations and Official Immigration Compliance {CURRENT_YEAR}", "category": "VISA"}
    ]
    
    # সাপ্তাহিক নির্দিষ্ট দিনের এক্সট্রা পোস্ট
    if today_weekday == "Monday":
        topics.append({"title": f"Europe Startup Ecosystem and Cross-Border Investment Guide {CURRENT_YEAR}", "category": "STARTUP"})
    elif today_weekday == "Sunday":
        topics.append({"title": f"Essential Free Digital Marketing and SEO Tools for Professionals {CURRENT_YEAR}", "category": "TOOLS"})
        
    return topics

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            return [item if isinstance(item, dict) else {"link": "", "title": item.strip().lower(), "date": "", "category": "", "post_url": ""} for item in raw_data]
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

def is_duplicate(entry_title):
    hist = load_history()
    clean_entry_title = re.sub(r'[^a-zA-Z0-9\s]', '', str(entry_title)).strip().lower()
    for item in hist:
        if isinstance(item, dict):
            item_title = re.sub(r'[^a-zA-Z0-9\s]', '', str(item.get("title", ""))).strip().lower()
            if item_title and clean_entry_title and item_title == clean_entry_title:
                return True
    return False

def get_featured_image(keyword):
    fallback_img = "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80"
    try:
        key = os.environ.get("UNSPLASH_ACCESS_KEY")
        if not key: return fallback_img
        url = f"https://api.unsplash.com/search/photos?query={keyword}&per_page=10&orientation=landscape&client_id={key}".strip()
        r = requests.get(url, timeout=15).json()
        if r.get('results') and len(r['results']) > 0:
            return random.choice(r['results']).get('urls', {}).get('regular', fallback_img)
    except Exception as e:
        print(f"Image API Error: {e}")
    return fallback_img

def send_telegram_notification(title, url):
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if bot_token and chat_id:
        try:
            msg = f"👑 <b>TRTT Draft Alert</b>\n\n<b>Title:</b> {title}\n\n<b>Status:</b> Saved as Draft"
            api_url = TELEGRAM_URL_TEMPLATE.format(token=bot_token)
            requests.post(api_url, json={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}, timeout=10)
        except Exception as e:
            print(f"⚠️ Telegram Error: {e}")

def generate_safe_news_with_fallback(topic: str, cat_key: str):
    info = OFFICIAL_DB[cat_key]
    
    prompt = f"""
SYSTEM: You are an experienced international journalist at TRTT NEWS 24 BD.
Write naturally, like an experienced human reporter covering global events. Avoid robotic or typical AI phrasing.

TOPIC: {topic}
OFFICIAL DESK SOURCE: {info['desk']}
REFERENCE URL: {info['url']}

WRITING INSTRUCTIONS:
1. Tone: Natural, engaging, human UK English, written in a professional journalistic narrative style. NO emojis inside the article text.
2. Personal Journalist Touch: Include EXACTLY ONE short personal story line or first-hand observational insight (e.g., "During my recent coverage at the international summit..." or "Speaking with a senior strategist last month in London, I observed...").
3. Length & Structure:
   - 800+ words.
   - Engaging opening lead with real-world impact.
   - Natural transition into detailed analysis using bold subheadings (H2).
   - Fact-based evergreen conclusions.
4. Compliance: Maintain high editorial standards, strictly avoid spammy phrasing, and ensure complete accuracy for the year {CURRENT_YEAR}.
"""

    gemini_key = os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        for attempt in range(3):
            try:
                client = genai.Client(api_key=gemini_key)
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                if response and response.text:
                    return response.text, info['label']
            except Exception as e:
                time.sleep(5)

    groq_key = os.environ.get("GROQ_API_KEY")
    if groq_key:
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2
            }
            r = requests.post(url, json=payload, headers=headers, timeout=60)
            if r.status_code == 200:
                return r.json()['choices'][0]['message']['content'], info['label']
        except Exception as e:
            print(f"Groq error: {e}")

    raise ValueError("API Failed")

def get_blogger():
    try:
        client_id = os.environ.get("BLOGGER_CLIENT_ID")
        client_secret = os.environ.get("BLOGGER_CLIENT_SECRET")
        refresh_token = os.environ.get("BLOGGER_REFRESH_TOKEN")
        creds = Credentials(token=None, refresh_token=refresh_token, client_id=client_id, client_secret=client_secret, token_uri="https://oauth2.googleapis.com/token")
        creds.refresh(Request())
        return build("blogger", "v3", credentials=creds)
    except Exception as e:
        print(f"❌ Blogger Auth Error: {e}")
        return None

def main():
    topics_to_post = get_today_topics()
    blogger_service = get_blogger()
    if not blogger_service:
        return

    blog_id = os.environ.get("BLOGGER_ID") or os.environ.get("BLOGGER_BLOG_ID")

    for item in topics_to_post:
        entry_title = item["title"]
        cat_key = item["category"]
        
        if is_duplicate(entry_title):
            print(f"Skipping duplicate: {entry_title}")
            continue

        info = OFFICIAL_DB[cat_key]
        article_body_html, label = generate_safe_news_with_fallback(entry_title, cat_key)
        image_url = get_featured_image(info["keyword"])

        full_html = f"""
        <div style="background: #f8fafc; border-left: 4px solid #2563eb; padding: 14px; margin-bottom: 20px; font-size: 14px; font-family: sans-serif;">
            <b>✍️ Verified Editorial & Global Bureau Standards:</b> Reviewed by TRTT International Desk.
            <br><b>Official Source Reference:</b> <a href="{info['url']}" target="_blank" rel="nofollow">{info['desk']}</a>
        </div>
        
        <div style="margin:20px 0;"><img src="{image_url}" alt="{entry_title}" style="width:100%; border-radius:8px;"/></div>
        
        {article_body_html}

        <!-- Hire Me Button -->
        <div style="text-align:center; margin-top:20px;">
        <a href="https://ttnews24bd.blogspot.com/p/hire-me-advertise.html" style="background:#2563eb; color:white; padding:12px 20px; text-decoration:none; border-radius:6px; font-weight:bold;">Need Help? Hire Me</a>
        </div>

        <!-- Community & Social Links Box -->
        <div style="margin-top:30px; padding:20px; background:#f1f5f9; text-align:center; border-radius:10px; border:1px solid #cbd5e1; font-family: sans-serif;">
            <h3 style="margin-top:0; color:#0f172a; font-size:18px;">📢 Join Our Official Community for Daily Updates</h3>
            <p style="font-size:14px; color:#475569; margin-bottom:15px;">Get verified global news, policy guides, and instant analytical updates directly on your device.</p>
            <div style="display:flex; justify-content:center; gap:10px; flex-wrap:wrap;">
                <a href="https://whatsapp.com/channel/0029Vb8co9VDeONEz0B5e51M" target="_blank" style="background:#25D366; color:white; padding:10px 18px; border-radius:6px; text-decoration:none; font-weight:bold; font-size:14px;">📲 Join WhatsApp Channel</a>
                <a href="https://t.me/trttnews24bd" target="_blank" style="background:#0088cc; color:white; padding:10px 18px; border-radius:6px; text-decoration:none; font-weight:bold; font-size:14px;">✈️ Join Telegram Channel</a>
            </div>
        </div>
        """

        post_body = {
            "kind": "blogger#post",
            "title": entry_title[:75],
            "content": full_html,
            "labels": [label, "Global Insights", f"Verified News {CURRENT_YEAR}"],
            "location": {"name": "London, United Kingdom", "lat": 51.5074, "lng": -0.1278}
        }

        # Blogger API v3 দিয়ে ড্রাফটে সংরক্ষণ
        result = blogger_service.posts().insert(blogId=blog_id, body=post_body, isDraft=True, fetchImages=True).execute()
        post_id = result.get('id')
        print(f"👑 DRAFT SAVED SUCCESSFULLY: {entry_title} (ID: {post_id})")

        save_history(info['url'], entry_title, label, f"Draft ID: {post_id}")
        send_telegram_notification(entry_title, "Saved as Draft")
        time.sleep(5)

if __name__ == "__main__":
    main()
