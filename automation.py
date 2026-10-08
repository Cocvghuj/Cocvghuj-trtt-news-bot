import feedparser, os, datetime, requests, json
from google import genai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

FEEDS = {
    "Bangladesh": "https://feeds.bbci.co.uk/news/world/asia/rss.xml",
    "International": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "Europe": "http://feeds.bbci.co.uk/news/world/europe/rss.xml",
    "Schengen Hub": "https://www.schengenvisainfo.com/feed/",
    "Visa & Immigration": "https://www.cicnews.com/feed",
    "Education & Scholarship": "https://www.scholarship-positions.com/feed/",
    "Technology & Gadgets": "http://feeds.bbci.co.uk/news/technology/rss.xml",
    "Guest Post": "http://feeds.bbci.co.uk/news/world/rss.xml"
}
WEEK_PLAN = {
    0: ["Bangladesh", "Schengen Hub"],
    1: ["Visa & Immigration", "International"],
    2: ["Europe", "Education & Scholarship"],
    3: ["Technology & Gadgets", "Bangladesh"],
    4: ["Schengen Hub", "Visa & Immigration"],
    5: ["International", "Europe"],
    6: ["Education & Scholarship", "Guest Post"]
}
TRAFFIC = {
    "Bangladesh": "Bangladesh News Today",
    "International": "Breaking News Today 2026",
    "Europe": "Europe Visa Update 2026",
    "Schengen Hub": "Schengen Visa 2026",
    "Visa & Immigration": "Italy Work Visa 2026",
    "Education & Scholarship": "Fully Funded Scholarship 2026",
    "Technology & Gadgets": "AI News Today",
    "Guest Post": "Guest Post News"
}

def get_category():
    now = datetime.datetime.now()
    slot = 0 if now.hour < 12 else 1
    return WEEK_PLAN[now.weekday()][slot]

def rewrite(text, category):
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    prompt = f"Rewrite for TRTT NEWS 24 BD, category {category}, 100% unique, 350 words, SEO friendly, add 1 H2. Original: {text}"
    res = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    return res.text

def post_to_blogger(title, content, labels):
    BLOG_ID = os.environ["BLOGGER_ID"]
    creds = Credentials.from_authorized_user_info(json.loads(os.environ["BLOGGER_TOKEN_JSON"]))
    service = build("blogger", "v3", credentials=creds)
    body = {"kind": "blogger#post", "blog": {"id": BLOG_ID}, "title": title, "content": content, "labels": labels}
    post = service.posts().insert(blogId=BLOG_ID, body=body, isDraft=False).execute()
    return post["url"]

def post_to_telegram(title, url):
    try:
        token = os.environ["TELEGRAM_BOT_TOKEN"]
        chat_id = os.environ["TELEGRAM_CHANNEL_ID"]
        msg = f"🔴 <b>{title}</b>\n\n👉 <a href='{url}'>বিস্তারিত পড়ুন</a>"
        requests.post(f"https://api.telegram.org/bot{token}/sendMessage", data={"chat_id": chat_id, "text": msg, "parse_mode": "HTML"})
    except: pass

category = get_category()
feed = feedparser.parse(FEEDS[category])
entry = feed.entries[0]
new_content = rewrite(entry.title + " " + entry.summary, category)
url = post_to_blogger(entry.title, new_content, [category, TRAFFIC[category]])
post_to_telegram(entry.title, url)
