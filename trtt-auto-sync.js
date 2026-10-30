/**
 * TRTT Enterprise Auto-Sync Engine v14.0 (3D VISION ROKSANA CARD + UPVOTE BADGE)
 * 
 * 1. 3D VISION & FLOATING CONIC GRADIENT:
 *    - Injects .roksana-img-card and .upvote-badge into Blogger DOM.
 *    - conic-gradient(#FFD700, #FF6B6B, #7F5EFF, #00D26A, #FFD700)
 *    - 3D perspective(1000px) rotateY(-5deg) rotateX(5deg) with smooth float animation.
 * 2. REDDIT UPVOTE BADGE (#FF4500):
 *    - "▲ 24.5k Upvoted • World Best Blog" floating badge on image.
 * 3. 100% GOOGLE & TRAVELPAYOUTS COMPLIANCE:
 *    - rel="sponsored nofollow noopener" on all affiliate links.
 *    - Dynamic subid=trtt_lock_{country_code} • Kiwitaxi tIZcbMOB • Amazon 4shg6Hn.
 *    - GDPR Cookie Consent Banner with localStorage persistence.
 */
(function() {
  const CONFIG = {
    MARKER: '787950',
    PIN: '7879',
    BLOG_NAME: 'trttnews24bd',
    SUPERSTORE_URL: 'https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/?marker=787950',
    GUIDE_URL: 'https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/blog/ultimate-europe-travel-guide-2026.html',
    BLOG_URL: 'https://trttnews24bd.blogspot.com',
    GITHUB_REPO: 'https://github.com/Cocvghuj/Cocvghuj-trtt-news-bot',
    FEATURE_IMAGE: 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhGIViEQzbsyK0KHWtYnl1bHbRrSKjX8XbeHyFU5kHlX4BSbwjV2mcy-K7bj_NuhPDzDojIZNzU5nzA1aVukNypAcOmzauPyTPSYYg72wWw8jmnegjxVCLBagh3-uyl7eyQK6oy9nnbWEMcVloAd88diVqPO8uw-zl7g7ey5HWzeLJ5KujfrxleCR5Hjvs/s1600/Photos.jpg'
  };

  let userCountry = 'it';

  // Inject Custom 3D Vision CSS into Blogger Head
  function inject3DVisionCSS() {
    if (document.getElementById('trtt-3d-vision-style')) return;
    const style = document.createElement('style');
    style.id = 'trtt-3d-vision-style';
    style.innerHTML = `
      .roksana-img-card {
        position: relative;
        border-radius: 24px;
        padding: 4px;
        background: conic-gradient(from 0deg, #FFD700, #FF6B6B, #7F5EFF, #00D26A, #FFD700);
        box-shadow: 0 20px 60px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,215,0,0.2);
        transform: perspective(1000px) rotateY(-5deg) rotateX(5deg);
        transition: all 0.6s cubic-bezier(0.23,1,0.32,1);
        animation: roksanaFloat 6s ease-in-out infinite;
        margin-bottom: 24px;
      }
      .roksana-img-card:hover {
        transform: perspective(1000px) rotateY(0deg) rotateX(0deg) translateY(-10px) scale(1.02);
        box-shadow: 0 30px 80px rgba(0,0,0,0.5), 0 0 0 2px #FFD700;
      }
      .roksana-img-card img {
        width: 100%;
        height: auto;
        max-height: 400px;
        border-radius: 20px;
        object-fit: cover;
        display: block;
        background: #0d1117;
      }
      @keyframes roksanaFloat {
        0%,100% { transform: perspective(1000px) rotateY(-5deg) rotateX(5deg) translateY(0px); }
        50% { transform: perspective(1000px) rotateY(-5deg) rotateX(5deg) translateY(-12px); }
      }
      .upvote-badge {
        position: absolute;
        top: -8px;
        right: -8px;
        background: #FF4500;
        color: #fff;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 800;
        box-shadow: 0 4px 14px rgba(255,69,0,0.4);
        display: flex;
        align-items: center;
        gap: 4px;
        z-index: 10;
        font-family: system-ui, sans-serif;
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

  // Strict URL Tracker with Google-mandated tags
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

  // Google Webmaster Guideline: Add rel="sponsored nofollow" to ALL monetized links
  function enforceGoogleCompliantLinks() {
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

    // Rich image alt text
    document.querySelectorAll('img:not([alt]), img[alt=""]').forEach(img => {
      img.setAttribute('alt', 'TRTT Verified Europe Travel & Logistics Guide');
    });
  }

  // GDPR & Affiliate Disclosure Banner
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
        TRTT News 24 BD participates in affiliate programs. When you book via our verified links (Aviasales, Airalo, Kiwitaxi, Amazon), we may earn a small commission at no additional cost to you. Fully compliant with EU GDPR and Google Webmaster Guidelines.
      </div>
      <div style="display:flex; gap:8px; align-items:center;">
        <a href="https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/privacy.html" target="_blank" style="color: #93c5fd; text-decoration: underline; font-size: 11px;">Privacy &amp; Affiliate Policy</a>
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

  // Clean 2 Navigation Menus
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
      if (nav.getAttribute('data-trtt-locked') === 'v14') return;
      nav.setAttribute('data-trtt-locked', 'v14');
      nav.innerHTML = twoMenusHtml;
    });

    const mobMenu = document.querySelector('.mobile-menu');
    if (mobMenu && !mobMenu.hasAttribute('data-trtt-mobile')) {
      mobMenu.setAttribute('data-trtt-mobile', 'v14');
      mobMenu.innerHTML = `
        <ul style="list-style:none; padding:15px; margin:0;">
          <li style="margin-bottom:10px;">
            <a href="${CONFIG.BLOG_URL}" style="display:block; background:#f1f5f9; color:#052962; padding:12px 16px; border-radius:10px; font-weight:800; text-decoration:none;">
              📖 Read The Blog
            </a>
          </li>
          <li>
            <a href="${CONFIG.SUPERSTORE_URL}" target="_blank" rel="noopener" style="display:block; background:#052962; color:#ffffff; padding:12px 16px; border-radius:10px; font-weight:800; text-decoration:none;">
              🚀 Explore Your Life (SuperStore)
            </a>
          </li>
        </ul>
      `;
    }
  }

  // Inject 3D Vision Roksana Card with Reddit Upvote Badge & Conic Gradient
  function inject3DVisionEditorialCard() {
    if (document.getElementById('trtt-3d-vision-card-v14')) return;

    const grid = document.querySelector('.grid-posts, .blog-posts, #Blog1');
    if (!grid) return;

    const card = document.createElement('div');
    card.id = 'trtt-3d-vision-card-v14';
    card.className = 'blog-post hentry index-post';
    card.style.cssText = `
      background: #ffffff !important; border: 2px solid #052962 !important;
      border-radius: 22px !important; padding: 24px !important; margin-bottom: 30px !important;
      box-shadow: 0 12px 35px rgba(5,41,98,0.15) !important; width: 100% !important; box-sizing: border-box !important;
      font-family: system-ui, -apple-system, sans-serif !important;
    `;

    card.innerHTML = `
      <div>
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:14px;">
          <span style="background:#052962; color:#ffffff; font-size:11px; font-weight:900; padding:4px 12px; border-radius:9999px; text-transform:uppercase;">
            🌟 World Best Blog • 3D Vision Architecture
          </span>
          <span style="font-size:11px; color:#0369a1; font-weight:700; background:#e0f2fe; padding:3px 10px; border-radius:6px;">
            Verified with FlightScoutPro
          </span>
        </div>

        <!-- 3D Floating Roksana Image Card with Reddit Upvote Badge -->
        <div class="roksana-img-card">
          <div class="upvote-badge">
            <span>▲ 24.5k</span> <span>Upvoted</span>
          </div>
          <a href="${CONFIG.GUIDE_URL}">
            <img src="${CONFIG.FEATURE_IMAGE}" alt="Qatar Airport Ground Logistics and Transit Operations Real Field Photo" />
          </a>
          <div style="position:absolute; bottom:4px; left:4px; right:4px; background:linear-gradient(to top, rgba(13,17,23,0.95), transparent); padding:14px 18px; border-radius:0 0 20px 20px; color:#ffffff; font-size:11.5px;">
            <span style="color:#FFD700; font-weight:800;">3D Vision • Authentic Field Operations</span> • <span>White shirt, mask, gloves &amp; POS machine experience</span>
          </div>
        </div>

        <h2 style="font-size:23px; font-weight:900; color:#052962; margin:0 0 10px 0; line-height:1.35;">
          <a href="${CONFIG.GUIDE_URL}" style="color:#052962; text-decoration:none;">
            The Complete European Travel, Flight Compensation &amp; 5G Connectivity Guide (2026-2027)
          </a>
        </h2>

        <p style="font-size:14px; color:#475569; margin:0 0 18px 0; line-height:1.75;">
          Practical field intelligence for international travelers: How to secure verified airfares on Aviasales, claim up to 600€ for delayed European flights under EC 261, deploy instant 5G eSIMs with Airalo &amp; Saily, and book fixed airport rides with Kiwitaxi.
        </p>

        <!-- 4 Pillars Grid -->
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(180px, 1fr)); gap:10px; margin-bottom:18px;">
          <a href="${getTrackedUrl('https://aviasales.tp.st/Fb8U9yav', 'plane')}" target="_blank" rel="sponsored nofollow noopener"
             style="background:#f0f9ff; border:1px solid #bae6fd; border-radius:10px; padding:11px 14px; text-decoration:none; color:#0369a1; font-weight:bold; font-size:12.5px; display:flex; justify-content:space-between; align-items:center;">
            <span>✈️ Aviasales Flights</span>
            <span style="font-size:10px; background:#0284c7; color:#fff; padding:2px 6px; border-radius:4px;">Compare</span>
          </a>

          <a href="${getTrackedUrl('https://airhelp.tp.st/3ItXS0E4', 'claim')}" target="_blank" rel="sponsored nofollow noopener"
             style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:10px; padding:11px 14px; text-decoration:none; color:#1d4ed8; font-weight:bold; font-size:12.5px; display:flex; justify-content:space-between; align-items:center;">
            <span>🛡️ AirHelp 600€ Claim</span>
            <span style="font-size:10px; background:#2563eb; color:#fff; padding:2px 6px; border-radius:4px;">EC 261</span>
          </a>

          <a href="${getTrackedUrl('https://airalo.tp.st/ZZoQC7Mz', 'esim')}" target="_blank" rel="sponsored nofollow noopener"
             style="background:#faf5ff; border:1px solid #e9d5ff; border-radius:10px; padding:11px 14px; text-decoration:none; color:#7e22ce; font-weight:bold; font-size:12.5px; display:flex; justify-content:space-between; align-items:center;">
            <span>📱 Airalo 5G eSIM</span>
            <span style="font-size:10px; background:#9333ea; color:#fff; padding:2px 6px; border-radius:4px;">Instant QR</span>
          </a>

          <a href="${getTrackedUrl('https://kiwitaxi.tp.st/tIZcbMOB', 'taxi')}&promo_id=4558" target="_blank" rel="sponsored nofollow noopener"
             style="background:#ecfdf5; border:1px solid #a7f3d0; border-radius:10px; padding:11px 14px; text-decoration:none; color:#047857; font-weight:bold; font-size:12.5px; display:flex; justify-content:space-between; align-items:center;">
            <span>🚖 Kiwitaxi Fixed Ride</span>
            <span style="font-size:10px; background:#059669; color:#fff; padding:2px 6px; border-radius:4px;">tIZcbMOB</span>
          </a>
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; border-top:1px solid #f1f5f9; padding-top:14px;">
          <div style="font-size:12px; color:#64748b;">
            <span>3D Perspective • All Links Google &amp; Travelpayouts Compliant</span>
          </div>
          <a href="${CONFIG.SUPERSTORE_URL}" target="_blank" rel="noopener"
             style="background:#052962; color:#ffffff; font-weight:800; font-size:13px; padding:9px 20px; border-radius:10px; text-decoration:none; box-shadow:0 4px 12px rgba(5,41,98,0.25);">
            🚀 Open Travel SuperStore &rarr;
          </a>
        </div>
      </div>
    `;

    grid.insertBefore(card, grid.firstChild);
  }

  function loop() {
    inject3DVisionCSS();
    renderGDPRBanner();
    enforce2Menus();
    inject3DVisionEditorialCard();
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
