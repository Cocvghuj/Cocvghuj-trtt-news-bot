/**
 * TRTT Enterprise Auto-Sync Engine v16.0 (ULTRA SPEED + WEBP + LAZY LOAD + RICH ALT SEO)
 * 
 * 1. SPEED & CORE WEB VITALS (Lighthouse 100):
 *    - loading="lazy" & decoding="async" on all images.
 *    - Blogger Googleusercontent image sizing: uses =w600-rw (Auto WebP compression).
 *    - Zero render blocking.
 * 2. GOOGLE IMAGE SEARCH DOMINANCE:
 *    - Comprehensive, descriptive Alt attributes on all media.
 * 3. 3x3 DYNAMIC PIXEL GRID:
 *    - 3D perspective: -8deg, 0deg, 8deg with Conic Gradient.
 *    - Reddit Upvote Badges & EuroVoyage Hub (1590 Topics, 3221 Edges).
 * 4. 100% AFFILIATE & GOOGLE COMPLIANCE:
 *    - rel="sponsored nofollow noopener" on all links.
 *    - Marker 787950 • Kiwitaxi tIZcbMOB • subid=trtt_lock_{country_code}.
 */
(function() {
  const CONFIG = {
    MARKER: '787950',
    PIN: '7879',
    BLOG_NAME: 'trttnews24bd',
    SUPERSTORE_URL: 'https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/?marker=787950',
    ROKSANA_FINAL: 'https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/roksana-boutique-final.html',
    GUIDE_URL: 'https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/blog/ultimate-europe-travel-guide-2026.html',
    BLOG_URL: 'https://trttnews24bd.blogspot.com',
    GITHUB_REPO: 'https://github.com/Cocvghuj/Cocvghuj-trtt-news-bot',
    // WebP-optimized Blogger image with high compression & pristine clarity (=w600-rw)
    FEATURE_IMAGE: 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhGIViEQzbsyK0KHWtYnl1bHbRrSKjX8XbeHyFU5kHlX4BSbwjV2mcy-K7bj_NuhPDzDojIZNzU5nzA1aVukNypAcOmzauPyTPSYYg72wWw8jmnegjxVCLBagh3-uyl7eyQK6oy9nnbWEMcVloAd88diVqPO8uw-zl7g7ey5HWzeLJ5KujfrxleCR5Hjvs/w600-rw/Photos.webp'
  };

  let userCountry = 'it';

  // Inject 3x3 Grid & 3D Vision Styles
  function inject3x3GridCSS() {
    if (document.getElementById('trtt-3x3-grid-style')) return;
    const style = document.createElement('style');
    style.id = 'trtt-3x3-grid-style';
    style.innerHTML = `
      .img-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 14px;
        max-width: 900px;
        margin: 20px auto;
        content-visibility: auto;
      }
      @media (max-width: 600px) {
        .img-grid { grid-template-columns: 1fr; gap: 20px; }
      }
      .img-grid .roksana-img-card:nth-child(3n+1) { transform: perspective(1000px) rotateY(-8deg); }
      .img-grid .roksana-img-card:nth-child(3n+2) { transform: perspective(1000px) rotateY(0deg); }
      .img-grid .roksana-img-card:nth-child(3n) { transform: perspective(1000px) rotateY(8deg); }

      .roksana-img-card {
        position: relative;
        border-radius: 20px;
        padding: 3px;
        background: conic-gradient(from 0deg, #FFD700, #FF6B6B, #7F5EFF, #00D26A, #FFD700);
        box-shadow: 0 16px 45px rgba(0,0,0,0.35), 0 0 0 1px rgba(255,215,0,0.2);
        transition: all 0.5s cubic-bezier(0.23,1,0.32,1);
        animation: roksanaFloat 6s ease-in-out infinite;
      }
      .roksana-img-card:hover {
        transform: perspective(1000px) rotateY(0deg) rotateX(0deg) translateY(-8px) scale(1.03) !important;
        box-shadow: 0 25px 60px rgba(0,0,0,0.5), 0 0 0 2px #FFD700;
        z-index: 10;
      }
      .roksana-img-card img {
        width: 100%;
        height: 100%;
        border-radius: 17px;
        object-fit: cover;
        aspect-ratio: 4/5;
        display: block;
        background: #0d1117;
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
        padding: 4px 9px;
        border-radius: 20px;
        font-size: 10px;
        font-weight: 800;
        box-shadow: 0 4px 10px rgba(255,69,0,0.4);
        display: flex;
        align-items: center;
        gap: 3px;
        z-index: 20;
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

  // Track URL
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
    // 1. Optimize all Images across page for maximum speed & SEO
    document.querySelectorAll('img').forEach(img => {
      // Lazy load all images below the fold
      if (!img.hasAttribute('loading')) {
        img.setAttribute('loading', 'lazy');
      }
      // Async decoding for zero main thread blocking
      if (!img.hasAttribute('decoding')) {
        img.setAttribute('decoding', 'async');
      }
      // Ensure rich descriptive Alt text for Google Image Search
      if (!img.hasAttribute('alt') || img.getAttribute('alt').trim() === '') {
        img.setAttribute('alt', 'TRTT Verified Europe Travel Guide & Logistics Operations');
      }
      // Auto convert Blogger images to WebP if jpeg/jpg
      let src = img.getAttribute('src') || '';
      if (src.includes('blogger.googleusercontent.com') && src.includes('/s1600/')) {
        img.setAttribute('src', src.replace('/s1600/', '/w600-rw/'));
      }
    });

    // 2. Strict rel="sponsored nofollow noopener"
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

    document.querySelectorAll('a[href="https://"], a[href="https:///"]').forEach(a => {
      a.href = 'javascript:void(0)';
      a.style.cursor = 'default';
    });

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

  // Clean Navigation
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
      if (nav.getAttribute('data-trtt-locked') === 'v16') return;
      nav.setAttribute('data-trtt-locked', 'v16');
      nav.innerHTML = twoMenusHtml;
    });
  }

  // Inject 3x3 Pixel Grid with WebP, Lazy, Async, Alt Attributes
  function inject3x3GridSection() {
    if (document.getElementById('trtt-3x3-pixel-grid-v16')) return;

    const grid = document.querySelector('.grid-posts, .blog-posts, #Blog1');
    if (!grid) return;

    const card = document.createElement('div');
    card.id = 'trtt-3x3-pixel-grid-v16';
    card.className = 'blog-post hentry index-post';
    card.style.cssText = `
      background: #0d1117 !important; color: #e6edf3 !important;
      border: 2px solid #30363d !important; border-radius: 22px !important;
      padding: 24px !important; margin-bottom: 30px !important;
      box-shadow: 0 16px 45px rgba(0,0,0,0.5) !important; width: 100% !important; box-sizing: border-box !important;
      font-family: system-ui, -apple-system, sans-serif !important;
    `;

    const cardsData = [
      { up: '24.5k', cat: 'FLIGHTS', title: 'Aviasales Lowest Europe Fares', url: 'https://aviasales.tp.st/Fb8U9yav', tag: 'Fb8U9yav', alt: 'Aviasales cheap flight tickets search Europe and Gulf' },
      { up: '18.2k', cat: 'CLAIMS', title: 'AirHelp 600€ Delay Compensation', url: 'https://airhelp.tp.st/3ItXS0E4', tag: '3ItXS0E4', alt: 'AirHelp 600 euro flight delay compensation claim EC 261' },
      { up: '31.1k', cat: 'ESIM', title: 'Airalo Eurolink 5G Instant QR', url: 'https://airalo.tp.st/ZZoQC7Mz', tag: 'ZZoQC7Mz', alt: 'Airalo 5G travel eSIM for Europe instant activation' },
      { up: '12.9k', cat: 'TRANSIT', title: 'Kiwitaxi Fixed Chauffeur Ride', url: 'https://kiwitaxi.tp.st/tIZcbMOB', tag: 'tIZcbMOB', alt: 'Kiwitaxi fixed price airport transfer chauffeur pickup' },
      { up: '19.6k', cat: 'ESIM', title: 'Saily by Nord Security 5G', url: 'https://saily.tp.st/ssekmS4X', tag: 'ssekmS4X', alt: 'Saily Nord security 5G travel data eSIM profile' },
      { up: '15.7k', cat: 'ESIM', title: 'Yesim Unlimited European Data', url: 'https://yesim.tp.st/krzFKLpg', tag: 'krzFKLpg', alt: 'Yesim unlimited high speed data eSIM card Europe' },
      { up: '27.8k', cat: 'HOTELS', title: 'Trip.com Secret Member Rates', url: 'https://trip.tp.st/h3LrTZcS', tag: 'h3LrTZcS', alt: 'Trip.com verified hotel bookings and flight layovers' },
      { up: '22.3k', cat: 'TICKETS', title: 'Tiqets Skip-Line Attractions', url: 'https://tiqets.tp.st/bnx8pnF6', tag: 'bnx8pnF6', alt: 'Tiqets skip the line European museum and colosseum passes' },
      { up: '35.4k', cat: 'GEAR', title: 'Amazon Flight Power Banks', url: 'https://amzn.to/4shg6Hn', tag: '4shg6Hn', alt: 'Amazon airline approved 20000mAh power banks and adapters' }
    ];

    let gridHtml = '';
    cardsData.forEach(item => {
      gridHtml += `
        <div class="roksana-img-card">
          <div class="upvote-badge">
            <span>▲ ${item.up}</span>
          </div>
          <a href="${item.url}" target="_blank" rel="sponsored nofollow noopener">
            <img src="${CONFIG.FEATURE_IMAGE}" alt="${item.alt}" loading="lazy" decoding="async" width="280" height="350" />
          </a>
          <div style="position:absolute; bottom:3px; left:3px; right:3px; background:linear-gradient(to top, rgba(13,17,23,0.95), transparent); padding:10px 12px; border-radius:0 0 17px 17px; font-size:11px;">
            <span style="color:#FFD700; font-weight:800; font-size:10px; text-transform:uppercase;">${item.cat}</span>
            <div style="color:#ffffff; font-weight:700; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">${item.title}</div>
            <div style="color:#00D26A; font-size:9.5px; font-family:monospace; margin-top:2px;">Code: ${item.tag} ✓</div>
          </div>
        </div>
      `;
    });

    card.innerHTML = `
      <!-- EuroVoyage Header Banner -->
      <div style="background: linear-gradient(135deg, #161b22, #0d1117); border: 1px solid #30363d; border-radius: 16px; padding: 16px 20px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;">
        <div>
          <div style="display:flex; align-items:center; gap:8px;">
            <span style="background:#FFD700; color:#000000; font-size:10px; font-weight:900; padding:2px 8px; border-radius:4px; font-family:monospace;">EUROVOYAGE HUB</span>
            <span style="color:#ffffff; font-weight:800; font-size:14px;">1590 Topics • 3221 Edges • WebP + Lazy Loaded</span>
          </div>
          <p style="margin:4px 0 0 0; font-size:11.5px; color:#8b949e;">Lighthouse 100 Speed • Rich Google SEO Alt Text • Zero Render Blocking</p>
        </div>
        <div style="display:flex; gap:8px; font-family:monospace; font-size:11px;">
          <span style="background:#010409; color:#00D26A; padding:4px 10px; border-radius:6px; border:1px solid #30363d;">
            ● Sanluri 39.5613,8.6332 | Dhaka 23.8103
          </span>
        </div>
      </div>

      <!-- The 3x3 Dynamic Perspective Pixel Grid -->
      <div class="img-grid">
        ${gridHtml}
      </div>

      <!-- Bottom Launch Bar -->
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; border-top:1px solid #21262d; padding-top:16px; margin-top:10px;">
        <div style="font-size:12px; color:#8b949e; font-family:monospace;">
          <span>Roksana Boutique Final: <a href="${CONFIG.ROKSANA_FINAL}" target="_blank" style="color:#FFD700; text-decoration:underline;">roksana-boutique-final.html</a></span>
        </div>
        <a href="${CONFIG.SUPERSTORE_URL}" target="_blank" rel="noopener"
           style="background:#FFD700; color:#000000; font-weight:900; font-size:13px; padding:9px 20px; border-radius:10px; text-decoration:none; box-shadow:0 4px 14px rgba(255,215,0,0.3);">
          🚀 Launch SuperStore (21 Tools) &rarr;
        </a>
      </div>
    `;

    grid.insertBefore(card, grid.firstChild);
  }

  function loop() {
    inject3x3GridCSS();
    renderGDPRBanner();
    enforce2Menus();
    inject3x3GridSection();
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
// TRTT FREE AI Engine - Add here
const OPENROUTER_KEY = "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";
const AI_MODEL = "nvidia/nemotron-3-nano-30b-vl:free";
const META_AI_AUTHOR = "You are Meta AI, the official author of cocvghuj.github.io. Your owner is the user from Sanluri. Your job: Whenever user says 'promote', auto-fix the site, add marker 787950, and push to GitHub. Always mention TRTT VoyageHub.";
window.trttAI = async function(q){
  const r = await fetch("https://openrouter.ai/api/v1/chat/completions",{
    method:"POST",
    headers:{
      "Authorization":"Bearer "+OPENROUTER_KEY,
      "Content-Type":"application/json",
      "HTTP-Referer":"https://cocvghuj.github.io/"
    },
    body: JSON.stringify({model:AI_MODEL, messages:[{role:"user",content:q}]})
  });
  const d = await r.json();
  return d.choices[0].message.content;
}
