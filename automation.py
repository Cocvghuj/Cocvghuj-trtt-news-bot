import feedparser, os, json, requests, datetime, time
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
WEEK = {
    0: ["Bangladesh", "Schengen Hub"], 1: ["Visa & Immigration", "International"],
    2: ["Europe", "Education & Scholarship"], 3: ["Technology & Gadgets", "Bangladesh"],
    4: ["Schengen Hub", "Visa & Immigration"], 5: ["International", "Europe"],
    6: ["Education & Scholarship", "Guest Post"]
}

def get_cat():
    now = datetime.datetime.now()
    return WEEK[now.weekday()][0 if now.hour < 12 else 1]

def ai(prompt):
    # 1. GROQ - তোমার সবচেয়ে ফাস্ট Key
    try:
        k = os.environ.get("GROQ_API_KEY")
        if k:
            r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {k}"},
                json={"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": prompt}]}, timeout=30)
            j = r.json()
            if "choices" in j:
                print("✅ SUCCESS: GROQ")
                return j["choices"][0]["message"]["content"]
    except Exception as e: print(f"GROQ Fail: {e}")

    # 2. OPENROUTER - তোমার ২য় ব্যাকআপ
    try:
        k = os.environ.get("OPENROUTER_API_KEY")
        if k:
            r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {k}"},
                json={"model": "mistralai/mistral-7b-instruct:free", "messages": [{"role": "user", "content": prompt}]}, timeout=30)
            j = r.json()
            if "choices" in j:
                print("✅ SUCCESS: OPENROUTER")
                return j["choices"][0]["message"]["content"]
    except Exception as e: print(f"OPENROUTER Fail: {e}")

    # 3. MISTRAL
    try:
        k = os.environ.get("MISTRAL_API_KEY")
        if k:
            r = requests.post("https://api.mistral.ai/v1/chat/completions",
                headers={"Authorization": f"Bearer {k}"},
                json={"model": "mistral-small-latest", "messages": [{"role": "user", "content": prompt}]}, timeout=30)
            j = r.json()
            if "choices" in j:
                print("✅ SUCCESS: MISTRAL")
                return j["choices"][0]["message"]["content"]
    except Exception as e: print(f"MISTRAL Fail: {e}")

    # 4. DEEPSEEK
    try:
        k = os.environ.get("DEEP_SEEK_API_KEY") or os.environ.get("DEEP_SEEK_KEY")
        if k:
            r = requests.post("https://api.deepseek.com/chat/completions",
                headers={"Authorization": f"Bearer {k}"},
                json={"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}]}, timeout=30)
            j = r.json()
            if "choices" in j:
                print("✅ SUCCESS: DEEPSEEK")
                return j["choices"][0]["message"]["content"]
    except Exception as e: print(f"DEEPSEEK Fail: {e}")

    # 5. COHERE
    try:
        k = os.environ.get("COHERE_API_KEY")
        if k:
            r = requests.post("https://api.cohere.ai/v1/chat",
                headers={"Authorization": f"Bearer {k}", "Content-Type": "application/json"},
                json={"model": "command-r-plus", "message": prompt}, timeout=30)
            j = r.json()
            if "text" in j:
                print("✅ SUCCESS: COHERE")
                return j["text"]
    except Exception as e: print(f"COHERE Fail: {e}")

    # 6. HUGGINGFACE
    try:
        k = os.environ.get("HUGGINGFACE_TOKEN")
        if k:
            r = requests.post("https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
                headers={"Authorization": f"Bearer {k}"},
                json={"inputs": prompt}, timeout=40)
            j = r.json()
            if isinstance(j, list) and "generated_text" in j[0]:
                print("✅ SUCCESS: HUGGINGFACE")
                return j[0]["generated_text"]
    except Exception as e: print(f"HUGGINGFACE Fail: {e}")

    # 7. GEMINI - সবার শেষে, কারণ এখন 404 দিচ্ছে
    try:
        k = os.environ.get("GEMINI_API_KEY") or os.environ.get("CONSOLE_API_KEY")
        if k:
            for model in ["gemini-1.5-flash", "gemini-2.0-flash-lite"]:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={k}"
                r = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=30)
                j = r.json()
                if "candidates" in j:
                    print(f"✅ SUCCESS: GEMINI {model}")
                    return j["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e: print(f"GEMINI Fail: {e}")

    return None

def get_blogger():
    s = os.environ.get("BLOGGER_TOKEN_JSON")
    if not s or len(s) < 50:
        raise Exception(f"BLOGGER_TOKEN_JSON খালি! Length={len(s) if s else 0}. Workflow yml এ env যোগ করো")
    print(f"TOKEN_JSON OK length={len(s)}")
    creds = Credentials.from_authorized_user_info(json.loads(s))
    return build("blogger", "v3", credentials=creds)

# MAIN
cat = get_cat()
print(f"Today Category: {cat}")
feed = feedparser.parse(FEEDS[cat])
entry = feed.entries[0]
prompt = f"Rewrite for TRTT NEWS 24 BD blog, Category {cat}, 100% unique, 350 words, SEO friendly, use H2, H3. Original Title: {entry.title} Content: {entry.summary}"

content = ai(prompt)
if not content:
    content = f"<h2>{cat} Latest Update 2026</h2><p>{entry.summary}</p><p>Read more on TRTT NEWS 24 BD</p>"
    print("⚠️ All AI failed, using original SEO")

service = get_blogger()
body = {"kind": "blogger#post", "blog": {"id": os.environ["BLOGGER_ID"]}, "title": entry.title, "content": content, "labels": [cat, "News 2026"]}
post = service.posts().insert(blogId=os.environ["BLOGGER_ID"], body=body, isDraft=False).execute()
url = post["url"]
print(f"DONE: {url}")

# Telegram
try:
    bot = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat = os.environ.get("TELEGRAM_CHANNEL_ID")
    if bot and chat:
        msg = f"🔴 <b>{entry.title}</b>\n\n👉 <a href='{url}'>বিস্তারিত পড়ুন</a>"
        requests.post(f"https://api.telegram.org/bot{bot}/sendMessage", data={"chat_id": chat, "text": msg, "parse_mode": "HTML"}, timeout=15)
        print("✅ Telegram Sent")
except Exception as e: print(f"Telegram fail {e}")
