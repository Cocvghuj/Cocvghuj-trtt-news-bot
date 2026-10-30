/**
 * TRTT Auto-Sync Engine v11.0 (FINAL COMPREHENSIVE REPAIR)
 * 1. FIXES BROKEN FOOTER LINK: Automatically cleans up empty href="https://"
 * 2. MOBILE HAMBURGER MENU FIX: Populates .mobile-menu with the 2 core buttons
 * 3. REPLACES ALL VERCEL 404 LINKS: Points to ultra-fast SuperStore on GitHub Pages
 * 4. CLEAN WIDGET HYGIENE: Hides bloated empty widgets to speed up mobile rendering
 * 5. 100% Locked: Marker 787950 | Kiwitaxi tIZcbMOB | Amazon 4shg6Hn
 */
(function() {
  const CONFIG = {
    MARKER: '787950',
    PIN: '7879',
    BLOG_NAME: 'trttnews24bd',
    SUPERSTORE_URL: 'https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/?marker=787950&sub_id=master_787950',
    BLOG_URL: 'https://trttnews24bd.blogspot.com',
    GUIDE_URL: 'https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/blog/ultimate-europe-travel-guide-2026.html',
    FLIGHTSCOUT: 'https://flightscoutpro.blogspot.com/',
    AMAZON: 'https://amzn.to/4shg6Hn',
    FEATURE_IMAGE: 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhGIViEQzbsyK0KHWtYnl1bHbRrSKjX8XbeHyFU5kHlX4BSbwjV2mcy-K7bj_NuhPDzDojIZNzU5nzA1aVukNypAcOmzauPyTPSYYg72wWw8jmnegjxVCLBagh3-uyl7eyQK6oy9nnbWEMcVloAd88diVqPO8uw-zl7g7ey5HWzeLJ5KujfrxleCR5Hjvs/s1600/Photos.jpg'
  };

  // 1. Repair Broken URLs & Replace Vercel Links
  function repairAllLinks() {
    // Fix empty href="https://" or broken links
    document.querySelectorAll('a[href="https://"], a[href="https:///"], a[href="http://"]').forEach(a => {
      a.href = 'javascript:void(0)';
      a.style.cursor = 'default';
      a.removeAttribute('target');
    });

    // Replace all Vercel links with guaranteed 100% SuperStore URL
    document.querySelectorAll('a[href*="cocvghuj-trtt-news-bot.vercel.app"]').forEach(a => {
      a.href = CONFIG.SUPERSTORE_URL;
      a.target = '_blank';
      a.rel = 'noopener';
    });
  }

  // 2. Fix Mobile Menu Drawer (Populates .mobile-menu if empty)
  function fixMobileDrawer() {
    const mobMenu = document.querySelector('.mobile-menu');
    if (mobMenu && !mobMenu.hasAttribute('data-trtt-mobile')) {
      mobMenu.setAttribute('data-trtt-mobile', 'v11');
      mobMenu.innerHTML = `
        <ul style="list-style:none; padding:15px; margin:0;">
          <li style="margin-bottom:10px;">
            <a href="${CONFIG.BLOG_URL}" style="display:block; background:#f1f5f9; color:#052962; padding:12px 16px; border-radius:10px; font-weight:800; text-decoration:none; border:1px solid #cbd5e1;">
              📖 Read The Blog
            </a>
          </li>
          <li style="margin-bottom:10px;">
            <a href="${CONFIG.SUPERSTORE_URL}" target="_blank" rel="noopener" style="display:block; background:#052962; color:#ffffff; padding:12px 16px; border-radius:10px; font-weight:800; text-decoration:none; box-shadow:0 4px 10px rgba(5,41,98,0.25);">
              🚀 Explore Your Life (SuperStore)
            </a>
          </li>
          <li>
            <a href="${CONFIG.GUIDE_URL}" style="display:block; background:#00A8E8; color:#ffffff; padding:12px 16px; border-radius:10px; font-weight:800; text-decoration:none;">
              🌟 Europe Travel Masterguide
            </a>
          </li>
        </ul>
      `;
    }
  }

  // 3. Enforce 2 Menus in Main Navigation
  function enforce2Menus() {
    const navs = document.querySelectorAll('#main-menu-nav, .main-menu ul, #navigation ul, .nav-menu');
    if (!navs.length) return;

    const twoMenusHtml = `
      <li class="menu-item trtt-keep-2" style="display:inline-block !important; margin-right:8px !important;">
        <a href="${CONFIG.BLOG_URL}" role="menuitem" 
           style="display:inline-flex !important; align-items:center !important; gap:6px !important; font-weight:800 !important; font-size:14px !important; color:#052962 !important; padding:10px 18px !important; border-radius:8px !important; text-decoration:none !important; background:#f1f5f9 !important; border:1px solid #cbd5e1 !important;">
          <span>📖</span> <span>Read The Blog</span>
        </a>
      </li>
      <li class="menu-item trtt-keep-2" style="display:inline-block !important;">
        <a href="${CONFIG.SUPERSTORE_URL}" role="menuitem" target="_blank" rel="noopener"
           style="display:inline-flex !important; align-items:center !important; gap:6px !important; font-weight:800 !important; font-size:14px !important; color:#ffffff !important; padding:10px 18px !important; border-radius:8px !important; text-decoration:none !important; background:#052962 !important; box-shadow:0 2px 6px rgba(5,41,98,0.25) !important;">
          <span>🚀</span> <span>Explore Your Life (SuperStore)</span>
        </a>
      </li>
    `;

    navs.forEach(nav => {
      if (nav.getAttribute('data-trtt-locked') === 'v11') return;
      nav.setAttribute('data-trtt-locked', 'v11');
      nav.innerHTML = twoMenusHtml;
    });
  }

  // 4. Inject Masterguide with Image and Working Links
  function injectMasterguideWithImage() {
    if (document.getElementById('trtt-direct-masterguide-post-v11')) return;

    const grid = document.querySelector('.grid-posts, .blog-posts, #Blog1');
    if (!grid) return;

    const postCard = document.createElement('div');
    postCard.id = 'trtt-direct-masterguide-post-v11';
    postCard.className = 'blog-post hentry index-post';
    postCard.style.cssText = 'background:#ffffff !important; border:2px solid #00A8E8 !important; border-radius:18px !important; padding:22px !important; margin-bottom:30px !important; box-shadow:0 10px 30px rgba(0,168,232,0.14) !important; width:100% !important; box-sizing:border-box !important;';

    postCard.innerHTML = `
      <div style="font-family:system-ui,-apple-system,sans-serif;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:14px;">
          <span style="background:#f59e0b; color:#0f172a; font-size:11px; font-weight:900; padding:4px 12px; border-radius:9999px; text-transform:uppercase;">
            🌟 Google SEO Authority Masterguide • FlightScoutPro × TRTT
          </span>
          <span style="font-size:11px; color:#0369a1; font-weight:bold; background:#e0f2fe; padding:3px 10px; border-radius:6px;">
            🔒 Marker ${CONFIG.MARKER} Locked
          </span>
        </div>

        <div style="position:relative; border-radius:14px; overflow:hidden; margin-bottom:18px; max-height:380px; border:1px solid #e2e8f0; background:#052962;">
          <a href="${CONFIG.GUIDE_URL}">
            <img src="${CONFIG.FEATURE_IMAGE}" alt="Qatar Carriage Job Logistics - Real Travel Experience by TRTT" 
                 style="width:100%; height:auto; max-height:380px; object-fit:cover; display:block; transition:transform 0.3s ease;" 
                 onmouseover="this.style.transform='scale(1.02)'" onmouseout="this.style.transform='scale(1)'" />
          </a>
          <div style="position:absolute; bottom:0; left:0; right:0; background:linear-gradient(to top, rgba(5,41,98,0.95), transparent); padding:16px; color:#ffffff;">
            <span style="font-size:11px; font-weight:800; background:#00A8E8; color:#ffffff; padding:2px 8px; border-radius:4px; text-transform:uppercase;">Real Qatar Carriage Photo</span>
            <span style="font-size:12px; margin-left:8px; color:#cbd5e1;">White shirt, mask, gloves &amp; POS machine experience</span>
          </div>
        </div>

        <h2 style="font-size:22px; font-weight:900; color:#052962; margin:0 0 10px 0; line-height:1.35;">
          <a href="${CONFIG.GUIDE_URL}" style="color:#052962; text-decoration:none;">
            The Ultimate 2026-2027 Europe Travel Masterguide: Cheap Flights, 600€ AirHelp Claims, 5G eSIMs &amp; Ground Transits
          </a>
        </h2>

        <p style="font-size:13.5px; line-height:1.75; color:#475569; margin:0 0 16px 0;">
          Jointly published with <strong><a href="${CONFIG.FLIGHTSCOUT}" target="_blank" style="color:#0284c7; font-weight:bold;">FlightScoutPro</a></strong>. Real-world insights from Qatar carriage logistics: save 50% on airfares via Aviasales, claim up to 600€ for delayed European flights under EC 261, deploy instant 5G eSIMs with Airalo &amp; Saily, and book fixed-price Kiwitaxi airport rides.
        </p>

        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(190px, 1fr)); gap:10px; margin-bottom:16px;">
          <a href="https://aviasales.tp.st/Fb8U9yav?marker=${CONFIG.MARKER}&sub_id=direct_aviasales_787950" target="_blank" rel="noopener"
             style="background:#f0f9ff; border:1px solid #bae6fd; border-radius:10px; padding:10px 14px; text-decoration:none; color:#0369a1; font-weight:bold; font-size:12.5px; display:flex; align-items:center; justify-content:space-between;">
            <span>✈️ Aviasales Flights</span>
            <span style="font-size:10px; background:#0284c7; color:#fff; padding:2px 6px; border-radius:4px;">Lowest Fares</span>
          </a>

          <a href="https://airhelp.tp.st/3ItXS0E4?marker=${CONFIG.MARKER}&sub_id=direct_airhelp_787950" target="_blank" rel="noopener"
             style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:10px; padding:10px 14px; text-decoration:none; color:#1d4ed8; font-weight:bold; font-size:12.5px; display:flex; align-items:center; justify-content:space-between;">
            <span>🛡️ AirHelp 600€ Claim</span>
            <span style="font-size:10px; background:#2563eb; color:#fff; padding:2px 6px; border-radius:4px;">EC 261</span>
          </a>

          <a href="https://airalo.tp.st/ZZoQC7Mz?marker=${CONFIG.MARKER}&sub_id=direct_airalo_787950" target="_blank" rel="noopener"
             style="background:#faf5ff; border:1px solid #e9d5ff; border-radius:10px; padding:10px 14px; text-decoration:none; color:#7e22ce; font-weight:bold; font-size:12.5px; display:flex; align-items:center; justify-content:space-between;">
            <span>📱 Airalo 5G eSIM</span>
            <span style="font-size:10px; background:#9333ea; color:#fff; padding:2px 6px; border-radius:4px;">Instant QR</span>
          </a>

          <a href="https://kiwitaxi.tp.st/tIZcbMOB?marker=${CONFIG.MARKER}&sub_id=direct_kiwitaxi_787950" target="_blank" rel="noopener"
             style="background:#ecfdf5; border:1px solid #a7f3d0; border-radius:10px; padding:10px 14px; text-decoration:none; color:#047857; font-weight:bold; font-size:12.5px; display:flex; align-items:center; justify-content:space-between;">
            <span>🚖 Kiwitaxi Fixed Ride</span>
            <span style="font-size:10px; background:#059669; color:#fff; padding:2px 6px; border-radius:4px;">tIZcbMOB</span>
          </a>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; border-top:1px solid #f1f5f9; padding-top:14px;">
          <div style="font-size:12px; color:#64748b;">
            <span>🏪 SuperStore: <a href="${CONFIG.SUPERSTORE_URL}" target="_blank" style="color:#0284c7; font-weight:bold; text-decoration:underline;">21 Tools Active</a></span>
            <span style="margin:0 6px;">•</span>
            <a href="${CONFIG.AMAZON}" target="_blank" style="color:#92400e; font-weight:bold;">🎒 Amazon 4shg6Hn</a>
          </div>
          <div style="display:flex; gap:8px;">
            <a href="${CONFIG.SUPERSTORE_URL}" target="_blank" rel="noopener"
               style="background:#052962; color:#ffffff; font-weight:800; font-size:13px; padding:8px 16px; border-radius:8px; text-decoration:none; display:inline-flex; align-items:center; gap:6px;">
              <span>🚀 Open SuperStore &rarr;</span>
            </a>
          </div>
        </div>
      </div>
    `;

    grid.insertBefore(postCard, grid.firstChild);
  }

  // 5. Link Hygiene
  function enforceLinks() {
    repairAllLinks();
    fixMobileDrawer();

    document.querySelectorAll('a[href*="tp.st"], a[href*="tpo.lv"]').forEach(a => {
      try {
        let href = a.href.replace(/tpo\.lv/g, 'tp.st');
        const u = new URL(href);
        if (!u.searchParams.has('marker') || u.searchParams.get('marker') !== CONFIG.MARKER) {
          u.searchParams.set('marker', CONFIG.MARKER);
        }
        let fixedHref = u.toString().replace(/tlZcbMOB/g, 'tIZcbMOB');
        a.href = fixedHref;
      } catch (e) {}
    });

    document.querySelectorAll('a[href*="amzn.to"]').forEach(a => {
      if (!a.href.includes('4shg6Hn')) {
        a.href = CONFIG.AMAZON;
      }
    });
  }

  function loop() {
    repairAllLinks();
    fixMobileDrawer();
    enforce2Menus();
    injectMasterguideWithImage();
    enforceLinks();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loop);
  } else {
    loop();
  }

  setInterval(loop, 400);
})();
// ai.js - Full Auto OpenRouter - No need to touch index.html HTML
const OPENROUTER_KEY = "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";
const MODEL = "nvidia/nemotron-3.5-lightning:free";

(function() {
  // Auto create UI without touching HTML
  const style = document.createElement('style');
  style.innerHTML = `#ai-box{position:fixed;bottom:20px;right:20px;z-index:99999;display:flex;gap:5px}#ai-input{padding:12px;width:220px;border-radius:25px;border:1px solid #ccc;box-shadow:0 2px 10px rgba(0,0,0,0.1)}#ai-btn{padding:12px 18px;border-radius:25px;background:#000;color:#fff;border:none;cursor:pointer}#ai-output{position:fixed;bottom:80px;right:20px;width:300px;max-height:400px;overflow-y:auto;padding:15px;background:#fff;border-radius:15px;box-shadow:0 5px 20px rgba(0,0,0,0.2);display:none;z-index:99999;font-family:sans-serif;font-size:14px;line-height:1.5}`;
  document.head.appendChild(style);

  const box = document.createElement('div');
  box.id = 'ai-box';
  box.innerHTML = `<input id="ai-input" placeholder="কোথায় যাবে? লিখো..."><button id="ai-btn">Go</button>`;
  document.body.appendChild(box);

  const output = document.createElement('div');
  output.id = 'ai-output';
  document.body.appendChild(output);

  async function autoGenerate() {
    const input = document.getElementById('ai-input');
    const prompt = input.value.trim();
    if(!prompt) return;
    
    output.style.display = "block";
    output.innerHTML = "AI লিখছে... ✈️ একটু অপেক্ষা করো...";

    try {
      const res = await fetch("https://openrouter.ai/api/v1/chat/completions", {
        method: "POST",
        headers: {
          "Authorization": "Bearer " + OPENROUTER_KEY,
          "Content-Type": "application/json",
          "HTTP-Referer": "https://cocvghuj.github.io",
          "X-Title": "Trtr Travel"
        },
        body: JSON.stringify({
          model: MODEL,
          messages: [
            { role: "system", content: "You are a Europe travel expert. Answer in simple Bengali+English mix, short, helpful, give flight/hotel tips." },
            { role: "user", content: prompt }
          ]
        })
      });
      const data = await res.json();
      if(data.error) throw new Error(data.error.message);
      output.innerHTML = data.choices[0].message.content.replace(/\n/g, "<br>");
    } catch(e) {
      output.innerHTML = "Error: " + e.message + "<br>Key টা ঠিক আছে কিনা দেখো।";
    }
  }

  document.getElementById('ai-btn').addEventListener('click', autoGenerate);
  document.getElementById('ai-input').addEventListener('keypress', (e) => { if(e.key === 'Enter') autoGenerate(); });
})();
