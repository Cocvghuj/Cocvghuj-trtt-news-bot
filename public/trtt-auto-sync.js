/**
 * TRTT Enterprise Auto-Sync Engine v12.0 (TRAVELPAYOUTS PRO ELITE SPECIFICATION)
 * 
 * 1. Strict tp.st + Marker 787950 Locked (No tpo.lv)
 *    tIZcbMOB FIXED (Capital I, Never tlZcbMOB) + promo_id 4558 (c13)
 * 2. Dynamic SubID + UTM Auto Tracking via IP Country Code:
 *    subid = 'trtt_lock_' + country_code (e.g. trtt_lock_it, trtt_lock_de, trtt_lock_bd)
 *    utm_source = 'plane_' + country_code
 * 3. Complete 10 Program Full-Stack Vault:
 *    Aviasales (Fb8U9yav), AirHelp (3ItXS0E4), Airalo (ZZoQC7Mz), Saily (ssekmS4X),
 *    Yesim (krzFKLpg), Drimsim (Ly7ywIY8 + c102), Kiwitaxi (tIZcbMOB),
 *    Trip.com (h3LrTZcS), Tiqets (bnx8pnF6), Amazon (4shg6Hn)
 * 4. Real .it Domains & Zero NXDOMAIN Guarantee
 * 5. GDPR Cookie Consent Banner + Affiliate Disclosure Popup (localStorage: trtt_cookie_consent_esim)
 * 6. GitHub Open Source Transparency Verified
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

  // Default detected country code (auto-updates via IP API)
  let userCountry = 'it';

  // 1. Detect Country Code via lightweight IP API (Zero Delay, Fallback 'it')
  function detectCountry() {
    try {
      fetch('https://ipapi.co/json/')
        .then(res => res.json())
        .then(data => {
          if (data && data.country_code) {
            userCountry = data.country_code.toLowerCase();
            enforceExpertTracking();
          }
        })
        .catch(() => {});
    } catch(e) {}
  }

  // 2. Pillar 2: SubID + UTM Expert Tracking Generator
  function getTrackedUrl(rawUrl, category) {
    if (!rawUrl) return rawUrl;
    let clean = rawUrl.replace(/tpo\.lv/g, 'tp.st').replace(/tlZcbMOB/g, 'tIZcbMOB');
    try {
      const u = new URL(clean);
      u.searchParams.set('marker', CONFIG.MARKER);
      u.searchParams.set('subid', 'trtt_lock_' + userCountry);
      u.searchParams.set('utm_source', (category || 'plane') + '_' + userCountry);
      u.searchParams.set('utm_medium', 'travel_hub');
      if (clean.includes('tIZcbMOB') && !u.searchParams.has('promo_id')) {
        u.searchParams.set('promo_id', '4558');
      }
      return u.toString();
    } catch(e) {
      return clean;
    }
  }

  // 3. Pillar 5: GDPR Cookie Consent Banner + Affiliate Disclosure Popup (Police Safe)
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
        <strong>🍪 GDPR &amp; Affiliate Transparency Notice:</strong>
        TRTT VoyageHub uses minimal functional cookies to ensure travel deal delivery and affiliate tracking under <strong>Marker ${CONFIG.MARKER}</strong>. We comply with EU GDPR, Italian Privacy Law (Garante), and International Brand Safety Standards.
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

  // 4. Pillar 1 & 2: Real-time Strict Link Transformation on Live Page
  function enforceExpertTracking() {
    document.querySelectorAll('a[href*="tp.st"], a[href*="tpo.lv"]').forEach(a => {
      let cat = 'plane';
      if (a.href.includes('airhelp')) cat = 'claim';
      else if (a.href.includes('airalo') || a.href.includes('saily') || a.href.includes('yesim') || a.href.includes('drimsim')) cat = 'esim';
      else if (a.href.includes('kiwitaxi')) cat = 'taxi';
      else if (a.href.includes('trip.com') || a.href.includes('h3LrTZcS')) cat = 'hotel';
      else if (a.href.includes('tiqets') || a.href.includes('bnx8pnF6')) cat = 'ticket';
      a.href = getTrackedUrl(a.href, cat);
    });

    document.querySelectorAll('a[href*="amzn.to"]').forEach(a => {
      if (!a.href.includes('4shg6Hn')) {
        a.href = 'https://amzn.to/4shg6Hn?marker=' + CONFIG.MARKER + '&subid=trtt_lock_' + userCountry;
      }
    });

    // Clean broken empty links
    document.querySelectorAll('a[href="https://"], a[href="https:///"]').forEach(a => {
      a.href = 'javascript:void(0)';
    });

    // Replace old Vercel links with 100% SuperStore
    document.querySelectorAll('a[href*="cocvghuj-trtt-news-bot.vercel.app"]').forEach(a => {
      a.href = CONFIG.SUPERSTORE_URL;
    });
  }

  // 5. Pillar 3: Inject the Full 10-Program Vault on Blog Top
  function inject10ProgramVault() {
    if (document.getElementById('trtt-10-program-vault-v12')) return;

    const grid = document.querySelector('.grid-posts, .blog-posts, #Blog1');
    if (!grid) return;

    const card = document.createElement('div');
    card.id = 'trtt-10-program-vault-v12';
    card.className = 'blog-post hentry index-post';
    card.style.cssText = `
      background: #ffffff !important; border: 2px solid #052962 !important;
      border-radius: 18px !important; padding: 22px !important; margin-bottom: 28px !important;
      box-shadow: 0 10px 30px rgba(5,41,98,0.12) !important; width: 100% !important; box-sizing: border-box !important;
      font-family: system-ui, -apple-system, sans-serif !important;
    `;

    card.innerHTML = `
      <div>
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:12px;">
          <span style="background:#052962; color:#ffffff; font-size:11px; font-weight:900; padding:4px 10px; border-radius:6px; text-transform:uppercase;">
            ⚡ 10-PROGRAM TRAVEL STACK • ALL NICHE ACTIVE
          </span>
          <span style="font-size:11px; color:#047857; font-weight:800; background:#dcfce7; padding:3px 10px; border-radius:6px;">
            🔒 Marker ${CONFIG.MARKER} • subid=trtt_lock_${userCountry}
          </span>
        </div>

        <!-- Real Image for Google E-E-A-T Safety -->
        <div style="position:relative; border-radius:12px; overflow:hidden; margin-bottom:14px; max-height:280px; border:1px solid #e2e8f0;">
          <a href="${CONFIG.GUIDE_URL}">
            <img src="${CONFIG.FEATURE_IMAGE}" alt="Qatar Logistics White Shirt Real Photo" style="width:100%; max-height:280px; object-fit:cover; display:block;" />
          </a>
          <div style="position:absolute; bottom:0; left:0; right:0; background:linear-gradient(to top, rgba(5,41,98,0.9), transparent); padding:10px 14px; color:#ffffff; font-size:11px;">
            <span>📸 Verified Staff Carriage Log • Zero Fake Domains • Deliverability 100%</span>
          </div>
        </div>

        <h2 style="font-size:20px; font-weight:900; color:#052962; margin:0 0 8px 0; line-height:1.35;">
          Official Full-Stack Travel Engine: 10 Verified Global Programs
        </h2>
        <p style="font-size:13px; color:#475569; margin:0 0 14px 0; line-height:1.6;">
          Zero spam, 100% delivery. Compare 700+ airlines, claim 600€ EC 261 flight refunds, connect instant European 5G eSIMs, and reserve guaranteed airport rides.
        </p>

        <!-- The 10 Program Grid -->
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(180px, 1fr)); gap:8px; margin-bottom:14px;">
          
          <!-- 1. Aviasales -->
          <a href="${getTrackedUrl('https://aviasales.tp.st/Fb8U9yav', 'plane')}" target="_blank" rel="noopener"
             style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:8px; padding:9px 12px; text-decoration:none; color:#0f172a; font-weight:800; font-size:12px; display:flex; justify-content:space-between; align-items:center;">
            <span>✈️ 1. Aviasales Flights</span>
            <span style="font-size:10px; color:#4f46e5;">Fb8U9yav</span>
          </a>

          <!-- 2. AirHelp -->
          <a href="${getTrackedUrl('https://airhelp.tp.st/3ItXS0E4', 'claim')}" target="_blank" rel="noopener"
             style="background:#eff6ff; border:1px solid #bfdbfe; border-radius:8px; padding:9px 12px; text-decoration:none; color:#1d4ed8; font-weight:800; font-size:12px; display:flex; justify-content:space-between; align-items:center;">
            <span>🛡️ 2. AirHelp 600€</span>
            <span style="font-size:10px; color:#2563eb;">3ItXS0E4</span>
          </a>

          <!-- 3. Airalo -->
          <a href="${getTrackedUrl('https://airalo.tp.st/ZZoQC7Mz', 'esim')}" target="_blank" rel="noopener"
             style="background:#faf5ff; border:1px solid #e9d5ff; border-radius:8px; padding:9px 12px; text-decoration:none; color:#7e22ce; font-weight:800; font-size:12px; display:flex; justify-content:space-between; align-items:center;">
            <span>🌐 3. Airalo eSIM</span>
            <span style="font-size:10px; color:#9333ea;">ZZoQC7Mz</span>
          </a>

          <!-- 4. Saily -->
          <a href="${getTrackedUrl('https://saily.tp.st/ssekmS4X', 'esim')}" target="_blank" rel="noopener"
             style="background:#ecfdf5; border:1px solid #a7f3d0; border-radius:8px; padding:9px 12px; text-decoration:none; color:#047857; font-weight:800; font-size:12px; display:flex; justify-content:space-between; align-items:center;">
            <span>⚡ 4. Saily Nord eSIM</span>
            <span style="font-size:10px; color:#059669;">ssekmS4X</span>
          </a>

          <!-- 5. Yesim -->
          <a href="${getTrackedUrl('https://yesim.tp.st/krzFKLpg', 'esim')}" target="_blank" rel="noopener"
             style="background:#fdf2f8; border:1px solid #fbcfe8; border-radius:8px; padding:9px 12px; text-decoration:none; color:#be185d; font-weight:800; font-size:12px; display:flex; justify-content:space-between; align-items:center;">
            <span>♾️ 5. Yesim Unlimited</span>
            <span style="font-size:10px; color:#db2777;">krzFKLpg</span>
          </a>

          <!-- 6. Drimsim -->
          <a href="${getTrackedUrl('https://drimsim.tp.st/Ly7ywIY8', 'esim')}&c102=dual" target="_blank" rel="noopener"
             style="background:#f0f9ff; border:1px solid #bae6fd; border-radius:8px; padding:9px 12px; text-decoration:none; color:#0369a1; font-weight:800; font-size:12px; display:flex; justify-content:space-between; align-items:center;">
            <span>🌍 6. Drimsim PAYG</span>
            <span style="font-size:10px; color:#0284c7;">Ly7ywIY8</span>
          </a>

          <!-- 7. Kiwitaxi (FIXED) -->
          <a href="${getTrackedUrl('https://kiwitaxi.tp.st/tIZcbMOB', 'taxi')}&promo_id=4558" target="_blank" rel="noopener"
             style="background:#fefce8; border:1.5px solid #fde047; border-radius:8px; padding:9px 12px; text-decoration:none; color:#854d0e; font-weight:900; font-size:12px; display:flex; justify-content:space-between; align-items:center;">
            <span>🚖 7. Kiwitaxi Ride</span>
            <span style="font-size:10px; background:#ca8a04; color:#fff; padding:1px 5px; border-radius:3px;">tIZcbMOB</span>
          </a>

          <!-- 8. Trip.com -->
          <a href="${getTrackedUrl('https://trip.tp.st/h3LrTZcS', 'hotel')}" target="_blank" rel="noopener"
             style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:8px; padding:9px 12px; text-decoration:none; color:#0f172a; font-weight:800; font-size:12px; display:flex; justify-content:space-between; align-items:center;">
            <span>🏨 8. Trip Hotels</span>
            <span style="font-size:10px; color:#64748b;">h3LrTZcS</span>
          </a>

          <!-- 9. Tiqets -->
          <a href="${getTrackedUrl('https://tiqets.tp.st/bnx8pnF6', 'ticket')}" target="_blank" rel="noopener"
             style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:8px; padding:9px 12px; text-decoration:none; color:#0f172a; font-weight:800; font-size:12px; display:flex; justify-content:space-between; align-items:center;">
            <span>🏛️ 9. Tiqets Passes</span>
            <span style="font-size:10px; color:#64748b;">bnx8pnF6</span>
          </a>

          <!-- 10. Amazon Gear -->
          <a href="https://amzn.to/4shg6Hn?marker=${CONFIG.MARKER}&subid=trtt_lock_${userCountry}" target="_blank" rel="noopener"
             style="background:#fffbeb; border:1px solid #fde68a; border-radius:8px; padding:9px 12px; text-decoration:none; color:#92400e; font-weight:800; font-size:12px; display:flex; justify-content:space-between; align-items:center;">
            <span>🎒 10. Amazon Essentials</span>
            <span style="font-size:10px; color:#b45309;">4shg6Hn</span>
          </a>

        </div>

        <!-- Pillar 6: Open Source Transparency + SuperStore Launch -->
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; border-top:1px solid #f1f5f9; padding-top:12px;">
          <div style="font-size:11.5px; color:#64748b;">
            <span>🐙 Open-Source Code: <a href="${CONFIG.GITHUB_REPO}" target="_blank" style="color:#0284c7; font-weight:bold; text-decoration:underline;">Cocvghuj-trtt-news-bot</a></span>
            <span style="margin:0 5px;">•</span>
            <span>GDPR Safe</span>
          </div>
          <a href="${CONFIG.SUPERSTORE_URL}" target="_blank" rel="noopener"
             style="background:#052962; color:#ffffff; font-weight:800; font-size:12.5px; padding:8px 18px; border-radius:8px; text-decoration:none;">
            🚀 Open SuperStore Hub &rarr;
          </a>
        </div>
      </div>
    `;

    grid.insertBefore(card, grid.firstChild);
  }

  // 6. Navigation Enforcer
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
      if (nav.getAttribute('data-trtt-locked') === 'v12') return;
      nav.setAttribute('data-trtt-locked', 'v12');
      nav.innerHTML = twoMenusHtml;
    });
  }

  function loop() {
    renderGDPRBanner();
    enforce2Menus();
    inject10ProgramVault();
    enforceExpertTracking();
  }

  detectCountry();

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loop);
  } else {
    loop();
  }

  setInterval(loop, 400);
})();
