import os
import random
import requests
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==================== ENVIRONMENT SECRETS ====================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY")
GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

BLOGGER_BLOG_ID = os.environ.get("BLOGGER_BLOG_ID")
BLOGGER_CLIENT_ID = os.environ.get("BLOGGER_CLIENT_ID")
BLOGGER_CLIENT_SECRET = os.environ.get("BLOGGER_CLIENT_SECRET")
BLOGGER_REFRESH_TOKEN = os.environ.get("BLOGGER_REFRESH_TOKEN")

TRAVEL_PAYOUT_MARKER = os.environ.get("TRAVEL_PAYOUT_MARKER", "787950")
AMAZON_AFFILIATE_LINK = "https://amzn.to/4shg6Hn"
GITHUB_GUIDE_URL = "https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/latest_travel_news.html"

# ==================== TRAVEL & BUSINESS GUIDE TOPICS ====================
GUIDE_TOPICS = [
    {
        "title": "Building a Remote Travel Consulting Business in Europe (2026 Guide)",
        "category": "Entrepreneurship & Travel Business",
        "focus": "How to start a boutique travel planning service, monetize via Aviasales flight booking tools, and scale online.",
        "image_keyword": "business,laptop,travel"
    },
    {
        "title": "The Ultimate Schengen Travel Blueprint: Low-Cost Routes & Smart Planning",
        "category": "Destination & Visa Strategy",
        "focus": "Step-by-step breakdown of European travel planning, finding hidden flight discounts, and insurance essentials.",
        "image_keyword": "europe,travel,landscape"
    },
    {
        "title": "Digital Nomad Productivity: Essential Gadgets & Workflow Setup",
        "category": "Nomad Lifestyle & Gear",
        "focus": "Smart packing, reliable mobile connectivity using Airalo eSIM, and high-performance travel tech gear.",
        "image_keyword": "technology,nomad,backpack"
    }
]

def get_smart_guide_topic():
    return random.choice(GUIDE_TOPICS)

# ==================== BLOGGER ACCESS TOKEN GENERATOR ====================
def get_blogger_access_token():
    if BLOGGER_CLIENT_ID and BLOGGER_CLIENT_SECRET and BLOGGER_REFRESH_TOKEN:
        try:
            url = "https://oauth2.googleapis.com/token"
            payload = {
                "client_id": BLOGGER_CLIENT_ID,
                "client_secret": BLOGGER_CLIENT_SECRET,
                "refresh_token": BLOGGER_REFRESH_TOKEN,
                "grant_type": "refresh_token"
            }
            res = requests.post(url, data=payload, timeout=10)
            if res.status_code == 200:
                print("✅ Blogger Access Token generated")
                return res.json().get("access_token")
            else:
                print(f"Blogger Token Error: {res.text}")
        except Exception as e:
            print(f"Failed to get Blogger token: {e}")
    return None

# ==================== PUBLISH TO BLOGGER ====================
def post_to_blogger(title, snippet, image_url):
    access_token = get_blogger_access_token()
    if access_token and BLOGGER_BLOG_ID:
        try:
            blogger_url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOGGER_BLOG_ID}/posts/"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            
            # HTML content with 1-second auto-redirect script to GitHub
            blog_post_html = f"""
            <div style="max-width:700px;margin:0 auto;font-family:sans-serif;background:#0f172a;color:#fff;padding:25px;border-radius:12px;text-align:center;">
                <img src="{image_url}" alt="{title}" style="width:100%;max-height:350px;object-fit:cover;border-radius:10px;margin-bottom:20px;">
                <h2 style="color:#f59e0b;font-size:24px;margin-bottom:15px;">{title}</h2>
                <p style="color:#cbd5e1;font-size:16px;line-height:1.6;margin-bottom:25px;">{snippet}</p>
                <div style="margin:25px 0;">
                    <a href="{GITHUB_GUIDE_URL}" style="background:#2563eb;color:#fff;padding:14px 28px;text-decoration:none;font-weight:bold;font-size:16px;border-radius:8px;display:inline-block;box-shadow:0 4px 12px rgba(37,99,235,0.4);">
                        🚀 বিস্তারিত ও মূল গাইডটি পড়ুন ↗
                    </a>
                </div>
                <p style="color:#9ca3af;font-size:13px;">১ সেকেন্ডের মধ্যে স্বয়ংক্রিয়ভাবে গিটহাব গাইডে রিডাইরেক্ট হচ্ছে...</p>
            </div>

            <script>
                setTimeout(function() {{
                    window.location.href = "{GITHUB_GUIDE_URL}";
                }}, 1000);
            </script>
            """
            
            post_data = {
                "kind": "blogger#post",
                "title": f"TRTT Travel Guide: {title}",
                "content": blog_post_html
            }
            
            res = requests.post(blogger_url, json=post_data, headers=headers, timeout=10)
            if res.status_code == 200:
                print("✅ Successfully published post to Blogger!")
            else:
                print(f"Blogger Post Error: {res.text}")
        except Exception as e:
            print(f"Failed to post on Blogger: {e}")

# ==================== AI CONTENT GENERATION ENGINE ====================
def generate_natural_guide(topic):
    prompt = f"""
    You are an elite, professional travel writer and digital business strategist. Write an in-depth, high-value, natural-sounding editorial article (approx 400-500 words) titled "{topic['title']}".
    Focus on: {topic['focus']}.
    
    Guidelines:
    - Write in a friendly, authoritative, and completely human tone.
    - Provide genuine insights, actionable steps, and professional business/travel advice.
    - Format cleanly using semantic HTML tags: <h2>, <h3>, <p>, <ul>, <li>, and <strong>.
    """

    if GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=15)
            if res.status_code == 200:
                print("✅ Guide generated with Gemini")
                return res.json()['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            print(f"Gemini error: {e}")

    if GROQ_API_KEY:
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
            res = requests.post(url, json={"model": "llama3-8b-8192", "messages": [{"role": "user", "content": prompt}]}, headers=headers, timeout=15)
            if res.status_code == 200:
                print("✅ Guide generated with Groq")
                return res.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"Groq error: {e}")

    return f"<h2>{topic['title']}</h2><p>Explore professional insights on travel planning and remote business strategies.</p>"

def get_unsplash_image(keyword):
    if UNSPLASH_ACCESS_KEY:
        try:
            url = f"https://api.unsplash.com/photos/random?query={keyword}&client_id={UNSPLASH_ACCESS_KEY}"
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                return res.json()['urls']['regular']
        except Exception as e:
            print(f"Unsplash error: {e}")
    return f"https://source.unsplash.com/1200x600/?{keyword}"

def send_telegram_alert(title):
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        try:
            text = f"🌍 *New Travel & Business Guide Published*\n\n*{title}*\n\n👉 [Read Full Guide Here]({GITHUB_GUIDE_URL})"
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}, timeout=5)
            print("✅ Telegram notification sent")
        except Exception as e:
            print(f"Telegram failed: {e}")

# ==================== MAIN EXECUTION ====================
if __name__ == "__main__":
    topic = get_smart_guide_topic()
    article_body = generate_natural_guide(topic)
    image_url = get_unsplash_image(topic['image_keyword'])
    
    # Recommendation Box for GitHub page
    recommendation_box = f"""
    <div style="background:#111827;border:1px solid #2563eb;padding:30px;border-radius:12px;margin-top:40px;">
        <h3 style="color:#60a5fa;margin-bottom:12px;font-size:20px;"><i class="fa-solid fa-compass"></i> Recommended Travel Tools & Resources</h3>
        <p style="color:#9ca3af;font-size:14px;margin-bottom:20px;">Planning your itinerary or launching your remote venture? Check out these top recommendations:</p>
        
        <div style="display:flex;gap:15px;flex-wrap:wrap;">
            <a href="https://aviasales.tpo.lv/Fb8U9yav?marker={TRAVEL_PAYOUT_MARKER}" target="_blank" style="background:#2563eb;color:#fff;padding:12px 20px;text-decoration:none;font-weight:600;border-radius:8px;font-size:14px;">
                🛫 Live Flight Deals ↗
            </a>
            <a href="https://airalo.tpo.lv/ZZoQC7Mz?marker={TRAVEL_PAYOUT_MARKER}" target="_blank" style="background:#059669;color:#fff;padding:12px 20px;text-decoration:none;font-weight:600;border-radius:8px;font-size:14px;">
                📱 Global eSIM Data ↗
            </a>
            <a href="{AMAZON_AFFILIATE_LINK}" target="_blank" style="background:#d97706;color:#fff;padding:12px 20px;text-decoration:none;font-weight:600;border-radius:8px;font-size:14px;">
                🎒 Recommended Travel Gear ↗
            </a>
        </div>
    </div>
    """

    full_page_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{topic['title']}</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
        <style>
            body {{ font-family: system-ui, -apple-system, sans-serif; background: #030712; color: #f3f4f6; line-height: 1.8; padding: 0; margin: 0; }}
            .header-bar {{ background: #0f172a; padding: 15px 5%; border-bottom: 1px solid #1f2937; display: flex; justify-content: space-between; align-items: center; }}
            .header-bar a {{ color: #9ca3af; text-decoration: none; font-size: 14px; font-weight: 500; }}
            .article-container {{ max-width: 800px; margin: 40px auto; padding: 0 20px; }}
            .badge {{ background: rgba(245, 158, 11, 0.15); color: #f59e0b; padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 600; text-transform: uppercase; display: inline-block; margin-bottom: 15px; }}
            h1 {{ font-size: 32px; color: #fff; margin-bottom: 20px; font-weight: 800; }}
            .featured-img {{ width: 100%; height: 420px; object-fit: cover; border-radius: 12px; margin-bottom: 30px; border: 1px solid #1f2937; }}
            .content p {{ margin-bottom: 20px; color: #cbd5e1; font-size: 16px; }}
            .content h2 {{ color: #fff; font-size: 22px; margin-top: 35px; margin-bottom: 15px; }}
            footer {{ text-align: center; padding: 40px; color: #9ca3af; font-size: 13px; border-top: 1px solid #1f2937; margin-top: 60px; }}
        </style>
    </head>
    <body>
        <div class="header-bar">
            <a href="index.html"><i class="fa-solid fa-arrow-left"></i> Back to Hub</a>
            <span style="color: #60a5fa; font-weight: 600;">TRTT Global Insights</span>
        </div>

        <main class="article-container">
            <span class="badge">{topic['category']}</span>
            <h1>{topic['title']}</h1>
            <img src="{image_url}" alt="{topic['title']}" class="featured-img">
            
            <div class="content">
                {article_body}
            </div>

            {recommendation_box}
        </main>

        <footer>
            <p>© 2026 TRTT News 24 BD | Roksana | Taifa | Tashrif Family Project</p>
        </footer>
    </body>
    </html>
    """

    # Save HTML file locally for GitHub Pages
    with open("latest_travel_news.html", "w", encoding="utf-8") as f:
        f.write(full_page_html)

    print(f"✅ Generated guide: {topic['title']}")
    
    # Send Telegram notification
    send_telegram_alert(topic['title'])
    
    # Auto-publish to Blogger with 1-second redirect to GitHub
    post_to_blogger(topic['title'], topic['focus'], image_url)
