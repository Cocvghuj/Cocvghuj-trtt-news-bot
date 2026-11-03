# MILLION DOLLAR - GOOGLE COMPLIANT - ENGLISH ONLY - NO DUPLICATE
# Title 1-100, Search Desc 120-160, Labels max 5 x 50, English Latin Only, Secrets+Vars, Vercel Ref, Draft
import os, sys, unicodedata
from urllib.parse import urlparse

DEFAULT_PWA_URL = "https://cocvghuj-trtt-news-bot.vercel.app"
MARKER = os.environ.get("TRAVEL_PAYOUT_MARKER") or os.environ.get("MARKER_LOCKED") or "787950"
FIXED = "tIZcbMOB"

def require_latin_english(value: str, field: str):
    for ch in value:
        if unicodedata.category(ch).startswith("L"):
            if "LATIN" not in unicodedata.name(ch, ""):
                raise ValueError(f"{field} must be English-only; non-Latin found.")

def validate_metadata(meta: dict):
    # GOOGLE STANDARD
    if not isinstance(meta, dict): raise ValueError("Metadata must be object")
    title = str(meta.get("title","")).strip()
    desc = str(meta.get("search_description","")).strip()
    if not 1 <= len(title) <= 100: raise ValueError("Title must be 1-100 chars")
    if not 120 <= len(desc) <= 160: raise ValueError("Search description must be 120-160 chars")
    require_latin_english(title, "Title")
    require_latin_english(desc, "Search description")
    raw_labels = meta.get("labels")
    if not isinstance(raw_labels, list): raise ValueError("Labels must be list")
    labels, seen = [], set()
    for raw in raw_labels:
        l = str(raw).strip()
        k = l.casefold()
        if not l or k in seen: continue
        require_latin_english(l, "Blogger label")
        if len(l) > 50: raise ValueError("Each label max 50 chars")
        labels.append(l); seen.add(k)
        if len(labels) == 5: break
    if not labels: raise ValueError("At least 1 English label required")
    m = dict(meta); m.update(title=title, search_description=desc, labels=labels); return m

def validate_source_url(v: str):
    p = urlparse(v.strip())
    if p.scheme != "https" or not p.netloc or p.username or p.password:
        raise ValueError("Provide valid HTTPS official-source URL")
    return p.geturl()

def add_vercel_reference(content: str, url: str):
    # TEST SAFE - if url in content: return content
    if url in content:
        return content
    subid = "trtt_lock_it"
    # MILLION DOLLAR TRAFFIC BLOCK - GOOGLE E-E-A-T + REAL .IT + GDPR + GLASSMORPHISM
    block = f'''<aside class="trtt-voyagehub-reference glassmorphism" style="background:rgba(255,255,255,0.1);backdrop-filter:blur(20px);border-radius:20px;padding:15px;border:1px solid rgba(255,255,255,0.2)">
<h2>Plan Your Trip From Sanluri - Real Italian Experience</h2>
<p><strong>Google E-E-A-T:</strong> I live in Sanluri, Sardinia. I travel from Cagliari Airport CAG. This is real experience.</p>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","author":{{"@type":"Person","name":"Roksana Nilla"}}}}</script>
<ul>
<li>✈️ <a href="https://aviasales.tp.st/Fb8U9yav?marker={MARKER}&subid={subid}">Cheap Flights Aviasales - Marker {MARKER} LOCKED</a></li>
<li>🚕 <a href="https://kiwitaxi.tp.st/{FIXED}?marker={MARKER}&subid={subid}">Kiwitaxi {FIXED} FIXED - CAG to Sanluri - No tl bug</a></li>
<li>📱 <a href="https://airalo.tp.st/ZZoQC7Mz?marker={MARKER}&subid={subid}">Airalo eSIM Italy</a> | <a href="https://saily.tp.st/ssekmS4X?marker={MARKER}&subid={subid}">Saily Backup</a></li>
<li>🏨 Real Hotel: <a href="https://www.hotel-bernini.it" target="_blank">hotel-bernini.it</a> - Real .it - 3-5% vs Booking 20% - TRTTVoyageHub ONE Vision</li>
<li>🎫 <a href="https://klook.tp.st/TWKnemhz?marker={MARKER}&subid={subid}">Klook</a> | <a href="https://tiqets.tp.st/bnx8pnF6?marker={MARKER}&subid={subid}">Tiqets</a> | <a href="https://airhelp.tp.st/3ItXS0E4?marker={MARKER}&subid={subid}">AirHelp</a></li>
</ul>
<p><small>Live Reference: {url}/?marker={MARKER} | GitHub: github.com/Cocvghuj/Cocvghuj-trtt-news-bot | GDPR: trtt_cookie_consent_esim | Open Source | #webdesign #uidesign #glassmorphism #TRTT #traveltech #lumina</small></p>
</aside>
<!-- Vercel Ref: {url} -->'''
    return content.rstrip() + "\n\n" + block

def main():
    import main as engine
    topic = os.environ.get("TRTT_NEWS_TOPIC","").strip()
    source_raw = os.environ.get("TRTT_OFFICIAL_SOURCE_URL","").strip()
    pwa_url = os.environ.get("PWA_REFERENCE_URL", DEFAULT_PWA_URL).strip()
    # AUTO for schedule - no error tomorrow
    if not topic:
        topic = "Cagliari to Rome Cheap Flights Today - Sanluri Travel News"
    if not source_raw:
        source_raw = "https://www.enac.gov.it"
    source_url = validate_source_url(source_raw)
    parsed = urlparse(pwa_url)
    # Allow vercel + github.io for traffic
    if "vercel.app" not in pwa_url and "github.io" not in pwa_url:
        pwa_url = DEFAULT_PWA_URL
    require_latin_english(topic, "News topic")
    category = "Current Travel News"
    selected = {
        "topic": f"{topic}. Official source: {source_url}. Include PRO LOCKED Marker 787950 tp.st ONLY tIZcbMOB FIXED trtt_lock_it Real hotel-bernini.it Glassmorphism Vercel {pwa_url}",
        "category": category,
        "default_labels": ["Travel News", "Europe Travel", "FlightScoutPro", "Sanluri", "TRTT"]
    }
    engine.TOPIC_POOL = [selected]
    engine.select_next_topic = lambda _pool, _history: selected
    orig_gen = engine.generate_article_with_metadata
    def guarded(topic_info):
        result = orig_gen(topic_info)
        if not isinstance(result, dict): raise ValueError("No validated article")
        result = dict(result)
        result["meta"] = validate_metadata(result.get("meta"))
        content = str(result.get("content",""))
        require_latin_english(content, "Article body")
        result["content"] = add_vercel_reference(content, pwa_url)
        return result
    engine.generate_article_with_metadata = guarded
    # Prevent duplicate via drafted.txt is handled in engine.main
    try:
        engine.main() # This saves as DRAFT to BLOGGER_BLOG_ID, FLIGHTSCOUTPRO_BLOG_ID, PARTNER_BLOG_IDS from secrets/vars
    finally:
        engine.generate_article_with_metadata = orig_gen
    return 0

if __name__ == "__main__":
    sys.exit(main())
