import os
import random
import requests
from datetime import datetime

# ================== ENV & SECRETS ==================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
BLOGGER_BLOG_ID = os.environ.get("BLOGGER_BLOG_ID")
BLOGGER_CLIENT_ID = os.environ.get("BLOGGER_CLIENT_ID")
BLOGGER_CLIENT_SECRET = os.environ.get("BLOGGER_CLIENT_SECRET")
BLOGGER_REFRESH_TOKEN = os.environ.get("BLOGGER_REFRESH_TOKEN")

TRAVEL_PAYOUT_MARKER = os.environ.get("TRAVEL_PAYOUT_MARKER", "787950")
AMAZON_AFFILIATE_LINK = os.environ.get("AMAZON_AFFILIATE_LINK", "https://amzn.to/4shg6Hn")
GITHUB_GUIDE_URL = "https://Cocvghuj.github.io/Cocvghuj-trtt-news-bot/latest_travel_news.html"
GITHUB_HUB_URL = "https://Cocvghuj.github.io/Cocvghuj-trtt-news-bot/"

GUIDE_TOPICS = [
    {"title": "Schengen Visa Guide 2026: 90/180 Rule Explained for Remote Workers", "focus": "Schengen visa and EES", "image_keyword": "europe travel passport"},
    {"title": "Cheapest Business Class to Europe: Aviasales Hidden Tricks 2026", "focus": "cheap business class flights", "image_keyword": "business class airplane"},
    {"title": "Digital Nomad Insurance + eSIM: Airalo vs Others for 150 Countries", "focus": "digital nomad eSIM and insurance", "image_keyword": "digital nomad working"},
    {"title": "Carry-On Only Europe Trip: Best Travel Gear from Amazon Tested", "focus": "best carry-on travel gear", "image_keyword": "travel backpack gear"},
]

def get_blogger_access_token():
    try:
        url = "https://oauth2.googleapis.com/token"
        data = {
            "client_id": BLOGGER_CLIENT_ID,
            "client_secret": BLOGGER_CLIENT_SECRET,
            "refresh_token": BLOGGER_REFRESH_TOKEN,
            "grant_type": "refresh_token"
        }
        res = requests.post(url, data=data, timeout=10)
        if res.status_code == 200:
            return res.json()["access_token"]
    except Exception as e:
        print(f"Blogger token error: {e}")
    return None

def get_smart_guide_topic():
    return random.choice(GUIDE_TOPICS)

def generate_natural_guide(topic):
    prompt = f"You are a professional travel writer for TRTT VoyageHub Inc. Write detailed SEO-friendly travel guide on: {topic['title']} Focus: {topic['focus']} Structure: Intro, 3-4 sections H2/H3, Money Tips, What to Avoid, Checklist. Tone professional helpful human. 800 words HTML with h2 h3 p ul li strong."
    
    # Try Groq First
    try:
        if GROQ_API_KEY:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
            payload = {"model": "llama3-8b-8192", "messages": [{"role": "user", "content": prompt}]}
            res = requests.post(url, headers=headers, json=payload, timeout=20)
            if res.status_code == 200:
                print("Guide generated with Groq")
                return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Groq error: {e}")
        
    # Try Gemini Fallback
    try:
        if GEMINI_API_KEY:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            res = requests.post(url, json=payload, timeout=20)
            if res.status_code == 200:
                print("Guide generated with Gemini")
                return res.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print(f"Gemini error: {e}")
        
    return f"<h2>{topic['title']}</h2><p>Explore professional insights on {topic['focus']}. Updated for 2026 with EES, ETIAS, digital nomad visas.</p><h3>Key Tips</h3><ul><li>Book flights 45-60 days early via Aviasales Marker {TRAVEL_PAYOUT_MARKER}</li><li>Use Airalo eSIM for 150+ countries</li><li>Gear from Amazon: {AMAZON_AFFILIATE_LINK}</li></ul>"

def get_unsplash_image(keyword):
    if UNSPLASH_ACCESS_KEY:
        try:
            url = f"https://api.unsplash.com/photos/random?query={keyword}&client_id={UNSPLASH_ACCESS_KEY}"
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                return res.json()["urls"]["regular"]
        except Exception as e:
            print(f"Unsplash error: {e}")
    return f"https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=1200"

def send_telegram_alert(title):
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        try:
            text = f"New Travel Guide Published: {title} - {GITHUB_GUIDE_URL}"
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text}, timeout=5)
        except Exception as e:
            print(f"Telegram failed: {e}")

def post_to_blogger(title, article_body, image_url):
    access_token = get_blogger_access_token()
    if not access_token:
        print("Blogger token failed")
        return
    
    blog_post_html = f"""
    <div style="max-width:800px;margin:0 auto;font-family:system-ui;color:#0f172a;line-height:1.8;padding:15px">
      <img src="{image_url}" style="width:100%;height:420px;object-fit:cover;border-radius:16px;margin-bottom:24px" />
      <h1 style="font-size:32px;font-weight:900;">{title}</h1>
      <p style="color:#64748b;font-size:13px;">TRTT VoyageHub Inc. | Marker {TRAVEL_PAYOUT_MARKER}</p>
      <div style="font-size:16px;color:#1e293b">{article_body}</div>
      <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:16px;padding:24px;margin-top:32px">
        <h3>Recommended Travel Tools</h3>
        <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:12px">
          <a href="https://aviasales.tp.st/Fb8U9yav?marker={TRAVEL_PAYOUT_MARKER}" target="_blank" style="background:#0f172a;color:#fff;padding:12px 20px;border-radius:999px;text-decoration:none;font-weight:700">Flight Deals</a>
          <a href="https://airalo.tpo.li/ZZoQCTMz?marker={TRAVEL_PAYOUT_MARKER}" target="_blank" style="background:#059669;color:#fff;padding:12px 20px;border-radius:999px;text-decoration:none;font-weight:700">eSIM Data</a>
          <a href="{AMAZON_AFFILIATE_LINK}" target="_blank" style="background:#d97706;color:#fff;padding:12px 20px;border-radius:999px;text-decoration:none;font-weight:700">Travel Gear</a>
        </div>
      </div>
      <div style="background:#0f172a;color:#fff;padding:24px;border-radius:16px;margin-top:32px;text-align:center">
        <a href="{GITHUB_HUB_URL}" target="_blank" style="background:#2563eb;color:#fff;padding:14px 28px;border-radius:999px;text-decoration:none;font-weight:800;display:inline-block;">Visit TRTT VoyageHub Hub</a>
      </div>
    </div>
    """
    try:
        url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOGGER_BLOG_ID}/posts/"
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        payload = {"kind": "blogger#post", "blog": {"id": BLOGGER_BLOG_ID}, "title": title, "content": blog_post_html}
        res = requests.post(url, headers=headers, json=payload, timeout=20)
        print(f"Blogger Posted: {res.status_code}")
    except Exception as e:
        print(f"Blogger Exception: {e}")

if __name__ == "__main__":
    topic = get_smart_guide_topic()
    article_body = generate_natural_guide(topic)
    image_url = get_unsplash_image(topic['image_keyword'])
    
    recommendation_box = f"""
    <div style="background:#111827;border:1px solid #2563eb;padding:30px;border-radius:12px;margin-top:40px;">
      <h3 style="color:#60a5fa;margin-bottom:12px;">Recommended Travel Tools</h3>
      <div style="display:flex;gap:15px;flex-wrap:wrap;">
        <a href="https://aviasales.tp.st/Fb8U9yav?marker={TRAVEL_PAYOUT_MARKER}" target="_blank" style="background:#2563eb;color:#fff;padding:12px 20px;text-decoration:none;border-radius:8px;font-weight:bold">Flight Deals</a>
        <a href="https://airalo.tpo.li/ZZoQCTMz?marker={TRAVEL_PAYOUT_MARKER}" target="_blank" style="background:#059669;color:#fff;padding:12px 20px;text-decoration:none;border-radius:8px;font-weight:bold">eSIM Data</a>
        <a href="{AMAZON_AFFILIATE_LINK}" target="_blank" style="background:#d97706;color:#fff;padding:12px 20px;text-decoration:none;border-radius:8px;font-weight:bold">Travel Gear</a>
      </div>
    </div>
    """
    
    full_page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{topic['title']}</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
body{{font-family:system-ui;background:#030712;color:#f3f4f6;line-height:1.8;margin:0}}
.header-bar{{background:#0f172a;padding:15px 5%;border-bottom:1px solid #1f2937;display:flex;justify-content:space-between}}
.header-bar a{{color:#9ca3af;text-decoration:none}}
.article-container{{max-width:800px;margin:40px auto;padding:0 20px}}
.badge{{background:rgba(245,158,11,0.15);color:#f59e0b;padding:6px 14px;border-radius:20px;font-size:12px}}
h1{{font-size:32px;color:#fff;margin-bottom:20px;font-weight:800}}
.featured-img{{width:100%;height:420px;object-fit:cover;border-radius:12px;margin-bottom:30px}}
.content p{{margin-bottom:20px;color:#d1d5db}}
.content h2{{color:#fff;font-size:22px;margin-top:35px;margin-bottom:15px}}
footer{{text-align:center;padding:40px;color:#9ca3af;font-size:13px;border-top:1px solid #1f2937;margin-top:40px}}
</style>
</head>
<body>
<div class="header-bar"><a href="index.html"><i class="fa-solid fa-arrow-left"></i> Back to Hub</a><span style="color:#60a5fa;font-weight:600;">TRTT Global Insights</span></div>
<main class="article-container"><span class="badge">{topic['focus']}</span><h1>{topic['title']}</h1><img src="{image_url}" alt="{topic['title']}" class="featured-img"><div class="content">{article_body}</div>{recommendation_box}</main>
<footer><p>2026 TRTT News 24 BD | Roksana | Taifa | Tashrif Family Project | Marker {TRAVEL_PAYOUT_MARKER}</p></footer>
</body>
</html>
"""
    
    with open("latest_travel_news.html", "w", encoding="utf-8") as f:
        f.write(full_page_html)
    print(f"Generated guide: {topic['title']}")
    
    send_telegram_alert(topic['title'])
    post_to_blogger(topic['title'], article_body, image_url)
