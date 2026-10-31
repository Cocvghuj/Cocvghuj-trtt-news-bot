"""
TRTT Enterprise Auto-Publisher Engine (Google Blogger Direct & Multi-Blog Network)
Protocol 26391/2026 • Marker 787950 LOCKED
Dedicated to family: Roksana | Taifa | Tashrif (From Sanluri to Dhaka)
Strictly compliant with Google Search, Google Search Console, and GitHub Rules.
"""

import json
import os
import re
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
import requests
from google import genai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
try:
    from slugify import slugify
except ImportError:
    def slugify(text: str) -> str:
        text = re.sub(r'[^\w\s-]', '', str(text).lower())
        return re.sub(r'[-\s]+', '-', text).strip('-')

# ==============================================================================
# CONFIGURATION & SECRETS
# ==============================================================================
MARKER = os.environ.get("TRAVEL_PAYOUT_MARKER", "787950")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Primary & Partner Blog IDs for Multi-Blog Syndication
BLOGGER_BLOG_ID = os.environ.get("BLOGGER_BLOG_ID")
FLIGHTSCOUTPRO_BLOG_ID = os.environ.get("FLIGHTSCOUTPRO_BLOG_ID")
PARTNER_BLOG_IDS = os.environ.get("PARTNER_BLOG_IDS", "")  # Comma-separated: "id1,id2,id3"

# Blogger OAuth2 Credentials
BLOGGER_CLIENT_ID = os.environ.get("BLOGGER_CLIENT_ID")
BLOGGER_CLIENT_SECRET = os.environ.get("BLOGGER_CLIENT_SECRET")
BLOGGER_REFRESH_TOKEN = os.environ.get("BLOGGER_REFRESH_TOKEN")

UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY")
AMAZON_LINK = os.environ.get("AMAZON_LINK", "https://amzn.to/4shg6Hn")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

BLOGGER_URL = "https://trttnews24bd.blogspot.com"
PWA_URL = "https://cocvghuj-trtt-news-bot.vercel.app/?marker=787950"
HISTORY_FILE = "published_history.txt"

# Core Topics designed for High Google Search Volume & Affiliate Conversion
TOPIC_POOL = [
    {
        "topic": "How to Claim Up to 600€ for Flight Delays in Europe Under EC 261",
        "category": "Passenger Rights",
        "default_labels": ["Flight Compensation", "AirHelp", "EU Regulation 261", "Passenger Rights", "Europe Travel", "TRTT News 24 BD"]
    },
    {
        "topic": "Best Travel eSIM for Europe 2026: Compare Airalo, Saily, and Unlimited Data",
        "category": "eSIM & Connectivity",
        "default_labels": ["eSIM", "Airalo", "Saily", "Europe Travel", "Travel Tech", "TRTT News 24 BD"]
    },
    {
        "topic": "Cheap Flights from Middle East and Gulf to Europe: Top Routing Secrets",
        "category": "Cheap Flights",
        "default_labels": ["Aviasales", "Cheap Flights", "Qatar Airways", "Gulf to Europe", "Flight Hacks", "TRTT News 24 BD"]
    },
    {
        "topic": "Airport Transfers Without Metered Surprises: Fixed Price Kiwitaxi Guide",
        "category": "Airport Transfers",
        "default_labels": ["Kiwitaxi", "Airport Transfer", "Taxi Booking", "Europe Travel", "Sanluri", "TRTT News 24 BD"]
    },
    {
        "topic": "Schengen Transit Checklist: Flight Safe Power Banks, SIMs and Rights",
        "category": "Travel Logistics",
        "default_labels": ["Schengen Travel", "Flight Essentials", "Amazon Travel", "Transit Guide", "TRTT News 24 BD"]
    },
    {
        "topic": "From Doha to Rome: Real Logistics and Flight Hack Strategies for Diaspora",
        "category": "Diaspora & Expat Travel",
        "default_labels": ["Doha to Rome", "Expat Travel", "Flight Routes", "Sanluri", "Dhaka", "TRTT News 24 BD"]
    },
    {
        "topic": "European Car Rental Secrets: How to Avoid Hidden Insurance Fees with LocalRent",
        "category": "Car Rental",
        "default_labels": ["Car Rental", "LocalRent", "Road Trip", "Italy Travel", "Budget Travel", "TRTT News 24 BD"]
    },
    {
        "topic": "Skip The Line in Rome, Paris, and Barcelona: Complete Museum Pass Guide",
        "category": "Sightseeing & Tours",
        "default_labels": ["Tiqets", "Museum Passes", "Rome Colosseum", "Paris Louvre", "Sightseeing", "TRTT News 24 BD"]
    }
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
# UNSPLASH API: Dynamic Real High-Res Photography
# ==============================================================================
def fetch_unsplash_photo(query: str) -> dict:
    fallback = {
        "url": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=1200&q=80",
        "author": "TRTT Travel Bureau",
        "alt": f"Europe travel flight and journey: {query}"
    }
    if not UNSPLASH_ACCESS_KEY:
        return fallback
    try:
        url = "https://api.unsplash.com/photos/random"
        headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
        params = {"query": f"{query} travel", "orientation": "landscape"}
        res = requests.get(url, headers=headers, params=params, timeout=10)
        if res.status_code == 200:
            data = res.json()
            return {
                "url": data["urls"]["regular"],
                "author": data["user"]["name"],
                "alt": data.get("alt_description") or f"Europe Travel: {query}"
            }
    except Exception as exc:
        print(f"Unsplash API notice: {exc}")
    return fallback

def clean_affiliate_link(base_url: str, partner_name: str) -> str:
    parsed = urlparse(base_url)
    params = dict(parse_qsl(parsed.query))
    params["marker"] = MARKER
    params["sub_id"] = f"blogger_seo_{partner_name}_{MARKER}"
    return urlunparse(parsed._replace(query=urlencode(params)))

# ==============================================================================
# GEMINI AI ARTICLE & METADATA GENERATOR (E-E-A-T Standards)
# ==============================================================================
def generate_article_with_metadata(topic_info: dict) -> dict:
    topic = topic_info["topic"]
    if not GEMINI_API_KEY:
        print("CRITICAL: GEMINI_API_KEY missing. Cannot generate fresh article.")
        return None

    client = genai.Client(api_key=GEMINI_API_KEY)
    
    prompt = f"""You are a senior European travel journalist and logistics expert writing for TRTT News 24 BD and partner network.
Generate a comprehensive, authentic, high-value guide for the topic: "{topic}".

EDITORIAL REQUIREMENTS (Google Helpful Content & E-E-A-T Standards):
1. TONE: Human, authoritative, practical, and empathetic. Mention real logistics perspective (ground transit in Sardinia, Via Carlo Felice, carriage logistics in Qatar) so it sounds like genuine field experience, NOT generic AI fluff.
2. STRUCTURE:
   - Output clean HTML body (headings with h2/h3, bullet points, callout boxes).
   - Real-world Executive Hook (80-100 words)
   - H2: Core Legal & Practical Reality
   - H2: Step-by-Step Action Guide
   - H2: Pitfalls & Airline Traps to Avoid
   - H2: Essential Checklist & Gear
   - H2: Frequently Asked Questions (3 clear Q&As)
3. ZERO MENTION of AI, LLM, or prompts.
4. Also generate a JSON header block formatted as:
[METADATA]
{{
  "title": "{topic}",
  "search_description": "Clear 150-char Google Search summary for Search Console",
  "labels": ["Tag1", "Tag2", "Tag3", "Tag4", "Tag5"],
  "permalink_slug": "url-friendly-slug-for-blogger"
}}
[/METADATA]
Followed by the complete HTML article."""

    try:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        text = getattr(response, "text", str(response)).strip()
        
        # Parse metadata block if present
        meta = {
            "title": topic,
            "search_description": f"Verified field guide on {topic} with official passenger rights and booking tips by TRTT News 24 BD.",
            "labels": topic_info["default_labels"],
            "permalink_slug": slugify(topic)
        }
        
        meta_match = re.search(r'\[METADATA\](.*?)\[/METADATA\]', text, re.DOTALL)
        content_html = text
        if meta_match:
            try:
                parsed_meta = json.loads(meta_match.group(1).strip())
                meta["title"] = parsed_meta.get("title", meta["title"])
                meta["search_description"] = parsed_meta.get("search_description", meta["search_description"])[:160]
                if parsed_meta.get("labels"):
                    meta["labels"] = list(set(meta["labels"] + parsed_meta["labels"]))
                if parsed_meta.get("permalink_slug"):
                    meta["permalink_slug"] = slugify(parsed_meta["permalink_slug"])
            except Exception as e:
                print(f"Metadata JSON parsing notice: {e}")
            content_html = text.replace(meta_match.group(0), "").strip()

        return {
            "meta": meta,
            "content": content_html
        }
    except Exception as exc:
        print(f"Gemini generation error: {exc}")
        return None

# ==============================================================================
# GOOGLE SCHEMA.ORG, OPEN GRAPH & RICH SNIPPETS INJECTION
# ==============================================================================
def build_enterprise_html(article_data: dict, photo: dict) -> str:
    meta = article_data["meta"]
    content = article_data["content"]
    title = meta["title"]
    search_desc = meta["search_description"]
    tags_str = ", ".join(meta["labels"])
    
    airhelp_link = clean_affiliate_link("https://airhelp.tp.st/3ItXS0E4", "airhelp")
    aviasales_link = clean_affiliate_link("https://aviasales.tp.st/Fb8U9yav", "aviasales")
    airalo_link = clean_affiliate_link("https://airalo.tp.st/ZZoQC7Mz", "airalo")
    kiwitaxi_link = clean_affiliate_link("https://kiwitaxi.tp.st/tlZcbMOB", "kiwitaxi")

    schema_json = {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": title,
        "description": search_desc,
        "image": [photo["url"]],
        "datePublished": datetime.utcnow().isoformat(),
        "dateModified": datetime.utcnow().isoformat(),
        "author": {
            "@type": "Person",
            "name": "Abu Taher & TRTT Editorial Bureau",
            "jobTitle": "Senior Travel Logistics Specialist"
        },
        "publisher": {
            "@type": "Organization",
            "name": "TRTT News 24 BD & FlightScoutPro Network",
            "logo": {
                "@type": "ImageObject",
                "url": "https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/trtt-original-logo.jpeg"
            }
        },
        "contentLocation": {
            "@type": "Place",
            "name": "Sanluri, Sardinia, Italy",
            "geo": {
                "@type": "GeoCoordinates",
                "latitude": 39.5613,
                "longitude": 8.6332
            }
        },
        "keywords": tags_str,
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": f"{BLOGGER_URL}/{meta['permalink_slug']}.html"
        }
    }

    html = f"""
<!-- Google Search Console & SEO Meta Header -->
<meta name="description" content="{search_desc}">
<meta name="keywords" content="{tags_str}">
<meta name="geo.region" content="IT-CA">
<meta name="geo.placename" content="Sanluri, Sardinia, Italy">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{search_desc}">
<meta property="og:image" content="{photo['url']}">
<meta property="og:type" content="article">

<!-- Schema.org Rich Snippet for Instant Google Search Indexing -->
<script type="application/ld+json">
{json.dumps(schema_json, indent=2)}
</script>

<div style="font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif; max-width: 860px; margin: 0 auto; color: #1e293b; line-height: 1.8;">

  <!-- Location & Metadata Badge -->
  <div style="display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 16px; font-size: 11px; color: #64748b;">
    <span style="background: #e0f2fe; color: #0369a1; padding: 4px 10px; border-radius: 6px; font-weight: bold;">📍 Sanluri, Sardinia, Italy &amp; Dhaka</span>
    <span style="background: #fef3c7; color: #92400e; padding: 4px 10px; border-radius: 6px; font-weight: bold;">🔒 Marker {MARKER} Locked</span>
    <span style="background: #f1f5f9; color: #475569; padding: 4px 10px; border-radius: 6px;">🏷️ {tags_str}</span>
  </div>

  <!-- High-Res Photography -->
  <div style="position: relative; border-radius: 16px; overflow: hidden; margin-bottom: 24px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1);">
    <img src="{photo['url']}" alt="{photo['alt']}" style="width: 100%; height: auto; max-height: 440px; object-fit: cover; display: block;" />
    <div style="position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(5,41,98,0.85), transparent); padding: 12px 18px; color: #ffffff; font-size: 11px;">
      <span>📸 Photography: {photo['author']} (via Unsplash)</span> • <span>Verified Field Report</span>
    </div>
  </div>

  <!-- Action Bar: Direct 21 Tools Super App Access -->
  <div style="background: linear-gradient(135deg, #052962, #00A8E8); color: #ffffff; padding: 18px 22px; border-radius: 14px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
    <div>
      <strong style="font-size: 15px;">TRTT VoyageHub Super App • 21 Travel Tools Active</strong>
      <p style="margin: 3px 0 0 0; font-size: 12px; color: #e2e8f0;">Compare flights, claim 600€ delays, and activate 5G eSIMs instantly.</p>
    </div>
    <div style="display: flex; gap: 8px;">
      <a href="{BLOGGER_URL}" style="background: #ffffff; color: #052962; font-weight: 800; font-size: 12px; padding: 9px 16px; border-radius: 8px; text-decoration: none;">
        📖 Blog Feed
      </a>
      <a href="{PWA_URL}" target="_blank" rel="noopener" style="background: #f59e0b; color: #0f172a; font-weight: 800; font-size: 12px; padding: 9px 16px; border-radius: 8px; text-decoration: none;">
        🚀 Explore 21 Tools
      </a>
    </div>
  </div>

  <!-- Article Body -->
  <div style="font-size: 15px; color: #334155;">
    {content}
  </div>

  <!-- High-Converting Verified Affiliate Strip -->
  <div style="background: #f8fafc; border: 2px solid #e2e8f0; border-radius: 16px; padding: 22px; margin-top: 36px;">
    <h3 style="margin: 0 0 14px 0; font-size: 16px; color: #0f172a;">🛡️ Verified Travel &amp; Logistics Partners (Marker {MARKER})</h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px;">
      <a href="{airhelp_link}" target="_blank" rel="noopener" style="display: block; padding: 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; text-decoration: none; color: #0f172a; font-weight: bold; font-size: 13px;">
        🛡️ AirHelp €600 Claim &rarr;
      </a>
      <a href="{aviasales_link}" target="_blank" rel="noopener" style="display: block; padding: 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; text-decoration: none; color: #0f172a; font-weight: bold; font-size: 13px;">
        ✈️ Aviasales Lowest Fares &rarr;
      </a>
      <a href="{airalo_link}" target="_blank" rel="noopener" style="display: block; padding: 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; text-decoration: none; color: #0f172a; font-weight: bold; font-size: 13px;">
        📱 Airalo Instant 5G eSIM &rarr;
      </a>
      <a href="{kiwitaxi_link}" target="_blank" rel="noopener" style="display: block; padding: 12px; background: #ffffff; border: 1px solid #cbd5e1; border-radius: 10px; text-decoration: none; color: #0f172a; font-weight: bold; font-size: 13px;">
        🚖 Kiwitaxi Fixed Airport Ride &rarr;
      </a>
    </div>
  </div>

  <!-- Dedicated Author Bio & Family Tribute -->
  <div style="border-top: 1px solid #e2e8f0; margin-top: 32px; padding-top: 20px; font-size: 12px; color: #64748b;">
    <p style="margin: 0;">
      <strong>Published by TRTT News 24 BD &amp; FlightScoutPro Network</strong> • Dedicated to Roksana, Taifa &amp; Tashrif • 
      Written from Sanluri, Sardinia, Italy (Via Carlo Felice ARST 08:17) to Dhaka, Bangladesh.
    </p>
  </div>

</div>
"""
    return html

# ==============================================================================
# MULTI-BLOG BROADCASTING VIA OFFICIAL GOOGLE BLOGGER API
# ==============================================================================
def post_to_multi_blogs(title: str, html_content: str, meta: dict) -> List[str]:
    """Simultaneously publishes to TRTT News 24 BD & Partner Blogs so each partner sees authentic Google Views."""
    if not all([BLOGGER_CLIENT_ID, BLOGGER_CLIENT_SECRET, BLOGGER_REFRESH_TOKEN]):
        print("Notice: Blogger OAuth credentials not configured in secrets. Skipping live Blogger API post.")
        return []

    target_blog_ids = []
    if BLOGGER_BLOG_ID:
        target_blog_ids.append(("TRTT News 24 BD (Main Hub)", BLOGGER_BLOG_ID))
    if FLIGHTSCOUTPRO_BLOG_ID:
        target_blog_ids.append(("FlightScoutPro (Partner Blog)", FLIGHTSCOUTPRO_BLOG_ID))
    
    # Also support multiple partner IDs passed as comma-separated list
    if PARTNER_BLOG_IDS:
        for idx, p_id in enumerate(PARTNER_BLOG_IDS.split(","), 1):
            cleaned = p_id.strip()
            if cleaned and cleaned not in [BLOGGER_BLOG_ID, FLIGHTSCOUTPRO_BLOG_ID]:
                target_blog_ids.append((f"Partner Network Blog #{idx}", cleaned))

    # Read from partners.json if available
    if os.path.exists("partners.json"):
        try:
            with open("partners.json", "r", encoding="utf-8") as pf:
                partners_data = json.load(pf)
                for partner in partners_data:
                    b_id = partner.get("blog_id")
                    b_name = partner.get("site_name", "Partner Blog")
                    if b_id and b_id not in [bid for _, bid in target_blog_ids]:
                        target_blog_ids.append((b_name, b_id))
        except Exception as e:
            print(f"partners.json read notice: {e}")

    published_urls = []
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
            "labels": meta["labels"],
            "location": {
                "name": "Sanluri, Sardinia, Italy",
                "lat": 39.5613,
                "lng": 8.6332,
                "span": "0.05,0.05"
            }
        }

        for blog_name, blog_id in target_blog_ids:
            try:
                post = service.posts().insert(blogId=blog_id, body=body, isDraft=False).execute()
                p_url = post.get("url")
                published_urls.append(p_url)
                print(f"SUCCESS: Published to {blog_name} (Blog ID: {blog_id})! URL: {p_url}")
            except Exception as blog_err:
                print(f"Notice posting to {blog_name} (ID: {blog_id}): {blog_err}")

        return published_urls
    except Exception as exc:
        print(f"Error initializing Google Blogger API: {exc}")
        return published_urls

# ==============================================================================
# TELEGRAM DISPATCH
# ==============================================================================
def send_telegram(title: str, url: str, excerpt: str):
    if not (TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID):
        return
    try:
        clean_excerpt = re.sub(r'<[^>]+>', '', excerpt)[:200]
        text = f"✈️ <b>TRTT Travel News Alert</b>\n\n<b>{title}</b>\n\n{clean_excerpt}...\n\n🔗 <a href='{url}'>Read Full Verified Article</a>\n\n<i>📍 Sanluri, Sardinia &amp; Dhaka • Marker {MARKER}</i>"
        endpoint = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(endpoint, json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=8)
        print("Telegram broadcast dispatched.")
    except Exception as exc:
        print(f"Telegram notice: {exc}")

# ==============================================================================
# MAIN ENTRYPOINT
# ==============================================================================
def main():
    history = load_history()
    
    # 1. Pick next fresh topic from pool
    selected_topic_info = TOPIC_POOL[0]
    for candidate in TOPIC_POOL:
        if slugify(candidate["topic"]) not in history:
            selected_topic_info = candidate
            break

    print(f"Selected Topic: {selected_topic_info['topic']}")

    # 2. Fetch real Unsplash Photography
    photo = fetch_unsplash_photo(selected_topic_info["topic"])
    print(f"Fetched Photography: {photo['url']}")

    # 3. Generate article with metadata (Title, Labels, Search Description, Slug, Location)
    article_data = generate_article_with_metadata(selected_topic_info)
    if not article_data:
        print("Skipping execution due to generation error.")
        return

    # 4. Build Enterprise HTML with Schema.org & Meta Tags
    full_html = build_enterprise_html(article_data, photo)

    # 5. Post directly to Google Blogger network (DO NOT save HTML to GitHub)
    published_urls = post_to_multi_blogs(
        title=article_data["meta"]["title"],
        html_content=full_html,
        meta=article_data["meta"]
    )
    
    primary_url = published_urls[0] if published_urls else BLOGGER_URL

    # 6. Telegram notification
    send_telegram(article_data["meta"]["title"], primary_url, article_data["content"][:220])

    # 7. Record to local history so we don't repeat topics
    save_history(article_data["meta"]["permalink_slug"])
    
    print(f"EXECUTION COMPLETE: Successfully published to {len(published_urls)} network blogs!")
    print(f"Google Search Console & Blogger View tracking active for: {article_data['meta']['title']}")

if __name__ == "__main__":
    main()
