# TRTT ULTIMATE BEST - Marker 787950 - FCO BGY LIN CAG - Google Rank #1
import random, hashlib, json, os
import config
from datetime import datetime

SEEN_FILE="seen_guidelines.json"

def load_seen():
    if os.path.exists(SEEN_FILE):
        try:
            with open(SEEN_FILE,"r",encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {"titles":[],"hashes":[],"dates":[],"backup_protected":True}

def save_seen(seen):
    # PART- filter - Backup Protected - Marker 787950
    seen["titles"]=[t for t in seen["titles"] if not t.startswith("PART-")][-100:]
    seen["hashes"]=seen["hashes"][-100:]
    seen["dates"]=seen["dates"][-100:]
    with open(SEEN_FILE,"w",encoding="utf-8") as f:
        json.dump(seen,f,ensure_ascii=False,indent=2)

def get_airport():
    try:
        with open("airports.json","r",encoding="utf-8") as f:
            data = json.load(f)
            return random.choice(data) if data else {"code":"FCO","city":"Rome"}
    except:
        return {"code":"FCO","city":"Rome"}

def build_ui(topic):
    ap=get_airport()
    code=ap.get('code','FCO')
    city=ap.get('city','Rome')
    links="".join([f'<a href="{i["url"]}" target="_blank" style="display:inline-block;background:#1e293b;color:#38bdf8;padding:8px 14px;margin:4px;border-radius:20px;text-decoration:none;border:1px solid #334155;">{i["name"]}</a>' for i in config.AFFILIATE_SERVICES])
    table=f"""
    <div style="background:#0f172a;border:1px solid #334155;border-radius:16px;padding:20px;margin:20px 0;">
    <h3 style="color:#38bdf8;margin:0;">💎 Real Value {city} {code} - Marker {config.MARKER}</h3>
    <p style="color:#cbd5e1;font-size:13px;">Airalo ZZoQC7Mz $4.5 Save $15 | Aviasales Fb8U9yav Save $120 | Amazon 4shg6Hn Essential | Tested Sanluri</p>
    </div>
    """
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{topic['title']} - Marker {config.MARKER}</title></head>
<body style="background:#0b0f19;color:#fff;font-family:system-ui;max-width:840px;margin:auto;padding:20px;">
<h1>{topic['title']}</h1>
<p>{topic.get('summary','')}</p>
<p>{topic.get('content','')}</p>
{table}
<div>{links}</div>
<p style="font-size:11px;color:#94a3b8;margin-top:20px;">{datetime.now().year} TRTT • Marker {config.MARKER} • FCO BGY LIN CAG • Backup Safe • ZZoQC7Mz + Fb8U9yav + 4shg6Hn</p>
</body></html>"""

if __name__=="__main__":
    seen=load_seen()
    # Cross Filter - No PART-
    valid_topics = [t for t in config.TOPICS if not t["title"].startswith("PART-")]
    cand=random.choice(valid_topics if valid_topics else config.TOPICS)
    seen["titles"].append(cand["title"])
    seen["hashes"].append(hashlib.md5((cand.get("content","")+cand.get("summary","")).encode()).hexdigest())
    seen["dates"].append(datetime.now().isoformat())
    save_seen(seen)
    html=build_ui(cand)
    for fn in ["latest_travel_news.html","index.html"]:
        with open(fn,"w",encoding="utf-8") as f:
            f.write(html)
    print(f"Built ULTIMATE BEST - Marker {config.MARKER} + ZZoQC7Mz + Fb8U9yav + 4shg6Hn - Backup Safe")
