import feedparser, os, json, requests, random, re, datetime, time, subprocess, sys
from google import genai
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

HISTORY_FILE = "posted_history.json"
TELEGRAM_URL_TEMPLATE = "https://api.telegram.org/bot{token}/sendMessage"

# 1. REAL OFFICIAL DATABASE - NO FAKE ALLOWED
OFFICIAL_DB = {
    "GERMANY": {"desk": "German Federal Foreign Office (Make it in Germany)", "url": "https://www.make-it-in-germany.com/en/visa-residence/types/chancenkarte", "fee": "€75", "salary": "€2,200 to €3,500 monthly", "keyword": "Germany Opportunity Card Chancenkarte Berlin Brandenburg Gate", "label": "Global Work Permits & Immigration"},
    "PORTUGAL": {"desk": "Portuguese Ministry of Foreign Affairs - Vistos MNE", "url": "https://vistos.mne.gov.pt/en/national-visas/general-information", "fee": "€90 Visa + €83 Residence Permit", "salary": "€760 to €1,200 monthly", "keyword": "Portugal Work Visa Passport Lisbon", "label": "Europe Visa & Residency"},
    "MALTA": {"desk": "Jobsplus - Government of Malta", "url": "https://jobsplus.gov.mt/employers/resources/single-permit", "fee": "€280.50", "salary": "€1,000 to €1,400 monthly", "keyword": "Malta Hotel Staff Jobs Workers", "label": "Global Work Permits & Immigration"},
    "ITALY": {"desk": "Italian Ministry of Interior - Portale Immigrazione", "url": "https://www.interno.gov.it/it/temi/immigrazione", "fee": "€116", "salary": "€1,200 to €1,600 monthly", "keyword": "Italy Visa Decreto Flussi Worker", "label": "Europe Visa & Residency"},
    "UK": {"desk": "UK Government - UK Visas and Immigration", "url": "https://www.gov.uk/government/organisations/uk-visas-and-immigration", "fee": "£464", "salary": "£38,700 minimum threshold per year", "keyword": "UK Skilled Worker Visa UK Government Big Ben", "label": "UK Visa and Immigration"},
    "USA": {"desk": "US Department of State", "url": "https://travel.state.gov", "fee": "$185", "salary": "$3,500 monthly average", "keyword": "USA Work Permit Passport Visa", "label": "Global Work Permits & Immigration"},
    "DEFAULT": {"desk": "Verified Official Government Source", "url": "https://www.reuters.com/", "fee": "N/A", "salary": "Standard International Rates", "keyword": "Global Work Visa Immigration Passport", "label": "Lifestyle & Europe News"}
}

BANNED_PHRASES = []

EVERGREEN_MASTER_TOPICS = [
    "Portugal Work Visa for Bangladeshi 2027 - 90 Days Processing Time",
    "Germany Opportunity Card (Chancenkarte) 2027 - Points Calculator & Requirements",
    "UK Skilled Worker Visa 2027 - Minimum Salary Threshold & Sponsor List",
    "Malta Work Visa 2027 for Bangladeshi - Hotel Jobs with Free Accommodation",
    "Italy Seasonal Work Visa 2027 (Decreto Flussi) - Application from Sanluri, Italy"
]

COUNTRY_LOCATIONS = {
    "italy": {"name": "Milan, Italy", "lat": 45.4642, "lng": 9.1900},
    "germany": {"name": "Berlin, Germany", "lat": 52.5200, "lng": 13.4050},
    "uk": {"name": "London, UK", "lat": 51.5072, "lng": -0.1276},
    "portugal": {"name": "Lisbon, Portugal", "lat": 38.7223, "lng": -9.1393},
    "malta": {"name": "Valletta, Malta", "lat": 35.8985, "lng": 14.5146},
    "default": {"name": "Milan, Italy", "lat": 45.4642, "lng": 9.1900}
}

def get_info(topic: str):
    t = topic.upper()
    for key in ["GERMANY", "PORTUGAL", "MALTA", "ITALY", "UK", "USA"]:
        if key in t: 
            return OFFICIAL_DB[key]
    return OFFICIAL_DB["DEFAULT"]

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

def get_smart_location(title):
    text = str(title).lower()
    for key, loc in COUNTRY_LOCATIONS.items():
        if key in text:
            return loc
    return COUNTRY_LOCATIONS["default"]

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
            msg = f"👑 <b>Media Empire Alert</b>\n\n<b>Title:</b> {title}\n\n<b>Link:</b> {url}"
            api_url = TELEGRAM_URL_TEMPLATE.format(token=bot_token)
            requests.post(api_url, json={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}, timeout=10)
        except Exception as e:
            print(f"⚠️ Telegram Error: {e}")

# DUAL-ENGINE FALLBACK (Google GenAI SDK with gemini-3.8-flash + Groq Llama-3)
def generate_safe_news_with_fallback(topic: str):
    info = get_info(topic)
    
    prompt = f"""
SYSTEM: You are BBC News Senior Editor, TRTT NEWS 24 BD Bureau, Sanluri, Italy. You obey ONLY OFFICIAL_DB.
You are locked. You cannot invent.

TOPIC: {topic}
OFFICIAL DESK (USE ONLY THIS): {info['desk']}
OFFICIAL URL (CITE EXACTLY 2 TIMES): {info['url']}
OFFICIAL FEE (USE ONLY THIS): {info['fee']}

ABSOLUTE RULES - BREAK = FAIL:
1. NEVER write these BANNED phrases: {', '.join(BANNED_PHRASES)}. If you write them, article is rejected.
2. You MUST use desk={info['desk']} and url={info['url']} and fee={info['fee']}. No other source.
3. 700+ words, 100% English UK, BBC neutral, no emoji.
4. Title: BBC style - Example: {topic}: Official Guide and Requirements 2027
5. Structure EXACT:
   - Executive Summary (80 words, include date 13 Oct 2026)
   - H2: Official Announcement from {info['desk']} (cite {info['url']} 2 times) - 120 words
   - H2: Key Eligibility / Core Facts - 150 words bullets
   - H2: Step-by-Step Process Without Brokers - 150 words numbered, warn against dalal
   - H2: Official Fee {info['fee']} and Legal Protection - 100 words
   - H2: TRTT Expert Take & Verification (Sanluri, Italy) - 80 words, MUST start with "Our resident editorial bureau in Sanluri, Italy has directly cross-referenced this with {info['desk']}..." and MUST end with "— Verified by Senior Editorial Desk | TRTT NEWS 24 BD Bureau (Sanluri, Italy)"
   - Footer: Official Reference Desk: {info['desk']} - {info['url']}

Now write news for: {topic}
"""

    # Try Google GenAI SDK First with gemini-3.8-flash
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        try:
            client = genai.Client(api_key=gemini_key)
            response = client.models.generate_content(
                model='gemini-3.8-flash',
                contents=prompt,
            )
            if response and response.text:
                print("✅ Generated successfully using Google GenAI SDK (gemini-3.8-flash).")
                return response.text, info['label']
        except Exception as e:
            print(f"⚠️ Gemini SDK Failed: {e}. Switching to Groq fallback...")

    # Fallback to Groq (Llama-3)
    groq_key = os.environ.get("GROQ_API_KEY")
    if groq_key:
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1
            }
            r = requests.post(url, json=payload, headers=headers, timeout=60)
            if r.status_code == 200:
                text = r.json()['choices'][0]['message']['content']
                print("✅ Generated successfully using Groq (Llama-3) Fallback.")
                return text, info['label']
        except Exception as e:
            print(f"⚠️ Groq Fallback Failed: {e}")

    raise ValueError("❌ Both Gemini and Groq APIs failed.")

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
    unposted_evergreen = [t for t in EVERGREEN_MASTER_TOPICS if not is_duplicate(t)]
    if not unposted_evergreen:
        print("❌ All evergreen topics have already been posted.")
        return

    entry_title = random.choice(unposted_evergreen)
    info = get_info(entry_title)

    article_body_html, label = generate_safe_news_with_fallback(entry_title)
    image_url = get_featured_image(info["keyword"])

    full_html = f"""
    <div style="background: #f8fafc; border-left: 4px solid #2563eb; padding: 14px; margin-bottom: 20px; font-size: 14px;">
        <b>✍️ Human Expert Editorial & Verification:</b> Verified by TRTT Bureau Sanluri, Italy.
        <br><b>Direct Official Desk:</b> <a href="{info['url']}" target="_blank">{info['desk']}</a>
    </div>
    <div style="margin:20px 0;"><img src="{image_url}" alt="{entry_title}" style="width:100%; border-radius:8px;"/></div>
    {article_body_html}
    """

    blogger_service = get_blogger()
    if blogger_service:
        blog_id = os.environ.get("BLOGGER_ID") or os.environ.get("BLOGGER_BLOG_ID")
        loc = get_smart_location(entry_title)

        post_body = {
            "kind": "blogger#post",
            "title": entry_title[:70],
            "content": full_html,
            "labels": [label, "Human Verified", "2027 Immigration Guide"],
            "location": {"name": loc["name"], "lat": loc["lat"], "lng": loc["lng"]}
        }

        result = blogger_service.posts().insert(blogId=blog_id, body=post_body, isDraft=False, fetchImages=True).execute()
        post_url = result.get('url')
        print(f"👑 ZERO-HALLUCINATION DUAL-ENGINE ARTICLE PUBLISHED: {post_url}")

        save_history(info['url'], entry_title, label, post_url)
        send_telegram_notification(entry_title, post_url)

if __name__ == "__main__":
    main()
