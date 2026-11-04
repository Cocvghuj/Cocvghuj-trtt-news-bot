// TRTT VOYAGE FINAL MENU - ALL MENUS INSIDE - ALL TOOLS INSIDE - American Market - No Confusion - Single File
// All previous menus combined: GitHub Style + 3 Dot Golden Animated + Full Screen Overlay + Vercel Inside + Auto Marker 787950 + Telegram + 5 Tools + Extra Tools
// For trttnews24bd.blogspot.com - Final - Based on screenshot

(function(){
  if(window.__TRTT_ALL_MENU_DONE__) return;
  window.__TRTT_ALL_MENU_DONE__ = true;
  
  const CFG = {
    vercel: "https://cocvghuj-trtt-news-bot.vercel.app",
    marker: "787950",
    telegram: "https://t.me/trttnews24bd",
    allMenus: [
      { name: "Dashboard", icon: "📊", link: "#dashboard" },
      { name: "Blog Stories", icon: "📝", link: "#blog", active: true },
      { name: "Flights", icon: "✈️", link: "#flights" },
      { name: "Analytics", icon: "📈", link: "#analytics" },
      { name: "Tracking Logs", icon: "📋", link: "#logs" },
      { name: "Settings", icon: "⚙️", link: "#settings" },
      { name: "Travel Guides", icon: "🗺️", link: "#travel" },
      { name: "Visa Info", icon: "🛂", link: "#visa" },
      { name: "eSIM Store", icon: "📱", link: "#esim" },
      { name: "News", icon: "📰", link: "#news" }
    ],
    allTools: [
      // Core 5 Tools from user
      { id: "flight", name: "Flight Tracker", desc: "New York → Rome • $549 • Biman", price: "$549", badge: "Best Price", icon: "✈️", cat: "Travel" },
      { id: "visa", name: "Visa Checker", desc: "USA → Italy • Visa Free", price: "free", badge: "Free", icon: "🛂", cat: "Travel" },
      { id: "esim", name: "eSIM Comparator", desc: "Italy • $9.99 data plan", price: "$9.99", badge: "Best Price", icon: "📱", cat: "Travel" },
      { id: "cost", name: "Cost Calculator", desc: "7 Days Rome • Est. $1309 total", price: "$1309", badge: "Est.", icon: "🧮", cat: "Travel" },
      { id: "weather", name: "Weather & News", desc: "Live from Europe • Updated now", price: "free", badge: "Live", icon: "⛅", cat: "Travel" },
      // Extra Tools from user list - American biggest market
      { id: "mortgage", name: "Mortgage Calculator", desc: "Home buying calculation", price: "free", badge: "US Market", icon: "🏠", cat: "Calculator" },
      { id: "age", name: "Age Calculator", desc: "Calculate age accurately", price: "free", badge: "Popular", icon: "🎂", cat: "Calculator" },
      { id: "bmi", name: "BMI Calculator", desc: "Body Mass Index", price: "free", badge: "Health", icon: "⚖️", cat: "Calculator" },
      { id: "gpa", name: "GPA Calculator", desc: "Grade Point Average", price: "free", badge: "Student", icon: "🎓", cat: "Calculator" },
      { id: "love", name: "Love Calculator", desc: "American teenagers crazy", price: "free", badge: "Fun", icon: "❤️", cat: "Calculator" },
      { id: "pdf", name: "PDF Tools", desc: "Merge, Split, Compress PDF", price: "free", badge: "Office", icon: "📄", cat: "PDF" },
      { id: "qr", name: "QR Code Generator", desc: "Generate QR for links", price: "free", badge: "Tool", icon: "🔳", cat: "Image" },
      { id: "bgremove", name: "Background Remover", desc: "Remove image background", price: "free", badge: "Image", icon: "🖼️", cat: "Image" },
      { id: "compress", name: "Image Compressor", desc: "Compress images fast", price: "free", badge: "Image", icon: "🗜️", cat: "Image" },
      { id: "thumbnail", name: "YouTube Thumbnail Downloader", desc: "Download YT thumbnails", price: "free", badge: "Video", icon: "🎬", cat: "Image" },
      { id: "myip", name: "What is my IP", desc: "980K searches/month in US", price: "free", badge: "980K/mo", icon: "🌐", cat: "Network" },
      { id: "wordcount", name: "Word Counter", desc: "Count words, chars", price: "free", badge: "Text", icon: "📝", cat: "Text" },
      { id: "plagiarism", name: "Plagiarism Checker", desc: "Check plagiarism", price: "free", badge: "Text", icon: "🔍", cat: "Text" },
      { id: "grammar", name: "Grammar Checker", desc: "After Canva, ChatGPT", price: "free", badge: "Text", icon: "✏️", cat: "Text" }
    ]
  };
  
  function injectCSS(){
    if(document.getElementById("trtt-all-menu-style")) return;
    const s=document.createElement("style"); s.id="trtt-all-menu-style";
    s.textContent=`
      #trtt-all-overlay{position:fixed;inset:0;z-index:2147483647;background:#0a0a12;color:#fff;font-family:Inter,sans-serif;display:none;overflow:auto}
      #trtt-all-overlay.open{display:block;animation:fadeIn .3s}
      @keyframes fadeIn{from{opacity:0}to{opacity:1}}
      .trtt-top{position:sticky;top:0;z-index:2;display:flex;justify-content:space-between;align-items:center;padding:12px 16px;background:linear-gradient(90deg,rgba(212,175,55,.12),rgba(255,46,99,.08));border-bottom:1.5px solid #d4af37;backdrop-filter:blur(12px)}
      .trtt-3dot{display:flex;gap:6px;align-items:center;filter:drop-shadow(0 0 12px gold);animation:pulse 2s infinite}
      @keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.08)}}
      .trtt-dot{width:14px;height:14px;border-radius:50%}.trtt-dot:nth-child(1){background:#ff2e63}.trtt-dot:nth-child(2){background:#FFC300}.trtt-dot:nth-child(3){background:#AF7AC5}
      .trtt-grid{display:grid;grid-template-columns:240px 1fr 380px;gap:14px;padding:14px}
      @media(max-width:1100px){.trtt-grid{grid-template-columns:1fr}}
      .trtt-box{background:#12121c;border:1.5px solid #d4af37;border-radius:14px;padding:12px;box-shadow:0 0 16px rgba(212,175,55,.15)}
      .trtt-nav-item{display:flex;gap:10px;padding:9px 10px;border-radius:10px;margin:5px 0;cursor:pointer;color:#cbd5e1;font-size:12px;font-weight:600}
      .trtt-nav-item.active{background:linear-gradient(90deg,#ff2e63,#FFC300);color:#000}
      .trtt-tool{display:flex;justify-content:space-between;align-items:center;background:#0f0f17;border:1px solid #2a2a3a;border-radius:10px;padding:8px 10px;margin:6px 0}
      .trtt-tool:hover{border-color:#d4af37}
      .trtt-price{background:#FFC300;color:#000;padding:3px 7px;border-radius:7px;font-weight:800;font-size:11px}
      .trtt-select{background:#d4af37;color:#000;border:none;padding:6px 12px;border-radius:8px;font-weight:800;cursor:pointer;font-size:11px}
      .trtt-telegram{display:flex;justify-content:space-between;align-items:center;background:linear-gradient(90deg,#0a84ff,#1e90ff);border-radius:12px;padding:10px 14px;margin:14px;box-shadow:0 6px 20px rgba(10,132,255,.4)}
      #trtt-all-fab{position:fixed;left:12px;bottom:12px;z-index:2147483646;width:56px;height:56px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#FFD86A,#FFC300 45%,#ff2e63 85%);border:2px solid #fff3;box-shadow:0 8px 28px rgba(212,175,55,.6);display:grid;place-items:center;cursor:pointer;animation:pulse 2.5s infinite}
    `;
    document.head.appendChild(s);
  }
  
  function track(){ try{ fetch(CFG.vercel + "/api/vault-click?m=" + CFG.marker + "&t=" + Date.now() + "&src=all_menu_open", {mode:"no-cors", keepalive:true}); }catch(e){} }
  
  function build(){
    if(document.getElementById("trtt-all-overlay")) return;
    const el=document.createElement("div"); el.id="trtt-all-overlay";
    el.innerHTML=`
      <div class="trtt-top">
        <div style="display:flex;gap:10px;align-items:center"><div class="trtt-3dot"><div class="trtt-dot"></div><div class="trtt-dot"></div><div class="trtt-dot" style="width:20px;height:20px"></div></div><div><b style="color:#FFD86A">TRTT VOYAGE</b><div style="font-size:10px;opacity:.6">ALL MENUS • ALL TOOLS INSIDE • FULL-SCREEN</div></div></div>
        <div style="display:flex;gap:8px;align-items:center"><input placeholder="Cmd+K Search all menus & tools..." style="background:#12121c;border:1px solid #2a2a3a;border-radius:10px;padding:8px 12px;color:#fff;width:220px"><div style="background:#0f1f0f;color:#7CFC8A;border:1px solid #2e7d32;padding:6px 10px;border-radius:10px;font-size:11px">📍 Marker Clicked! +1 127→128 • stealth</div><button onclick="document.getElementById('trtt-all-overlay').classList.remove('open')" style="background:#1a1a28;border:1px solid #2a2a3a;color:#fff;width:32px;height:32px;border-radius:8px;cursor:pointer">✕</button></div>
      </div>
      <div class="trtt-grid">
        <div class="trtt-box"><div style="font-size:10px;opacity:.5;margin-bottom:6px">ALL MENUS INSIDE</div>${CFG.allMenus.map(m=>`<div class="trtt-nav-item ${m.active?'active':''}"><span>${m.icon}</span> ${m.name}</div>`).join('')}<div style="margin-top:12px;background:#0f1f0f;border:1px solid #2e7d32;border-radius:8px;padding:8px;font-size:10px;color:#7CFC8A">● Operational 99.99% • System Healthy • v2.4.1 Secure</div></div>
        <div>
          <div class="trtt-box"><b>Blog Stories • Featured</b><div style="height:120px;background:linear-gradient(180deg,rgba(0,0,0,.1),rgba(0,0,0,.6)),url('https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=800') center/cover;border-radius:10px;margin-top:8px;display:flex;align-items:flex-end;padding:10px"><b>Exploring Rome: Hidden Stories & Travel Insights</b></div><p style="font-size:11px;opacity:.7;margin-top:6px">Discover culture, travel guides, insider tips for Americans exploring Italy.</p></div>
          <div class="trtt-box" style="margin-top:12px"><b>Latest Stories</b><div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:8px"><div style="background:#0f0f17;border-radius:8px;padding:8px;font-size:11px"><b>Packing for Italy: 7-Day Essentials</b><br><span style="opacity:.6">2h ago • 4 min</span></div><div style="background:#0f0f17;border-radius:8px;padding:8px;font-size:11px"><b>Visa-Free Travel: What Americans Need</b><br><span style="opacity:.6">1d ago • 6 min</span></div></div></div>
        </div>
        <div class="trtt-box"><div style="display:flex;justify-content:space-between"><b style="font-size:12px">Vercel Deployment</b><span style="font-size:10px;background:#0f1f0f;color:#7CFC8A;padding:3px 6px;border-radius:6px">● Deployed • Ready</span></div><div style="font-weight:800;margin:8px 0">All Tools Inside • ${CFG.allTools.length} Tools</div><div style="font-size:10px;opacity:.6;margin-bottom:8px">All menus & all tools combined - select to start - American market</div><div style="max-height:520px;overflow:auto">${CFG.allTools.map(t=>`<div class="trtt-tool"><div style="display:flex;gap:8px;align-items:center"><div style="width:28px;height:28px;background:#1a1a28;border:1px solid #2a2a3a;border-radius:8px;display:grid;place-items:center">${t.icon}</div><div><div style="font-weight:700;font-size:11px">${t.name}</div><div style="font-size:10px;opacity:.6">${t.desc}</div></div></div><div style="display:flex;gap:6px;align-items:center"><div class="trtt-price">${t.price}</div><button class="trtt-select" onclick="window.open('${CFG.vercel}/tools/${t.id}?m=${CFG.marker}','_blank')">Select →</button></div></div>`).join('')}</div></div>
      </div>
      <div class="trtt-telegram"><div style="display:flex;gap:10px;align-items:center"><div style="width:36px;height:36px;background:#fff;border-radius:50%;display:grid;place-items:center">✈️</div><div><a href="${CFG.telegram}" target="_blank" style="color:#fff;font-weight:800;text-decoration:none">Join our Telegram → t.me/trttnews24bd</a><div style="font-size:10px;opacity:.9">Exclusive for Americans • Join for $99 Deals • Limited Spots • Daily Travel Alerts</div></div></div><button style="background:#FFD86A;color:#000;padding:8px 14px;border-radius:10px;font-weight:800;border:none;cursor:pointer" onclick="window.open('${CFG.telegram}','_blank')">Join for $99 Deals →</button></div>
      <div style="text-align:center;font-size:9px;opacity:.4;padding:6px">TRTT VOYAGE • Secured • Data encrypted • GDPR-compliant • Stealth tracking active • All menus inside • All tools inside • ${CFG.allTools.length} tools</div>
    `;
    document.body.appendChild(el);
  }
  
  function fab(){
    if(document.getElementById("trtt-all-fab")) return;
    const f=document.createElement("div"); f.id="trtt-all-fab"; f.innerHTML="•••"; f.title="Open TRTT Voyage - All Menus Inside";
    f.onclick=()=>{ const ov=document.getElementById("trtt-all-overlay"); if(ov){ ov.classList.add("open"); track(); } };
    document.body.appendChild(f);
  }
  
  function init(){ injectCSS(); build(); fab(); }
  if(document.readyState==="loading"){ document.addEventListener("DOMContentLoaded", init); } else { init(); }
})();
