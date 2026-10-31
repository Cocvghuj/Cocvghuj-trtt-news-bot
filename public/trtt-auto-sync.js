/**
 * TRTT Enterprise Auto-Sync Engine v17.0 (WORLD-CLASS LUXURY BLOG ARCHITECTURE)
 * 
 * 1. MODERN SILICON VALLEY MAGAZINE DESIGN:
 *    - Injects global luxury typography, smooth gradients, and glassmorphic cards.
 *    - Cleans up cluttered default Blogger layout with high-end responsive styling.
 * 2. HERO SHOWCASE WITH 3D VISION & SPEED:
 *    - Modern Featured Hero Card with dynamic 3D tilt and Conic Gradient border.
 *    - 3x3 Pixel Grid with authentic boutique & travel imagery.
 * 3. 1-CLICK INSTANT BOOKING BAR:
 *    - Flights (Aviasales), 600€ Cash (AirHelp), 5G eSIM (Airalo/Saily), Transfers (Kiwitaxi).
 * 4. 100% GOOGLE E-E-A-T & SPAM IMMUNITY:
 *    - rel="sponsored nofollow noopener" on all monetized links.
 *    - Marker 787950 • Kiwitaxi tIZcbMOB • subid=trtt_lock_{country_code}.
 *    - WebP + loading="lazy" + decoding="async" for Core Web Vitals.
 */
(function() {
  const CONFIG = {
    MARKER: '787950',
    PIN: '7879',
    BLOG_NAME: 'trttnews24bd',
    SUPERSTORE_URL: 'https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/?marker=787950',
    ROKSANA_FINAL: 'https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/roksana-boutique-final.html',
    ROKSANA_STORE: 'https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/roksana-nila-cloths-store.html',
    GUIDE_URL: 'https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/blog/ultimate-europe-travel-guide-2026.html',
    BLOG_URL: 'https://trttnews24bd.blogspot.com',
    GITHUB_REPO: 'https://github.com/Cocvghuj/Cocvghuj-trtt-news-bot',
    HERO_IMAGE: 'https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=1200&q=80',
    QATAR_PHOTO: 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhGIViEQzbsyK0KHWtYnl1bHbRrSKjX8XbeHyFU5kHlX4BSbwjV2mcy-K7bj_NuhPDzDojIZNzU5nzA1aVukNypAcOmzauPyTPSYYg72wWw8jmnegjxVCLBagh3-uyl7eyQK6oy9nnbWEMcVloAd88diVqPO8uw-zl7g7ey5HWzeLJ5KujfrxleCR5Hjvs/w600-rw/Photos.webp'
  };

  let userCountry = 'it';

  // 1. Inject World-Class Magazine CSS into Blogger
  function injectLuxuryStyling() {
    if (document.getElementById('trtt-luxury-style-v17')) return;
    const style = document.createElement('style');
    style.id = 'trtt-luxury-style-v17';
    style.innerHTML = `
      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap');

      /* Global Modern Layout Polish */
      body {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        background-color: #f8fafc !important;
        color: #0f172a !important;
        line-height: 1.7 !important;
      }

      /* Clean Navigation Bar */
      #main-menu-nav, .main-menu {
        background: rgba(5, 41, 98, 0.98) !important;
        backdrop-filter: blur(12px) !important;
        padding: 6px 12px !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 20px rgba(5, 41, 98, 0.15) !important;
      }

      /* Luxury Hero Card */
      .trtt-hero-container {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 24px;
        padding: 24px;
        margin-bottom: 32px;
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.05);
      }

      /* 3D Vision Roksana Floating Card */
      .roksana-img-card {
        position: relative;
        border-radius: 20px;
        padding: 3px;
        background: conic-gradient(from 0deg, #FFD700, #FF6B6B, #7F5EFF, #00D26A, #FFD700);
        box-shadow: 0 16px 45px rgba(0,0,0,0.25), 0 0 0 1px rgba(255,215,0,0.2);
        transition: all 0.5s cubic-bezier(0.23,1,0.32,1);
        animation: roksanaFloat 6s ease-in-out infinite;
      }
      .roksana-img-card:hover {
        transform: perspective(1000px) rotateY(0deg) rotateX(0deg) translateY(-6px) scale(1.02) !important;
        box-shadow: 0 25px 60px rgba(0,0,0,0.35), 0 0 0 2px #FFD700;
        z-index: 10;
      }
      .roksana-img-card img {
        width: 100%;
        height: auto;
        border-radius: 17px;
        object-fit: cover;
        display: block;
      }
      @keyframes roksanaFloat {
        0%,100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
      }

      .upvote-badge {
        position: absolute;
        top: -6px;
        right: -6px;
        background: #FF4500;
        color: #fff;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 10px;
        font-weight: 800;
        box-shadow: 0 4px 12px rgba(255,69,0,0.4);
        display: flex;
        align-items: center;
        gap: 4px;
        z-index: 20;
      }

      /* Booking Pill Action Buttons */
      .booking-pill {
        transition: transform 0.2s ease, box-shadow 0.2s ease;
      }
      .booking-pill:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.08);
      }
    `;
    document.head.appendChild(style);
  }

  // Detect Country Code via IP
  function detectCountry() {
    try {
      fetch('https://ipapi.co/json/')
        .then(res => res.json())
        .then(data => {
          if (data && data.country_code) {
            userCountry = data.country_code.toLowerCase();
            enforceGoogleCompliantLinks();
          }
        })
        .catch(() => {});
    } catch(e) {}
  }

  // Strict URL Tracker
  function getTrackedUrl(rawUrl, category) {
    if (!rawUrl) return rawUrl;
    let clean = rawUrl.replace(/tpo\.lv/g, 'tp.st').replace(/tlZcbMOB/g, 'tIZcbMOB');
    try {
      const u = new URL(clean);
      u.searchParams.set('marker', CONFIG.MARKER);
      u.searchParams.set('subid', 'trtt_lock_' + userCountry);
      u.searchParams.set('utm_source', (category || 'plane') + '_' + userCountry);
      u.searchParams.set('utm_medium', 'affiliate');
      if (clean.includes('tIZcbMOB') && !u.searchParams.has('promo_id')) {
        u.searchParams.set('promo_id', '4558');
      }
      return u.toString();
    } catch(e) {
      return clean;
    }
  }

  // Google Compliance & Performance Optimizer (WebP, Lazy, Async, Alt)
  function enforceGoogleCompliantLinks() {
    document.querySelectorAll('img').forEach(img => {
      if (!img.hasAttribute('loading')) img.setAttribute('loading', 'lazy');
      if (!img.hasAttribute('decoding')) img.setAttribute('decoding', 'async');
      if (!img.hasAttribute('alt') || img.getAttribute('alt').trim() === '') {
        img.setAttribute('alt', 'TRTT Verified Europe Travel & Logistics Guide');
      }
    });

    // Enforce rel="sponsored nofollow noopener"
    document.querySelectorAll('a[href*="tp.st"], a[href*="tpo.lv"], a[href*="amzn.to"]').forEach(a => {
      a.setAttribute('rel', 'sponsored nofollow noopener');
      a.setAttribute('target', '_blank');

      let cat = 'plane';
      if (a.href.includes('airhelp')) cat = 'claim';
      else if (a.href.includes('airalo') || a.href.includes('saily') || a.href.includes('yesim') || a.href.includes('drimsim')) cat = 'esim';
      else if (a.href.includes('kiwitaxi')) cat = 'taxi';
      else if (a.href.includes('trip.com') || a.href.includes('h3LrTZcS')) cat = 'hotel';
      else if (a.href.includes('tiqets') || a.href.includes('bnx8pnF6')) cat = 'ticket';
      else if (a.href.includes('amzn.to')) cat = 'gear';

      if (a.href.includes('amzn.to')) {
        if (!a.href.includes('4shg6Hn')) {
          a.href = 'https://amzn.to/4shg6Hn?marker=' + CONFIG.MARKER + '&subid=trtt_lock_' + userCountry;
        }
      } else {
        a.href = getTrackedUrl(a.href, cat);
      }
    });

    // Fix empty hrefs
    document.querySelectorAll('a[href="https://"], a[href="https:///"]').forEach(a => {
      a.href = 'javascript:void(0)';
      a.style.cursor = 'default';
    });

    // Replace old Vercel links
    document.querySelectorAll('a[href*="cocvghuj-trtt-news-bot.vercel.app"]').forEach(a => {
      a.href = CONFIG.SUPERSTORE_URL;
      a.setAttribute('target', '_blank');
      a.setAttribute('rel', 'noopener');
    });
  }

  // GDPR Cookie Banner
  function renderGDPRBanner() {
    if (localStorage.getItem('trtt_cookie_consent_esim') === 'accepted') return;
    if (document.getElementById('trtt-gdpr-banner')) return;

    const banner = document.createElement('div');
    banner.id = 'trtt-gdpr-banner';
    banner.style.cssText = `
      position: fixed; bottom: 0; left: 0; right: 0; z-index: 999999;
      background: #052962; color: #ffffff; padding: 14px 20px;
      box-shadow: 0 -4px 25px rgba(0,0,0,0.3); border-top: 2px solid #00A8E8;
      font-family: system-ui, -apple-system, sans-serif; font-size: 12px;
      display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;
    `;
    banner.innerHTML = `
      <div style="max-width: 780px; line-height: 1.5;">
        <strong>🍪 Google Search Transparency &amp; Cookie Notice:</strong>
        TRTT News 24 BD participates in verified travel affiliate programs (Aviasales, Airalo, Kiwitaxi, Amazon) under <strong>Marker ${CONFIG.MARKER}</strong>. 100% Compliant with EU GDPR &amp; Italian Privacy Laws.
      </div>
      <div style="display:flex; gap:8px; align-items:center;">
        <a href="https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/privacy.html" target="_blank" style="color: #93c5fd; text-decoration: underline; font-size: 11px;">Privacy Policy</a>
        <button id="trtt-accept-cookie" style="background: #f59e0b; color: #0f172a; font-weight: 800; border: none; padding: 7px 16px; border-radius: 6px; cursor: pointer; font-size: 11px;">
          Accept &amp; Continue
        </button>
      </div>
    `;
    document.body.appendChild(banner);

    document.getElementById('trtt-accept-cookie')?.addEventListener('click', function() {
      localStorage.setItem('trtt_cookie_consent_esim', 'accepted');
      banner.style.display = 'none';
    });
  }

  // Clean Navigation Bar
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
      if (nav.getAttribute('data-trtt-locked') === 'v17') return;
      nav.setAttribute('data-trtt-locked', 'v17');
      nav.innerHTML = twoMenusHtml;
    });
  }

  // 2. Inject Luxury Silicon Valley Hero Showcase on Top of Blog
  function injectLuxuryHero() {
    if (document.getElementById('trtt-luxury-hero-v17')) return;

    const grid = document.querySelector('.grid-posts, .blog-posts, #Blog1');
    if (!grid) return;

    const hero = document.createElement('div');
    hero.id = 'trtt-luxury-hero-v17';
    hero.className = 'blog-post hentry index-post trtt-hero-container';

    hero.innerHTML = `
      <!-- Top Luxury Badge Bar -->
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:18px;">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="background:#052962; color:#ffffff; font-size:11px; font-weight:900; padding:4px 12px; border-radius:9999px; text-transform:uppercase; letter-spacing:0.5px;">
            💎 Official Travel Intelligence Bureau
          </span>
          <span style="background:#fef3c7; color:#92400e; font-size:11px; font-weight:800; padding:4px 10px; border-radius:6px;">
            FlightScoutPro Verified
          </span>
        </div>
        <div style="font-family:'JetBrains Mono', monospace; font-size:11px; color:#64748b;">
          <span>● Sanluri 39.5613,8.6332</span> • <span>Dhaka 23.8103</span>
        </div>
      </div>

      <!-- Main Showcase Grid (Editorial + 3D Card) -->
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(290px, 1fr)); gap:24px; align-items:center; margin-bottom:24px;">
        
        <!-- Left Editorial Details -->
        <div style="space-y:14px;">
          <h1 style="font-size:26px; font-weight:900; color:#052962; margin:0 0 10px 0; line-height:1.25;">
            TRTT VoyageHub: European Flight Logistics, Passenger Rights &amp; 5G Connectivity (2026-2027)
          </h1>
          <p style="font-size:14px; color:#475569; margin:0 0 16px 0; line-height:1.75;">
            Built with authentic ground handling field expertise. Discover secret airline layovers, legally claim up to <strong>600€ for flight delays under EC 261</strong>, deploy instant 5G travel eSIMs, and eliminate airport taxi surge pricing.
          </p>

          <!-- Quick 4-Pillar Booking Row -->
          <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(130px, 1fr)); gap:8px; margin-bottom:16px;">
            <a href="${getTrackedUrl('https://aviasales.tp.st/Fb8U9yav', 'plane')}" target="_blank" rel="sponsored nofollow noopener"
               class="booking-pill" style="background:#f0f9ff; border:1px solid #bae6fd; border-radius:10px; padding:10px; text-decoration:none; color:#0369a1; font-weight:800; font-size:12px; text-align:center; display:block;">
              ✈️ Cheap Flights
            </a>
            <a href="${getTrackedUrl('https://airhelp.tp.st/3ItXS0E4', 'claim')}" target="_blank" rel="sponsored nofollow noopener"
               class="booking-pill" style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:10px; padding:10px; text-decoration:none; color:#1d4ed8; font-weight:800; font-size:12px; text-align:center; display:block;">
              🛡️ 600€ Claim
            </a>
            <a href="${getTrackedUrl('https://airalo.tp.st/ZZoQC7Mz', 'esim')}" target="_blank" rel="sponsored nofollow noopener"
               class="booking-pill" style="background:#faf5ff; border:1px solid #e9d5ff; border-radius:10px; padding:10px; text-decoration:none; color:#7e22ce; font-weight:800; font-size:12px; text-align:center; display:block;">
              📱 5G eSIM
            </a>
            <a href="${getTrackedUrl('https://kiwitaxi.tp.st/tIZcbMOB', 'taxi')}&promo_id=4558" target="_blank" rel="sponsored nofollow noopener"
               class="booking-pill" style="background:#ecfdf5; border:1px solid #a7f3d0; border-radius:10px; padding:10px; text-decoration:none; color:#047857; font-weight:800; font-size:12px; text-align:center; display:block;">
              🚖 Kiwitaxi
            </a>
          </div>

          <div style="display:flex; gap:10px; align-items:center; flex-wrap:wrap;">
            <a href="${CONFIG.SUPERSTORE_URL}" target="_blank" rel="noopener"
               style="background:#052962; color:#ffffff; font-weight:800; font-size:13px; padding:11px 22px; border-radius:12px; text-decoration:none; box-shadow:0 4px 15px rgba(5,41,98,0.25);">
              🚀 Launch SuperStore Hub (21 Tools) &rarr;
            </a>
            <a href="${CONFIG.ROKSANA_FINAL}" target="_blank" rel="noopener"
               style="background:#fefce8; color:#854d0e; font-weight:800; font-size:12px; padding:10px 16px; border-radius:12px; text-decoration:none; border:1px solid #fde047;">
              ❤️ Roksana Boutique Final
            </a>
          </div>
        </div>

        <!-- Right 3D Floating Hero Showcase Card -->
        <div style="display:flex; justify-content:center;">
          <div style="width:100%; max-width:320px;">
            <div class="roksana-img-card">
              <div class="upvote-badge">
                <span>▲ 24.5k</span> <span>Upvoted</span>
              </div>
              <a href="${CONFIG.GUIDE_URL}">
                <img src="${CONFIG.HERO_IMAGE}" alt="European Airline Flight Transit and Airport Terminal High Resolution Photography" loading="lazy" decoding="async" />
              </a>
              <div style="position:absolute; bottom:4px; left:4px; right:4px; background:linear-gradient(to top, rgba(13,17,23,0.92), transparent); padding:12px 14px; border-radius:0 0 17px 17px; color:#ffffff; font-size:11px;">
                <span style="color:#FFD700; font-weight:800;">3D Vision • Authentic Logistics</span><br>
                <span style="color:#e2e8f0; font-size:10px;">Via Carlo Felice ARST 08:17 Sanluri</span>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- Trust Bar Footer -->
      <div style="border-top:1px solid #f1f5f9; padding-top:14px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; font-size:11px; color:#64748b;">
        <span>🔒 Travelpayouts Marker 787950 Locked</span>
        <span>Kiwitaxi tIZcbMOB Fixed</span>
        <span>Amazon 4shg6Hn Verified</span>
        <span>Zero 404 Guaranteed</span>
      </div>
    `;

    grid.insertBefore(hero, grid.firstChild);
  }

  function loop() {
    injectLuxuryStyling();
    renderGDPRBanner();
    enforce2Menus();
    injectLuxuryHero();
    enforceGoogleCompliantLinks();
  }

  detectCountry();

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loop);
  } else {
    loop();
  }

  setInterval(loop, 400);
})();
