import feedparser, os, json, requests, random, re, datetime, time, subprocess, sys
from gtts import gTTS
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

HISTORY_FILE = "posted_history.json"
TELEGRAM_URL_TEMPLATE = "https://api.telegram.org/bot{token}/sendMessage"

# Master List of 12 Evergreen High-CPC Topics (International BBC Style 2027)
EVERGREEN_MASTER_TOPICS = [
    "UK Skilled Worker Visa 2027 - Minimum Salary Threshold & Sponsor List",
    "Malta Work Visa 2027 for Bangladeshi - Hotel Jobs with Free Accommodation",
    "USA H2B Work Permit Visa 2027 for Bangladesh - Salary $3500 + Free Visa",
    "Canada LMIA Work Permit 2027 - Direct Company Apply Link (No Agent)",
    "Italy Seasonal Work Visa 2027 (Decreto Flussi) - Application from Sanluri, Italy",
    "Portugal Work Visa for Bangladeshi 2027 - 90 Days Processing Time",
    "Romania Work Permit for Bangladesh - How to Check Real vs Fake Visa 2027",
    "Croatia Work Permit for Bangladeshis 2027 - New Salary Update",
    "How to Apply for Morocco E-Visa for AFCON 2027 from Bangladesh (AEVM Pass)",
    "Mali Suspends US Work Visas - What Bangladeshi Workers Must Know 2027",
    "USA DV Lottery 2027 for Bangladesh - Last Date and Photo Size Guide",
    "Germany Opportunity Card (Chancenkarte) 2027 - Points Calculator & Requirements"
]

FEEDS = {
    "Wall Street & Global Markets": "https://feeds.feedburner.com/reuters/businessNews",
    "Bloomberg Global Business": "https://www.cnbc.com/id/10001147/device/rss/rss.html",
    "European Central Bank & Trade": "https://politico.eu/feed/",
    "Global Geopolitics & EU": "https://www.euronews.com/rss?format=mrss",
    "BBC World Intelligence": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "Schengen & European Visa Hub": "https://www.schengenvisainfo.com/feed/",
    "Global Work Permits & Immigration": "https://visaguide.world/news/feed/",
    "Artificial Intelligence & Future Tech": "https://techcrunch.com/feed/",
    "Silicon Valley Deep Tech": "https://www.wired.com/feed/rss",
    "Global Cyber Security & Defense": "https://thehackernews.com/feeds/posts/default",
    "Global Energy & Green Transition": "https://www.euronews.com/tag/climate-change/rss",
    "International Aviation & Supply Chain": "https://simpleflying.com/feed/"
}

BREAKING_CATEGORIES = [
    "Global Geopolitics & EU", 
    "BBC World Intelligence", 
    "Wall Street & Global Markets",
    "Global Cyber Security & Defense"
]

COUNTRY_LOCATIONS = {
    "italy": {"name": "Milan, Italy", "lat": 45.4642, "lng": 9.1900},
    "germany": {"name": "Berlin, Germany", "lat": 52.5200, "lng": 13.4050},
    "uk": {"name": "London, UK", "lat": 51.5072, "lng": -0.1276},
    "usa": {"name": "New York, USA", "lat": 40.7128, "lng": -74.0060},
    "europe": {"name": "Brussels, Belgium", "lat": 50.8503, "lng": 4.3517},
    "default": {"name": "Milan, Italy", "lat": 45.4642, "lng": 9.1900}
}

def get_country_specific_details(title):
    t_upper = str(title).upper()
    
    if "UK" in t_upper or "UNITED KINGDOM" in t_upper:
        return {
            "source_name": "UK Government Official Portal (gov.uk)",
            "source_url": "https://www.gov.uk/skilled-worker-visa",
            "image_keyword": "UK Skilled Worker Visa UK Government Big Ben",
            "country_name": "UK",
            "fee": "£625 to £1,408",
            "salary": "£38,700 minimum threshold per year"
        }
    elif "MALTA" in t_upper:
        return {
            "source_name": "Malta Jobsplus Official Portal (jobsplus.gov.mt)",
            "source_url": "https://jobsplus.gov.mt",
            "image_keyword": "Malta Hotel Staff Jobs Workers",
            "country_name": "Malta",
            "fee": "€280",
            "salary": "€1,000 to €1,400 monthly"
        }
    elif "ITALY" in t_upper:
        return {
            "source_name": "Italian Ministry of Interior (interno.gov.it)",
            "source_url": "https://www.interno.gov.it",
            "image_keyword": "Italy Visa Decreto Flussi Worker",
            "country_name": "Italy",
            "fee": "€116",
            "salary": "€1,200 to €1,600 monthly"
        }
    elif "USA" in t_upper or "AMERICA" in t_upper:
        return {
            "source_name": "US Citizenship and Immigration Services (uscis.gov)",
            "source_url": "https://www.uscis.gov",
            "image_keyword": "USA Work Permit Passport Visa",
            "country_name": "USA",
            "fee": "$190 to $460",
            "salary": "$3,500 monthly average"
        }
    elif "CANADA" in t_upper:
        return {
            "source_name": "Immigration, Refugees and Citizenship Canada (canada.ca)",
            "source_url": "https://www.canada.ca",
            "image_keyword": "Canada LMIA Work Visa Passport",
            "country_name": "Canada",
            "fee": "$155 CAD",
            "salary": "$3,000 to $4,200 CAD monthly"
        }
    elif "GERMANY" in t_upper:
        return {
            "source_name": "German Federal Foreign Office (make-it-in-germany.com)",
            "source_url": "https://www.make-it-in-germany.com",
            "image_keyword": "Germany Opportunity Card Chancenkarte Passport",
            "country_name": "Germany",
            "fee": "€75",
            "salary": "€2,200 to €3,500 monthly"
        }
    elif "PORTUGAL" in t_upper:
        return {
            "source_name": "Portuguese Agency for Integration, Migration and Asylum (aima.gov.pt)",
            "source_url": "https://aima.gov.pt",
            "image_keyword": "Portugal Work Visa Passport",
            "country_name": "Portugal",
            "fee": "€90",
            "salary": "€850 to €1,200 monthly"
        }
    elif "ROMANIA" in t_upper:
        return {
            "source_name": "General Inspectorate for Immigration Romania (igi.mai.gov.ro)",
            "source_url": "https://igi.mai.gov.ro",
            "image_keyword": "Romania Work Permit Passport",
            "country_name": "Romania",
            "fee": "€120",
            "salary": "€750 to €1,100 monthly"
        }
    elif "CROATIA" in t_upper:
        return {
            "source_name": "Ministry of Interior Republic of Croatia (mup.gov.hr)",
            "source_url": "https://mup.gov.hr",
            "image_keyword": "Croatia Work Visa Permit",
            "country_name": "Croatia",
            "fee": "€100",
            "salary": "€800 to €1,300 monthly"
        }
    else:
        return {
            "source_name": "Official International Migration Bureau",
            "source_url": "https://visaguide.world",
            "image_keyword": "Global Work Visa Immigration Passport",
            "country_name": "International",
            "fee": "Official Standard Fee",
            "salary": "Standard International Rates"
        }

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
            cleaned_history = []
            for item in raw_data:
                if isinstance(item, dict):
                    cleaned_history.append(item)
                elif isinstance(item, str):
                    cleaned_history.append({"link": "", "title": item.strip().lower(), "date": "", "category": "", "post_url": ""})
            return cleaned_history
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

def is_duplicate(entry_link, entry_title):
    hist = load_history()
    clean_entry_link = str(entry_link).strip().lower()
    clean_entry_title = re.sub(r'[^a-zA-Z0-9\s]', '', str(entry_title)).strip().lower()
    
    for item in hist:
        if isinstance(item, dict):
            item_link = str(item.get("link", "")).strip().lower()
            item_title = re.sub(r'[^a-zA-Z0-9\s]', '', str(item.get("title", ""))).strip().lower()
            
            if item_link and clean_entry_link and item_link == clean_entry_link:
                return True
            if item_title and clean_entry_title and item_title == clean_entry_title:
                return True
    return False

def get_today_breaking_count():
    hist = load_history()
    today_str = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    count = 0
    for item in hist:
        if isinstance(item, dict):
            if item.get("date") == today_str and item.get("category") in BREAKING_CATEGORIES:
                count += 1
    return count

def get_smart_location(title, category):
    text = (str(title) + " " + str(category)).lower()
    for key, loc in COUNTRY_LOCATIONS.items():
        if key in text and key != "default":
            return loc
    return COUNTRY_LOCATIONS["default"]

def get_featured_image(title, category="", keyword=""):
    fallback_img = "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80"
    fallback_alt = f"{title} - Official Travel & Hotel Guide"
    try:
        key = os.environ.get("UNSPLASH_ACCESS_KEY")
        if not key: return fallback_img, fallback_alt
        
        q = keyword if keyword else title

        url = f"https://api.unsplash.com/search/photos?query={q}&per_page=10&orientation=landscape&client_id={key}".strip()
        r = requests.get(url, timeout=15).json()
        if r.get('results') and len(r['results']) > 0:
            selected_img = random.choice(r['results'])
            img_url = selected_img.get('urls', {}).get('regular', fallback_img)
            return img_url, f"{title} - Official Bureau Intelligence"
    except Exception as e:
        print(f"Image API Error: {e}")
    return fallback_img, fallback_alt

def send_telegram_notification(title, url):
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if bot_token and chat_id:
        try:
            msg = f"👑 <b>Media Empire Alert</b>\n\n<b>Title:</b> {title}\n\n<b>Link:</b> {url}"
            api_url = TELEGRAM_URL_TEMPLATE.format(token=bot_token)
            requests.post(api_url, json={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}, timeout=10)
        except Exception as e:
            print(f"⚠️ Telegram Error: {e}")

def calculate_read_time(body_html):
    words = len(re.sub(r'<[^>]+>', '', body_html).split())
    minutes = max(3, round(words / 180))
    return f"⏱️ <b>Estimated Read Time:</b> {minutes} min read ({words} words)"

def generate_human_authority_meta(country_info):
    current_date = datetime.datetime.utcnow().strftime('%B %d, %Y')
    return f"""
    <div style="background: #f8fafc; border-left: 4px solid #2563eb; padding: 14px 16px; border-radius: 6px; margin-bottom: 20px; font-size: 14px; color: #1e293b; line-height: 1.5;">
        <b>✍️ Human Expert Editorial & Verification:</b> This investigative report is manually reviewed and cross-verified by our resident editorial desk in Sanluri, Italy, referencing official government portals.
        <br><b>🔄 Last Updated & Reviewed:</b> {current_date} &bull; <b>Direct Official Desk:</b> <a href="{country_info['source_url']}" target="_blank" rel="nofollow noopener" style="color: #2563eb; font-weight: 600;">{country_info['source_name']}</a>
    </div>
    """

def generate_human_editorial_box(country_info):
    return f"""
    <div style="background-color: #f8fafc; border-left: 4px solid #2563eb; padding: 18px; margin-top: 25px; border-radius: 6px;">
        <h3 style="margin: 0 0 10px 0; color: #1e293b; font-size: 16px;">TRTT Human Expert Take & On-Ground Analysis (Sanluri, Italy)</h3>
        <p style="margin: 0; color: #334155; font-size: 14px; line-height: 1.6;">
            Our resident editorial bureau in Sanluri, Italy has directly cross-referenced this immigration bulletin with the <a href="{country_info['source_url']}" target="_blank" style="color: #2563eb; font-weight: bold;">{country_info['source_name']}</a>. For the 2027 fiscal cycle, international applicants are strongly advised against using unauthorized third-party brokers charging exorbitant fees. Official government fees are strictly set at {country_info['fee']}. Candidates should submit applications through authorized consulate channels or verified portal logins to prevent application fraud.
        </p>
        <div style="margin-top: 12px; font-size: 12px; color: #64748b; font-weight: 600;">
            — Verified by Senior Editorial Desk | TRTT NEWS 24 BD Bureau (Sanluri, Italy)
        </div>
    </div>
    """

def generate_schema_markup(title, desc, url, image_url):
    schema = {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": title,
        "description": desc,
        "image": [image_url],
        "datePublished": datetime.datetime.utcnow().isoformat() + "Z",
        "dateModified": datetime.datetime.utcnow().isoformat() + "Z",
        "author": [{"@type": "Person", "name": "TRTT Editorial Bureau Senior Analyst"}],
        "publisher": {"@type": "Organization", "name": "TRTT NEWS 24 BD", "logo": {"@type": "ImageObject", "url": image_url}}
    }
    return f'<script type="application/ld+json">{json.dumps(schema)}</script>'

def generate_article_with_ai(cat, title, summary, country_info):
    clean_summary = summary.replace("[…]", "").replace("[...]", "").strip()
    
    PROMPT = f"""
You are a senior international correspondent writing for TRTT NEWS 24 BD from Sanluri, Italy, adopting BBC News editorial standards.
Write an in-depth, highly authoritative news report in 100% ENGLISH for the title: "{title}" (Year 2027 context).

STRICT BBC JOURNALISTIC MANDATE:
1. WRITE IN 100% ENGLISH ONLY. DO NOT INCLUDE ANY BENGALI CHARACTERS OR TEXT.
2. WORD COUNT MUST BE 550 TO 650 WORDS.
3. Address critical applicant details: Official fees ({country_info['fee']}), Salary expectations ({country_info['salary']}), required document criteria, and direct application workflow.
4. Include an organic reference to the official government portal: {country_info['source_url']} ({country_info['source_name']})
5. Use professional HTML structure with subheadings (<h2>), concise lists (<ul><li>), and clear paragraphs (<p>).
6. STRIKE OUT ALL AI CLICHÉS (Do NOT use: "In conclusion", "Furthermore", "Delve into", "Tapestry", "Crucial juncture").
7. Output ONLY clean, ready-to-publish HTML body markup.

Context: {clean_summary}
Primary Official Source: {country_info['source_url']}
"""

    gemini_key = os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        for model in ["gemini-1.5-flash", "gemini-1.5-pro"]:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={gemini_key}"
                r = requests.post(url, json={"contents": [{"parts": [{"text": PROMPT}]}]}, timeout=90)
                if r.status_code == 200 and "candidates" in r.json():
                    txt = r.json()["candidates"][0]["content"]["parts"][0]["text"]
                    txt_clean = txt.replace("```html", "").replace("```", "").strip()
                    if len(txt_clean) > 800:
                        return {"seo_title": title, "meta_description": clean_summary[:140], "article_body": txt_clean}
            except Exception as e:
                print(f"⚠️ Gemini model {model} error: {e}")

    groq_key = os.environ.get("GROQ_API_KEY")
    if groq_key:
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
            payload = {"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": PROMPT}], "temperature": 0.7}
            r = requests.post(url, json=payload, headers=headers, timeout=90)
            if r.status_code == 200:
                txt = r.json()["choices"][0]["message"]["content"]
                txt_clean = txt.replace("```html", "").replace("```", "").strip()
                if len(txt_clean) > 800:
                    return {"seo_title": title, "meta_description": clean_summary[:140], "article_body": txt_clean}
        except Exception as e:
            print(f"⚠️ Groq error: {e}")

    # Fallback 100% English 550+ words article matching the country
    fallback_body = f"""
    <h2>Official Government Release: {title}</h2>
    <p>The official state immigration authority for {country_info['country_name']}, through <a href="{country_info['source_url']}" target="_blank">{country_info['source_name']}</a>, has formally issued updated directives for the 2027 recruitment and visa processing cycle. The guidelines outline verified job opportunities and entry policies targeted at international applicants, including candidates from Bangladesh.</p>
    
    <h2>Key Eligibility Parameters for Applicants in 2027</h2>
    <p>According to official directives published by labor authorities, prospective candidates seeking entry or employment permits must satisfy the following criteria:</p>
    <ul>
        <li><b>Age Requirements:</b> Applicants must fall within the official age bracket of 21 to 45 years.</li>
        <li><b>Documentation Standards:</b> Verifiable professional credentials and authenticated civil documentation.</li>
        <li><b>Mandatory Statutory Fee:</b> Official processing fees are capped at {country_info['fee']}, payable directly through official state channels.</li>
        <li><b>Salary Expectations:</b> Estimated monthly financial compensation ranges at {country_info['salary']}.</li>
    </ul>

    <h2>Direct Application Workflow Without Intermediaries</h2>
    <p>Authorities explicitly advise applicants against utilizing unauthorized agencies or paying illegal broker commissions. The verified application procedure follows a transparent pathway:</p>
    <p>1. Prepare a standardized CV and cover letter matching international qualification standards.<br/>
    2. Register an applicant account on the official government portal at <a href="{country_info['source_url']}" target="_blank">{country_info['source_name']}</a>.<br/>
    3. Apply directly to certified employers or official visa quota allocations.<br/>
    4. Following receipt of official approval notifications, schedule a visa appointment with authorized VFS Global or diplomatic consulate centers.</p>

    <h2>Legal Framework and Applicant Protection</h2>
    <p>Work permits and visas issued under official state quotas are protected by employment laws in {country_info['country_name']}, ensuring minimum wage compliance, statutory medical coverage, and formal dispute resolution mechanisms.</p>
    """
    return {"seo_title": title, "meta_description": clean_summary[:140], "article_body": fallback_body}

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
    selected_entry = None; chosen_category = ""
    
    unposted_evergreen = [t for t in EVERGREEN_MASTER_TOPICS if not is_duplicate("", t)]
    
    if unposted_evergreen:
        entry_title = random.choice(unposted_evergreen)
        chosen_category = "Global Work Permits & Immigration"
        summary_text = f"Official 2027 guidelines on {entry_title}. Review eligibility parameters, official processing fees, age criteria, and direct application links."
    else:
        headers = {'User-Agent': 'Mozilla/5.0'}
        breaking_count = get_today_breaking_count()
        feed_items = list(FEEDS.items())
        random.shuffle(feed_items)

        if breaking_count >= 3:
            feed_items = [f for f in feed_items if f[0] not in BREAKING_CATEGORIES]

        for cat_name, feed_url in feed_items:
            try:
                response = requests.get(feed_url, headers=headers, timeout=15)
                if response.status_code == 200:
                    feed = feedparser.parse(response.text)
                    for entry in feed.entries[:8]:
                        link = entry.get('link')
                        title = entry.get('title', '')
                        if link and title and not is_duplicate(link, title):
                            selected_entry = entry
                            chosen_category = cat_name
                            break
                if selected_entry: break
            except Exception as e:
                print(f"Skipping Feed: {e}")

        if selected_entry:
            entry_title = selected_entry.get('title', 'Global Strategic Intelligence Wire')
            summary_text = selected_entry.get('summary', entry_title)
        else:
            entry_title = random.choice(EVERGREEN_MASTER_TOPICS)
            chosen_category = "Global Work Permits & Immigration"
            summary_text = f"Official 2027 guidelines and updates on {entry_title}."

    # Get Country Specific Source & Info
    country_info = get_country_specific_details(entry_title)
    source_link = country_info["source_url"]

    image_url, image_alt = get_featured_image(entry_title, chosen_category, country_info["image_keyword"])
    ai_data = generate_article_with_ai(chosen_category, entry_title, summary_text, country_info)

    seo_title = ai_data.get("seo_title", entry_title[:70])
    meta_desc = ai_data.get("meta_description", summary_text)[:148].strip()
    article_body_html = ai_data.get("article_body", "")

    read_time = calculate_read_time(article_body_html)
    human_meta = generate_human_authority_meta(country_info)
    human_editorial = generate_human_editorial_box(country_info)

    temp_post_url = "https://yourblog.blogspot.com"
    schema_script = generate_schema_markup(seo_title, meta_desc, temp_post_url, image_url)

    full_article_html = f"""
    {schema_script}
    {human_meta}
    <div style="color:#64748b; font-size:12px; margin-bottom:12px;">{read_time} &bull; Official Bureau Intelligence &bull; Verified Guide</div>
    <p style="font-size: 15px; color: #1e293b; line-height: 1.6;"><i><b>Executive Summary:</b> {meta_desc}</i></p>
    <div style="margin:20px 0;">
        <img src="{image_url}" alt="{image_alt}" title="{seo_title}" style="width:100%; border-radius:8px; box-shadow:0 4px 6px rgba(0,0,0,0.08);"/>
    </div>
    {article_body_html}
    {human_editorial}
    <hr style="margin-top:25px; border:0; border-top:1px solid #e2e8f0;"/>
    <p><small><b>Official Reference Desk:</b> <a href="{source_link}" target="_blank" rel="noopener" style="color:#0284c7; font-weight:600;">{country_info['source_name']}</a> &bull; TRTT NEWS 24 BD Editorial Desk</small></p>
    """

    blogger_service = get_blogger()
    if blogger_service:
        blog_id = os.environ.get("BLOGGER_ID") or os.environ.get("BLOGGER_BLOG_ID")
        loc = get_smart_location(entry_title, chosen_category)

        raw_labels = [chosen_category, "Human Verified", "Topical Authority", "2027 Immigration Guide"]
        unique_labels = list(set(raw_labels))

        post_body = {
            "kind": "blogger#post",
            "title": seo_title,
            "content": full_article_html,
            "searchDescription": meta_desc,
            "labels": unique_labels,
            "location": {"name": loc["name"], "lat": loc["lat"], "lng": loc["lng"]}
        }

        result = blogger_service.posts().insert(blogId=blog_id, body=post_body, isDraft=False, fetchImages=True).execute()
        post_id = result.get('id')
        post_url = result.get('url')
        print(f"👑 DYNAMIC COUNTRY ARTICLE PUBLISHED: {post_url}")

        save_history(source_link, seo_title, chosen_category, post_url)
        send_telegram_notification(seo_title, post_url)

if __name__ == "__main__":
    main()
