import json
import os
import re
from datetime import datetime, timedelta
from typing import List
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

import requests
from google import genai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from slugify import slugify

MARKER = os.environ.get("TRAVEL_PAYOUT_MARKER", "787950")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
BLOGGER_BLOG_ID = os.environ.get("BLOGGER_BLOG_ID")
BLOGGER_CLIENT_ID = os.environ.get("BLOGGER_CLIENT_ID")
BLOGGER_CLIENT_SECRET = os.environ.get("BLOGGER_CLIENT_SECRET")
BLOGGER_REFRESH_TOKEN = os.environ.get("BLOGGER_REFRESH_TOKEN")
AMAZON_LINK = os.environ.get("AMAZON_LINK", "https://amzn.to/4shg6Hn")
BLOGGER_URL = "https://ttnews24bd.blogspot.com"
PWA_URL = "https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/"
HISTORY_FILE = "published_history.txt"

TOPIC_POOL = [
    "flight delay compensation",
    "best travel eSIM for Europe",
    "budget airport transfer tips",
    "cheaper flights without losing convenience",
    "Europe trip planning and savings",
    "travel essentials and airport prep",
]


def load_history() -> List[str]:
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as handle:
        return [line.strip() for line in handle if line.strip()]


def save_history(title_id: str):
    with open(HISTORY_FILE, "a", encoding="utf-8") as handle:
        handle.write(f"{title_id}\n")


def load_partners() -> List[str]:
    if not os.path.exists("partners.json"):
        return []
    with open("partners.json", "r", encoding="utf-8") as handle:
        data = json.load(handle)
    nodes = data.get("nodes", [])
    return [node.get("link") for node in nodes if node.get("link")]


def append_tracking_params(url: str, *, via: str = "trtt-blog", source: str | None = None) -> str:
    if not url:
        return url
    parsed = urlparse(url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query["via"] = via
    if source:
        query["source"] = source
    if "marker" not in query and "travelpayout" in url.lower():
        query["marker"] = MARKER
    return urlunparse(parsed._replace(query=urlencode(query)))


def build_affiliate_links() -> List[str]:
    links = load_partners()
    return [append_tracking_params(link, via="trtt-blog") for link in links if link]


def ensure_public_guides_dir():
    os.makedirs("public/guides", exist_ok=True)


def send_telegram(message: str):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": message, "parse_mode": "HTML"}, timeout=20)
    except Exception as exc:
        print(f"Telegram send failed: {exc}")


def post_to_blogger(title: str, content: str, labels: List[str]):
    if not all([BLOGGER_BLOG_ID, BLOGGER_CLIENT_ID, BLOGGER_CLIENT_SECRET, BLOGGER_REFRESH_TOKEN]):
        print("Blogger credentials missing. Skipping Blogger post.")
        return None
    try:
        creds = Credentials(
            None,
            refresh_token=BLOGGER_REFRESH_TOKEN,
            client_id=BLOGGER_CLIENT_ID,
            client_secret=BLOGGER_CLIENT_SECRET,
            token_uri="https://oauth2.googleapis.com/token",
        )
        service = build("blogger", "v3", credentials=creds)
        body = {"title": title, "content": content, "labels": labels}
        post = service.posts().insert(blogId=BLOGGER_BLOG_ID, body=body).execute()
        print(f"Posted to Blogger successfully! URL: {post.get('url')}")
        return post.get("url")
    except Exception as exc:
        print(f"Error posting to Blogger: {exc}")
        return None


def create_prompt(topic: str, affiliate_links: List[str]) -> str:
    first_link = affiliate_links[0] if affiliate_links else "https://airhelp.tpo.lv/3ItXS0E4"
    second_link = affiliate_links[1] if len(affiliate_links) > 1 else "https://gettransfer.tpo.lv/1u8zRU5s"
    third_link = affiliate_links[2] if len(affiliate_links) > 2 else "https://airalo.tpo.lv/ZZoQC7Mz"
    pwa_link = f"{PWA_URL}?source=blogger_post"
    blog_link = f"{BLOGGER_URL}?source=trtt_blog"
    return f"""
You are an expert travel writer and SEO editor for a Europe-focused travel blog. Write one premium article in English, 1000-1200 words, covering the topic: {topic}.

Required structure exactly:
1. SEO Title (60 chars, format like 'How to ...', 'Best ...', or 'Is ...')
2. Intro (80-100 words, personal story hook)
3. H2: What is / Overview
4. H2: Who is Eligible / Best Time
5. H2: Step-by-Step Guide (3-4 bullets)
6. H2: Cost / Documents / FAQ (3 Q&A)
7. MANDATORY BOX 1 after paragraph 2: 'My Personal Recommendation' with text: 'Check out AirHelp.' Include a link to this affiliate URL: {first_link}
8. MANDATORY BOX 2 at end: 'Explore More via TRTT VoyageHub PWA' with link: {pwa_link}
9. Add one image with alt text inside the article. Use a realistic travel stock image URL.
10. Add exactly 3 internal links placeholders named 'Internal Link 1', 'Internal Link 2', 'Internal Link 3' that act as placeholders for site pages.
11. Add disclosure text exactly: 'This post contains affiliate links'.
12. Add a final CTA line reading: 'Read Daily Travel Blog' with hyperlink to {blog_link}.
13. Keep the tone human, practical, and evergreen.
14. Use clear Markdown headings and paragraphs, and make it polished enough for publication.
15. Use value-driven English, not fluff. Make it feel like a real expert article for travel readers.
16. Keep total length around 1100 words.
17. Add 1 image with alt text and ensure it is placed near the top.

Affiliate link references: {first_link}, {second_link}, {third_link}
"""


def generate_article(topic: str) -> str:
    client = genai.Client(api_key=GEMINI_API_KEY)
    prompt = create_prompt(topic, build_affiliate_links())
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    text = getattr(response, "text", None)
    if not text:
        text = str(response)
    article = text.strip()
    if not article:
        raise RuntimeError("Gemini returned empty content.")
    return article


def build_html_article(article_markdown: str, topic: str) -> str:
    article_html = article_markdown.strip()
    article_html = article_html.replace("\r\n", "\n")

    image_url = "https://images.unsplash.com/photo-1527631746610-bca00a040d60?auto=format&fit=crop&w=1200&q=80"
    article_html = (
        f"<div style='max-width: 900px; margin: 0 auto; font-family: Arial, sans-serif; line-height: 1.7; color: #1d1d1d;'>"
        f"<img src='{image_url}' alt='Travelers exploring a destination with luggage and planning notes' style='width:100%; border-radius: 12px; margin-bottom: 18px;' />"
        f"{article_html}"
        f"</div>"
    )

    article_html = re.sub(r"\n{2,}", "\n\n", article_html)
    article_html = article_html.replace("Read Daily Travel Blog", "<a href='https://ttnews24bd.blogspot.com?source=trtt_blog' target='_blank' rel='dofollow'>Read Daily Travel Blog</a>")
    article_html = article_html.replace("Internal Link 1", "<a href='travel-guide.html'>Travel Guide</a>")
    article_html = article_html.replace("Internal Link 2", "<a href='about.html'>About</a>")
    article_html = article_html.replace("Internal Link 3", "<a href='contact.html'>Contact</a>")
    article_html = article_html.replace("Check out AirHelp.", "Check out AirHelp. <a href='https://airhelp.tpo.lv/3ItXS0E4?via=trtt-blog' target='_blank' rel='sponsored nofollow'>AirHelp</a>")
    article_html = article_html.replace("This post contains affiliate links", "<strong>This post contains affiliate links</strong>")
    article_html = article_html.replace("TRTT VoyageHub PWA", "<a href='https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/?source=blogger_post' target='_blank' rel='dofollow'>TRTT VoyageHub PWA</a>")
    return article_html


def main():
    ensure_public_guides_dir()
    history = load_history()
    topic = TOPIC_POOL[(datetime.utcnow().day - 1) % len(TOPIC_POOL)]
    title_slug = slugify(topic)
    if title_slug in history:
        topic = TOPIC_POOL[(datetime.utcnow().day + 1) % len(TOPIC_POOL)]
        title_slug = slugify(topic)

    article_text = generate_article(topic)
    html_article = build_html_article(article_text, topic)

    date_key = datetime.utcnow().strftime("%Y-%m-%d")
    output_file = os.path.join("public", "guides", f"{date_key}-{title_slug}.html")
    with open(output_file, "w", encoding="utf-8") as handle:
        handle.write(html_article)

    article_title = topic.capitalize()
    post_url = post_to_blogger(article_title, html_article, ["travel", "article", "blog"])
    save_history(title_slug)

    print(f"Pushed 1 article")
    if post_url:
        print(f"Blogger URL: {post_url}")
    else:
        print("Blogger post skipped due to missing credentials.")
    send_telegram(f"<b>Pushed 1 article</b>\n{article_title}\n{post_url or PWA_URL}")


if __name__ == "__main__":
    main()
