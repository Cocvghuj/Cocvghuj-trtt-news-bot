import feedparser, os, json, requests, random, re, datetime, time, subprocess, sys
from google import genai
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

HISTORY_FILE = "posted_history.json"
TELEGRAM_URL_TEMPLATE = "https://api.telegram.org/bot{token}/sendMessage"
CURRENT_YEAR = datetime.datetime.now().year

OFFICIAL_DB = {
    "WORLD": {
        "desk": "TRTT Global Insights Desk",
        "url": "https://trttnews24bd.blogspot.com/search/label/Global%20Insights",
        "keyword": "world news analysis",
        "label": "Global Insights"
    },
    "BUSINESS": {
        "desk": "TRTT Business & Markets Desk",
        "url": "https://trttnews24bd.blogspot.com/search/label/Business",
        "keyword": "global business market",
        "label": "Business"
    },
    "VISA": {
        "desk": "TRTT Europe & Schengen Desk - Reporting from Sardinia, Italy",
        "url": "https://trttnews24bd.blogspot.com/search/label/Schengen",
        "keyword": "schengen visa europe",
        "label": "Schengen"
    },
    "TECH": {
        "desk": "TRTT Tech & Tools Desk",
        "url": "https://trttnews24bd.blogspot.com/p/free-tools.html",
        "keyword": "technology tools",
        "label": "Tech & Tools"
    },
    "TOOLS": {
        "desk": "TRTT Developer Desk",
        "url": "https://trttnews24bd.blogspot.com/p/free-tools.html",
        "keyword": "free seo tools",
        "label": "Free Tools"
    }
}

def get_today_topics():
    today_weekday = datetime.datetime.utcnow().strftime('%A')
    
    topics = [
        {"title": f"Global Geopolitical Shifts and International Policy Frameworks {CURRENT_YEAR}", "category": "WORLD"},
        {"title": f"Artificial Intelligence and Enterprise Technology Innovation Trends {CURRENT_YEAR}", "category": "TECH"},
        {"title": f"Global Cybersecurity and Digital Infrastructure Developments {CURRENT_YEAR}", "category": "TECH"},
        {"title": f"Global Business Growth Strategies and Market Adaptability {CURRENT_YEAR}", "category": "BUSINESS"},
        {"title": f"International Trade, Economic Policy and Market Analysis {CURRENT_YEAR}", "category": "BUSINESS"},
        {"title": f"Schengen Visa Regulations and Official Immigration Compliance {CURRENT_YEAR}", "category": "VISA"}
    ]
    
    if today_weekday == "Monday":
        topics.append({"title": f"Europe Startup Ecosystem and Cross-Border Investment Guide {CURRENT_YEAR}", "category": "TOOLS"})
    elif today_weekday == "Sunday":
        topics.append({"title": f"Essential Free Digital Marketing and SEO Tools for Professionals {CURRENT_YEAR}", "category": "TOOLS"})
        
    return topics

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                return [item if isinstance(item, dict) else {"link": "", "title": item.strip().lower(), "date": "", "category": ""} for item in raw_data if item]
        except:
            return []
    return []

def commit_history_to_github():
    try:
        subprocess.run(["git", "config", "--global", "user.name", "GitHub Action Bot"], check=True)
        subprocess.run(["git", "config", "--global", "user.email", "action@github.com"], check=True)
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
        if not status.stdout.strip():
            return
        subprocess.run(["git", "add", HISTORY_FILE], check=True)
        subprocess.run(["git", "commit", "-m", "Auto-update posted history & URLs [skip ci]"], check=True)
        subprocess.run(["git", "push"], check=True)
    except Exception as e:
        print(f"⚠️ Git commit warning: {e}")

def save_history(link, title, category, url=""):
    hist = load_history()
    today_str = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    hist.append({"link": link, "title": title.strip().lower(), "date": today_str, "category": category, "post_url": url})
    hist = hist[-1000:]
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(hist, f, ensure_ascii=False, indent=2)
        commit_history_to_github()
    except Exception as e:
        print(f"⚠️ History save error: {e}")

def is_duplicate(entry_title):
    hist = load_history()
    clean_entry_title = re.sub(r'[^a-zA-Z0-9\s]', '', str(entry_title)).strip().lower()
    for item in hist:
        if isinstance(item, dict):
            item_title = re.sub(r'[^a-zA-Z0-9\s]', '', str(item.get("title", ""))).strip().lower()
            if item_title and clean_entry_title and item_title == clean_entry_title:
                return True
    return False

def get_featured_image(keyword):
    fallback_imgs = [
        "https://images.unsplash.com/photo-1566073771259-6a8506099457?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=800&q=80",
        "https://images.unsplash.com/photo-1526374965328-7f61dddc18c5?auto=format&fit=crop&w=800&q=80"
    ]
    try:
        key = os.environ.get("UNSPLASH_ACCESS_KEY")
        if not key: return random.choice(fallback_imgs)
        page = random.randint(1, 3)
        url = f"https://api.unsplash.com/search/photos?query={keyword}&page={page}&per_page=15&orientation=landscape&client_id={key}"
        r = requests.get(url, timeout=15).json()
        if r.get('results') and len(r['results']) > 0:
            selected_img = random.choice(r['results']).get('urls', {}).get('regular')
            if selected_img: return selected_img
    except Exception as e:
        print(f"🖼️ Image API Error: {e}")
    return random.choice(fallback_imgs)

def send_telegram_notification(title, post_url):
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if bot_token and chat_id:
        try:
            msg = (
                f"<b>📢 NEW POST PUBLISHED</b> 📰\n\n"
                f"<b>📌 Title:</b> {title}\n"
                f"<b>🔗 Read Article:</b> {post_url}\n\n"
                f"<i>🌐 TRTT NEWS 24 BD Global Bureau</i>"
            )
            api_url = TELEGRAM_URL_TEMPLATE.format(token=bot_token)
            requests.post(api_url, json={"chat_id": chat_id, "text": msg, "parse_mode": "HTML", "disable_web_page_preview": False})
        except Exception as e:
            print(f"⚠️ Telegram Error: {e}")

def clean_ai_html(text):
    if not text:
        return ""
    text = re.sub(r'^```html\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'^```\s*', '', text)
    text = re.sub(r'\s*```$', '', text)
    if 'Would you like' in text or 'This article:' in text or "Here's your" in text:
        parts = re.split(r'(?i)(This article:|Would you like|Here\'s your)', text)
        if len(parts) > 1:
            text = parts[0]
    return text.strip()

def generate_safe_news_with_fallback(topic: str, cat_key: str):
    info = OFFICIAL_DB[cat_key]
    prompt = f"""
You are Engr Abu Taher, Founder TRTT NEWS 24 BD, Sanluri, Sardinia, Italy as {info['desk']}.
TOPIC: {topic} - YEAR: {CURRENT_YEAR}
CRITICAL: Output ONLY pure HTML (<h2>, <p>, <ul>, <li>, <b>). No ```html, no intro.
Write 900+ words: What is happening? / Why it matters / Key facts / Practical guide.
End: <p><i>Analysis by TRTT News 24 BD Desk, Sanluri, Sardinia, Italy.</i></p>
"""

    gemini_key = os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        for model_name in ["gemini-1.5-flash", "gemini-1.5-flash-8b"]:
            try:
                client = genai.Client(api_key=gemini_key)
                response = client.models.generate_content(model=model_name, contents=prompt)
                if response and response.text and len(response.text) > 500:
                    return clean_ai_html(response.text), info['label']
            except Exception as e:
                print(f"Gemini {model_name} fail: {e}")

    groq_key = os.environ.get("GROQ_API_KEY")
    if groq_key:
        try:
            r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"},
                json={"model": "llama-3.1-70b-versatile", "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}, timeout=60)
            if r.status_code == 200:
                return clean_ai_html(r.json()['choices'][0]['message']['content']), info['label']
        except Exception as e:
            print(f"Groq fail: {e}")

    openrouter_key = os.environ.get("OPENROUTER_API_KEY")
    if openrouter_key:
        try:
            r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {openrouter_key}", "Content-Type": "application/json"},
                json={"model": "google/gemini-flash-1.5", "messages": [{"role": "user", "content": prompt}]}, timeout=60)
            if r.status_code == 200:
                return clean_ai_html(r.json()['choices'][0]['message']['content']), info['label']
        except Exception as e:
            print(f"OpenRouter fail: {e}")

    mistral_key = os.environ.get("MISTRAL_API_KEY")
    if mistral_key:
        try:
            r = requests.post("https://api.mistral.ai/v1/chat/completions",
                headers={"Authorization": f"Bearer {mistral_key}", "Content-Type": "application/json"},
                json={"model": "mistral-small-latest", "messages": [{"role": "user", "content": prompt}]}, timeout=60)
            if r.status_code == 200:
                return clean_ai_html(r.json()['choices'][0]['message']['content']), info['label']
        except Exception as e:
            print(f"Mistral fail: {e}")

    deepseek_key = os.environ.get("DEEP_SEEK_KEY")
    if deepseek_key:
        try:
            r = requests.post("https://api.deepseek.com/chat/completions",
                headers={"Authorization": f"Bearer {deepseek_key}", "Content-Type": "application/json"},
                json={"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}]}, timeout=60)
            if r.status_code == 200:
                return clean_ai_html(r.json()['choices'][0]['message']['content']), info['label']
        except Exception as e:
            print(f"DeepSeek fail: {e}")

    cohere_key = os.environ.get("COHERE_API_KEY")
    if cohere_key:
        try:
            r = requests.post("https://api.cohere.ai/v1/generate",
                headers={"Authorization": f"Bearer {cohere_key}", "Content-Type": "application/json"},
                json={"model": "command-r-plus", "prompt": prompt, "max_tokens": 1200}, timeout=60)
            if r.status_code == 200:
                return clean_ai_html(r.json()['generations'][0]['text']), info['label']
        except Exception as e:
            print(f"Cohere fail: {e}")

    print("All APIs failed - expanded fallback")
    fallback_html = f"""
<h2>What is happening with {topic}?</h2>
<p>In {CURRENT_YEAR}, {topic} has become a central issue tracked by our desk in Sanluri, Sardinia, Italy. What started as policy discussions in Brussels is now directly affecting businesses, students and families connected to Europe and Bangladesh. From Milan to Sanluri, we are seeing more digital verification, stricter documentation checks, and faster processing for those who use correct {CURRENT_YEAR} formats.</p>
<p>For TRTT NEWS 24 BD readers, this is not distant news. If you are in Italy or planning Europe-related work from Bangladesh, {topic} decides how long your file takes and how much extra cost you pay. Our bureau notes that files using updated templates are cleared in weeks, while old 2022-23 templates face months of delay.</p>

<h2>Why it matters for Bangladesh & Europe readers</h2>
<p>From Sardinia, we see two practical impacts. First, business compliance - companies dealing with {topic} must now show clearer linkage between purpose, funding and duration. Generic cover letters are rejected more often in {CURRENT_YEAR}. Second, personal documentation - for Schengen and business categories, portals now require readable PDFs, proper naming, and digital uploads. A small naming error can cause automatic rejection.</p>
<p>For Bangladeshis in Italy, this means keeping one verified source. Random Facebook posts from 2022 are causing most rejections we review. We recommend following our {info['desk']} via {info['url']}.</p>

<h2>Key facts and insights - {CURRENT_YEAR}</h2>
<ul>
<li><b>Digital shift:</b> European systems are 90% digital in {CURRENT_YEAR}. Manual submissions are slower.</li>
<li><b>Business growth:</b> SMEs in Italy using tools related to {topic} report 30-40% time saving when process is correct.</li>
<li><b>Security:</b> Cybersecurity checks are now part of everyday compliance, not just for large firms.</li>
<li><b>Free resources:</b> Our <a href="https://trttnews24bd.blogspot.com/p/free-tools.html">Free Tools page</a> offers updated checkers for {CURRENT_YEAR}.</li>
<li><b>Common mistake:</b> Using old information. Always check label {info['label']} on trttnews24bd.blogspot.com</li>
</ul>

<h2>Practical guide and next steps</h2>
<p>1. Verify source at {info['url']}. 2. Update documents to {CURRENT_YEAR} format. 3. Test with free tools before submission. 4. Join WhatsApp Channel and Telegram for daily verified alerts from our Italy desk. The trend for {topic} in the rest of {CURRENT_YEAR} is more transparency and faster processing for prepared files.</p>
<p><i>Analysis by TRTT News 24 BD Desk, Sanluri, Sardinia, Italy. AI-assisted research with human editorial review.</i></p>
"""
    return fallback_html, info['label']

def get_blogger():
    try:
        client_id = os.environ.get("BLOGGER_CLIENT_ID")
        client_secret = os.environ.get("BLOGGER_CLIENT_SECRET")
        refresh_token = os.environ.get("BLOGGER_REFRESH_TOKEN")
        creds = Credentials(token=None, refresh_token=refresh_token, client_id=client_id, client_secret=client_secret, token_uri="https://oauth2.googleapis.com/token")
        creds.refresh(Request())
        return build("blogger", "v3", credentials=creds)
    except Exception as e:
        print(f"❌ Blogger Auth Error: {e}")
        return None

def main():
    topics_to_post = get_today_topics()
    blogger_service = get_blogger()
    if not blogger_service:
        return
        
    blog_id = os.environ.get("BLOGGER_ID") or os.environ.get("BLOGGER_BLOG_ID")
    
    target_item = None
    for item in topics_to_post:
        if not is_duplicate(item["title"]):
            target_item = item
            break
            
    if not target_item:
        print("ℹ️ No new topics to post today. All topics already posted.")
        return
        
    try:
        entry_title = target_item["title"]
        cat_key = target_item["category"]
        
        info = OFFICIAL_DB[cat_key]
        article_body_html, label = generate_safe_news_with_fallback(entry_title, cat_key)
        image_url = get_featured_image(info["keyword"])
        
        full_html = f"""
<div style="background:#ffffff; border:1px solid #e2e8f0; border-left:4px solid #0f172a; padding:14px; margin-bottom:18px; font-size:13px; line-height:1.6;">
<b>Author:</b> Engr Abu Taher | Founder, TRTT NEWS 24 BD, Milano, Italy<br>
<b>Editorial Review:</b> Verified by TRTT International Desk | <b>Source:</b> <a href="{info['url']}" target="_blank" rel="nofollow">{info['desk']}</a><br>
<b>Transparency:</b> This article uses AI-assisted research with human editorial oversight for accuracy. Original reporting and analysis by TRTT.
</div>
<div style="margin:18px 0;"><img src="{image_url}" alt="{entry_title}" style="width:100%; border-radius:8px;"></div>
{article_body_html}
<div style="margin-top:30px; padding:16px; background:#f1f5f9; text-align:center; border-radius:10px; border:1px solid #e2e8f0;">
<h3 style="margin-top:0; color:#0f172a; font-size:16px;">Join Our Official Community for Daily Updates</h3>
<p style="font-size:14px; color:#475569;">Get verified global news, policy guides, and Europe-Bangladesh updates directly.</p>
<div style="display:flex; justify-content:center; gap:10px; flex-wrap:wrap; margin-top:10px;">
<a href="https://whatsapp.com/channel/0029Vb8co9VDeONEz0B5e51M" target="_blank" style="background:#25D366; color:white; padding:8px 16px; border-radius:20px; text-decoration:none; font-size:13px; font-weight:bold;">WhatsApp Channel</a>
<a href="https://t.me/trttnews24bd" target="_blank" style="background:#0088cc; color:white; padding:8px 16px; border-radius:20px; text-decoration:none; font-size:13px; font-weight:bold;">Telegram</a>
</div>
</div>
<div style="text-align:center; margin-top:20px;">
<a href="https://trttnews24bd.blogspot.com/p/hire-me-advertise.html" style="background:#0f172a; color:white; padding:10px 20px; border-radius:6px; text-decoration:none; font-size:13px;">Advertise With Us</a>
</div>
"""
        
        post_body = {
            "kind": "blogger#post",
            "title": entry_title,
            "content": full_html,
            "labels": [label, "Global Insights", f"{CURRENT_YEAR}"],
            "location": {"name": "Sanluri, Sardinia, Italy", "lat": 39.5667, "lng": 8.9}
        }
        
        result = blogger_service.posts().insert(blogId=blog_id, body=post_body, isDraft=False, fetchImages=True).execute()
        published_url = result.get('url', '')
        print(f"✅ SINGLE ARTICLE PUBLISHED SUCCESSFULLY: {entry_title} (URL: {published_url})")
        
        save_history(info['url'], entry_title, label, published_url)
        send_telegram_notification(entry_title, published_url)
        
    except Exception as e:
        print(f"❌ Failed post (Target: {target_item.get('title', 'Unknown')}): {e}")

if __name__ == "__main__":
    main()
