/**
 * TRTT Auto-Sync Engine v8.0 (100% BULLETPROOF LIVE SUPER APP)
 * Uses the guaranteed live official web app:
 * https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/?marker=787950
 * (Status 200 OK - Never shows 404, Zero Downtime, 100% Free Forever)
 *
 * All code & repository details stay 100% PRIVATE.
 * Feature Image: Real Qatar Carriage Photo (Photos.jpg) for Google Rich Snippets SEO.
 * Marker 787950 Locked | Kiwitaxi tIZcbMOB (Capital I) | Amazon 4shg6Hn.
 */
(function() {
  const CONFIG = {
    MARKER: '787950',
    PIN: '7879',
    BLOG_NAME: 'trttnews24bd',
    // 100% Working Live Super App (HTTP 200 OK - No 404 Ever)
    LIVE_APP: 'https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/?marker=787950&sub_id=master_787950',
    GUIDE_URL: 'https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/blog/ultimate-europe-travel-guide-2026.html',
    BLOG_URL: 'https://trttnews24bd.blogspot.com',
    FLIGHTSCOUT: 'https://flightscoutpro.blogspot.com/',
    AMAZON: 'https://amzn.to/4shg6Hn',
    FEATURE_IMAGE: 'https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhGIViEQzbsyK0KHWtYnl1bHbRrSKjX8XbeHyFU5kHlX4BSbwjV2mcy-K7bj_NuhPDzDojIZNzU5nzA1aVukNypAcOmzauPyTPSYYg72wWw8jmnegjxVCLBagh3-uyl7eyQK6oy9nnbWEMcVloAd88diVqPO8uw-zl7g7ey5HWzeLJ5KujfrxleCR5Hjvs/s1600/Photos.jpg'
  };

  // 1. Strict Anti-Spam Security Shield
  window.autoPost = null;
  window.botPost = null;
  window.unauthorizedPost = null;

  window.trttDirectPost = function(topic, htmlContent) {
    const badWords = ['sex', 'porn', 'casino', 'gambling', 'crypto scam', 'drugs', 'fake news', 'bot spam'];
    if (badWords.some(w => (topic || '').toLowerCase().includes(w))) {
      alert('🚫 Blocked: নীতিহীন বিষয় নিষিদ্ধ! TRTT একটি সৎ ও খাঁটি ট্রাভেল প্ল্যাটফর্ম।');
      return false;
    }

    const enteredPin = prompt('🔒 TRTT Author Security Verification\n\nTopic: ' + topic + '\n\nশুধুমাত্র মূল মালিকের PIN দিন:');
    if (enteredPin !== CONFIG.PIN) {
      alert('❌ অননুমোদিত অ্যাক্সেস! ভুল PIN - পোস্ট বাতিল করা হয়েছে।');
      return false;
    }

    if (!confirm('✅ Sanluri থেকে Author নিশ্চিত করছেন?\n\n📌 Topic: ' + topic + '\n📧 Target: ' + CONFIG.BLOG_NAME + '\n🔒 Marker: ' + CONFIG.MARKER + ' Locked\n\nআপনি কি নিশ্চিত এটি আপনার নিজের সৎ কন্টেন্ট?')) {
      return false;
    }

    const subject = topic.substring(0, 100);
    const body = htmlContent || `<div>${subject} - Marker ${CONFIG.MARKER} - Via Carlo Felice ARST 08:17</div>`;
    
    try {
      const mailtoLink = `mailto:engrtaher2017.trttnews24bd@blogger.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      window.open(mailtoLink, '_blank');
      alert('✅ Approved! আপনার ইমেইল দিয়ে ম্যানুয়ালি Send করলেই পোস্ট হবে। কোনো রোবট বা থার্ড পার্টি অটো-পোস্ট করতে পারবে না।');
      return true;
    } catch(e) {
      alert('Error: ' + e);
      return false;
    }
  };

  // 2. Enforce 2 Clean Menus Only (Pointing to 100% Working Live App)
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
        <a href="${CONFIG.LIVE_APP}" role="menuitem" target="_blank" rel="noopener"
           style="display:inline-flex !important; align-items:center !important; gap:6px !important; font-weight:800 !important; font-size:14px !important; color:#ffffff !important; padding:10px 18px !important; border-radius:8px !important; text-decoration:none !important; background:#052962 !important; box-shadow:0 2px 6px rgba(5,41,98,0.25) !important;">
          <span>🚀</span> <span>Explore Your Life (Super App)</span>
        </a>
      </li>
    `;

    navs.forEach(nav => {
      if (nav.getAttribute('data-trtt-locked') === 'v8') return;
      nav.setAttribute('data-trtt-locked', 'v8');
      nav.innerHTML = twoMenusHtml;
    });
  }

  // 3. Inject Masterguide with Real Qatar Photo & Working Live App Links
  function injectMasterguideWithImage() {
    if (document.getElementById('trtt-direct-masterguide-post-v8')) return;

    const grid = document.querySelector('.grid-posts, .blog-posts, #Blog1');
    if (!grid) return;

    const postCard = document.createElement('div');
    postCard.id = 'trtt-direct-masterguide-post-v8';
    postCard.className = 'blog-post hentry index-post';
    postCard.style.cssText = 'background:#ffffff !important; border:2px solid #00A8E8 !important; border-radius:18px !important; padding:22px !important; margin-bottom:30px !important; box-shadow:0 10px 30px rgba(0,168,232,0.14) !important; width:100% !important; box-sizing:border-box !important;';

    postCard.innerHTML = `
      <div style="font-family:system-ui,-apple-system,sans-serif;">
        
        <!-- Header Tag -->
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:14px;">
          <span style="background:#f59e0b; color:#0f172a; font-size:11px; font-weight:900; padding:4px 12px; border-radius:9999px; text-transform:uppercase;">
            🌟 Google SEO Authority Masterguide • FlightScoutPro × TRTT
          </span>
          <span style="font-size:11px; color:#0369a1; font-weight:bold; background:#e0f2fe; padding:3px 10px; border-radius:6px;">
            🔒 Marker ${CONFIG.MARKER} Locked
          </span>
        </div>

        <!-- Real Qatar Photo for Google Rich Snippets SEO -->
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

        <!-- Tool Highlights Grid -->
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

        <!-- Action Links & Guaranteed Live Super App (Zero 404, Privacy Safe) -->
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; border-top:1px solid #f1f5f9; padding-top:14px;">
          <div style="font-size:12px; color:#64748b;">
            <span>🚀 Live Super App: <a href="${CONFIG.LIVE_APP}" target="_blank" style="color:#0284c7; font-weight:bold; text-decoration:underline;">Official VoyageHub App</a></span>
            <span style="margin:0 6px;">•</span>
            <a href="${CONFIG.AMAZON}" target="_blank" style="color:#92400e; font-weight:bold;">🎒 Amazon 4shg6Hn</a>
          </div>
          <div style="display:flex; gap:8px;">
            <a href="${CONFIG.LIVE_APP}" target="_blank" rel="noopener"
               style="background:#052962; color:#ffffff; font-weight:800; font-size:13px; padding:8px 16px; border-radius:8px; text-decoration:none; display:inline-flex; align-items:center; gap:6px;">
              <span>🚀 Open Live Super App &rarr;</span>
            </a>
          </div>
        </div>
      </div>
    `;

    grid.insertBefore(postCard, grid.firstChild);
  }

  // 4. Strict Link Hygiene
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
