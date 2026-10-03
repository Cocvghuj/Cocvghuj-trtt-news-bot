from datetime import datetime
import json
import logging
import os
import re
import time
import xml.etree.ElementTree as ET
import requests

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

RSS_URL = "https://trttnews24bd.blogspot.com/feeds/posts/default?alt=rss"
POSTED_FILE = "posted.json"
MAX_POST_PER_DAY = 8

# জনগণের চাহিদাপূর্ণ জনপ্রিয় ক্যাটাগরি বা কিউয়ার্ডসমূহের তালিকা
POPULAR_KEYWORDS = [
    "ব্রেকিং",
    "জরুরি",
    "চাকরি",
    "নিয়োগ",
    "বোর্ড",
    "ফলাফল",
    "টেক",
    "প্রযুক্তি",
    "স্মার্টফোন",
    "এআই",
    "বিজ্ঞপ্তি",
    "শিক্ষার্থী",
    "আবহাওয়া",
    "বাজারদর",
    "জাতীয়",
    "আন্তর্জাতিক",
]


def is_high_demand_news(title, desc):
    """খবরের শিরোনাম বা বিবরণে মানুষের চাহিদাপূর্ণ শব্দ আছে কি না চেক করবে"""
    text = (title + " " + desc).lower()
    for keyword in POPULAR_KEYWORDS:
        if keyword.lower() in text:
            return True
    return False


def get_pages_auto():
    token = os.getenv("FB_USER_ACCESS_TOKEN") or os.getenv(
        "FB_PAGE_ACCESS_TOKEN"
    )
    if not token:
        return []
    try:
        url = f"https://graph.facebook.com/v21.0/me/accounts?access_token={token}"
        data = requests.get(url, timeout=20).json()
        pages = []
        for p in data.get("data", []):
            pages.append(
                {"id": p["id"], "token": p["access_token"], "name": p["name"]}
            )
        if not pages:
            pages.append(
                {
                    "id": os.getenv("FB_PAGE_ID"),
                    "token": os.getenv("FB_PAGE_ACCESS_TOKEN"),
                    "name": "TRTT Page",
                }
            )
        return pages
    except Exception as e:
        logging.error(f"FB Pages Error: {e}")
        return [
            {
                "id": os.getenv("FB_PAGE_ID"),
                "token": os.getenv("FB_PAGE_ACCESS_TOKEN"),
                "name": "TRTT Page",
            }
        ]


def load_posted():
    if not os.path.exists(POSTED_FILE):
        return []
    try:
        with open(POSTED_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_posted(link):
    posted = load_posted()
    links = [p["link"] if isinstance(p, dict) else p for p in posted]
    if link not in links:
        posted.append({"link": link, "time": datetime.now().isoformat()})
        with open(POSTED_FILE, "w", encoding="utf-8") as f:
            json.dump(posted[-200:], f, ensure_ascii=False, indent=2)


def get_today_count():
    posted = load_posted()
    today = datetime.now().date().isoformat()
    return sum(
        1
        for p in posted
        if isinstance(p, dict) and today in p.get("time", "")
    )


def get_news():
    try:
        r = requests.get(
            RSS_URL, timeout=20, headers={"User-Agent": "Mozilla/5.0"}
        )
        root = ET.fromstring(r.content)
        ns = {
            "atom": "http://www.w3.org/2005/Atom",
            "media": "http://search.yahoo.com/mrss/",
        }
        news_list = []
        for entry in root.findall("atom:entry", ns)[:15]:
            title = entry.findtext("atom:title", "", ns).strip()
            link = ""
            for l in entry.findall("atom:link", ns):
                if l.get("rel") == "alternate":
                    link = l.get("href")
                    break
            content = entry.findtext("atom:content", "", ns) or ""
            img = None
            thumb = entry.find("media:thumbnail", ns)
            if thumb is not None:
                img = thumb.get("url")
            if not img:
                m = re.search(r'<img[^>]+src="([^"]+)"', content)
                if m:
                    img = m.group(1)
            if img:
                img = img.replace("/s72-c/", "/s1600/").replace(
                    "/s72/", "/s1600/"
                )
            desc = re.sub("<[^<]+?>", "", content).strip()[:350]
            if title and link:
                news_list.append(
                    {"title": title, "link": link, "desc": desc, "image": img}
                )
        return news_list
    except Exception as e:
        logging.error(f"RSS Error: {e}")
        return []


def post_to_telegram(message, image_url):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = (
        os.getenv("TELEGRAM_CHANNEL_ID")
        or os.getenv("TELEGRAM_CHAT_ID")
        or "@trttnews24bd"
    )
    if not token:
        return
    try:
        if image_url:
            url = f"https://api.telegram.org/bot{token}/sendPhoto"
            data = {
                "chat_id": chat_id,
                "photo": image_url,
                "caption": message,
                "parse_mode": "HTML",
            }
        else:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            data = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML",
            }
        requests.post(url, data=data, timeout=20)
        logging.info("Telegram Posted")
    except Exception as e:
        logging.error(f"Telegram Error: {e}")


def post_all(message, image_url):
    pages = get_pages_auto()
    for page in pages:
        try:
            if image_url:
                url = f"https://graph.facebook.com/{page['id']}/photos"
                data = {
                    "url": image_url,
                    "caption": message,
                    "access_token": page["token"],
                }
            else:
                url = f"https://graph.facebook.com/{page['id']}/feed"
                data = {"message": message, "access_token": page["token"]}

            res = requests.post(url, data=data, timeout=30)
            res_json = res.json()
            logging.info(f"FB {page['name']}: {res.status_code}")

            # ফেসবুক পোস্টে সফলভাবে পোস্ট হওয়ার পর অটো কমেন্ট যুক্ত করার অংশ
            post_id = res_json.get("id") or res_json.get("post_id")
            if post_id:
                time.sleep(5)
                comment_url = f"https://graph.facebook.com/{post_id}/comments"
                comment_data = {
                    "message": (
                        "👉 নিয়মিত সব আপডেট ও নিউজ সবার আগে পেতে আমাদের ওয়েবসাইট"
                        " ভিজিট করুন: https://trttnews24bd.blogspot.com"
                    ),
                    "access_token": page["token"],
                }
                comm_res = requests.post(
                    comment_url, data=comment_data, timeout=20
                )
                logging.info(f"Auto Comment Status: {comm_res.status_code}")

            time.sleep(10)
        except Exception as e:
            logging.error(f"FB Error: {e}")


def main():
    if get_today_count() >= MAX_POST_PER_DAY:
        logging.info("Today limit reached")
        return
    posted_links = [
        p["link"] if isinstance(p, dict) else p for p in load_posted()
    ]
    for n in get_news():
        if n["link"] in posted_links:
            continue

        # জনগণের চাহিদার সাথে মিলে কি না চেক করা (না মিললে স্কিপ করবে)
        if not is_high_demand_news(n["title"], n["desc"]):
            logging.info(f"Skipped (Not in high demand): {n['title'][:30]}")
            continue

        whatsapp = "https://whatsapp.com/channel/0029Vb8co9VDeONEz0B5e51M"

        msg_fb = (
            f"🔥 এই মুহূর্তের আলোচিত খবর:\n🇧🇩 {n['title']}\n\n"
            f"{n['desc']}...\n\n🔗 বিস্তারিতঃ {n['link']}\n\n"
            "👉 পেজ লাইক দিয়ে সাথেই থাকুন\n"
            f"📲 WhatsApp: {whatsapp}\n"
            "✈️ Telegram: https://t.me/trttnews24bd\n\n"
            "#TRTTNEWS #BanglaNews"
        )
        msg_tg = (
            f"🔥 <b>{n['title']}</b>\n\n{n['desc']}...\n\n"
            f"🔗 <b>বিস্তারিতঃ</b> {n['link']}\n\n"
            f"📲 WhatsApp: {whatsapp}\n"
            "✈️ Telegram: https://t.me/trttnews24bd"
        )

        post_to_telegram(msg_tg, n["image"])
        post_all(msg_fb, n["image"])
        save_posted(n["link"])
        break


if __name__ == "__main__":
    main()
