# TRTT Auto Builder - Google Blogger + Vercel Super App - Marker 787950 Locked
# Via Carlo Felice ARST 08:17 Sanluri - Qatar Carriage Job to Super App
import json, os, datetime

MARKER = "787950"
VERCEL_URL = f"https://cocvghuj-trtt-news-bot.vercel.app/?marker={MARKER}"
# পরে trttsite.com / trttpayout.com কিনলে এখানে Change করবি
# VERCEL_URL = f"https://trttsite.com/?marker={MARKER}"
# VERCEL_URL = f"https://trttpayout.com/?marker={MARKER}"

# তোর News - এখানে লিখ - Auto Blog + Vercel + Money Box
NEWS = [
    {
        "title": "Travel Is Not Touring: I Built 21 Tools in 1 App After Qatar Carriage Job",
        "content": "Qatar 2020 Carriage Job Photo - Mask + Hair Cap + Gloves + POS - From Sanluri Via Carlo Felice ARST 08:17 to Global - 21 Tools in 1 App - Cheap Flights + eSIM + Hotels + Claim",
        "link": VERCEL_URL
    }
]

# Auto Build blog.json - Vercel Super App + Google Blog Same Page
blog_data = {
    "marker": MARKER,
    "vercel_url": VERCEL_URL,
    "money_source": VERCEL_URL,
    "updated": datetime.datetime.now().isoformat(),
    "menus": [
        {"title": "📖 Read The Blog", "url": "https://ttnews24bd.blogspot.com", "type": "blog"},
        {"title": "🚀 Explore Your Life", "url": VERCEL_URL + "&sub_id=blog_menu_explore_787950", "type": "money"}
    ],
    "posts": NEWS,
    "affiliates": {
        "aviasales": f"Fb8U9yav?marker={MARKER}",
        "airhelp": f"3ItXS0E4?marker={MARKER}",
        "airalo": f"ZZoQC7Mz?marker={MARKER}",
        "kiwitaxi": f"tIZcbMOB?marker={MARKER} Fixed from tIZcbMOB",
        "【entity-amazon¦canonical_name=Amazon】": "4shg6Hn"
    }
}

# Save blog.json - GitHub Pages + Vercel Load করবে
os.makedirs("public", exist_ok=True)
with open("public/blog.json", "w", encoding="utf-8") as f:
    json.dump(blog_data, f, indent=2, ensure_ascii=False)

# Auto Build trtt-auto-sync.js - Blogger Gadget Load করবে - Real <a href> - Touch Fixed
js_content = f"""
// TRTT Auto Builder - Google Blog Auto Sync - Marker {MARKER} Locked - Real <a href> - Touch Fixed
(function(){{
  const VERCEL_URL = '{VERCEL_URL}&sub_id=blog_end_money_787950';
  const MARKER = '{MARKER}';
  function injectMoney(){{
    const posts = document.querySelectorAll('.post-body, .entry-content, .post-content, .post');
    posts.forEach(post=>{{
      if(post.querySelector('.trtt-money-source')) return;
      const box = document.createElement('div');
      box.className = 'trtt-money-source';
      box.innerHTML = `<div style="background:linear-gradient(135deg,#FF6B35,#F7931E);border:2px solid #FF6B35;border-radius:12px;padding:15px;margin:20px 0;font-family:system-ui;box-shadow:0 4px 15px rgba(255,107,53,0.3);"><div style="background:rgba(0,0,0,0.15);color:white;padding:5px 10px;border-radius:20px;font-size:10px;display:inline-block;margin-bottom:8px;font-weight:bold;">💰 টাকার উৎস - Marker ${{MARKER}} Locked</div><div style="color:white;font-weight:bold;font-size:14px;margin-bottom:8px;">🚀 Explore Your Life - Full Super App - Flights + Hotels + eSIM + Claim</div><a href="${{VERCEL_URL}}" style="display:block;background:white;color:#FF6B35;padding:14px;border-radius:10px;text-decoration:none;font-weight:bold;text-align:center;font-size:14px;">🚀 Explore Your Life - {VERCEL_URL} - Click Here →</a><div style="color:rgba(255,255,255,0.7);font-size:8px;text-align:center;margin-top:8px;">Real &lt;a href&gt; - Touch Fixed - tp.st?marker={MARKER} - tIZcbMOB Fixed - Amazon 4shg6Hn</div></div>`;
      post.appendChild(box);
    }});
    document.querySelectorAll('a[href*="tp.st"], a[href*="tp.st"]').forEach(a=>{{ try{{ let h=a.href.replace('tp.st','tp.st'); const u=new URL(h); if(!u.searchParams.has('marker')) u.searchParams.set('marker',MARKER); a.href=u.toString().replace(/tIZcbMOB/g,'tIZcbMOB'); }}catch(e){{}} }});
  }}
  injectMoney(); setInterval(injectMoney, 3000);
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', injectMoney);
  window.addEventListener('load', injectMoney);
  console.log('💰 TRTT Auto Builder - Money Source Injected - Marker {MARKER} Locked');
}})();
"""

with open("public/trtt-auto-sync.js", "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"✅ Auto Built - blog.json + trtt-auto-sync.js - Marker {MARKER} Locked - Vercel {VERCEL_URL}")
