import feedparser, os, datetime, requests, json, time
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

FEEDS = {
    "Bangladesh": "https://feeds.bbci.co.uk/news/world/asia/rss.xml",
    "International": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "Europe": "http://feeds.bbci.co.uk/news/world/europe/rss.xml",
    "Schengen Hub": "https://www.schengenvisainfo.com/feed/",
    "Visa & Immigration": "https://www.cicnews.com/feed",
    "Education & Scholarship": "https://www.scholarship-positions.com/feed/",
    "Technology & Gadgets": "http://feeds.bbci.co.uk/news/technology/rss.xml",
    "Guest Post": "http://feeds.bbci.co.uk/news/world/rss.xml"
}
WEEK_PLAN = {
    0: ["Bangladesh", "Schengen Hub"],
    1: ["Visa & Immigration", "International"],
    2: ["Europe", "Education & Scholarship"],
    3: ["Technology & Gadgets", "Bangladesh"],
    4: ["Schengen Hub", "Visa & Immigration"],
    5: ["International", "Europe"],
    6: ["Education & Scholarship", "Guest Post"]
}

def get_category():
    now = datetime.datetime.now()
    slot = 0 if now.hour < 12 else 1
    return WEEK_PLAN[now.weekday()][slot]

def try_gemini(prompt):
    key = os.environ.get("GEMINI_API_KEY")
    if not key: return None
    # তুমি 3.8 চেয়েছো, তাই আমরা 3 টা মডেল ট্রাই করবো - যেটা পাবে সেটাই চলবে
    models_to_try = [
        "gemini-2.0-flash", # সবচেয়ে নতুন স্টেবল (তুমি 3.8 বলতে এটাই বুঝিয়েছো)
        "gemini-1.5-flash-latest",
        "gemini-1.5-flash-8b"
    ]
    for model in models_to_try:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
            r = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
            j = r.json()
            if "candidates" in j:
                print(f"✅ SUCCESS: GEMINI with {model}")
                return j["candidates"][0]["content"]["parts"][0]["text"]
            else:
                print(f"Gemini {model} response: {j}")
        except Exception as e:
            print(f"❌ Gemini {model} Failed: {e}")
            continue
    return None

def try_groq(prompt):
    try:
        key = os.environ.get("GROQ_API_KEY")
        if not key: return None
        r = requests.post("https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}"},
            json={"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": prompt}]}, timeout=30)
        data = r.json()
        if "choices" in data:
            print("✅ SUCCESS: GROQ")
            return data["choices"][0]["message"]["content"]
    except Exception as e: print(f"❌ Groq Failed: {e}")
    return None

def try_openrouter(prompt):
    try:
        key = os.environ.get("OPENROUTER_API_KEY")
        if not key: return None
        r = requests.post("https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}"},
            json={"model": "mistralai/mistral-7b-instruct:free", "messages": [{"role": "user", "content": prompt}]}, timeout=30)
        data = r.json()
        if "choices" in data:
            print("✅ SUCCESS: OPENROUTER")
            return data["choices"][0]["message"]["content"]
    except Exception as e: print(f"❌ OpenRouter Failed: {e}")
    return None

def rewrite_with_all_keys(text, category):
    prompt = f"Rewrite for TRTT NEWS 24 BD, Category {category}, 100% unique, 350 words, SEO, add H2. Original: {text}"
    for func in [try_gemini, try_groq, try_openrouter]:
        result = func(prompt)
        if result and len(result) > 100:
            return result
        time.sleep(1)
    return f"<h2>{category} Latest Update 2026</h2><p>{text}</p>"

def get_blogger_service():
    if os.environ.get("BLOGGER_TOKEN_JSON"):
        creds = Credentials.from_authorized_user_info(json.loads(os.environ["BLOGGER_TOKEN_JSON"]))
        return build("blogger", "v3", credentials=creds)
    else:
        creds = Credentials.from_authorized_user_info({
            "client_id": os.environ["BLOGGER_CLIENT_ID"],
            "client_secret": os.environ["BLOGGER_CLIENT_SECRET"],
            "refresh_token": os.environ["BLOGGER_REFRESH_TOKEN"]
        })
        return build("blogger", "v3", credentials=creds)

def post_to_blogger(title, content, labels):
    service = get_blogger_service()
    body = {"kind": "blogger#post", "blog": {"id": os.environ["BLOGGER_ID"]}, "title": title, "content": content, "labels": labels}
    post = service.posts().insert(blogId=os.environ["BLOGGER_ID"], body=body, isDraft=False).execute()
    return post["url"]

def post_to_telegram(title, url):
    try:
        token = os.environ.get("TELEGRAM_BOT_TOKEN") or os.environ.get("TELEGRAM_TOKEN")
        chat_id = os.environ.get("TELEGRAM_CHANNEL_ID") or os.environ.get("TELEGRAM_CHAT_ID")
        if not token or not chat_id: return
        msg = f"🔴 <b>{title}</b>\n\n👉 <a href='{url}'>বিস্তারিত পড়ুন</a>"
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}, timeout=15)
    except: pass

category = get_category()
feed = feedparser.parse(FEEDS[category])
entry = feed.entries[0]
new_content = rewrite_with_all_keys(entry.title + " " + entry.summary, category)
url = post_to_blogger(entry.title, new_content, [category])
post_to_telegram(entry.title, url)
print(f"DONE: {url}")
