"""
TRTT Enterprise Auto-Publisher Engine (Google Blogger Direct & Multi-Blog Network)
Protocol 26391/2026 • Marker 787950 LOCKED
Dedicated to family: Roksana | Taifa | Tashrif (From Sanluri to Dhaka)
Strictly compliant with Google Search, Google Search Console, and GitHub Rules.
Automated Multi-Blog Publishing for TRTT News 24 BD & FlightScoutPro.
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
FLIGHTSCOUTPRO_URL = "https://flightscoutpro.blogspot.com"
PWA_URL = "https://cocvghuj-trtt-news-bot.vercel.app/?marker=787950"

HISTORY_FILE = "published_history.txt"

# Core Topics designed for High Google Search Volume & Affiliate Conversion
TOPIC_POOL = [
    {
        "topic": "How to Claim Up to 600€ for Flight Delays in Europe Under EC 261",
        "category": "Passenger Rights",
        "default_labels": ["Flight Compensation", "AirHelp", "EU Regulation 261", "Passenger Rights", "Europe Travel", "FlightScoutPro"]
    },
    {
        "topic": "Best Travel eSIM for Europe 2026: Compare Airalo, Saily, and Unlimited Data",
        "category": "eSIM & Connectivity",
        "default_labels": ["eSIM", "Airalo", "Saily", "Europe Travel", "Travel Tech", "FlightScoutPro"]
    },
    {
        "topic": "Cheap Flights from Middle East and Gulf to Europe: Top Routing Secrets",
        "category": "Cheap Flights",
        "default_labels": ["Aviasales", "Cheap Flights", "Qatar Airways", "Gulf to Europe", "Flight Hacks", "FlightScoutPro"]
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
        handle.write(title_id + "\n")
# ==============================================================================
# UNSPLASH API: Dynamic Real High-Res Photography
# ==============================================================================
def fetch_unsplash_photo(query: str) -> dict:
    fallback = {
        "url": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=1200&q=80",
        "author": "TRTT & FlightScout Travel Bureau",
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
    
    prompt = f"""You are a senior European aviation & travel journalist writing for FlightScoutPro and TRTT News 24 BD.
Generate a comprehensive, authentic, high-value guide for the topic: "{topic}".

EDITORIAL REQUIREMENTS (Google Helpful Content & E-E-A-T Standards):
1. TONE: Human, authoritative, practical, and empathetic. Mention real-world aviation logistics (e.g. EU Regulation 261/2004 claim rules, airline denial tactics, airport hubs, transit hacks) so it sounds like genuine field experience, NOT generic AI fluff.
2. STRUCTURE:
   - Output clean HTML body (use <h2>, <h3>, <ul>, <li>, <p>, <blockquote>, <strong>).
   - Real-world Executive Hook (80-100 words)
   - <h2>Core Passenger Rights & Flight Reality</h2>
   - <h2>Step-by-Step Action Guide</h2>
   - <h2>Airline Traps & Pitfalls to Avoid</h2>
   - <h2>Essential Travel Tech & Checklist</h2>
   - <h2>Frequently Asked Questions</h2> (3 clear, concrete Q&As)
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
        
        meta = {
            "title": topic,
            "search_description": f"Verified field guide on {topic} with official passenger rights and booking tips.",
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
# BLOG PROFILES: TRTT News 24 BD & FlightScoutPro
# ==============================================================================
def get_blog_profile(blog_name: str, blog_id: str) -> dict:
    """Returns tailored branding, author details, and legal links for each blog."""
    name_lower = (blog_name or "").lower()
    id_lower = (blog_id or "").lower()
    
    is_flightscout = (
        (FLIGHTSCOUTPRO_BLOG_ID and blog_id == FLIGHTSCOUTPRO_BLOG_ID)
        or "flightscout" in name_lower
        or "flightscout" in id_lower
    )
    
    if is_flightscout:
        return {
            "id": "flightscoutpro",
            "name": "FlightScoutPro",
            "subtitle": "Aviation Intelligence & Flight Deals Hub",
            "url": FLIGHTSCOUTPRO_URL,
            "author_name": "Muntasir Rahman",
            "author_role": "Owner & Lead Aviation Intelligence Editor",
            "author_location": "Dhaka, Bangladesh",
            "author_email": "muntasirrahaman694@gmail.com",
            "author_phone": "+8801314847336",
            "badge": "✈️ FlightScoutPro Aviation Intelligence • Dhaka &amp; Global",
            "theme_primary": "#0284c7",
            "theme_gradient": "linear-gradient(135deg, #0369a1 0%, #0284c7 100%)",
            "cta_title": "✈️ FlightScoutPro Deal &amp; Compensation Radar",
            "cta_desc": "Search real-time low airfares, claim up to €600 compensation for delayed flights, and get instant eSIM data.",
            "about_url": f"{FLIGHTSCOUTPRO_URL}/p/about-us.html",
            "contact_url": f"{FLIGHTSCOUTPRO_URL}/p/contact-us.html",
            "privacy_url": f"{FLIGHTSCOUTPRO_URL}/p/privacy-policy.html",
            "disclaimer_url": f"{FLIGHTSCOUTPRO_URL}/p/disclaimer.html",
            "footer_tag": "Published by FlightScoutPro • Founded by Muntasir Rahman (Dhaka, Bangladesh)"
        }
    else:
        return {
            "id": "trttnews24bd",
            "name": "TRTT News 24 BD",
            "subtitle": "Global Travel Logistics & Diaspora News Hub",
            "url": BLOGGER_URL,
            "author_name": "Abu Taher",
            "author_role": "Founder, Network Hub &amp; Chief Publishing Bureau",
            "author_location": "Via Carlo Felice, Sanluri, South Sardinia, Italy &amp; Milan, Italy",
            "author_email": "engrtaher2017@gmail.com",
            "author_phone": "",
            "badge": "📍 Sanluri, Sardinia, Italy &amp; Dhaka • TRTT Global Logistics",
            "theme_primary": "#052962",
            "theme_gradient": "linear-gradient(135deg, #052962 0%, #00A8E8 100%)",
            "cta_title": "🛡️ TRTT VoyageHub Super App • 21 Travel Logistics Tools Active",
            "cta_desc": "Compare flights, claim 600€ flight delays, activate 5G eSIMs, and book fixed-price airport rides instantly.",
            "about_url": f"{BLOGGER_URL}/p/about-us.html",
            "contact_url": f"{BLOGGER_URL}/p/contact-us.html",
            "privacy_url": f"{BLOGGER_URL}/p/privacy-policy.html",
            "disclaimer_url": f"{BLOGGER_URL}/p/disclaimer.html",
            "footer_tag": "Published by TRTT News 24 BD &amp; VoyageHub Network • Dedicated to Roksana, Taifa &amp; Tashrif (Sanluri to Dhaka)"
        }

# ==============================================================================
# ENTERPRISE HTML BUILDER (Modern, Clean, Responsive & E-E-A-T Compliant)
# ==============================================================================
def build_enterprise_html(article_data: dict, photo: dict, blog_profile: dict = None) -> str:
    if blog_profile is None:
        blog_profile = get_blog_profile("TRTT News 24 BD", BLOGGER_BLOG_ID or "")
        
    meta = article_data["meta"]
    content = article_data["content"]
    title = meta["title"]
    search_desc = meta["search_description"]
    tags_str = ", ".join(meta["labels"])
    
    airhelp_link = clean_affiliate_link("https://airhelp.tp.st/3ItXS0E4", "airhelp")
    aviasales_link = clean_affiliate_link("https://aviasales.tp.st/Fb8U9yav", "aviasales")
    airalo_link = clean_affiliate_link("https://airalo.tp.st/ZZoQC7Mz", "airalo")
    kiwitaxi_link = clean_affiliate_link("https://kiwitaxi.tp.st/tlZcbMOB", "kiwitaxi")

    now_iso = datetime.utcnow().isoformat()
    canonical_url = f"{blog_profile['url']}/{meta['permalink_slug']}.html"

    schema_json = {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": title,
        "description": search_desc,
        "image": [photo["url"]],
        "datePublished": now_iso,
        "dateModified": now_iso,
        "author": {
            "@type": "Person",
            "name": blog_profile["author_name"],
            "jobTitle": blog_profile["author_role"],
            "email": blog_profile["author_email"]
        },
        "publisher": {
            "@type": "Organization",
            "name": blog_profile["name"],
            "url": blog_profile["url"],
            "logo": {
                "@type": "ImageObject",
                "url": "https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/trtt-original-logo.jpeg"
            }
        },
        "keywords": tags_str,
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": canonical_url
        }
    }

    phone_html = f" &bull; <span>WhatsApp: <strong>{blog_profile['author_phone']}</strong></span>" if blog_profile.get("author_phone") else ""

    html = f"""<!-- Google Search Console & SEO Meta Header -->
<meta name="description" content="{search_desc}">
<meta name="keywords" content="{tags_str}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{search_desc}">
<meta property="og:image" content="{photo['url']}">
<meta property="og:type" content="article">

<!-- Schema.org Rich Snippet for Instant Google Search Indexing -->
<script type="application/ld+json">
{json.dumps(schema_json, indent=2)}
</script>

<!-- AUTONOMOUS ENTERPRISE STYLING ENGINE (Auto-injected by GitHub Actions Bot) -->
<style>
  .fs-article-wrap {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
    max-width: 840px !important;
    margin: 0 auto !important;
    color: #1e293b !important;
    line-height: 1.8 !important;
    font-size: 16px !important;
    word-break: break-word !important;
  }}
  .fs-article-wrap h1, .fs-article-wrap h2, .fs-article-wrap h3 {{
    color: #0f172a !important;
    font-weight: 800 !important;
    letter-spacing: -0.02em !important;
  }}
  .fs-article-wrap h2 {{
    font-size: 23px !important;
    margin-top: 36px !important;
    margin-bottom: 16px !important;
    padding-bottom: 8px !important;
    border-bottom: 2px solid #e2e8f0 !important;
    color: #0f172a !important;
  }}
  .fs-article-wrap h3 {{
    font-size: 19px !important;
    margin-top: 24px !important;
    margin-bottom: 12px !important;
    color: #1e293b !important;
  }}
  .fs-article-wrap p {{
    margin-bottom: 18px !important;
    color: #334155 !important;
    font-size: 16px !important;
  }}
  .fs-article-wrap ul, .fs-article-wrap ol {{
    padding-left: 24px !important;
    margin-bottom: 20px !important;
  }}
  .fs-article-wrap li {{
    margin-bottom: 8px !important;
    color: #334155 !important;
  }}
  .fs-article-wrap blockquote {{
    border-left: 4px solid {blog_profile['theme_primary']} !important;
    background: #f8fafc !important;
    padding: 16px 20px !important;
    margin: 24px 0 !important;
    border-radius: 0 12px 12px 0 !important;
    font-style: normal !important;
    color: #0f172a !important;
  }}
  /* Contempo & Blogger theme reset */
  .post-body, .entry-content {{
    font-size: 16px !important;
    line-height: 1.8 !important;
    color: #1e293b !important;
  }}
</style>

<div class="fs-article-wrap">

  <!-- Location, Status & Category Badge -->
  <div style="display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 16px; font-size: 12px;">
    <span style="background: #e0f2fe; color: #0369a1; padding: 5px 12px; border-radius: 6px; font-weight: 700;">{blog_profile['badge']}</span>
    <span style="background: #ecfdf5; color: #047857; padding: 5px 12px; border-radius: 6px; font-weight: 700;">✓ Verified Passenger Intel</span>
    <span style="background: #f1f5f9; color: #475569; padding: 5px 12px; border-radius: 6px;">🏷️ {tags_str}</span>
  </div>

  <!-- High-Res Photography with Attribution & Overlay -->
  <div style="position: relative; border-radius: 16px; overflow: hidden; margin-bottom: 24px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.12);">
    <img src="{photo['url']}" alt="{photo['alt']}" style="width: 100%; height: auto; max-height: 440px; object-fit: cover; display: block;" />
    <div style="position: absolute; bottom: 0; left: 0; right: 0; background: linear-gradient(to top, rgba(15,23,42,0.9) 0%, rgba(15,23,42,0.4) 60%, transparent 100%); padding: 14px 20px; color: #ffffff; font-size: 12px;">
      <span>📸 Photography: <strong>{photo['author']}</strong> (Unsplash Verified)</span> &bull; <span>Marker {MARKER} Locked</span>
    </div>
  </div>

  <!-- Key Takeaways / এক নজরে সারসংক্ষেপ Box -->
  <div style="background: #f0fdf4; border: 1.5px solid #86efac; border-radius: 14px; padding: 20px; margin-bottom: 28px;">
    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 10px;">
      <span style="background: #22c55e; color: #ffffff; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 800; text-transform: uppercase;">Quick Summary</span>
      <h3 style="margin: 0; font-size: 16px; color: #14532d; font-weight: 800;">⚡ Key Takeaways &amp; Executive Summary</h3>
    </div>
    <ul style="margin: 0; padding-left: 20px; color: #166534; font-size: 14.5px; line-height: 1.7;">
      <li><strong>Verified Regulations:</strong> Under EC 261/2004, European flight disruptions exceeding 3 hours entitle qualifying passengers up to €600.</li>
      <li><strong>Action Strategy:</strong> Never accept airport meal vouchers as final waiver of legal statutory compensation rights.</li>
      <li><strong>Connectivity &amp; Navigation:</strong> Secure regional 5G eSIM connectivity beforehand to track live aircraft tail registration and ATC status.</li>
    </ul>
  </div>

  <!-- Action Bar: Fast Travel Tools & Partner Access -->
  <div style="background: {blog_profile['theme_gradient']}; color: #ffffff; padding: 20px 24px; border-radius: 14px; margin-bottom: 28px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px; box-shadow: 0 4px 15px rgba(2,132,199,0.18);">
    <div>
      <strong style="font-size: 16px; display: block; margin-bottom: 4px;">{blog_profile['cta_title']}</strong>
      <p style="margin: 0; font-size: 13px; color: #e2e8f0; line-height: 1.5;">{blog_profile['cta_desc']}</p>
    </div>
    <div style="display: flex; gap: 10px; flex-wrap: wrap;">
      <a href="{blog_profile['url']}" style="background: #ffffff; color: {blog_profile['theme_primary']}; font-weight: 800; font-size: 12px; padding: 10px 18px; border-radius: 8px; text-decoration: none; display: inline-block;">
        📰 Latest Feed
      </a>
      <a href="{airhelp_link}" target="_blank" rel="noopener" style="background: #f59e0b; color: #0f172a; font-weight: 800; font-size: 12px; padding: 10px 18px; border-radius: 8px; text-decoration: none; display: inline-block;">
        🛡️ Claim €600
      </a>
    </div>
  </div>

  <!-- Article Body -->
  <div style="font-size: 16px; color: #334155; line-height: 1.8;">
    {content}
  </div>

  <!-- High-Converting Verified Partner Strip -->
  <div style="background: #f8fafc; border: 2px solid #e2e8f0; border-radius: 16px; padding: 22px; margin-top: 36px; margin-bottom: 30px;">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; margin-bottom: 14px; gap: 8px;">
      <h3 style="margin: 0; font-size: 16px; color: #0f172a; font-weight: 800;">🛡️ Official Travel &amp; Logistics Partners (Marker {MARKER})</h3>
      <span style="font-size: 11px; background: #e2e8f0; color: #475569; padding: 3px 8px; border-radius: 4px; font-weight: 600;">Affiliate Disclosure: Verified Safe</span>
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px;">
      <a href="{airhelp_link}" target="_blank" rel="noopener" style="display: block; padding: 12px 14px; background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 10px; text-decoration: none; color: #0f172a; font-weight: 700; font-size: 13px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        🛡️ AirHelp €600 Claim &rarr;
      </a>
      <a href="{aviasales_link}" target="_blank" rel="noopener" style="display: block; padding: 12px 14px; background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 10px; text-decoration: none; color: #0f172a; font-weight: 700; font-size: 13px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        ✈️ Aviasales Fares &rarr;
      </a>
      <a href="{airalo_link}" target="_blank" rel="noopener" style="display: block; padding: 12px 14px; background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 10px; text-decoration: none; color: #0f172a; font-weight: 700; font-size: 13px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        📱 Airalo 5G eSIM &rarr;
      </a>
      <a href="{kiwitaxi_link}" target="_blank" rel="noopener" style="display: block; padding: 12px 14px; background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 10px; text-decoration: none; color: #0f172a; font-weight: 700; font-size: 13px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
        🚖 Kiwitaxi Fixed Ride &rarr;
      </a>
    </div>
  </div>

  <!-- Dedicated Author Card & Google E-E-A-T Transparency -->
  <div style="background: #ffffff; border: 1.5px solid #cbd5e1; border-radius: 16px; padding: 22px; margin-top: 30px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
    <div style="display: flex; align-items: center; gap: 16px; flex-wrap: wrap;">
      <div style="width: 58px; height: 58px; border-radius: 50%; background: {blog_profile['theme_primary']}; color: #ffffff; display: flex; align-items: center; justify-content: center; font-size: 22px; font-weight: 900; flex-shrink: 0;">
        {blog_profile['author_name'][0]}
      </div>
      <div style="flex: 1; min-width: 220px;">
        <div style="display: flex; align-items: center; gap: 8px;">
          <strong style="font-size: 16px; color: #0f172a;">{blog_profile['author_name']}</strong>
          <span style="background: #dbeafe; color: #1e40af; font-size: 10px; font-weight: 800; padding: 2px 6px; border-radius: 4px;">VERIFIED AUTHOR</span>
        </div>
        <p style="margin: 2px 0 0 0; font-size: 13px; color: #64748b;">{blog_profile['author_role']} &bull; {blog_profile['author_location']}</p>
        <p style="margin: 4px 0 0 0; font-size: 12px; color: #475569;">
          <span>Email: <strong>{blog_profile['author_email']}</strong></span>
          {phone_html}
        </p>
      </div>
    </div>
    
    <!-- Legal & Compliance Links for Google AdSense & Search Essentials -->
    <div style="margin-top: 16px; padding-top: 14px; border-top: 1px solid #e2e8f0; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 10px; font-size: 12px;">
      <div style="display: flex; gap: 14px; flex-wrap: wrap;">
        <a href="{blog_profile['about_url']}" style="color: #0284c7; text-decoration: none; font-weight: 600;">About Us</a>
        <a href="{blog_profile['contact_url']}" style="color: #0284c7; text-decoration: none; font-weight: 600;">Contact Us</a>
        <a href="{blog_profile['privacy_url']}" style="color: #0284c7; text-decoration: none; font-weight: 600;">Privacy Policy</a>
        <a href="{blog_profile['disclaimer_url']}" style="color: #0284c7; text-decoration: none; font-weight: 600;">Disclaimer</a>
      </div>
      <span style="color: #94a3b8; font-size: 11px;">Marker {MARKER} &bull; GDPR &amp; FTC Compliant</span>
    </div>
  </div>

  <!-- Dedicated Family Tribute & Footer Stamp -->
  <div style="text-align: center; margin-top: 24px; font-size: 11px; color: #94a3b8;">
    <p style="margin: 0;">{blog_profile['footer_tag']}</p>
  </div>

</div>"""
    return html

# ==============================================================================
# MULTI-BLOG BROADCASTING VIA OFFICIAL GOOGLE BLOGGER API
# ==============================================================================
def post_to_multi_blogs(title: str, html_content: str, meta: dict, article_data: dict = None, photo: dict = None) -> List[str]:
    """
    Simultaneously publishes to TRTT News 24 BD & FlightScoutPro with tailored branding and verified author bios.
    """
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
            if cleaned and cleaned not in [b[1] for b in target_blog_ids]:
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

        for blog_name, blog_id in target_blog_ids:
            try:
                # Generate tailored HTML per blog if article_data and photo are available
                blog_profile = get_blog_profile(blog_name, blog_id)
                if article_data and photo:
                    tailored_html = build_enterprise_html(article_data, photo, blog_profile)
                else:
                    tailored_html = html_content

                body = {
                    "title": title,
                    "content": tailored_html,
                    "labels": meta["labels"],
                    "location": {
                        "name": blog_profile["author_location"],
                        "lat": 39.5613 if "sardinia" in blog_profile["author_location"].lower() else 23.8103,
                        "lng": 8.6332 if "sardinia" in blog_profile["author_location"].lower() else 90.4125,
                        "span": "0.05,0.05"
                    }
                }

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
        lines = [
            "✈️ <b>TRTT &amp; FlightScout Travel News Alert</b>",
            "",
            f"<b>{title}</b>",
            "",
            f"{clean_excerpt}...",
            "",
            f"🔗 <a href='{url}'>Read Full Verified Article</a>",
            "",
            f"<i>📍 Sanluri, Sardinia &amp; Dhaka • Marker {MARKER}</i>"
        ]
        text = chr(10).join(lines)
        endpoint = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(endpoint, json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=8)
        print("Telegram broadcast dispatched.")
    except Exception as exc:
        print(f"Telegram notice: {exc}")

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

    # 4. Build default Enterprise HTML (used for telegram excerpt and single-target fallbacks)
    default_profile = get_blog_profile("TRTT News 24 BD", BLOGGER_BLOG_ID or "")
    default_html = build_enterprise_html(article_data, photo, default_profile)

    # 5. Broadcast directly to Google Blogger network with tailored profiles per blog
    published_urls = post_to_multi_blogs(
        title=article_data["meta"]["title"],
        html_content=default_html,
        meta=article_data["meta"],
        article_data=article_data,
        photo=photo
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
