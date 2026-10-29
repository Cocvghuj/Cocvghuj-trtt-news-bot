/**
 * TRTT Auto-Sync Engine (AGGRESSIVE 2 SECTIONS ENFORCER)
 * EXACT 2 MENUS ONLY:
 * 1. Read The Blog (https://trttnews24bd.blogspot.com)
 * 2. Explore Your Life (https://cocvghuj-trtt-news-bot.vercel.app/?marker=787950&sub_id=explore_life_787950)
 *
 * COMPLETELY DELETES & HIDES ALL OLD MENUS (Global Insights, Europe & Schengen,
 * Business, Tech & Tools, Advertise, Guest Post, Free Tools, TRAVELPAYOUTS HUB, Insubuy)
 *
 * ALL LINKS: tp.st?marker=787950 | tlZcbMOB -> tIZcbMOB (Capital I) | Amazon: 4shg6Hn
 */
(function() {
  const CONFIG = {
    MARKER: '787950',
    PIN: '7879',
    BLOG_NAME: 'trttnews24bd',
    BLOG_SECRET_EMAIL: 'engrtaher2017.trttnews24bd@blogger.com',
    LOCATION: 'Sanluri',
    AMAZON: 'https://amzn.to/4shg6Hn',
    URL_READ_BLOG: 'https://trttnews24bd.blogspot.com',
    URL_EXPLORE_LIFE: 'https://cocvghuj-trtt-news-bot.vercel.app/?marker=787950&sub_id=explore_life_787950'
  };

  // =========================================================================
  // 1. AGGRESSIVE CSS OVERRIDE (Immediately Hides Old Menus via Stylesheet)
  // =========================================================================
  const styleId = 'trtt-strict-2-sections-style';
  if (!document.getElementById(styleId)) {
    const style = document.createElement('style');
    style.id = styleId;
    style.textContent = `
      /* Hide all old menu items by default */
      #main-menu-nav > li:not(.trtt-keep-2),
      .main-menu ul > li:not(.trtt-keep-2),
      #mobile-menu-list > li:not(.trtt-keep-2),
      .mobile-menu ul > li:not(.trtt-keep-2) {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
      }

      /* Clean modern styling for the 2 allowed sections */
      .trtt-keep-2 {
        display: inline-block !important;
        visibility: visible !important;
        opacity: 1 !important;
      }
      .trtt-keep-2 a {
        display: inline-flex !important;
        align-items: center !important;
        gap: 6px !important;
        font-family: system-ui, -apple-system, sans-serif !important;
        font-weight: 800 !important;
        font-size: 14.5px !important;
        letter-spacing: -0.2px !important;
        padding: 10px 18px !important;
        border-radius: 10px !important;
        text-decoration: none !important;
        transition: all 0.2s ease-in-out !important;
      }
      .trtt-btn-read a {
        background: #f1f5f9 !important;
        color: #052962 !important;
        border: 1px solid #cbd5e1 !important;
      }
      .trtt-btn-read a:hover {
        background: #e2e8f0 !important;
        color: #0284c7 !important;
      }
      .trtt-btn-explore a {
        background: #052962 !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(5,41,98,0.25) !important;
        border: 1px solid #052962 !important;
      }
      .trtt-btn-explore a:hover {
        background: #00A8E8 !important;
        border-color: #00A8E8 !important;
        transform: translateY(-1px) !important;
      }
    `;
    (document.head || document.documentElement).appendChild(style);
  }

  // =========================================================================
  // 2. AGGRESSIVE DOM ENFORCEMENT (Clears Old Menus & Injects Only 2 Sections)
  // =========================================================================
  function enforceExact2Sections() {
    const prohibitedWords = [
      'global insights',
      'europe & schengen',
      'schengen',
      'business',
      'tech & tools',
      'technology',
      'advertise with us',
      'guest post',
      'free tools',
      'travel cost',
      'calculator',
      'calcolo',
      'reisekosten',
      'travelpayouts',
      'hotels only',
      'flights only',
      'transport only',
      'car & bike',
      'tours & tickets',
      'insurance & compensation',
      'extras only',
      'insubuy',
      'booking.com',
      'agoda',
      'expedia',
      'hostelworld',
      'vrbo',
      'rakuten',
      'omio',
      '12go',
      'discovercars',
      'viator',
      'getyourguide',
      'ekta',
      'visitorscoverage',
      'airhelp',
      'compensair',
      'radical storage',
      'drimsim',
      'saily',
      'ticketmaster'
    ];

    // Find all menu list containers
    const menuContainers = document.querySelectorAll('#main-menu-nav, .main-menu ul, #navigation ul, .nav-menu, #mobile-menu-list, .mobile-menu ul');

    menuContainers.forEach(ul => {
      // 1. Hide/remove any old LI containing prohibited words
      const items = Array.from(ul.children);
      items.forEach(li => {
        const text = (li.innerText || li.textContent || '').toLowerCase().trim();
        const isRead = text.includes('read the blog') || text === 'read blog';
        const isExplore = text.includes('explore your life');

        if (!isRead && !isExplore) {
          li.style.setProperty('display', 'none', 'important');
          li.style.setProperty('visibility', 'hidden', 'important');
          // If prohibited, remove from DOM completely
          if (prohibitedWords.some(w => text.includes(w)) || text.startsWith('_')) {
            try { li.remove(); } catch (e) {}
          }
        }
      });

      // 2. Check if our 2 sections exist
      let hasRead = false;
      let hasExplore = false;
      Array.from(ul.children).forEach(li => {
        const txt = (li.innerText || li.textContent || '').trim();
        if (txt.includes('Read The Blog')) hasRead = true;
        if (txt.includes('Explore Your Life')) hasExplore = true;
      });

      // 3. Inject only the 2 sections if missing
      if (!hasRead || !hasExplore) {
        ul.innerHTML = `
          <li class="menu-item trtt-keep-2 trtt-btn-read" role="none" style="margin-right:8px;">
            <a href="${CONFIG.URL_READ_BLOG}" role="menuitem">
              <span>📝</span> <span>Read The Blog</span>
            </a>
          </li>
          <li class="menu-item trtt-keep-2 trtt-btn-explore" role="none">
            <a href="${CONFIG.URL_EXPLORE_LIFE}" role="menuitem" target="_blank" rel="noopener">
              <span>🚀</span> <span>Explore Your Life</span>
            </a>
          </li>
        `;
      }
    });
  }

  // =========================================================================
  // 3. STRICT AFFILIATE HYGIENE & TYPO FIXER
  // =========================================================================
  function enforceLinks() {
    // Enforce marker 787950 & fix typo tlZcbMOB to tIZcbMOB
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

    // Enforce Amazon 4shg6Hn
    document.querySelectorAll('a[href*="amzn.to"]').forEach(a => {
      if (!a.href.includes('4shg6Hn')) {
        a.href = CONFIG.AMAZON;
      }
    });
  }

  // =========================================================================
  // 4. TOP SUPER BAR INJECTION (Read The Blog + Explore Your Life)
  // =========================================================================
  function injectTopSuperBar() {
    if (document.getElementById('trtt-super-2sections-banner')) return;
    const target = document.querySelector('.main-wrapper, #main-wrapper, #Blog1, .blog-posts, main, #main');
    if (target) {
      const banner = document.createElement('div');
      banner.id = 'trtt-super-2sections-banner';
      banner.innerHTML = `
        <div style="background:#ffffff; border:2px solid #00A8E8; border-radius:16px; padding:18px 22px; margin:16px 0 24px 0; box-shadow:0 6px 20px rgba(0,168,232,0.1); font-family:system-ui,-apple-system,sans-serif;">
          <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #f1f5f9; padding-bottom:10px; margin-bottom:12px;">
            <div style="display:flex; align-items:center; gap:8px;">
              <span style="display:inline-block; width:10px; height:10px; border-radius:50%; background:#10b981;"></span>
              <strong style="color:#052962; font-size:16px;">TRTT Super App • Marker ${CONFIG.MARKER} Locked</strong>
            </div>
            <span style="font-size:11px; font-weight:800; background:#e0f2fe; color:#0369a1; padding:3px 10px; border-radius:9999px;">
              Via Carlo Felice ARST 08:17
            </span>
          </div>
          <p style="font-size:13.5px; font-weight:700; color:#0f172a; margin:0 0 14px 0;">
            Only App = Ticket আছে, Customer নাই • App + Blog = Customerও আছে, Ticketও আছে = Super App!
          </p>
          <div style="display:flex; gap:12px; flex-wrap:wrap;">
            <a href="${CONFIG.URL_READ_BLOG}" 
               style="display:inline-flex; align-items:center; gap:6px; background:#f1f5f9; color:#052962; font-weight:800; font-size:13.5px; padding:11px 20px; border-radius:10px; text-decoration:none; border:1px solid #cbd5e1;">
              <span>📝</span> <span>1. Read The Blog</span>
            </a>
            <a href="${CONFIG.URL_EXPLORE_LIFE}" target="_blank" rel="noopener"
               style="display:inline-flex; align-items:center; gap:6px; background:#052962; color:#ffffff; font-weight:800; font-size:13.5px; padding:11px 22px; border-radius:10px; text-decoration:none; box-shadow:0 4px 12px rgba(5,41,98,0.25);">
              <span>🚀</span> <span>2. Explore Your Life (Super App)</span>
            </a>
            <a href="${CONFIG.AMAZON}" target="_blank" rel="noopener"
               style="display:inline-flex; align-items:center; gap:6px; background:#fef3c7; border:1px solid #fde68a; color:#92400e; font-weight:800; font-size:13.5px; padding:11px 16px; border-radius:10px; text-decoration:none;">
              <span>🎒</span> <span>Amazon 4shg6Hn</span>
            </a>
          </div>
        </div>
      `;
      target.insertBefore(banner, target.firstChild);
    }
  }

  // =========================================================================
  // 5. SAFETY LOCKED DIRECT POSTING ENGINE
  // =========================================================================
  window.trttDirectPost = function(topic, htmlContent) {
    const badWords = ['sex', 'porn', 'casino', 'crypto scam', 'drugs', 'fake news'];
    if (badWords.some(w => topic.toLowerCase().includes(w))) {
      alert('🚫 Blocked: খারাপ টপিক! - ' + topic);
      return false;
    }

    const pin = prompt('🔒 TRTT Direct Post?\n\nTopic: ' + topic + '\n\nPIN দিন (' + CONFIG.PIN + '):\n\nSanluri থেকে Confirm করছেন?');
    if (pin !== CONFIG.PIN) {
      alert('❌ Wrong PIN - Post Cancelled!');
      return false;
    }

    if (!confirm('✅ Sanluri থেকে Confirm করছেন?\n\n📌 Topic: ' + topic + '\n\n📧 Post to: ' + CONFIG.BLOG_NAME + '\n🔒 Marker: ' + CONFIG.MARKER + ' Locked\n\nDirect Post করবেন?')) {
      return false;
    }

    const subject = topic.substring(0, 100);
    const body = htmlContent || `<div>${subject} - Marker ${CONFIG.MARKER} Locked</div>`;
    try {
      const mailtoLink = `mailto:${CONFIG.BLOG_SECRET_EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      window.open(mailtoLink, '_blank');
      alert('✅ Approved from Sanluri!\n\nEmail খোলা হচ্ছে: ' + CONFIG.BLOG_SECRET_EMAIL + '\n\nSend করলেই ব্লগে পোস্ট হবে!');
      return true;
    } catch (e) {
      alert('❌ Error: ' + e);
      return false;
    }
  };

  // Execution loop
  function loop() {
    enforceExact2Sections();
    injectTopSuperBar();
    enforceLinks();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loop);
  } else {
    loop();
  }

  setInterval(loop, 400);

  console.log(`%c 🔒 TRTT 2-Sections Enforcer Active | 1: Read The Blog | 2: Explore Your Life | Marker: ${CONFIG.MARKER} Locked `, 'background:#052962; color:#fff; padding:6px 12px; border-radius:6px; font-weight:bold;');
})();
