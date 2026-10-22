import random, requests
from datetime import datetime
import config
from email_service import send_transactional_email

def build_modern_ui(topic):
    """
    Generates a modern, mobile-first responsive web design with dark slate theme.
    """
    links_html = "".join([
        f'<a href="{item["url"]}" target="_blank" style="display:inline-block;background:#1e293b;color:#38bdf8;padding:10px 16px;border-radius:10px;text-decoration:none;font-size:13px;font-weight:600;border:1px solid #334155;margin:4px;">{item["name"]} <span style="font-size:10px;background:#0369a1;color:#e0f2fe;padding:2px 6px;border-radius:6px;margin-left:4px;">{item["tag"]}</span></a>'
        for item in config.AFFILIATE_SERVICES
    ])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{topic["title"]}</title>
<style>
    :root {{ --bg: #0b0f19; --card: #151c2c; --border: #232d42; --accent: #38bdf8; --text: #f8fafc; --sub: #94a3b8; }}
    body {{ background: var(--bg); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; padding: 24px 12px; margin: 0; line-height: 1.6; }}
    .container {{ max-width: 760px; margin: auto; background: var(--card); padding: 36px; border-radius: 24px; border: 1px solid var(--border); box-shadow: 0 20px 40px rgba(0,0,0,0.5); }}
    .badge {{ background: rgba(56, 189, 248, 0.1); color: var(--accent); padding: 6px 12px; border-radius: 9999px; font-size: 11px; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; border: 1px solid rgba(56, 189, 248, 0.2); }}
    .meta {{ display: flex; gap: 16px; color: var(--sub); font-size: 13px; margin: 16px 0 24px; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 16px; }}
    h1 {{ font-size: 28px; line-height: 1.3; margin-top: 12px; font-weight: 800; letter-spacing: -0.5px; }}
    .hero-img {{ width: 100%; height: 360px; object-fit: cover; border-radius: 16px; margin-bottom: 28px; }}
    .hub-box {{ background: #0f172a; border: 1px solid #1e293b; border-radius: 18px; padding: 24px; margin-top: 32px; }}
    .footer {{ text-align: center; color: var(--sub); margin-top: 40px; font-size: 12px; border-top: 1px solid var(--border); padding-top: 24px; }}
</style>
</head>
<body>
<div class="container">
    <span class="badge">{topic["cat"]}</span>
    <h1>{topic["title"]}</h1>
    <div class="meta">
        <span>📅 {datetime.now().strftime('%b %d, 2026')}</span>
        <span>⏱️ {topic["read_time"]}</span>
        <span>⭐ Verified Travel Guide</span>
    </div>
    
    <img src="[https://picsum.photos/seed/travel787950/1200/600](https://picsum.photos/seed/travel787950/1200/600)" class="hero-img" alt="Travel Header">
    
    <div style="font-size: 16px; color: #cbd5e1;">
        <p style="font-size: 18px; color: #f8fafc; font-weight: 500;">{topic["summary"]}</p>
        <p>Planning travel across Europe requires precision. Rates update dynamically, making automated price checks and instant eSIM setups essential for modern itineraries.</p>
    </div>

    <!-- Smart Hub Section -->
    <div class="hub-box">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
            <h3 style="margin:0; color:#fff; font-size:18px;">TRTT Smart Travel Engine</h3>
            <span style="font-size:11px; color:var(--sub);">Marker #{config.MARKER}</span>
        </div>
        <div>{links_html}</div>
    </div>

    <div class="footer">
        TRTT Global Voyage Architecture © 2026 • Verified Affiliate Network
    </div>
</div>
</body>
</html>"""

def post_to_blogger(html, title):
    if not all([config.BLOGGER_BLOG_ID, config.BLOGGER_CLIENT_ID, config.BLOGGER_CLIENT_SECRET, config.BLOGGER_REFRESH_TOKEN]):
        print("[BLOGGER] Config missing.")
        return False
    try:
        token_res = requests.post("[https://oauth2.googleapis.com/token](https://oauth2.googleapis.com/token)", data={
            "client_id": config.BLOGGER_CLIENT_ID,
            "client_secret": config.BLOGGER_CLIENT_SECRET,
            "refresh_token": config.BLOGGER_REFRESH_TOKEN,
            "grant_type": "refresh_token"
        }, timeout=10).json()
        
        access_token = token_res.get("access_token")
        if not access_token:
            return False

        res = requests.post(
            f"[https://www.googleapis.com/blogger/v3/blogs/](https://www.googleapis.com/blogger/v3/blogs/){config.BLOGGER_BLOG_ID}/posts/",
            json={"kind": "blogger#post", "blog": {"id": config.BLOGGER_BLOG_ID}, "title": title, "content": html},
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10
        )
        print(f"[BLOGGER] Status: {res.status_code}")
        return res.status_code == 200
    except Exception as e:
        print(f"[BLOGGER ERROR] {e}")
        return False

def post_to_telegram(title):
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
        return False
    try:
        link = "[https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/latest_travel_news.html](https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/latest_travel_news.html)"
        msg = f"✈️ <b>{title}</b>\n\nVerified 2026 Travel Guide released.\n🔗 <a href='{link}'>Read Online</a>"
        res = requests.post(
            f"[https://api.telegram.org/bot](https://api.telegram.org/bot){config.TELEGRAM_BOT_TOKEN}/sendMessage",
            data={"chat_id": config.TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "HTML"},
            timeout=10
        )
        print(f"[TELEGRAM] Status: {res.status_code}")
        return res.status_code == 200
    except Exception as e:
        print(f"[TELEGRAM ERROR] {e}")
        return False

if __name__ == "__main__":
    selected_topic = random.choice(config.TOPICS)
    final_html = build_modern_ui(selected_topic)

    # 1. Output HTML File
    with open("latest_travel_news.html", "w", encoding="utf-8") as f:
        f.write(final_html)
    print("[SUCCESS] Local build generated.")

    # 2. Trigger Integrations
    post_to_blogger(final_html, selected_topic["title"])
    post_to_telegram(selected_topic["title"])
    send_transactional_email(f"✈️ {selected_topic['title']}", final_html)
