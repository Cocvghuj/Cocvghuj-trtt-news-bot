import os, random, json, requests, feedparser
from datetime import datetime
from zoneinfo import ZoneInfo
import telebot
from PIL import Image, ImageDraw

# ===== SECRETS =====
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
FB_PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")
FB_PAGE_ID = os.getenv("FB_PAGE_ID")
BLOGGER_BLOG_ID = os.getenv("BLOGGER_BLOG_ID")
BLOGGER_ACCESS_TOKEN = os.getenv("BLOGGER_ACCESS_TOKEN")
GOOGLE_SHEET_WEBHOOK_URL = os.getenv("GOOGLE_SHEET_WEBHOOK_URL")
bot = telebot.TeleBot(TOKEN)
TEMPLATE_FILE = "template.jpeg" if os.path.exists("template.jpeg") else "template.jpg"

BLOCKED_KEYWORDS = ["সরকারি নোটিশ","প্রজ্ঞাপন","গেজেট","NID","পাসপোর্ট","অফিস আদেশ","নিয়োগ বিজ্ঞপ্তি সরকারি","সেনাবাহিনী","police","মন্ত্রণালয়"]
EVERGREEN_NEWS = ["মোবাইলের ব্যাটারি দীর্ঘক্ষণ বাঁচানোর ৭টি উপায়","ফেসবুক প্রোফাইল নিরাপদ রাখার ৫টি উপায়","প্রবাস থেকে টাকা পাঠানোর আগে যে ৩টি ভুল করবেন না","বাংলাদেশের অজানা ১০টি সুন্দর জায়গা"]
RSS_FEEDS = ["https://www.prothomalo.com/feed","https://www.jugantor.com/feed","https://www.kalerkantho.com/rss","https://feeds.bbci.co.uk/bengali/rss.xml"]

MASTER_FILES = {
"requirements.txt": "pyTelegramBotAPI\nrequests\nPillow\nfeedparser",
".github/workflows/trtt.yml": """name: TRTT All In One
on:
  schedule:
    - cron: '0 2 * * *'
    - cron: '0 5 * * *'
    - cron: '0 7 * * *'
    - cron: '0 10 * * *'
    - cron: '0 13 * * *'
    - cron: '0 16 * * *'
  workflow_dispatch:
jobs:
  run-bot:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - name: Run Bot
        env:
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
          FB_PAGE_ACCESS_TOKEN: ${{ secrets.FB_PAGE_ACCESS_TOKEN }}
          FB_PAGE_ID: ${{ secrets.FB_PAGE_ID }}
          BLOGGER_BLOG_ID: ${{ secrets.BLOGGER_BLOG_ID }}
          BLOGGER_ACCESS_TOKEN: ${{ secrets.BLOGGER_ACCESS_TOKEN }}
          GOOGLE_SHEET_WEBHOOK_URL: ${{ secrets.GOOGLE_SHEET_WEBHOOK_URL }}
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: python automation.py
      - name: Smart Backup
        run: |
          git config user.name "TRTT Bot"
          git config user.email "bot@trtt.com"
          echo "$(date) - Posted" >> logs.txt
          git add posted.json logs.txt || trueগ
          git commit -m "Backup [skip ci]" || true
          git push || true
"""
}

def self_heal():
    for path, content in MASTER_FILES.items():
        d = os.path.dirname(path)
        if d and not os.path.exists(d): os.makedirs(d, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f: f.write(content.strip()+"\n")

def get_slot():
    h = datetime.now(ZoneInfo("Asia/Dhaka")).hour
    if 7 <= h < 10: return "weather"
    elif 10 <= h < 12: return "jobs_edu"
    elif 12 <= h < 15: return "viral_human"
    elif 15 <= h < 18: return "sports_ent"
    elif 18 <= h < 21: return "probash_int"
    else: return "tips_evergreen"

def get_news():
    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)
            for e in feed.entries[:15]:
                if not any(k.lower() in e.title.lower() for k in BLOCKED_KEYWORDS):
                    return e.title, e.get("description","")[:300], e.link
        except: continue
    t = random.choice(EVERGREEN_NEWS)
    return t, t, "https://trttnews24bd.blogspot.com"

def make_image(title):
    try:
        img = Image.open(TEMPLATE_FILE).convert("RGB")
        draw = ImageDraw.Draw(img)
        draw.rectangle([(20,500),(980,750)], fill=(0,0,0))
        draw.text((40,520), title[:90], fill=(255,255,255))
        out="final_post.jpg"; img.save(out); return out
    except: return TEMPLATE_FILE

def post_fb(title, cap, img_path):
    if not FB_PAGE_ACCESS_TOKEN or not FB_PAGE_ID: return "Skipped"
    try:
        url=f"https://graph.facebook.com/{FB_PAGE_ID}/photos"
        data={'message': f"🚨 {title}\n\n{cap}", 'access_token': FB_PAGE_ACCESS_TOKEN}
        with open(img_path,'rb') as im: r=requests.post(url, data=data, files={'source': im}, timeout=20)
        return "OK" if r.status_code==200 else "FAIL"
    except: return "ERROR"

def post_blog(title, content, link):
    if not BLOGGER_BLOG_ID or not BLOGGER_ACCESS_TOKEN: return "Skipped"
    try:
        url=f"https://www.googleapis.com/blogger/v3/blogs/{BLOGGER_BLOG_ID}/posts/"
        h={"Authorization": f"Bearer {BLOGGER_ACCESS_TOKEN}", "Content-Type": "application/json"}
        p={"kind":"blogger#post","title":title,"content": f"<p>{content}</p><br><a href='{link}'>মূল খবর</a>"}
        r=requests.post(url, headers=h, json=p, timeout=20)
        return "OK" if r.status_code==200 else "EXPIRED"
    except: return "ERROR"

def backup_sheet(title, cat):
    if not GOOGLE_SHEET_WEBHOOK_URL: return "Skipped"
    try:
        payload={"date": datetime.now(ZoneInfo("Asia/Dhaka")).strftime('%Y-%m-%d %H:%M'), "category": cat, "title": title, "status": "POSTED"}
        r=requests.post(GOOGLE_SHEET_WEBHOOK_URL, json=payload, timeout=10)
        return "OK" if r.status_code==200 else "FAIL"
    except: return "FAIL"

if __name__=="__main__":
    self_heal()
    slot=get_slot()
    title,content,link=get_news()
    img=make_image(title)
    cap=f"{content}\n\n🔗 {link}\n#TRTTNEWS24BD"
    fb=post_fb(title,cap,img)
    blog=post_blog(title,content,link)
    sheet=backup_sheet(title,slot)
    report=f"✅ TRTT Autopilot Pro\n\n📰 {title}\n📂 {slot}\n📘 FB:{fb} 📝 Blog:{blog} 📊 Sheet:{sheet}\n🔗 {link}"
    try:
        if os.path.exists(img): bot.send_photo(ADMIN_CHAT_ID, open(img,'rb'), caption=report, parse_mode="Markdown")
        else: bot.send_message(ADMIN_CHAT_ID, report, parse_mode="Markdown")
    except: pass
    data=json.load(open("posted.json")) if os.path.exists("posted.json") else []
    data.insert(0,{"date":datetime.now().isoformat(),"title":title,"slot":slot})
    json.dump(data[:15], open("posted.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"DONE {slot} FB:{fb} Blog:{blog} Sheet:{sheet}")
