import os, random, requests, google.generativeai as genai
from slugify import slugify

MARKER_ID = os.environ.get("TRAVEL_PAYOUT_MARKER", "787950")
AMAZON_LINK = os.environ.get("AMAZON_LINK", "https://amzn.to/4shg6Hn")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
VERCEL_APP_URL = "https://cocvghuj-trtt-news-bot.vercel.app/"

genai.configure(api_key=GEMINI_API_KEY)

GUIDE_TOPICS = [
    {
        "id": "guide_001",
        "title": "ইউরোপ ভ্রমণের সময় সস্তায় সেরা e-SIM নেওয়ার সহজ নির্দেশিকা",
        "labels": "Europe eSIM, Travel Tips",
        "location": "Rome, Italy",
        "service_link": f"https://airalo.tpo.lv/ZZoQC7Mz?marker={MARKER_ID}",
        "service_name": "Airalo e-SIM",
        "amazon_product": "ইউরোপ ট্রাভেল অ্যাডাপ্টার",
        "img_url": "https://images.unsplash.com/photo-1522083165195-34b4dc196c73?w=1200",
        "img_caption": "ইউরোপে ল্যান্ড করার পর পরই ইন্টারনেট সংযোগ"
    },
    {
        "id": "guide_002",
        "title": "ফ্লাইট বিলম্ব বা ক্যানসেল হলে ৬০০ ইউরো পর্যন্ত ক্ষতিপূরণ",
        "labels": "Flight Delay, AirHelp",
        "location": "European Airports",
        "service_link": f"https://airhelp.tpo.lv/3ItXS0E4?marker={MARKER_ID}",
        "service_name": "AirHelp",
        "amazon_product": "নয়েজ ক্যানসেলিং হেডফোন",
        "img_url": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=1200",
        "img_caption": "ফ্লাইট বিলম্বে আপনার অধিকার"
    }
]

HISTORY_FILE = "published_history.txt"

def load_history():
    if not os.path.exists(HISTORY_FILE): return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f]

def save_history(tid):
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"{tid}\n")

def send_telegram(msg):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID: return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "HTML"})

def main():
    history = load_history()
    available = [t for t in GUIDE_TOPICS if t["id"] not in history]
    if not available:
        open(HISTORY_FILE, "w").close()
        available = GUIDE_TOPICS
    selected = random.choice(available)

    prompt = f"""
    তুমি একজন প্র্যাকটিক্যাল ট্রাভেল ডেভেলপার। বাংলায় ১০০০+ শব্দের বিস্তারিত এভারগ্রিন গাইড লেখো।
    শিরোনাম: '{selected['title']}'
    স্ট্রাকচার: ভূমিকা (কেন অটোমেশন বড় কোম্পানির চেয়ে ভালো), H2/H3 সহ ধাপে ধাপে সমাধান, ব্যক্তিগত টিপস, এবং শেষে কেন এই প্রজেক্ট বানাচ্ছো তার ভিশন।
    """

    # Gemini Pro মডেল ব্যবহার করা হচ্ছে যা অত্যন্ত নির্ভরযোগ্য
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content(prompt)
    article_text = response.text

    full_html = f"""
    <div style="max-width:800px;margin:auto;font-family:Arial">
      <img src="{selected['img_url']}" style="width:100%;border-radius:12px"/>
      <p style="color:#666;font-style:italic">{selected['img_caption']} | {selected['location']}</p>
      <div>{article_text}</div>
      <div style="background:#e9f7ef;padding:20px;border-radius:10px;margin-top:20px">
        <h3>💡 আমার রেকমেন্ডেশন</h3>
        <p>আমি নিজে টেস্ট করে দেখেছি:</p>
        <p><a href="{selected['service_link']}" target="_blank" style="background:#28a745;color:white;padding:12px 20px;text-decoration:none;border-radius:6px;display:inline-block">👉 {selected['service_name']} চেক করুন</a></p>
        <p style="margin-top:15px">🎒 সাথে রাখুন: <a href="{AMAZON_LINK}" target="_blank">{selected['amazon_product']}</a></p>
      </div>
      <div style="background:#e2f0d9;padding:20px;border-radius:10px;margin-top:20px;text-align:center">
        <h4>📱 TRTT VoyageHub PWA</h4>
        <p><a href="{VERCEL_APP_URL}" target="_blank">👉 আমাদের লাইভ অ্যাপ ও পোর্টাল দেখুন</a></p>
      </div>
    </div>
    """
    
    os.makedirs("public/guides", exist_ok=True)
    filename = f"public/guides/{slugify(selected['title'])}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(full_html)
    
    print(f"Generated: {filename}")
    save_history(selected["id"])
    
    tg_msg = f"<b>📖 নতুন গাইড: {selected['title']}</b>\n\n{selected['img_caption']}\n\n👉 {VERCEL_APP_URL}"
    send_telegram(tg_msg)

if __name__ == "__main__":
    main()
