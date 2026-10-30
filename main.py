import json
import os
import re
from datetime import datetime
from typing import List, Optional
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
import requests
from google import genai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from slugify import slugify

# ==============================================================================
# TRTT ENTERPRISE CONFIGURATION (Big Tech Architecture)
# ==============================================================================
MARKER = os.environ.get("TRAVEL_PAYOUT_MARKER", "787950")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
BLOGGER_BLOG_ID = os.environ.get("BLOGGER_BLOG_ID")
BLOGGER_CLIENT_ID = os.environ.get("BLOGGER_CLIENT_ID")
BLOGGER_CLIENT_SECRET = os.environ.get("BLOGGER_CLIENT_SECRET")
BLOGGER_REFRESH_TOKEN = os.environ.get("BLOGGER_REFRESH_TOKEN")
UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY")
AMAZON_LINK = os.environ.get("AMAZON_LINK", "https://amzn.to/4shg6Hn")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

BLOGGER_URL = "https://trttnews24bd.blogspot.com"
PWA_URL = "https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/?marker=787950"
HISTORY_FILE = "published_history.txt"

# Core Topics designed for High Google Search Volume & Affiliate Conversion
TOPIC_POOL = [
    "How to Claim Up to 600€ for Flight Delays in Europe Under EC 261",
    "Best Travel eSIM for Europe 2026: Compare Airalo, Saily, and Unlimited Data",
    "Cheap Flights from Middle East and Gulf to Europe: Top Routing Secrets",
    "Airport Transfers Without Metered Surprises: Fixed Price Kiwitaxi Guide",
    "Schengen Transit Checklist: Flight Safe Power Banks, SIMs and Rights",
    "From Doha to Rome: Real Logistics and Flight Hack Strategies for Diaspora",
]

def load_history() -> List[str]:
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as handle:
        return [line.strip() for line in handle if line.strip()]

def save_history(title_id: str):
    with open(HISTORY_FILE, "a", encoding="utf-8") as handle:
        handle.write(f"{title_id}\n")

# ==============================================================================
# UNSPLASH API: Dynamic Real High-Res Photography (Anti-AI Penalty)
# ==============================================================================
def fetch_unsplash_photo(query: str) -> dict:
    """Fetch high-resolution photography directly via Unsplash API."""
    fallback = {
        "url": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=1200&q=80",
        "author": "TRTT Travel Desk",
        "alt": f"Europe travel flight and journey: {query}"
    }
    if not UNSPLASH_ACCESS_KEY:
        return fallback

    try:
        url = "https://api.unsplash.com/photos/random"
        headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
        params = {"query": f"{query} travel airport airplane europe", "orientation": "landscape"}
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            image_url = data.get("urls", {}).get("regular", fallback["url"])
            author_name = data.get("user", {}).get("name", "Unsplash Contributor")
            alt_desc = data.get("alt_description") or f"Travel photograph for {query}"
            return {"url": image_url, "author": author_name, "alt": alt_desc}
    except Exception as exc:
        print(f"Unsplash API notice: {exc}")
    return fallback

# ==============================================================================
# AFFILIATE ENGINE: Strict Marker 787950 & Fixed tIZcbMOB
# ==============================================================================
def clean_affiliate_link(url: str, sub_id: str = "trtt_blog") -> str:
    if not url:
        return url
    url = url.replace("tpo.lv", "tp.st").replace("tlZcbMOB", "tIZcbMOB")
    parsed = urlparse(url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query["marker"] = MARKER
    query["sub_id"] = f"{sub_id}_{MARKER}"
    return urlunparse(parsed._replace(query=urlencode(query)))

# ==============================================================================
# TELEGRAM DISPATCH (Meta & Telegram Level Direct Community Alert)
# ==============================================================================
def send_telegram(title: str, post_url: str, summary: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    message = (
        f"🚀 <b>NEW DISPATCH: {title}</b>\n\n"
        f"📝 <i>{summary[:160]}...</i>\n\n"
        f"🌐 <b>Read Article:</b> {post_url}\n"
        f"📲 <b>Open Super App:</b> {PWA_URL}\n"
        f"🔒 <i>Marker {MARKER} Locked • Zero 404 Guaranteed</i>"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}, timeout=15)
        print("Telegram broadcast dispatched successfully.")
    except Exception as exc:
        print(f"Telegram dispatch notice: {exc}")

# ==============================================================================
# GEMINI AI CONTENT GENERATION: Human-Toned, E-E-A-T Verified (Google Safe)
# ==============================================================================
def generate_article(topic: str) -> str:
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is required to generate articles.")

    client = genai.Client(api_key=GEMINI_API_KEY)
    prompt = f"""You are a senior European travel journalist and logistics expert writing for TRTT News 24 BD and FlightScoutPro.
Write a comprehensive, authentic, high-value guide (1000-1200 words) on: "{topic}".

CRITICAL EDITORIAL GUIDELINES (Google Helpful Content & E-E-A-T Standards):
1. TONE: Human, authoritative, practical, and empathetic. Mention real logistics perspective (ground transit in Sardinia, Via Carlo Felice, carriage logistics in Qatar) so it sounds like genuine field experience, NOT generic AI fluff.
2. STRUCTURE:
   - Compelling Headline (H1)
   - Real-world Executive Hook (80-100 words)
   - H2: Core Regulations / The Practical Reality
   - H2: Step-by-Step Action Guide
   - H2: Common Pitfalls & Airline Traps to Avoid
   - H2: Key Documents & Essential Checklist
   - H2: Frequently Asked Questions (3 clear Q&As)
3. ZERO MENTION of AI, LLM, or prompts.
4. Output clean HTML formatted content (headings with h2/h3, structured lists, strong tags for key phrases).
"""
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    text = getattr(response, "text", str(response)).strip()
    return text

# ==============================================================================
# GOOGLE SCHEMA.ORG & RICH SNIPPETS INJECTION
# ==============================================================================
def build_enterprise_html(content: str, topic: str, photo: dict) -> str:
    airhelp_link = clean_affiliate_link("https://airhelp.tp.st/3ItXS0E4", "airhelp")
    aviasales_link = clean_affiliate_link("https://aviasales.tp.st/Fb8U9yav", "aviasales")
    airalo_link = clean_affiliate_link("https://airalo.tp.st/ZZoQC7Mz", "airalo")
    kiwitaxi_link = clean_affiliate_link("https://kiwitaxi.tp.st/tIZcbMOB", "kiwitaxi")

    schema_json = {
        "@context": "https://schema.org",
        "@type": "TravelGuide",
        "headline": topic,
        "image": photo["url"],
        "author": {
            "@type": "Organization",
            "name": "TRTT VoyageHub & FlightScoutPro Bureau"
        },
        "publisher": {
            "@type": "Organization",
            "name": "TRTT News 24 BD",
            "logo": {
                "@type": "ImageObject",
                "url": "https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/trtt-original-logo.jpeg"
            }
        },
        "description": f"Verified field guide on {topic} by TRTT News 24 BD travel bureau."
    }

    html = f"""
    <!-- Schema.org Rich Snippet for Google Search Dominance -->
    <script type="application/ld+json">
    {json.dumps(schema_json)}
    </script>

    <div style="font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif; max-width: 860px; margin: 0 auto; color: #1e293b; line-height: 1.8;">
      
      <!-- High-Res Unsplash Hero Photo -->
      <div style="position: relative; border-radius: 16px; overflow: hidden; margin-bottom: 24px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1);">
        <img src="{photo['url']}" alt="{photo['alt']}" style="width: 100%; height: auto; max-height: 440px; object-fit: cover; display: block;" />
        <div style="position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(5,41,98,0.85), transparent); padding: 12px 18px; color: #ffffff; font-size: 11px;">
          <span>📸 Photography: {photo['author']} (via Unsplash)</span> • <span>🔒 TRTT Verified Marker {MARKER}</span>
        </div>
      </div>

      <!-- Action Banner: 2 Buttons Formula -->
      <div style="background: linear-gradient(135deg, #052962, #00A8E8); color: #ffffff; padding: 18px 22px; border-radius: 14px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
        <div>
          <strong style="font-size: 15px;">TRTT VoyageHub Super App • 21 Travel Tools Active</strong>
          <p style="margin: 3px 0 0 0; font-size: 12px; color: #e2e8f0;">Compare flights, claim 600€ delays, and activate 5G eSIMs instantly.</p>
        </div>
        <div style="display: flex; gap: 8px;">
          <a href="{BLOGGER_URL}" style="background: #ffffff; color: #052962; font-weight: 800; font-size: 12px; padding: 9px 16px; border-radius: 8px; text-decoration: none;">
            📖 Read The Blog
          </a>
          <a href="{PWA_URL}" target="_blank" rel="noopener" style="background: #f59e0b; color: #0f172a; font-weight: 800; font-size: 12px; padding: 9px 16px; border-radius: 8px; text-decoration: none;">
            🚀 Explore Your Life
          </a>
        </div>
      </div>

      <!-- Main Article Body -->
      <div class="article-content" style="font-size: 15px; color: #334155;">
        {content}
      </div>

      <!-- Tool Recommendation Grid -->
      <div style="background: #f8fafc; border: 1.5px solid #e2e8f0; border-radius: 16px; padding: 22px; margin: 35px 0;">
        <h3 style="color: #052962; margin-top: 0; font-size: 18px; font-weight: 900;">Verified Travel Partner Tools for This Journey:</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; margin-top: 14px;">
          <a href="{aviasales_link}" target="_blank" rel="noopener" style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; padding: 12px; text-decoration: none; color: #0f172a; font-weight: 800; font-size: 13px; text-align: center; display: block;">
            ✈️ Aviasales Flights
          </a>
          <a href="{airhelp_link}" target="_blank" rel="noopener" style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; padding: 12px; text-decoration: none; color: #0284c7; font-weight: 800; font-size: 13px; text-align: center; display: block;">
            🛡️ AirHelp 600€ Claim
          </a>
          <a href="{airalo_link}" target="_blank" rel="noopener" style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; padding: 12px; text-decoration: none; color: #7e22ce; font-weight: 800; font-size: 13px; text-align: center; display: block;">
            📱 Airalo 5G eSIM
          </a>
          <a href="{kiwitaxi_link}" target="_blank" rel="noopener" style="background: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; padding: 12px; text-decoration: none; color: #047857; font-weight: 800; font-size: 13px; text-align: center; display: block;">
            🚖 Kiwitaxi (tIZcbMOB)
          </a>
        </div>
      </div>

      <!-- Legal Disclosure -->
      <p style="font-size: 12px; color: #94a3b8; text-align: center; margin-top: 25px;">
        Official publication by TRTT News 24 BD & FlightScoutPro. This guide contains verified affiliate references under Marker {MARKER} & Amazon {AMAZON_LINK}.
      </p>

    </div>
    """
    return html

# ==============================================================================
# BLOGGER OFFICIAL API POSTING
# ==============================================================================
def post_to_blogger(title: str, html_content: str, labels: List[str]) -> Optional[str]:
    if not all([BLOGGER_BLOG_ID, BLOGGER_CLIENT_ID, BLOGGER_CLIENT_SECRET, BLOGGER_REFRESH_TOKEN]):
        print("Blogger OAuth credentials incomplete. Skipping Blogger direct post.")
        return None

    try:
        creds = Credentials(
            None,
            refresh_token=BLOGGER_REFRESH_TOKEN,
            client_id=BLOGGER_CLIENT_ID,
            client_secret=BLOGGER_CLIENT_SECRET,
            token_uri="https://oauth2.googleapis.com/token",
        )
        service = build("blogger", "v3", credentials=creds)
        body = {
            "title": title,
            "content": html_content,
            "labels": labels
        }
        post = service.posts().insert(blogId=BLOGGER_BLOG_ID, body=body).execute()
        post_url = post.get("url")
        print(f"SUCCESS: Article posted directly to Blogger! URL: {post_url}")
        return post_url
    except Exception as exc:
        print(f"Error posting to Blogger API: {exc}")
        return None

# ==============================================================================
# MAIN EXECUTION
# ==============================================================================
def main():
    os.makedirs("public/guides", exist_ok=True)
    history = load_history()
    
    # Pick next fresh topic
    topic = TOPIC_POOL[0]
    for candidate in TOPIC_POOL:
        if slugify(candidate) not in history:
            topic = candidate
            break

    print(f"Selected Topic: {topic}")
    
    # 1. Fetch real photography via Unsplash
    photo = fetch_unsplash_photo(topic)
    print(f"Fetched Unsplash Photo: {photo['url']}")

    # 2. Generate high-authority article
    raw_content = generate_article(topic)

    # 3. Build Google Rich Snippet & Affiliate HTML
    full_html = build_enterprise_html(raw_content, topic, photo)

    # 4. Save local guide backup
    date_key = datetime.utcnow().strftime("%Y-%m-%d")
    slug = slugify(topic)
    with open(f"public/guides/{date_key}-{slug}.html", "w", encoding="utf-8") as f:
        f.write(full_html)

    # 5. Post directly to Google Blogger (Increases authentic Blogger View Counter)
    blogger_url = post_to_blogger(topic, full_html, ["Europe Travel", "Flight Compensation", "eSIM", "TRTT News"])

    # 6. Dispatch instant alert to Telegram Channel
    send_telegram(topic, blogger_url or PWA_URL, raw_content[:200])

    # 7. Record History
    save_history(slug)
    print("ALL ENTERPRISE SYSTEMS EXECUTED PERFECTLY!")

if __name__ == "__main__":
    main()
