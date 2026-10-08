import feedparser, os, json, requests, datetime, time
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

FEEDS = {
    "Bangladesh": "https://feeds.bbci.co.uk/news/world/asia/rss.xml",
    "International": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "Schengen Hub": "https://www.schengenvisainfo.com/feed/",
    "Visa & Immigration": "https://www.cicnews.com/feed",
    "Education & Scholarship": "https://www.scholarship-positions.com/feed/",
    "Technology & Gadgets": "http://feeds.bbci.co.uk/news/technology/rss.xml",
}
WEEK = {0: ["Bangladesh","Schengen Hub"],1: ["Visa & Immigration","International"],2: ["Bangladesh","Education & Scholarship"],3: ["Technology & Gadgets","Bangladesh"],4: ["Schengen Hub","Visa & Immigration"],5: ["International","Bangladesh"],6: ["Education & Scholarship","Bangladesh"]}

def get_cat():
    now=datetime.datetime.now()
    return WEEK[now.weekday()][0 if now.hour<12 else 1]

def ai_rewrite(prompt):
    # তোমার নাম অনুযায়ী সব Key ট্রাই করবে
    # 1. GROQ
    try:
        k=os.environ.get("GROQ_API_KEY")
        if k:
            r=requests.post("https://api.groq.com/openai/v1/chat/completions", headers={"Authorization":f"Bearer {k}"}, json={"model":"llama-3.1-8b-instant","messages":[{"role":"user","content":prompt}]}, timeout=30)
            j=r.json()
            if "choices" in j:
                print("✅ SUCCESS: GROQ"); return j["choices"][0]["message"]["content"]
            print(f"GROQ resp: {j}")
    except Exception as e: print(f"GROQ Fail {e}")
    # 2. OPENROUTER
    try:
        k=os.environ.get("OPENROUTER_API_KEY")
        if k:
            r=requests.post("https://openrouter.ai/api/v1/chat/completions", headers={"Authorization":f"Bearer {k}"}, json={"model":"mistralai/mistral-7b-instruct:free","messages":[{"role":"user","content":prompt}]}, timeout=30)
            j=r.json()
            if "choices" in j:
                print("✅ SUCCESS: OPENROUTER"); return j["choices"][0]["message"]["content"]
    except Exception as e: print(f"OPENROUTER Fail {e}")
    # 3. MISTRAL
    try:
        k=os.environ.get("MISTRAL_API_KEY")
        if k:
            r=requests.post("https://api.mistral.ai/v1/chat/completions", headers={"Authorization":f"Bearer {k}"}, json={"model":"mistral-small-latest","messages":[{"role":"user","content":prompt}]}, timeout=30)
            j=r.json()
            if "choices" in j:
                print("✅ SUCCESS: MISTRAL"); return j["choices"][0]["message"]["content"]
    except Exception as e: print(f"MISTRAL Fail {e}")
    # 4. DEEPSEEK
    try:
        k=os.environ.get("DEEP_SEEK_KEY")
        if k:
            r=requests.post("https://api.deepseek.com/chat/completions", headers={"Authorization":f"Bearer {k}"}, json={"model":"deepseek-chat","messages":[{"role":"user","content":prompt}]}, timeout=30)
            j=r.json()
            if "choices" in j:
                print("✅ SUCCESS: DEEP_SEEK"); return j["choices"][0]["message"]["content"]
    except Exception as e: print(f"DEEPSEEK Fail {e}")
    # 5. COHERE
    try:
        k=os.environ.get("COHERE_API_KEY")
        if k:
            r=requests.post("https://api.cohere.ai/v1/chat", headers={"Authorization":f"Bearer {k}","Content-Type":"application/json"}, json={"model":"command-r-plus","message":prompt}, timeout=30)
            j=r.json()
            if "text" in j:
                print("✅ SUCCESS: COHERE"); return j["text"]
    except Exception as e: print(f"COHERE Fail {e}")
    # 6. HUGGINGFACE - তোমার নাম HUGGINGFACE_API_KEY
    try:
        k=os.environ.get("HUGGINGFACE_API_KEY")
        if k:
            r=requests.post("https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2", headers={"Authorization":f"Bearer {k}"}, json={"inputs":prompt}, timeout=40)
            j=r.json()
            if isinstance(j,list) and "generated_text" in j[0]:
                print("✅ SUCCESS: HUGGINGFACE"); return j[0]["generated_text"]
    except Exception as e: print(f"HF Fail {e}")
    # 7. GEMINI শেষে
    try:
        k=os.environ.get("GEMINI_API_KEY") or os.environ.get("CONSOLE_API_KEY")
        if k:
            for m in ["gemini-1.5-flash","gemini-1.5-flash-8b"]:
                url=f"https://generativelanguage.googleapis.com/v1/models/{m}:generateContent?key={k}"
                r=requests.post(url, json={"contents":[{"parts":[{"text":prompt}]}]}, timeout=30)
                j=r.json()
                if "candidates" in j:
                    print(f"✅ SUCCESS: GEMINI {m}"); return j["candidates"][0]["content"]["parts"][0]["text"]
                print(f"Gemini {m}: {j}")
    except Exception as e: print(f"GEMINI Fail {e}")
    return None

def get_blogger():
    # তোমার নাম অনুযায়ী CLIENT_ID, SECRET, REFRESH_TOKEN দিয়ে
    cid=os.environ.get("BLOGGER_CLIENT_ID")
    csec=os.environ.get("BLOGGER_CLIENT_SECRET")
    rtoken=os.environ.get("BLOGGER_REFRESH_TOKEN")
    print(f"Checking Blogger: CLIENT_ID={len(cid) if cid else 0}, SECRET={len(csec) if csec else 0}, REFRESH={len(rtoken) if rtoken else 0}")
    if not cid or not csec or not rtoken:
        raise Exception("Blogger ID/Secret/Token খালি! Secret list চেক করো")
    creds=Credentials.from_authorized_user_info({"client_id":cid,"client_secret":csec,"refresh_token":rtoken})
    return build("blogger","v3",credentials=creds)

cat=get_cat()
print(f"Today Category: {cat}")
feed=feedparser.parse(FEEDS[cat])
entry=feed.entries[0]
prompt=f"Rewrite for TRTT NEWS 24 BD blog, Category {cat}, 100% unique, 350 words, SEO, use H2. Original: {entry.title} {entry.summary}"
content=ai_rewrite(prompt)
if not content:
    content=f"<h2>{cat} Latest Update 2026</h2><p>{entry.summary}</p>"
    print("⚠️ All AI failed, using original")

service=get_blogger()
body={"kind":"blogger#post","blog":{"id":os.environ["BLOGGER_ID"]},"title":entry.title,"content":content,"labels":[cat]}
post=service.posts().insert(blogId=os.environ["BLOGGER_ID"],body=body,isDraft=False).execute()
url=post["url"]
print(f"DONE: {url}")

try:
    bot=os.environ.get("TELEGRAM_BOT_TOKEN")
    chat=os.environ.get("TELEGRAM_CHAT_ID")
    if bot and chat:
        msg=f"🔴 <b>{entry.title}</b>\n\n👉 <a href='{url}'>বিস্তারিত পড়ুন</a>"
        requests.post(f"https://api.telegram.org/bot{bot}/sendMessage", data={"chat_id":chat,"text":msg,"parse_mode":"HTML"}, timeout=15)
        print("✅ Telegram Sent")
except Exception as e: print(f"Telegram fail {e}")
