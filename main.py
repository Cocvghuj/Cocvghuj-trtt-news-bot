# TRTT FINAL BOSS INTERLINKED - Marker 787950 - FCO BGY LIN CAG - Google Rank #1 - 1 DAY 1 TOPIC
import random, hashlib, json, os, glob, pathlib
import config
from datetime import datetime

SEEN_FILE = "seen_guidelines.json"

def load_seen():
    if os.path.exists(SEEN_FILE):
        try:
            with open(SEEN_FILE,"r",encoding="utf-8") as f:
                data = json.load(f)
                # Ensure all keys
                data.setdefault("titles",[])
                data.setdefault("hashes",[])
                data.setdefault("dates",[])
                return data
        except: pass
    return {"titles":[], "hashes":[], "dates":[], "backup_protected": True}

def save_seen(seen):
    # PART- filter - Backup Protected - Marker 787950 LOCKED - Anti-Piston
    seen["titles"] = [t for t in seen["titles"] if not str(t).startswith("PART-")][-100:]
    seen["hashes"] = seen["hashes"][-100:]
    seen["dates"] = seen["dates"][-100:]
    with open(SEEN_FILE,"w",encoding="utf-8") as f:
        json.dump(seen,f,ensure_ascii=False,indent=2)

def get_airport():
    try:
        with open("airports.json","r",encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list) and data:
                return random.choice(data)
            if isinstance(data, dict):
                return data
    except: pass
    return {"code":"FCO","city":"Rome"}

def build_ui(topic, persona="neighbor_maria"):
    ap = get_airport()
    code = ap.get("code","FCO")
    city = ap.get("city","Rome")
    marker = getattr(config, 'MARKER', '787950')
    
    # ALL ROUTES + AMAZON - 7 Routes - LOCKED with sub_id
    def mk(base, sid): return f"{base}?sub_id={sid}_lock_it_{marker}"
    
    links_map = {
        "avia": mk(f"https://aviasales.tpo.lv/{getattr(config,'AVIA_CODE','Fb8U9yav')}", f"interlinked_avia_{topic['id']}_{persona}"),
        "airalo": mk(f"https://airalo.tpo.lv/{getattr(config,'AIRALO_CODE','ZZoQC7Mz')}", f"interlinked_airalo_{persona}"),
        "saily": mk(f"https://saily.tpo.lv/{getattr(config,'SAILY_CODE','ssekmS4X')}", f"interlinked_saily_{persona}"),
        "yesim": mk(f"https://yesim.tpo.lv/{getattr(config,'YESIM_CODE','krzFKLpg')}", f"interlinked_yesim_{persona}"),
        "drim": mk(f"https://drimsim.tpo.lv/{getattr(config,'DRIM_CODE','Ly7ywIY8')}", f"interlinked_drim_{persona}"),
        "klook": mk(f"https://klook.tpo.lv/{getattr(config,'KLOOK_CODE','TWKnemhz')}", f"interlinked_klook_{persona}"),
        "amazon": mk(f"https://amazon.tpo.lv/{getattr(config,'AMAZON_CODE','4shg6Hn')}", f"interlinked_amazon_{topic['id']}_{persona}"),
        "airhelp": mk(f"https://airhelp.tpo.lv/{getattr(config,'AIRHELP_CODE','3ItXS0E4')}", f"interlinked_help_{persona}"),
        "gettrans": mk(f"https://gettransfer.tpo.lv/{getattr(config,'GETTRANS_CODE','1u8zRU5s')}", f"interlinked_gett_{persona}"),
        "hub": f"https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/?sub_id=interlinked_hub_{topic['id']}_{persona}_lock_it_{marker}"
    }

    # INTERLINKED - Read previous 6 posts
    prev_posts = sorted(glob.glob("posts/*.html"), reverse=True)[:6]
    interlinks = ""
    for pp in prev_posts:
        name = pathlib.Path(pp).stem.replace('-',' ')[:60]
        interlinks += f'<li><a href="https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/{pp}" style="color:#0d2a6f">↗ {name}</a></li>'

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{topic['title']} - Marker {marker}</title></head>
<body style="background:#0b0f19;color:#fff;font-family:system-ui;max-width:840px;margin:auto;padding:20px">
<h1 style="color:#38bdf8">{topic['title']} - 1 Day 1 Topic - Interlinked</h1>
<p style="color:#cbd5e1">{topic.get('summary','')}</p>
<div style="background:#0f172a;border:1px solid #334155;border-radius:16px;padding:20px;margin:20px 0">
<h3 style="color:#38bdf8;margin:0;">💎 Real Value {city} ({code}) - Marker {marker} - {persona}</h3>
<p style="color:#cbd5e1;font-size:13px;">Airalo {links_map['airalo']} $4.5 Save $15 | Aviasales {links_map['avia']} Save $120 | Amazon {links_map['amazon']} | All 7 Routes + Amazon Included</p>
<p style="color:#94a3b8;font-size:12px">Route: Sanluri Via Carlo Felice 08:17 ARST 5 Euro → Cagliari Elmas → Rome 19 Euro → Milan 24 Euro → Venice 29 Euro → Amazon Gear</p>
</div>
<p>{topic.get('content','')}</p>
<div style="background:#eef6ff;color:#111;padding:18px;border-radius:10px;margin:20px 0">
<h3>🔗 INTERLINKED NEWS - Every News Connected - Better than Piston Guy</h3>
<ul>{interlinks if interlinks else '<li>First post - No previous - Next will link this!</li>'}</ul>
</div>
<div style="text-align:center;margin:20px 0">
<a onclick="window.open('{links_map['hub']}','_blank'); window.open('{links_map['avia']}','_blank'); return false;" href="{links_map['avia']}" style="display:inline-block;padding:14px 28px;background:#febb02;color:#000;text-decoration:none;border-radius:10px;font-weight:900">Magic 1 Click 2 Tabs - Check {city} Live + Hub - {marker} LOCKED</a>
</div>
<p style="font-size:11px;color:#94a3b8">{datetime.now().year} TRTT - Marker {marker} - FCO BGY LIN CAG - Interlinked - All Routes + Amazon - sub_id trtt_lock_it_{marker}</p>
</body></html>"""
    return html

if __name__ == "__main__":
    seen = load_seen()
    # Cross Filter - No PART- - No Duplicate
    valid_topics = [t for t in config.TOPICS if not str(t.get('title','')).startswith("PART-")]
    # Avoid seen hashes
    candidates = [t for t in valid_topics if t.get('title') not in seen["titles"]]
    if not candidates:
        candidates = valid_topics if valid_topics else config.TOPICS
    cand = random.choice(candidates)
    # Add ID if missing
    cand.setdefault('id', f"topic_{datetime.now().strftime('%A').lower()}")
    
    seen["titles"].append(cand["title"])
    seen["hashes"].append(hashlib.md5((cand.get("content","")+cand.get("summary","")).encode()).hexdigest())
    seen["dates"].append(datetime.now().isoformat())
    save_seen(seen)
    
    html = build_ui(cand, persona=os.getenv('PERSONA','neighbor_maria'))
    
    # Save to posts/ for Interlinked SEO + latest + index
    pathlib.Path("posts").mkdir(exist_ok=True)
    date_str = datetime.now().strftime('%Y-%m-%d')
    post_path = f"posts/{date_str}-INTERLINKED-{cand['id']}.html"
    for fn in [post_path, "latest_travel_news.html", "index.html"]:
        with open(fn,"w",encoding="utf-8") as f:
            f.write(html)
    
    print(f"Built ULTIMATE INTERLINKED - Marker {config.MARKER} - ZZoQC7Mz - Fb8U9yav - 4shg6Hn - All Routes + Amazon - {post_path}")
