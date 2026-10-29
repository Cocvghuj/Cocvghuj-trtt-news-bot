/**
 * TRTT Auto-Sync Engine v5.0 (LIVE DIRECT INJECTOR)
 * Auto-injects the Ultimate Travel Guide directly on top of the blog posts list
 * Marker: 787950 Locked | Typo: tIZcbMOB Fixed (Capital I) | Amazon: 4shg6Hn
 * FlightScoutPro + TRTT News 24 BD + GitHub Ecosystem
 */
(function() {
  const CONFIG = {
    MARKER: '787950',
    AMAZON: 'https://amzn.to/4shg6Hn',
    GITHUB_REPO: 'https://github.com/Cocvghuj/Cocvghuj-trtt-news-bot',
    GUIDE_URL: 'https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/blog/ultimate-europe-travel-guide-2026.html',
    FLIGHTSCOUT: 'https://flightscoutpro.blogspot.com/',
    BLOG_URL: 'https://trttnews24bd.blogspot.com',
    VERCEL_URL: 'https://cocvghuj-trtt-news-bot.vercel.app/?marker=787950&sub_id=explore_life_787950'
  };

  // 1. Enforce 2 Menus (Read The Blog + Explore Your Life)
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
        <a href="${CONFIG.VERCEL_URL}" role="menuitem" target="_blank" rel="noopener"
           style="display:inline-flex !important; align-items:center !important; gap:6px !important; font-weight:800 !important; font-size:14px !important; color:#ffffff !important; padding:10px 18px !important; border-radius:8px !important; text-decoration:none !important; background:#052962 !important; box-shadow:0 2px 6px rgba(5,41,98,0.25) !important;">
          <span>🚀</span> <span>Explore Your Life</span>
        </a>
      </li>
    `;

    navs.forEach(nav => {
      if (nav.getAttribute('data-trtt-locked') === 'v5') return;
      nav.setAttribute('data-trtt-locked', 'v5');
      nav.innerHTML = twoMenusHtml;
    });
  }

  // 2. Directly Inject the Masterguide Card on top of posts
  function injectUltimateMasterguide() {
    if (document.getElementById('trtt-direct-masterguide-post')) return;

    const grid = document.querySelector('.grid-posts, .blog-posts, #Blog1');
    if (!grid) return;

    const postCard = document.createElement('div');
    postCard.id = 'trtt-direct-masterguide-post';
    postCard.className = 'blog-post hentry index-post';
    postCard.style.cssText = 'background:#ffffff !important; border:2px solid #00A8E8 !important; border-radius:16px !important; padding:20px !important; margin-bottom:28px !important; box-shadow:0 8px 25px rgba(0,168,232,0.12) !important; width:100% !important; box-sizing:border-box !important;';

    postCard.innerHTML = `
      <div style="font-family:system-ui,-apple-system,sans-serif;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:12px;">
          <span style="background:#f59e0b; color:#0f172a; font-size:11px; font-weight:900; padding:4px 10px; border-radius:9999px; text-transform:uppercase;">
            🌟 Featured Authority Masterguide • FlightScoutPro × TRTT
          </span>
          <span style="font-size:11px; color:#0369a1; font-weight:bold; background:#e0f2fe; padding:3px 8px; border-radius:6px;">
            🔒 Marker ${CONFIG.MARKER} Locked
          </span>
        </div>

        <h2 style="font-size:22px; font-weight:900; color:#052962; margin:0 0 10px 0; line-height:1.35;">
          <a href="${CONFIG.GUIDE_URL}" style="color:#052962; text-decoration:none;" hover="text-decoration:underline;">
            The Ultimate 2026-2027 Europe Travel Masterguide: Cheap Flights, 600€ AirHelp Claims, 5G eSIMs &amp; Ground Transits
          </a>
        </h2>

        <p style="font-size:13.5px; line-height:1.7; color:#475569; margin:0 0 16px 0;">
          Jointly published with <strong><a href="${CONFIG.FLIGHTSCOUT}" target="_blank" style="color:#0284c7; font-weight:bold;">FlightScoutPro</a></strong>. Real-world insights from Qatar carriage operations into 21 smart travel tools: save 50% on airfares via Aviasales, claim up to 600€ for delayed European flights under EC 261, deploy instant 5G eSIMs with Airalo &amp; Saily, and book fixed-price Kiwitaxi airport rides.
        </p>

        <!-- Tool Highlights Grid -->
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:10px; margin-bottom:16px;">
          <a href="https://aviasales.tp.st/Fb8U9yav?marker=${CONFIG.MARKER}&sub_id=direct_aviasales_787950" target="_blank" rel="noopener"
             style="background:#f0f9ff; border:1px solid #bae6fd; border-radius:10px; padding:10px 14px; text-decoration:none; color:#0369a1; font-weight:bold; font-size:12.5px; display:flex; align-items:center; justify-content:space-between;">
            <span>✈️ Aviasales Flights</span>
            <span style="font-size:10px; background:#0284c7; color:#fff; padding:2px 6px; border-radius:4px;">Low Fares</span>
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

        <!-- Action Links & GitHub details -->
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; border-top:1px solid #f1f5f9; pt-3; padding-top:12px;">
          <div style="font-size:12px; color:#64748b;">
            <span>🐙 GitHub: <a href="${CONFIG.GITHUB_REPO}" target="_blank" style="color:#0284c7; font-weight:bold; text-decoration:underline;">Cocvghuj-trtt-news-bot</a></span>
            <span style="margin:0 6px;">•</span>
            <a href="${CONFIG.AMAZON}" target="_blank" style="color:#92400e; font-weight:bold;">🎒 Amazon 4shg6Hn</a>
          </div>
          <a href="${CONFIG.GUIDE_URL}" 
             style="background:#052962; color:#ffffff; font-weight:800; font-size:13px; padding:8px 18px; border-radius:8px; text-decoration:none; display:inline-flex; align-items:center; gap:6px;">
            <span>Read Full Masterguide &rarr;</span>
          </a>
        </div>
      </div>
    `;

    grid.insertBefore(postCard, grid.firstChild);
  }

  // 3. Strict Link Hygiene
  function enforceLinks() {
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
    enforce2Menus();
    injectUltimateMasterguide();
    enforceLinks();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loop);
  } else {
    loop();
  }

  setInterval(loop, 400);
})();
