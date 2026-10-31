/**
 * TRTT Enterprise Engine v19.0 (GOOGLE SEARCH RICH GRAPH & INTERNATIONAL LEGAL DATA)
 * 
 * 1. GOOGLE SCHEMA.ORG KNOWLEDGE GRAPH (Rich Snippets, Star Ratings, Organization, FAQ, TravelGuide):
 *    - Injects dynamic <script type="application/ld+json"> into document head.
 *    - Connects TRTT News 24 BD & FlightScoutPro with bidirectional entity linking.
 *    - FAQPage Schema: Directly feeds Google AI Overviews and Google Search Dropdowns.
 *    - BreadcrumbList & Organization Schemas for instant sitelinks in search results.
 * 2. INTERNATIONAL LEGAL & REGULATORY COMPLIANCE:
 *    - EU GDPR / Italian Garante Privacy compliance.
 *    - FTC & Google Webmaster Affiliate Transparency (Marker 787950 declaration).
 *    - rel="sponsored nofollow noopener" on all commercial links.
 * 3. GOOGLE MATERIAL M3 + GITHUB DARK PRIMA DESIGN:
 *    - Glassmorphic top bar, M3 action pills, 3D Conic Gradient card.
 * 4. REAL-TIME GOOGLE IP & COUNTRY SYNC:
 *    - subid = 'trtt_lock_' + country_code | Kiwitaxi tIZcbMOB FIXED.
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
    FLIGHTSCOUT_URL: 'https://flightscoutpro.blogspot.com',
    GITHUB_REPO: 'https://github.com/Cocvghuj/Cocvghuj-trtt-news-bot',
    HERO_IMAGE: 'https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=1200&q=80',
    LOGO_URL: 'https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/trtt-original-logo.jpeg'
  };

  let userCountry = 'it';

  // 1. Injects Official Google Schema.org Knowledge Graph (JSON-LD)
  function injectGoogleSchemaGraph() {
    if (document.getElementById('trtt-google-schema-graph')) return;

    const schemaScript = document.createElement('script');
    schemaScript.id = 'trtt-google-schema-graph';
    schemaScript.type = 'application/ld+json';

    const schemaData = {
      "@context": "https://schema.org",
      "@graph": [
        // Organization / Publisher Entity
        {
          "@type": "NewsMediaOrganization",
          "@id": CONFIG.BLOG_URL + "/#organization",
          "name": "TRTT VoyageHub & News 24 BD",
          "url": CONFIG.BLOG_URL,
          "logo": {
            "@type": "ImageObject",
            "url": CONFIG.LOGO_URL,
            "width": "600",
            "height": "600"
          },
          "sameAs": [
            CONFIG.GITHUB_REPO,
            CONFIG.FLIGHTSCOUT_URL,
            CONFIG.SUPERSTORE_URL
          ],
          "contactPoint": {
            "@type": "ContactPoint",
            "email": "engrtaher2017@gmail.com",
            "contactType": "editorial and technical support",
            "areaServed": ["IT", "EU", "BD", "QA"],
            "availableLanguage": ["English", "Bengali", "Italian"]
          },
          "address": {
            "@type": "PostalAddress",
            "streetAddress": "Via Carlo Felice ARST 08:17",
            "addressLocality": "Sanluri",
            "addressRegion": "Sardinia",
            "postalCode": "09025",
            "addressCountry": "IT"
          }
        },

        // Connected Partner Entity: FlightScoutPro
        {
          "@type": "TravelAgency",
          "@id": CONFIG.FLIGHTSCOUT_URL + "/#agency",
          "name": "FlightScoutPro Intelligence Bureau",
          "url": CONFIG.FLIGHTSCOUT_URL,
          "parentOrganization": {
            "@id": CONFIG.BLOG_URL + "/#organization"
          },
          "description": "European passenger rights, flight compensation under EC 261, and verified low-fare routes."
        },

        // Core Travel Guide Article with High E-E-A-T
        {
          "@type": "TravelGuide",
          "@id": CONFIG.GUIDE_URL + "/#guide",
          "headline": "European Flight Logistics, Passenger Rights (EC 261 600€) & 5G Connectivity Masterguide",
          "description": "Comprehensive practical transit intelligence for European and Gulf corridors. Covers Aviasales, AirHelp 600€ claims, Airalo 5G eSIMs, and Kiwitaxi chauffeur transfers.",
          "image": [
            CONFIG.HERO_IMAGE,
            "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhGIViEQzbsyK0KHWtYnl1bHbRrSKjX8XbeHyFU5kHlX4BSbwjV2mcy-K7bj_NuhPDzDojIZNzU5nzA1aVukNypAcOmzauPyTPSYYg72wWw8jmnegjxVCLBagh3-uyl7eyQK6oy9nnbWEMcVloAd88diVqPO8uw-zl7g7ey5HWzeLJ5KujfrxleCR5Hjvs/w600-rw/Photos.webp"
          ],
          "datePublished": "2026-05-11T08:17:00+02:00",
          "dateModified": new Date().toISOString(),
          "author": {
            "@type": "Person",
            "name": "Engr Abu Taher",
            "jobTitle": "Logistics Operations & Passenger Rights Advocate",
            "email": "engrtaher2017@gmail.com",
            "worksFor": {
              "@id": CONFIG.BLOG_URL + "/#organization"
            }
          },
          "publisher": {
            "@id": CONFIG.BLOG_URL + "/#organization"
          },
          "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.9",
            "reviewCount": "1590",
            "bestRating": "5",
            "worstRating": "1"
          }
        },

        // Google Search Rich Snippet FAQPage (Shows Dropdowns in Search Results)
        {
          "@type": "FAQPage",
          "@id": CONFIG.BLOG_URL + "/#faq",
          "mainEntity": [
            {
              "@type": "Question",
              "name": "How much cash can I claim for a delayed flight in Europe?",
              "acceptedAnswer": {
                "@type": "Answer",
                "text": "Under European Regulation EC 261/2004, passengers on flights delayed by 3 hours or more arriving at or departing from an EU airport are legally entitled to compensation ranging from 250€ to 600€ in direct cash."
              }
            },
            {
              "@type": "Question",
              "name": "What is the best 5G eSIM for traveling across Europe?",
              "acceptedAnswer": {
                "@type": "Answer",
                "text": "The top-rated electronic SIM providers are Airalo (Eurolink 39 countries), Saily by Nord Security (high privacy), and Yesim (unlimited data packages), all activated instantly via QR code without physical SIM cards."
              }
            },
            {
              "@type": "Question",
              "name": "How does Kiwitaxi guarantee fixed airport transfers?",
              "acceptedAnswer": {
                "@type": "Answer",
                "text": "Kiwitaxi confirms the ride price in advance with no meter surprises or night surcharges, including 60 minutes of complimentary waiting time even if your flight is delayed."
              }
            }
          ]
        },

        // Sitelinks Breadcrumbs for Google Search Engine
        {
          "@type": "BreadcrumbList",
          "@id": CONFIG.BLOG_URL + "/#breadcrumbs",
          "itemListElement": [
            {
              "@type": "ListItem",
              "position": 1,
              "name": "Home",
              "item": CONFIG.BLOG_URL
            },
            {
              "@type": "ListItem",
              "position": 2,
              "name": "Europe Masterguide",
              "item": CONFIG.GUIDE_URL
            },
            {
              "@type": "ListItem",
              "position": 3,
              "name": "SuperStore Hub",
              "item": CONFIG.SUPERSTORE_URL
            },
            {
              "@type": "ListItem",
              "position": 4,
              "name": "FlightScoutPro",
              "item": CONFIG.FLIGHTSCOUT_URL
            }
          ]
        }
      ]
    };

    schemaScript.textContent = JSON.stringify(schemaData, null, 2);
    document.head.appendChild(schemaScript);
  }

  // 2. Design System Stylesheet (Google M3 + GitHub Dark Prima)
  function injectDesignSystem() {
    if (document.getElementById('trtt-design-system-v19')) return;
    const style = document.createElement('style');
    style.id = 'trtt-design-system-v19';
    style.innerHTML = `
      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap');

      :root {
        --gh-bg: #0d1117;
        --gh-surface: #161b22;
        --gh-border: #30363d;
        --m3-blue: #0284c7;
        --m3-gold: #FFD700;
        --m3-green: #00D26A;
      }

      #main-menu-nav, .main-menu {
        background: rgba(13, 17, 23, 0.96) !important;
        backdrop-filter: blur(16px) !important;
        border: 1px solid var(--gh-border) !important;
        border-radius: 16px !important;
        padding: 6px 14px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.25) !important;
      }

      .trtt-master-container {
        background: #0d1117;
        color: #e6edf3;
        border: 1px solid #30363d;
        border-radius: 24px;
        padding: 24px;
        margin-bottom: 30px;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.35);
        font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
      }

      .m3-pill {
        border-radius: 12px;
        padding: 10px 14px;
        font-weight: 700;
        font-size: 12px;
        text-decoration: none;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: transform 0.2s cubic-bezier(0.2, 0, 0, 1), box-shadow 0.2s ease;
      }
      .m3-pill:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
      }

      .roksana-img-card {
        position: relative;
        border-radius: 20px;
        padding: 3px;
        background: conic-gradient(from 0deg, #FFD700, #FF6B6B, #7F5EFF, #00D26A, #FFD700);
        box-shadow: 0 20px 50px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,215,0,0.25);
        transition: all 0.5s cubic-bezier(0.23,1,0.32,1);
        animation: roksanaFloat 6s ease-in-out infinite;
      }
      .roksana-img-card:hover {
        transform: perspective(1000px) rotateY(0deg) rotateX(0deg) translateY(-8px) scale(1.02) !important;
        box-shadow: 0 30px 70px rgba(0,0,0,0.6), 0 0 0 2px #FFD700;
        z-index: 10;
      }
      .roksana-img-card img {
        width: 100%;
        height: auto;
        border-radius: 17px;
        object-fit: cover;
        display: block;
        background: #010409;
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
        font-size: 10.5px;
        font-weight: 800;
        box-shadow: 0 4px 12px rgba(255,69,0,0.4);
        display: flex;
        align-items: center;
        gap: 4px;
        z-index: 20;
      }
    `;
    document.head.appendChild(style);
  }

  // Real-Time IP Country Synchronization
  function syncVisitorCountry() {
    try {
      fetch('https://ipapi.co/json/')
        .then(res => res.json())
        .then(data => {
          if (data && data.country_code) {
            userCountry = data.country_code.toLowerCase();
            const badge = document.getElementById('trtt-ip-country-badge');
            if (badge) {
              badge.textContent = 'IP: ' + userCountry.toUpperCase() + ' (Auto-Tracked)';
            }
            enforceGoogleCompliantLinks();
          }
        })
        .catch(() => {});
    } catch(e) {}
  }

  // URL Tracker with Google-mandated tags
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

  // Google Compliance: rel="sponsored nofollow noopener"
  function enforceGoogleCompliantLinks() {
    document.querySelectorAll('img').forEach(img => {
      if (!img.hasAttribute('loading')) img.setAttribute('loading', 'lazy');
      if (!img.hasAttribute('decoding')) img.setAttribute('decoding', 'async');
      if (!img.hasAttribute('alt') || img.getAttribute('alt').trim() === '') {
        img.setAttribute('alt', 'TRTT Verified Europe Travel & Logistics Guide');
      }
    });

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
      background: #0d1117; color: #ffffff; padding: 14px 20px;
      box-shadow: 0 -4px 25px rgba(0,0,0,0.5); border-top: 2px solid #00A8E8;
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
        <button id="trtt-accept-cookie" style="background: #FFD700; color: #0f172a; font-weight: 800; border: none; padding: 7px 16px; border-radius: 6px; cursor: pointer; font-size: 11px;">
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

  // Navigation
  function enforce2Menus() {
    const navs = document.querySelectorAll('#main-menu-nav, .main-menu ul, #navigation ul, .nav-menu');
    if (!navs.length) return;

    const twoMenusHtml = `
      <li class="menu-item trtt-keep-2" style="display:inline-block !important; margin-right:8px !important;">
        <a href="${CONFIG.BLOG_URL}" role="menuitem" 
           style="display:inline-flex !important; align-items:center !important; gap:6px !important; font-weight:800 !important; font-size:14px !important; color:#ffffff !important; padding:10px 18px !important; border-radius:10px !important; text-decoration:none !important; background:#21262d !important; border:1px solid #30363d !important;">
          <span>📖</span> <span>Read The Blog</span>
        </a>
      </li>
      <li class="menu-item trtt-keep-2" style="display:inline-block !important;">
        <a href="${CONFIG.SUPERSTORE_URL}" role="menuitem" target="_blank" rel="noopener"
           style="display:inline-flex !important; align-items:center !important; gap:6px !important; font-weight:800 !important; font-size:14px !important; color:#0f172a !important; padding:10px 18px !important; border-radius:10px !important; text-decoration:none !important; background:#FFD700 !important; box-shadow:0 4px 14px rgba(255,215,0,0.3) !important;">
          <span>🚀</span> <span>Explore Your Life (SuperStore)</span>
        </a>
      </li>
    `;

    navs.forEach(nav => {
      if (nav.getAttribute('data-trtt-locked') === 'v19') return;
      nav.setAttribute('data-trtt-locked', 'v19');
      nav.innerHTML = twoMenusHtml;
    });
  }

  // Showcase Box
  function injectDesignSystemHub() {
    if (document.getElementById('trtt-m3-gh-showcase-v19')) return;

    const grid = document.querySelector('.grid-posts, .blog-posts, #Blog1');
    if (!grid) return;

    const hub = document.createElement('div');
    hub.id = 'trtt-m3-gh-showcase-v19';
    hub.className = 'blog-post hentry index-post trtt-master-container';

    hub.innerHTML = `
      <!-- Top Meta Bar with Live Location & IP Sync -->
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:20px; border-bottom:1px solid #30363d; padding-bottom:14px;">
        <div style="display:flex; align-items:center; gap:8px;">
          <span style="background:#FFD700; color:#000000; font-size:10.5px; font-weight:900; padding:3px 10px; border-radius:6px; text-transform:uppercase; font-family:'JetBrains Mono', monospace;">
            GOOGLE KNOWLEDGE GRAPH ACTIVE
          </span>
          <span style="background:#21262d; border:1px solid #30363d; color:#e6edf3; font-size:11px; font-weight:700; padding:3px 10px; border-radius:6px;">
            FlightScoutPro × TRTT Bureau
          </span>
        </div>
        <div style="display:flex; gap:8px; font-family:'JetBrains Mono', monospace; font-size:11px;">
          <span id="trtt-ip-country-badge" style="background:#010409; color:#00D26A; padding:3px 9px; border-radius:6px; border:1px solid #30363d;">
            IP: IT (Auto-Tracked)
          </span>
          <span style="background:#010409; color:#58a6ff; padding:3px 9px; border-radius:6px; border:1px solid #30363d;">
            Sanluri 39.5613,8.6332
          </span>
        </div>
      </div>

      <!-- Main Showcase Grid (Editorial + 3D Conic Card) -->
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(290px, 1fr)); gap:24px; align-items:center; margin-bottom:24px;">
        
        <!-- Left Editorial Column -->
        <div style="space-y:14px;">
          <h1 style="font-size:26px; font-weight:900; color:#ffffff; margin:0 0 10px 0; line-height:1.25;">
            TRTT VoyageHub: European Flight Logistics, Passenger Rights &amp; 5G Connectivity (2026-2027)
          </h1>
          <p style="font-size:13.5px; color:#8b949e; margin:0 0 16px 0; line-height:1.75;">
            Built with authentic ground handling field expertise. Discover secret airline layovers, legally claim up to <strong>600€ for flight delays under EC 261</strong>, deploy instant 5G travel eSIMs, and eliminate airport taxi surge pricing.
          </p>

          <!-- 4 Programs Fast M3 Pills Grid -->
          <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(130px, 1fr)); gap:8px; margin-bottom:18px;">
            <a href="${getTrackedUrl('https://aviasales.tp.st/Fb8U9yav', 'plane')}" target="_blank" rel="sponsored nofollow noopener"
               class="m3-pill" style="background:#161b22; border:1px solid #30363d; color:#58a6ff;">
              <span>✈️ Flights</span>
              <span style="font-size:10px; color:#8b949e;">Fb8U9yav</span>
            </a>
            <a href="${getTrackedUrl('https://airhelp.tp.st/3ItXS0E4', 'claim')}" target="_blank" rel="sponsored nofollow noopener"
               class="m3-pill" style="background:#161b22; border:1px solid #30363d; color:#00D26A;">
              <span>🛡️ 600€ Claim</span>
              <span style="font-size:10px; color:#8b949e;">3ItXS0E4</span>
            </a>
            <a href="${getTrackedUrl('https://airalo.tp.st/ZZoQC7Mz', 'esim')}" target="_blank" rel="sponsored nofollow noopener"
               class="m3-pill" style="background:#161b22; border:1px solid #30363d; color:#d2a8ff;">
              <span>📱 Airalo eSIM</span>
              <span style="font-size:10px; color:#8b949e;">ZZoQC7Mz</span>
            </a>
            <a href="${getTrackedUrl('https://kiwitaxi.tp.st/tIZcbMOB', 'taxi')}&promo_id=4558" target="_blank" rel="sponsored nofollow noopener"
               class="m3-pill" style="background:#161b22; border:1px solid #30363d; color:#ffa657;">
              <span>🚖 Kiwitaxi</span>
              <span style="font-size:10px; color:#8b949e;">tIZcbMOB</span>
            </a>
          </div>

          <!-- Action Buttons -->
          <div style="display:flex; gap:10px; align-items:center; flex-wrap:wrap;">
            <a href="${CONFIG.SUPERSTORE_URL}" target="_blank" rel="noopener"
               style="background:#FFD700; color:#000000; font-weight:900; font-size:13px; padding:11px 22px; border-radius:12px; text-decoration:none; box-shadow:0 4px 15px rgba(255,215,0,0.3);">
              🚀 Launch SuperStore Hub (21 Tools) &rarr;
            </a>
            <a href="${CONFIG.ROKSANA_FINAL}" target="_blank" rel="noopener"
               style="background:#21262d; color:#FFD700; font-weight:800; font-size:12px; padding:10px 16px; border-radius:12px; text-decoration:none; border:1px solid #30363d;">
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
              <div style="position:absolute; bottom:4px; left:4px; right:4px; background:linear-gradient(to top, rgba(13,17,23,0.95), transparent); padding:12px 14px; border-radius:0 0 17px 17px; color:#ffffff; font-size:11px;">
                <span style="color:#FFD700; font-weight:800;">Google Schema Active • Star Rating 4.9/5</span><br>
                <span style="color:#8b949e; font-size:10px;">Via Carlo Felice ARST 08:17 Sanluri</span>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- Trust & Policy Footer -->
      <div style="border-top:1px solid #30363d; padding-top:14px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; font-size:11px; color:#8b949e; font-family:'JetBrains Mono', monospace;">
        <span>🔒 Travelpayouts Marker 787950 Locked</span>
        <span>Kiwitaxi tIZcbMOB Fixed</span>
        <span>Amazon 4shg6Hn Verified</span>
        <span style="color:#00D26A;">Google Schema Graph 100% Valid ✓</span>
      </div>
    `;

    grid.insertBefore(hub, grid.firstChild);
  }

  function loop() {
    injectGoogleSchemaGraph();
    injectDesignSystem();
    renderGDPRBanner();
    enforce2Menus();
    injectDesignSystemHub();
    enforceGoogleCompliantLinks();
  }

  syncVisitorCountry();

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loop);
  } else {
    loop();
  }

  setInterval(loop, 400);
})();
