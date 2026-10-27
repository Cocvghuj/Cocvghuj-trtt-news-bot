import os, random, requests
import google.generativeai as genai
from slugify import slugify
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Environment Variables
MARKER_ID = os.environ.get("TRAVEL_PAYOUT_MARKER", "787950")
AMAZON_LINK = os.environ.get("AMAZON_LINK", "https://amzn.to/4shg6Hn")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
VERCEL_APP_URL = "https://cocvghuj-trtt-news-bot.vercel.app/"

# Blogger Credentials
BLOGGER_BLOG_ID = os.environ.get("BLOGGER_BLOG_ID")
BLOGGER_CLIENT_ID = os.environ.get("BLOGGER_CLIENT_ID")
BLOGGER_CLIENT_SECRET = os.environ.get("BLOGGER_CLIENT_SECRET")
BLOGGER_REFRESH_TOKEN = os.environ.get("BLOGGER_REFRESH_TOKEN")

genai.configure(api_key=GEMINI_API_KEY)

# Topic List (English Guides)
GUIDE_TOPICS = [
    {
        "id": "guide_001",
        "title": "The Ultimate Human Guide to Finding and Using the Best eSIM for European Travel",
        "labels": ["Europe eSIM", "Travel Tech", "Travel Tips"],
        "location": "Rome, Italy",
        "service_link": f"https://airalo.tpo.lv/ZZoQC7Mz?marker={MARKER_ID}",
        "service_name": "Airalo e-SIM",
        "amazon_product": "Universal Travel Adapter",
        "img_url": "https://images.unsplash.com/photo-1522083165195-34b4dc196c73?w=1200",
        "img_caption": "Seamless internet connectivity right after landing in Europe"
    },
    {
        "id": "guide_002",
        "title": "How to Claim Up to €600 for Flight Delays and Cancellations: A Complete Traveler's Manual",
        "labels": ["Flight Delay", "AirHelp", "Passenger Rights"],
        "location": "European Airports",
        "service_link": f"https://airhelp.tpo.lv/3ItXS0E4?marker={MARKER_ID}",
        "service_name": "AirHelp",
        "amazon_product": "Active Noise Cancelling Headphones",
        "img_url": "https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=1200",
        "img_caption": "Knowing your rights when travel plans face unexpected disruptions"
    }
]

HISTORY_FILE = "published_history.txt"

def load_history():
    if not os.path.exists(HISTORY_FILE): return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def save_history(tid):
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"{tid}\n")

def send_telegram(msg):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID: return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "HTML"})

def post_to_blogger(title, content, labels):
    if not all([BLOGGER_BLOG_ID, BLOGGER_CLIENT_ID, BLOGGER_CLIENT_SECRET, BLOGGER_REFRESH_TOKEN]):
        print("Blogger credentials missing. Skipping Blogger post.")
        return None

    try:
        creds = Credentials(
            None,
            refresh_token=BLOGGER_REFRESH_TOKEN,
            client_id=BLOGGER_CLIENT_ID,
            client_secret=BLOGGER_CLIENT_SECRET,
            token_uri="https://oauth2.googleapis.com/token"
        )
        service = build('blogger', 'v3', credentials=creds)
        
        body = {
            "title": title,
            "content": content,
            "labels": labels
        }
        
        post = service.posts().insert(blogId=BLOGGER_BLOG_ID, body=body).execute()
        print(f"Posted to Blogger successfully! URL: {post.get('url')}")
        return post.get('url')
    except Exception as e:
        print(f"Error posting to Blogger: {e}")
        return None

def main():
    history = load_history()
    available = [t for t in GUIDE_TOPICS if t["id"] not in history]
    
    # সব টপিক শেষ হলে হিস্ট্রি রিসেট হবে
    if not available:
        open(HISTORY_FILE, "w", encoding="utf-8").close()
        available = GUIDE_TOPICS
        
    # প্রতি রানে ঠিক ১টি মাত্র টপিক সিলেক্ট হবে
    selected = random.choice(available)

    prompt = f"""
    You are an expert human travel developer and professional blog writer. 
    Write an extensive, highly detailed, natural, human-like travel guide in ENGLISH.
    Target word count: strictly between 1200 and 1500 words. Do not make it short or summarized.
    Title: '{selected['title']}'

    Structure requirements using proper HTML formatting tags (<h2>, <h3>, <p>, <ul>, <li>):
    1. Introduction: Engaging opening about independent travel and why automated tools beat corporate booking.
    2. Deep Dive Sections: Multiple detailed subheadings (H2, H3) covering step-by-step strategies, technical nuances, and practical advice.
    3. Practical Tips & Common Pitfalls: Real-world suggestions, hidden traps, and solutions.
    4. Conclusion & Project Vision: Final thoughts on modern digital travel tools and independent platforms.
    """

    # Gemini Content Generation
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    article_text = response.text

    # যদি জেনারেট করা টেক্সট ছোট হয়, তাহলে প্রসেস বন্ধ করবে
    if not article_text or len(article_text) < 500:
        raise Exception("Gemini generated invalid or short content. Stopping execution to prevent low quality post.")

    full_html = f"""
    <div style="max-width:850px;margin:auto;font-family:Arial,sans-serif;line-height:1.7;color:#333;">
      <img src="{selected['img_url']}" style="width:100%;border-radius:12px;box-shadow:0 4px 12px rgba(0,0,0,0.1);"/>
      <p style="color:#666;font-style:italic;text-align:center;margin-top:8px;">{selected['img_caption']} — Location: {selected['location']}</p>
      
      <div style="margin-top:25px;">
        {article_text}
      </div>

      <div style="background:#f4f9f4;padding:25px;border-radius:12px;margin-top:30px;border-left:5px solid #28a745;">
        <h3 style="color:#1e7e34;margin-top:0;">💡 My Personal Recommendation</h3>
        <p>I have personally tested and verified this service for seamless travel experiences:</p>
        <p><a href="{selected['service_link']}" target="_blank" style="background:#28a745;color:white;padding:12px 24px;text-decoration:none;border-radius:6px;display:inline-block;font-weight:bold;">👉 Check out {selected['service_name']}</a></p>
        <p style="margin-top:15px;">🎒 <strong>Essential Travel Gear:</strong> <a href="{AMAZON_LINK}" target="_blank" style="color:#0056b3;text-decoration:underline;">{selected['amazon_product']}</a></p>
      </div>

      <div style="background:#eef6fc;padding:20px;border-radius:12px;margin-top:20px;text-align:center;">
        <h4 style="margin:0 0 10px 0;color:#0056b3;">📱 Explore More via TRTT VoyageHub PWA</h4>
        <p style="margin:0;"><a href="{VERCEL_APP_URL}" target="_blank" style="color:#0056b3;font-weight:bold;text-decoration:none;">👉 Visit our Live Web App & Portal</a></p>
      </div>
    </div>
    """
    
    # Save local file backup
    os.makedirs("public/guides", exist_ok=True)
    filename = f"public/guides/{slugify(selected['title'])}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(full_html)
    
    # Post to Blogger
    blog_post_url = post_to_blogger(selected['title'], full_html, selected['labels'])
    
    # Update History File
    save_history(selected["id"])
    
    target_link = blog_post_url if blog_post_url else VERCEL_APP_URL
    tg_msg = f"<b>📖 New Detailed English Guide Published:</b> {selected['title']}\n\n👉 {target_link}"
    send_telegram(tg_msg)

if __name__ == "__main__":
    main()
