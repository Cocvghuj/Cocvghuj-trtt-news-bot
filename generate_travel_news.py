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
OPEN_AI_API_KEY = os.environ.get("OPEN_AI_API_KEY")
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")
DEEP_SEEK_KEY = os.environ.get("DEEP_SEEK_KEY")

UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY")
GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

TRAVEL_PAYOUT_MARKER = os.environ.get("TRAVEL_PAYOUT_MARKER", "787950")
AMAZON_AFFILIATE_LINK = "https://amzn.to/4shg6Hn"

# ==================== DAILY 4 TOPICS ====================
DAILY_TOPICS = [
    {
        "category": "Flight & Airport Deals",
        "focus": "Aviasales Flight Price Drops & AirHelp Compensation",
        "amazon_item": "Universal Travel Adapter & Noise Canceling Headphones",
        "amazon_tag": "Electronics & Gadgets",
        "image_keyword": "airplane,airport"
    },
    {
        "category": "Amazon Top Search Gadgets 2026",
        "focus": "AirPods 4, Smart Home Gadgets & Powerbanks",
        "amazon_item": "Anker MagSafe Power Bank & AirPods Accessories",
        "amazon_tag": "Amazon Deals 2026",
        "image_keyword": "technology,gadgets"
    },
    {
        "category": "eSIM & Destination Guide",
        "focus": "Airalo eSIM Data & Localrent Car Hire",
        "amazon_item": "Waterproof Travel Backpack & TSA Lock",
        "amazon_tag": "Travel Gear",
        "image_keyword": "travel,destination"
    },
    {
        "category": "Lifestyle, Books & Skincare",
        "focus": "Klook Tours & Organic Travel Essentials",
        "amazon_item": "Premium Sunscreen SPF50 & Travel Novels",
        "amazon_tag": "Skincare & Books",
        "image_keyword": "lifestyle,book"
    }
]

def get_current_topic():
    hour = datetime.now().hour
    if 5 <= hour < 11:
        return DAILY_TOPICS[0]
    elif 11 <= hour < 17:
        return DAILY_TOPICS[1]
    elif 17 <= hour < 23:
        return DAILY_TOPICS[2]
    else:
        return DAILY_TOPICS[3]

# ==================== MULTI-AI FALLBACK ENGINE ====================
def generate_ai_news(prompt):
    # 1. Try Gemini API
    if GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=10)
            if res.status_code == 200:
                print("✅ Generated with Gemini API")
                return res.json()['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            print(f"Gemini error: {e}")

    # 2. Try Groq API
    if GROQ_API_KEY:
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
            res = requests.post(url, json={"model": "llama3-8b-8192", "messages": [{"role": "user", "content": prompt}]}, headers=headers, timeout=10)
            if res.status_code == 200:
                print("✅ Generated with Groq API")
                return res.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"Groq error: {e}")

    # 3. Try OpenRouter API
    if OPENROUTER_API_KEY:
        try:
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
            res = requests.post(url, json={"model": "meta-llama/llama-3-8b-instruct:free", "messages": [{"role": "user", "content": prompt}]}, headers=headers, timeout=10)
            if res.status_code == 200:
                print("✅ Generated with OpenRouter API")
                return res.json()['choices'][0]['message']['content']
        except Exception as e:
            print(f"OpenRouter error: {e}")

    return "<h2>TRTT Daily Travel Update</h2><p>Check live flight prices on Aviasales and top travel gear on Amazon.</p>"

# ==================== UNSPLASH IMAGE FETCH ENGINE ====================
def get_unsplash_image(keyword):
    if UNSPLASH_ACCESS_KEY:
        try:
            url = f"https://api.unsplash.com/photos/random?query={keyword}&client_id={UNSPLASH_ACCESS_KEY}"
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                return res.json()['urls']['regular']
        except Exception as e:
            print(f"Unsplash error: {e}")
    return f"https://source.unsplash.com/800x400/?{keyword}"

# ==================== EMAIL & TELEGRAM NOTIFICATION ====================
def send_email_and_telegram(title, html_content):
    # Gmail SMTP Dispatch
    if GMAIL_USER and GMAIL_APP_PASSWORD:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"TRTT Travel Update: {title}"
            msg["From"] = GMAIL_USER
            msg["To"] = GMAIL_USER
            msg.attach(MIMEText(html_content, "html"))
            
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
                server.sendmail(GMAIL_USER, GMAIL_USER, msg.as_string())
            print("✅ Email sent via Gmail SMTP")
        except Exception as e:
            print(f"Email failed: {e}")

    # Telegram Bot Message Dispatch
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        try:
            text = f"📢 *TRTT EuroVoyage Hub Update*\n\n*Title:* {title}\n\n👉 [Read Live Article](https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/)"
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}, timeout=5)
            print("✅ Telegram notification sent")
        except Exception as e:
            print(f"Telegram failed: {e}")

# ==================== MAIN EXECUTION ====================
if __name__ == "__main__":
    topic = get_current_topic()
    
    prompt = f"""
    Act as an expert SEO journalist for TRTT EuroVoyage Hub.
    Write a 100% UNIQUE SEO Article in ENGLISH about:
    Category: {topic['category']} featuring {topic['focus']}.
    Must recommend Amazon product: {topic['amazon_item']}.
    Include 'Travelpayouts' or 'Amazon' in the Title.
    Format as HTML using <h2>, <h3>, <p>, <ul>, <li>.
    """
    
    news_body = generate_ai_news(prompt)
    title = f"{topic['category']} - Amazon & Travelpayouts Guide 2026"
    image_url = get_unsplash_image(topic['image_keyword'])
    amazon_label = topic['amazon_item'][:20]
    
    affiliate_widget = f"""
    <div style="background:#111827;border:2px solid #00ff88;padding:22px;border-radius:14px;margin-top:25px;color:#fff">
     <h3 style="color:#00ff88;margin:0 0 8px 0;">🛂 Instant Visa & Flight Route Radar</h3>
     <p style="color:#9ca3af;font-size:13px">Select destination - Visa + Price + Insurance auto update:</p>
     
     <select id="newsVisaCountry" onchange="updateFlightRoute()" style="width:100%;padding:12px;border-radius:8px;background:#000;color:#fff;border:1px solid #1f2937;margin:12px 0;font-weight:700">
      <option value="italy">🇮🇹 Italy (Rome FCO) - $450</option>
      <option value="france">🇫🇷 France (Paris CDG) - $480</option>
      <option value="germany">🇩🇪 Germany (Frankfurt FRA) - $420</option>
      <option value="uk">🇬🇧 UK (London LHR) - $510</option>
      <option value="usa">🇺🇸 USA (New York JFK) - $650</option>
      <option value="uae">🇦🇪 Dubai (DXB) - $280</option>
     </select>

     <p id="newsVisaResult" style="font-size:13px;font-weight:800;color:#00aaff;margin:0 0 14px 0">⚠️ Schengen Visa & Travel Insurance required. Fare: DAC to FCO $450.</p>
     
     <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:20px">
      <a id="dynamicFlightBtn" href="https://aviasales.tpo.lv/Fb8U9yav?marker={TRAVEL_PAYOUT_MARKER}" target="_blank" style="background:#00aaff;color:#000;padding:10px 15px;text-decoration:none;font-weight:800;border-radius:8px;font-size:13px">🛫 Book to Rome ↗</a>
      <a href="https://airalo.tpo.lv/ZZoQC7Mz?marker={TRAVEL_PAYOUT_MARKER}" target="_blank" style="background:#00ff88;color:#000;padding:10px 15px;text-decoration:none;font-weight:800;border-radius:8px;font-size:13px">📱 eSIM ↗</a>
      <a href="{AMAZON_AFFILIATE_LINK}" target="_blank" style="background:#ff9900;color:#fff;padding:10px 15px;text-decoration:none;font-weight:800;border-radius:8px;font-size:13px">🎒 {amazon_label} ↗</a>
     </div>

     <hr style="border:0;border-top:1px solid #1f2937;margin:20px 0">

     <h3 style="color:#ff3b3b;margin:0 0 8px 0;">🛡️ Schengen Insurance Calculator</h3>
     <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:12px 0">
      <input id="insDays" type="number" value="7" min="1" style="width:70px;padding:9px;background:#000;color:#fff;border:1px solid #333;border-radius:6px;font-weight:bold"> <span style="color:#fff">Days</span>
      <button onclick="calcIns()" style="background:#ff3b3b;color:#fff;padding:9px 16px;border:0;border-radius:6px;font-weight:800;cursor:pointer">Calculate</button>
     </div>
     <p id="insResult" style="color:#00ff88;font-weight:800;font-size:14px">7 Days - $17.50 (Schengen Approved €30k)</p>
    </div>

    <script>
    function updateFlightRoute(){{
     const c=document.getElementById('newsVisaCountry').value;
     const map={{
      italy:['⚠️ Schengen Visa + Insurance required. DAC→FCO $450','🛫 Book to Rome (FCO) ↗'],
      france:['⚠️ Schengen Visa required. DAC→CDG $480','🛫 Book to Paris (CDG) ↗'],
      germany:['⚠️ Schengen + €45/day proof. DAC→FRA $420','🛫 Book to Frankfurt ↗'],
      uk:['Standard Visitor Visa. DAC→LHR $510','🛫 Book to London ↗'],
      usa:['B1/B2 Visa. DAC→JFK $650','🛫 Book to New York ↗'],
      uae:['Instant 30 Days Visa. DAC→DXB $280','🛫 Book to Dubai ↗']
     }};
     if(map[c]){{
      document.getElementById('newsVisaResult').innerText=map[c][0];
      document.getElementById('dynamicFlightBtn').innerText=map[c][1];
     }}
    }}

    function calcIns(){{
     let d=document.getElementById('insDays').value||7;
     document.getElementById('insResult').innerText=d+' Days Schengen Coverage - $'+(d*2.5).toFixed(2)+' (Approved)';
    }}
    </script>
    """

    final_post_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>{title}</title>
        <style>
            body {{ background-color: #00070f; color: #fff; font-family: sans-serif; padding: 20px; margin: 0; }}
            h1 {{ color: #00ff88; font-size: 24px; }}
            img {{ width: 100%; max-height: 400px; object-fit: cover; border-radius: 12px; margin-bottom: 15px; }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        <img src="{image_url}" alt="{title}">
        {news_body}
        {affiliate_widget}
    </body>
    </html>
    """

    with open("latest_travel_news.html", "w", encoding="utf-8") as f:
        f.write(final_post_html)

    print(f"✅ Generated: {title}")
    send_email_and_telegram(title, final_post_html)
