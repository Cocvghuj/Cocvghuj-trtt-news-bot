#!/usr/bin/env python3
"""Forward newly published TRTT Blogger posts to the configured Telegram channel."""
from __future__ import annotations
import html, json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

FEEDS = [
    ("TRTT Voyage", "https://trttvoyage.blogspot.com/feeds/posts/default?alt=rss&max-results=100"),
    ("TRTT News 24 BD", "https://trttnews24bd.blogspot.com/feeds/posts/default?alt=rss&max-results=100"),
]
STATE_PATH = Path(".telegram-state/sent-posts.json")

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.images = [], []
    def handle_data(self, data):
        if data.strip(): self.parts.append(data.strip())
    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img":
            values = dict(attrs)
            src = values.get("src") or values.get("data-src")
            if src and src.startswith("https://"): self.images.append(src)

def fetch_feed(name, url):
    req = urllib.request.Request(url, headers={"User-Agent":"TRTT-Voyage-Telegram-Bridge/1.0"})
    with urllib.request.urlopen(req, timeout=25) as response: payload = response.read()
    root = ET.fromstring(payload)
    posts = []
    for item in root.findall("./channel/item")[:100]:
        title = (item.findtext("title") or "TRTT Voyage update").strip()
        link = (item.findtext("link") or "").strip()
        guid = (item.findtext("guid") or link or title).strip()
        parser = TextExtractor()
        parser.feed(item.findtext("description") or "")
        summary = re.sub(r"\s+", " ", " ".join(parser.parts)).strip()
        if link.startswith("https://") and guid:
            posts.append({"id":guid,"title":title,"link":link,"summary":summary[:650],
                          "image":parser.images[0] if parser.images else "", "source":name})
    return posts

def load_state():
    if not STATE_PATH.exists(): return {"initialized":False,"sent_ids":[]}
    try:
        obj=json.loads(STATE_PATH.read_text(encoding="utf-8"))
        return {"initialized":bool(obj.get("initialized")),
                "sent_ids":[str(x) for x in obj.get("sent_ids",[])][-1000:]}
    except (OSError, json.JSONDecodeError, AttributeError):
        raise RuntimeError("Telegram state is invalid; refusing to risk duplicate sends.")

def save_state(state):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

def telegram_request(method,payload):
    token=os.environ.get("TELEGRAM_BOT_TOKEN","").strip()
    if not token: raise RuntimeError("Missing GitHub Actions Secret: TELEGRAM_BOT_TOKEN")
    req=urllib.request.Request("https://api.telegram.org/bot"+token+"/"+method,
        data=urllib.parse.urlencode(payload).encode("utf-8"),method="POST")
    with urllib.request.urlopen(req,timeout=30) as response:
        result=json.loads(response.read().decode("utf-8"))
    if not result.get("ok"): raise RuntimeError("Telegram API rejected "+method+": "+str(result.get("description","unknown")))
    return result

def send_post(post):
    chat=os.environ.get("TELEGRAM_CHAT_ID","").strip()
    if not chat: raise RuntimeError("Missing GitHub Actions Secret: TELEGRAM_CHAT_ID")
    title=html.escape(post["title"])
    summary=html.escape(post["summary"] or "Open the article to read the full story.")
    link=html.escape(post["link"],quote=True)
    message=f"💎 <b>{title}</b>\n\n{summary}\n\n📖 <a href=\"{link}\">Read the full article</a>\n🌍 <i>{html.escape(post['source'])} · TRTT Voyage</i>"
    if post["image"]:
        try:
            telegram_request("sendPhoto",{"chat_id":chat,"photo":post["image"],
                "caption":message[:1000],"parse_mode":"HTML"})
            return
        except (urllib.error.HTTPError,urllib.error.URLError,RuntimeError):
            pass
    telegram_request("sendMessage",{"chat_id":chat,"text":message[:3900],
        "parse_mode":"HTML","disable_web_page_preview":"false"})

def main():
    state=load_state()
    posts,errors=[],[]
    for name,url in FEEDS:
        try: posts.extend(fetch_feed(name,url))
        except Exception as exc: errors.append(f"{name}: {type(exc).__name__}: {exc}")
    if not posts and errors: raise RuntimeError("All Blogger feeds failed: "+" | ".join(errors))
    if errors: print("Feed warning: "+" | ".join(errors))
    if not state["initialized"]:
        state["sent_ids"]=list(dict.fromkeys(p["id"] for p in posts))[-1000:]
        state["initialized"]=True
        save_state(state)
        print(f"Baseline created for {len(state['sent_ids'])} existing posts; archive not forwarded.")
        return 0
    known=set(state["sent_ids"])
    fresh=[p for p in posts if p["id"] not in known]
    if not fresh:
        print("No new published Blogger posts.")
        return 0
    # Feed order is newest-first; reverse to publish chronologically.
    fresh.reverse()
    sent=[]
    for post in fresh:
        send_post(post)
        sent.append(post["id"])
        print("Telegram delivery confirmed: "+post["title"])
        time.sleep(1)
    state["sent_ids"]=(state["sent_ids"]+sent)[-1000:]
    save_state(state)
    print(f"Forwarded {len(sent)} new published post(s).")
    return 0

if __name__=="__main__":
    try: raise SystemExit(main())
    except Exception as exc:
        print("ERROR: "+str(exc),file=sys.stderr)
        raise SystemExit(1)
