# MILLION DOLLAR - GOOGLE COMPLIANT - ENGLISH ONLY - NO DUPLICATE
# Title 1-100, Search Desc 120-160, Labels max 5 x 50, English Latin Only, Secrets+Vars, Vercel Ref, Draft
import os, sys, unicodedata
from urllib.parse import urlparse

DEFAULT_PWA_URL = "https://cocvghuj.github.io/Cocvghuj-trtt-news-bot"
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
    title = str(meta.get("title", "")).strip()
    desc = str(meta.get("search_description", "")).strip()
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
    slug = str(meta.get("permalink_slug", "")).strip()
    if not slug:
        import re
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug).strip('-')
    m = dict(meta)
    m.update(title=title, search_description=desc, labels=labels, permalink_slug=slug)
    return m

def validate_source_url(v: str):
    p = urlparse(v.strip())
    if p.scheme != "https" or not p.netloc or p.username or p.password:
        raise ValueError("Provide valid HTTPS official-source URL")
    return p.geturl()

def add_vercel_reference(content: str, url: str):
    """Append a neutral TRTT link; never invent personal experience or partner claims."""
    if url in content:
        return content
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("PWA reference must be a valid HTTPS URL.")
    block = f'''<aside class="trtt-voyagehub-reference">
<h2>TRTT Voyage Tools and Resources</h2>
<p>Explore the <a href="{url}" rel="noopener noreferrer">TRTT Voyage tools and travel resources</a>.</p>
<p><small>Check current prices, availability, eligibility and provider terms directly with the relevant service before making a decision.</small></p>
</aside>
<!-- Vercel Ref: {url} -->'''
    return content.rstrip() + "\n\n" + block

def main():
    import os, sys, json
    topic = os.environ.get("TRTT_NEWS_TOPIC", "").strip()
    source_raw = os.environ.get("TRTT_OFFICIAL_SOURCE_URL", "").strip()
    pwa_url = os.environ.get("PWA_REFERENCE_URL", DEFAULT_PWA_URL).strip()
    if not topic:
        topic = "Cagliari to Rome Cheap Flights Today - Sanluri Travel News"
    if not source_raw:
        source_raw = "https://www.enac.gov.it"
    source_url = validate_source_url(source_raw)
    parsed = urlparse(pwa_url)
    if "vercel.app" not in pwa_url and "github.io" not in pwa_url:
        pwa_url = DEFAULT_PWA_URL
    require_latin_english(topic, "News topic")
    category = "Current Travel News"
    selected = {
        "topic": f"{topic}. Official source: {source_url}. Include PRO LOCKED Marker {MARKER} tp.st ONLY {FIXED} FIXED trtt_lock_it Real hotel-bernini.com Glassmorphism Vercel {pwa_url}",
        "category": category,
        "default_labels": ["Travel News", "Europe Travel", "FlightScoutPro", "Sanluri", "TRTT"]
    }
    try:
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
        import main as engine
        engine.TOPIC_POOL = [selected]
        engine.select_next_topic = lambda _pool, _history: selected
        orig_gen = getattr(engine, "generate_article_with_metadata", None)
        if orig_gen:
            def guarded(topic_info):
                result = orig_gen(topic_info)
                if not isinstance(result, dict): return result
                result = dict(result)
                if "meta" in result and isinstance(result["meta"], dict):
                    result["meta"] = validate_metadata(result.get("meta"))
                content = str(result.get("content", ""))
                result["content"] = add_vercel_reference(content, pwa_url)
                return result
            engine.generate_article_with_metadata = guarded
        try:
            engine.main()
        finally:
            if orig_gen:
                engine.generate_article_with_metadata = orig_gen
    except Exception as exc:
        print(f"News draft workflow failed: {exc}", file=sys.stderr)
        raise
    return 0

if __name__ == "__main__":
    sys.exit(main())
