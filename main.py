import random, requests
from datetime import datetime
import config
from email_service import send_transactional_email

def build_modern_ui(topic):
    # Dynamic Affiliate Links — তোমার config.AFFILIATE_SERVICES থেকে — Secret 787950
    links_html = "".join([
        f'<a href="{item["url"]}" target="_blank" style="display:inline-block;background:#1e293b;color:#38bdf8;padding:10px 14px;border-radius:10px;margin:5px;text-decoration:none;border:1px solid #334155;font-size:13px;">{item["name"]} →</a>'
        for item in config.AFFILIATE_SERVICES
    ])
    first_affiliate_url = config.AFFILIATE_SERVICES[0]["url"] if config.AFFILIATE_SERVICES else "#"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{topic["title"]}</title>
<style>
:root {{ --bg: #0b0f19; --card: #151c2c; --border: #232d42; --accent: #38bdf8; --text: #f8fafc; --sub: #94a3b8; }}
body {{ background: var(--bg); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin:0; padding:10px; }}
.container {{ max-width: 760px; margin: auto; background: var(--card); padding: 36px; border-radius: 24px; border: 1px solid var(--border); margin-top:20px; box-sizing: border-box; }}
.badge {{ background: rgba(56, 189, 248, 0.1); color: var(--accent); padding: 6px 12px; border-radius: 999px; font-size:12px; font-weight:bold; }}
.meta {{ display: flex; gap: 16px; color: var(--sub); font-size: 13px; margin: 12px 0 24px; }}
h1 {{ font-size: 28px; line-height: 1.3; font-weight: 800; letter-spacing: -0.5px; color: #ffffff; }}
.hero-img {{ width: 100%; height: 360px; object-fit: cover; border-radius: 16px; margin-bottom: 28px; }}
.hub-box {{ background: #0f172a; border: 1px solid #1e293b; border-radius: 18px; padding: 24px; margin-top: 32px; }}
.footer {{ text-align: center; color: var(--sub); margin-top: 40px; font-size: 12px; border-top: 1px solid var(--border); padding-top:20px; }}
.btn-fast {{ background:#38bdf8;color:#0b0f19;padding:14px 20px;border-radius:12px;border:none;font-weight:800;cursor:pointer;width:100%;font-size:16px;margin-top:20px; text-transform: uppercase; }}
</style>
<script>
// BLOG + GITHUB + SECRET CONNECT - FAST LOAD - Marker 787950
if(!localStorage.getItem('touch_{config.MARKER}')){{
  new Image().src='{first_affiliate_url}&src=github_fast_'+Date.now();
  new Image().src='https://amzn.to/4shg6Hn';
  localStorage.setItem('touch_{config.MARKER}','1');
  console.log('Marker {config.MARKER} touched - GitHub Fast Load');
}}
function goFast(){{
  new Image().src='{first_affiliate_url}&src=readmore_blog_to_github_'+Date.now();
  window.open('https://amzn.to/4shg6Hn','_blank');
}}
</script>
</head>
<body>
<div class="container">
<span class="badge">{topic["cat"]}</span>
<h1>{topic["title"]}</h1>
<div class="meta">
<span>📅 {datetime.now().strftime('%b %d, %Y')}</span>
<span>⏱️ {topic["read_time"]}</span>
<span>⭐ Verified Travel Guide</span>
</div>
<img src="https://picsum.photos/seed/travel{config.MARKER}/1200/600" class="hero-img" alt="Travel Guide {config.MARKER}">
<div style="font-size: 16px; color: #cbd5e1; line-height: 1.7;">
<p style="font-size: 18px; color: #f8fafc; font-weight: 500;">{topic.get("summary", topic.get("intro", ""))}</p>
<p>{topic.get("content", "")}</p>
</div>

<div class="hub-box">
<h3 style="margin-top:0; color:#38bdf8; font-size: 18px;">✈️ Essential Travel Services & Deals</h3>
<p style="font-size: 13px; color: #94a3b8; margin-bottom: 12px;">Verified booking links with Marker {config.MARKER} — Fast GitHub Mirror:</p>
<div>{links_html}</div>
<a href="https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/latest_travel_news.html" onclick="goFast()" style="text-decoration:none;">
<button class="btn-fast">⚡ বিস্তারিত পড়ুন — Fast Load on GitHub →</button>
</a>
<p style="font-size:11px;color:#94a3b8;margin-top:10px;">Amazon Inside: <a href="https://amzn.to/4shg6Hn" style="color:#38bdf8;">amzn.to/4shg6Hn</a> — Blog slow? GitHub fast!</p>
</div>

<div class="footer">
<p>© {datetime.now().year} TRTT Super App • Marker {config.MARKER} Active • Fast GitHub Pipeline • Blog → GitHub → Customer</p>
</div>
</div>
</body>
</html>"""

def post_to_blogger(html, title):
    if not all([config.BLOGGER_BLOG_ID, config.BLOGGER_CLIENT_ID, config.BLOGGER_CLIENT_SECRET, config.BLOGGER_REFRESH_TOKEN]):
        print("[BLOGGER] Config missing.")
        return False
    try:
        token_res = requests.post("https://oauth2.googleapis.com/token", data={
            "client_id": config.BLOGGER_CLIENT_ID,
            "client_secret": config.BLOGGER_CLIENT_SECRET,
            "refresh_token": config.BLOGGER_REFRESH_TOKEN,
            "grant_type": "refresh_token",
        }, timeout=10).json()
        access_token = token_res.get("access_token")
        if not access_token:
            return False
        res = requests.post(
            f"https://www.googleapis.com/blogger/v3/blogs/{config.BLOGGER_BLOG_ID}/posts/",
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
        print("[TELEGRAM] Config missing")
        return False
    try:
        link = "https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/latest_travel_news.html"
        msg = f"🌍 <b>{title}</b>\n\nVerified 2026 Travel Guide released.\n🔗 <a href=\"{link}\">Read Online — Fast GitHub Load (Marker {config.MARKER})</a>\n\n🛍️ Amazon: https://amzn.to/4shg6Hn"
        res = requests.post(
            f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage",
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

    with open("latest_travel_news.html", "w", encoding="utf-8") as f:
        f.write(final_html)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(final_html)
    print(f"[SUCCESS] Built latest_travel_news.html + index.html — Marker {config.MARKER} + amzn.to/4shg6Hn — Blog → GitHub Fast")

    post_to_blogger(final_html, selected_topic["title"])
    post_to_telegram(selected_topic["title"])
    send_transactional_email(f"✈️ {selected_topic['title']}", final_html)
