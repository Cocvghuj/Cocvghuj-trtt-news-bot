/*! TRTT VOYAGE — THINKING ROOM / V106 — GOOGLE-STYLE AI ANSWER ENGINE (TEAM MAGIC ROKSANA EDITION)
 * Marker: TRTT MAGIC-787950 ROKSANA LOCKED
 * Team: Muse (CEO), Abu Taher (Publisher & Founder), Gemini & Google AI Studio (Intelligence), ChatGPT (Developer)
 * Language: English (Global Standard)
 */
(function () {
  "use strict";

  if (window.__TRTT_APP_106_ACTIVE__) return;
  window.__TRTT_APP_106_ACTIVE__ = true;

  var ROUTES = [
    ["Home", "Start here", "/"],
    ["My Diary", "Personal journal", "/search/label/My%20Diary"],
    ["Flight", "Flight search & claims", "/search/label/Flight"],
    ["Ride", "Taxi & airport rides", "/search/label/Ride"],
    ["eSIM", "Global 5G data", "/search/label/eSIM"],
    ["Tour", "Activities & tickets", "/search/label/Tour"],
    ["Shop", "TRTT Travel Shop", "/search/label/Shop"],
    ["Night", "Night & lounge services", "/search/label/Night"]
  ];

  var SERVICES_21 = [
    { name: "Aviasales", cat: "Flights", domain: "aviasales.com", icon: "✈️", url: "https://aviasales.tpo.lv/Fb8U9yav?marker=787950", desc: "Compare low fares across 1,000+ airlines & global travel sites." },
    { name: "AirHelp", cat: "600€ Claim", domain: "airhelp.com", icon: "⚖️", url: "https://airhelp.tpo.lv/3ItXS0E4?marker=787950", desc: "Claim up to €600 compensation for delayed, cancelled or overbooked flights." },
    { name: "Compensair", cat: "EU Claim", domain: "compensair.com", icon: "🛡️", url: "https://compensair.tpo.lv/YgVXgRnB?marker=787950", desc: "No-win-no-fee European passenger rights compensation enforcement." },
    { name: "Kiwitaxi", cat: "Taxi/Transfer", domain: "kiwitaxi.com", icon: "🚕", url: "https://kiwitaxi.tpo.lv/tIZcbMOB?marker=787950", desc: "Fixed-rate airport transfers & door-to-door chauffeured rides worldwide." },
    { name: "GetTransfer", cat: "Chauffeured", domain: "gettransfer.com", icon: "🚘", url: "https://gettransfer.tpo.lv/1u8zRU5s?marker=787950", desc: "Worldwide transfer bookings with driver bidding for lowest prices." },
    { name: "Intui.travel", cat: "Airport Ride", domain: "intui.travel", icon: "🚐", url: "https://intui.tpo.lv/tiSkz4Yq?marker=787950", desc: "Global airport shuttle, minivan, and VIP private car transfers." },
    { name: "Welcome Pickups", cat: "Pickups", domain: "welcomepickups.com", icon: "📍", url: "https://tpo.lv/h3LrTZcS?marker=787950", desc: "English-speaking drivers, curated local tips, and personalized meet & greet." },
    { name: "Localrent", cat: "Car Rental", domain: "localrent.com", icon: "🚗", url: "https://localrent.tpo.lv/4jd1IRQG?marker=787950", desc: "Best local car hire in Europe & Mediterranean with low deposits." },
    { name: "EconomyBookings", cat: "Car Rental", domain: "economybookings.com", icon: "🚙", url: "https://economybookings.tpo.lv/pyHqRiOo?marker=787950", desc: "Worldwide car rental comparison with transparent pricing and top brands." },
    { name: "QEEQ", cat: "Deals & Cars", domain: "qeeq.com", icon: "🏎️", url: "https://qeeq.tpo.lv/HKhCeDhY?marker=787950", desc: "Car rentals featuring price-drop refund protection and VIP discounts." },
    { name: "Airalo", cat: "Global eSIM", domain: "airalo.com", icon: "📶", url: "https://airalo.tpo.lv/ZZoQC7Mz?marker=787950", desc: "Digital 5G travel eSIMs for 200+ countries with instant QR activation." },
    { name: "Yesim", cat: "Travel eSIM", domain: "yesim.app", icon: "📲", url: "https://yesim.tpo.lv/krzFKLpg?marker=787950", desc: "High-speed and unlimited data eSIM plans for Europe and overseas trips." },
    { name: "Drimsim", cat: "Universal SIM", domain: "drimsim.com", icon: "🌐", url: "https://drimsim.tpo.lv/Ly7ywlY8?marker=787950", desc: "Universal physical SIM & eSIM connecting you seamlessly across borders." },
    { name: "Saily", cat: "Nord eSIM", domain: "saily.com", icon: "🛡️", url: "https://saily.tpo.lv/ssekmS4X?marker=787950", desc: "Secure international travel eSIM powered by the creators of NordVPN." },
    { name: "Tiqets", cat: "Tickets", domain: "tiqets.com", icon: "🎟️", url: "https://tiqets.tpo.lv/bnx8pnF6?marker=787950", desc: "Instant mobile admission to famous museums, castles, and historic venues." },
    { name: "Klook", cat: "Tours & Transit", domain: "klook.com", icon: "🎢", url: "https://klook.tpo.lv/TWKnemhz?marker=787950", desc: "Theme park passes, bullet trains, day tours, and outdoor adventures." },
    { name: "Go City", cat: "City Passes", domain: "gocity.com", icon: "🎫", url: "https://gocity.tpo.lv/QSQw8FwU?marker=787950", desc: "All-inclusive multi-attraction city passes saving up to 50% on sightseeing." },
    { name: "KKday", cat: "Experiences", domain: "kkday.com", icon: "🗺️", url: "https://kkday.tpo.lv/JaAfTgGF?marker=787950", desc: "Curated local experiences, island hopping, and authentic travel activities." },
    { name: "Radical Storage", cat: "Luggage", domain: "radicalstorage.com", icon: "🧳", url: "https://radicalstorage.tpo.lv/WkGqxIsD?marker=787950", desc: "Secure luggage storage near train stations, airports, and city hubs worldwide." },
    { name: "Amazon Flight Gear", cat: "Travel Gear", domain: "amazon.com", icon: "🎒", url: "https://amzn.to/4shg6Hn?marker=787950", desc: "Curated flight backpacks, carry-on bags, power banks, and accessories." },
    { name: "SuperStore Portal", cat: "21-in-1 Hub", domain: "vercel.app", icon: "🚀", url: "https://cocvghuj-trtt-news-bot.vercel.app/?marker=787950", desc: "Complete 21-in-1 travel dashboard uniting all verified tools under one roof." }
  ];

  var QUICK_PROMPTS = [
    { label: "✈️ €600 Flight Delay Claim", query: "How do I claim €600 for a delayed or cancelled flight under EU Regulation EC 261?" },
    { label: "📶 Best 5G Travel eSIM", query: "Which eSIM is best for international travel and avoiding roaming charges?" },
    { label: "🏛️ Sanluri to Cagliari Airport", query: "What is the best way to travel from Sanluri to Cagliari Elmas Airport (CAG)?" },
    { label: "🚖 Trusted Airport Taxi", query: "How can I book a reliable airport transfer or chauffeured taxi in advance?" }
  ];

  function node(tag, className, value) {
    var el = document.createElement(tag);
    if (className) el.className = className;
    if (value !== undefined) el.textContent = value;
    return el;
  }

  function makeRoute(tuple) {
    var a = node("a", "trtt-route-bubble");
    a.href = tuple[2];
    a.appendChild(node("strong", "", tuple[0]));
    a.appendChild(node("span", "", tuple[1]));
    return a;
  }

  function findMount() {
    return document.querySelector("#header-wrap .header-menu") ||
      document.querySelector("#header-wrap #main-menu");
  }

  function openRoom() {
    var overlay = document.getElementById("trtt-room-overlay-106");
    if (!overlay) {
      overlay = buildRoomOverlay();
      document.body.appendChild(overlay);
    }
    overlay.classList.add("is-active");
    document.documentElement.classList.add("trtt-room-open");
    var input = overlay.querySelector(".trtt-google-search-input");
    if (input) setTimeout(function () { input.focus(); }, 120);
  }

  function closeRoom() {
    var overlay = document.getElementById("trtt-room-overlay-106");
    if (overlay) {
      overlay.classList.remove("is-active");
      document.documentElement.classList.remove("trtt-room-open");
    }
  }

  function formatAnswerText(text) {
    var container = node("div", "trtt-ai-text-body");
    var lines = text.split("\n");
    var ul = null;

    lines.forEach(function (line) {
      var trimmed = line.trim();
      if (!trimmed) {
        ul = null;
        return;
      }
      if (trimmed.indexOf("• ") === 0 || trimmed.indexOf("- ") === 0 || trimmed.indexOf("* ") === 0) {
        if (!ul) {
          ul = node("ul", "trtt-ai-bullet-list");
          container.appendChild(ul);
        }
        var li = node("li", "", trimmed.replace(/^([•\-\*]\s*)/, ""));
        ul.appendChild(li);
      } else {
        ul = null;
        var p = node("p", "trtt-ai-para", trimmed);
        container.appendChild(p);
      }
    });

    return container;
  }

  function getFallbackAnswer(query) {
    var q = query.toLowerCase();
    var ans = "";
    var matched = [SERVICES_21[0], SERVICES_21[1], SERVICES_21[10]];

    if (q.indexOf("claim") !== -1 || q.indexOf("delay") !== -1 || q.indexOf("600") !== -1 || q.indexOf("cancel") !== -1 || q.indexOf("compens") !== -1) {
      ans = "Under EU Regulation EC 261/2004, passengers are legally entitled to between €250 and €600 compensation if their flight arrives 3+ hours late or is cancelled less than 14 days prior to departure.\n\n" +
        "• Short haul (<1,500 km): €250 compensation per passenger.\n" +
        "• Medium haul (1,500 km - 3,500 km): €400 compensation.\n" +
        "• Long haul (>3,500 km): Up to €600 compensation.\n" +
        "• No Win, No Fee: Check your claim in 2 minutes via AirHelp or Compensair with zero upfront risk.";
      matched = [SERVICES_21[1], SERVICES_21[2], SERVICES_21[0]];
    } else if (q.indexOf("esim") !== -1 || q.indexOf("sim") !== -1 || q.indexOf("data") !== -1 || q.indexOf("internet") !== -1 || q.indexOf("roam") !== -1) {
      ans = "Travel eSIMs eliminate expensive roaming charges by providing instant 4G/5G data connectivity upon arrival in over 200 countries.\n\n" +
        "• Airalo: World leader in prepaid regional & local country eSIMs.\n" +
        "• Yesim: High-speed unlimited data packages for Europe and global hubs.\n" +
        "• Saily: Ultra-secure travel eSIM developed by the creators of NordVPN.\n" +
        "• Quick Setup: Scan a QR code before departure or on airport Wi-Fi to activate in minutes.";
      matched = [SERVICES_21[10], SERVICES_21[11], SERVICES_21[13]];
    } else if (q.indexOf("sanluri") !== -1 || q.indexOf("cagliari") !== -1 || q.indexOf("sardinia") !== -1 || q.indexOf("cag") !== -1) {
      ans = "Sanluri is a medieval jewel in southern Sardinia, connected to Cagliari and the rest of the island via the modern SS131 Carlo Felice express highway.\n\n" +
        "• Transit to Cagliari Airport (CAG): Approximately 35 minutes by car or regional Trenitalia from Sanluri Stato.\n" +
        "• Flight Connections: Direct low-cost flights from Cagliari Elmas (CAG) to Milan (BGY/MXP), Rome (FCO), Barcelona, and London.\n" +
        "• Island Exploration: Localrent and EconomyBookings provide transparent car rentals with minimal deposits.";
      matched = [SERVICES_21[0], SERVICES_21[7], SERVICES_21[3]];
    } else if (q.indexOf("taxi") !== -1 || q.indexOf("transfer") !== -1 || q.indexOf("ride") !== -1 || q.indexOf("car") !== -1) {
      ans = "Pre-booking private airport transfers avoids crowded taxi queues and eliminates dynamic surge pricing.\n\n" +
        "• Kiwitaxi: Guaranteed door-to-door meet & greet transfers across 100+ countries.\n" +
        "• Welcome Pickups: English-speaking local drivers offering personalized city introductions.\n" +
        "• Localrent & EconomyBookings: Reliable car hire with comprehensive insurance options.";
      matched = [SERVICES_21[3], SERVICES_21[6], SERVICES_21[7]];
    } else {
      ans = "Team MAGIC AI provides real-time travel intelligence and direct access to 21 verified global travel partners.\n\n" +
        "• Flight Booking: Compare low fares across global routes with Aviasales.\n" +
        "• Flight Delay Rights: Claim €250–€600 compensation with AirHelp & Compensair.\n" +
        "• Global Connectivity: Instant 5G travel data with Airalo, Yesim, and Saily eSIM.\n" +
        "• All services include verified tracking under Marker 787950.";
    }

    return {
      answer: ans,
      model: "Gemini 3.8 Flash & ChatGPT (Team MAGIC Core)",
      sources: matched.map(function (m) {
        return { title: m.name + " (" + m.cat + ")", url: m.url, domain: m.domain };
      })
    };
  }

  function buildRoomOverlay() {
    var overlay = node("div", "trtt-room-overlay");
    overlay.id = "trtt-room-overlay-106";
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");

    var modal = node("div", "trtt-room-modal");

    // Header
    var header = node("div", "trtt-room-header");
    var titleBox = node("div", "trtt-room-titlebox");
    var badge = node("span", "trtt-room-badge", "TRTT MAGIC-787950 ROKSANA LOCKED");
    var h2 = node("h2", "trtt-room-title", "THINKING ROOM & AI SUPERSTORE");
    var sub = node("p", "trtt-room-subtitle", "Team MAGIC: Muse (CEO) • Abu Taher (Publisher) • Gemini & AI Studio (Intelligence) • ChatGPT (Developer) • Sanluri to World");
    titleBox.appendChild(badge);
    titleBox.appendChild(h2);
    titleBox.appendChild(sub);

    var closeBtn = node("button", "trtt-room-close", "✕");
    closeBtn.setAttribute("aria-label", "Close Thinking Room");
    closeBtn.addEventListener("click", closeRoom);
    header.appendChild(titleBox);
    header.appendChild(closeBtn);
    modal.appendChild(header);

    // ==========================================
    // GOOGLE-STYLE AI ANSWER ENGINE CORE
    // ==========================================
    var engineWrap = node("div", "trtt-google-engine-wrap");

    // Google-style 4-Color Accent Line
    var googleAccent = node("div", "trtt-google-accent-line");
    engineWrap.appendChild(googleAccent);

    // Google Search Pill Bar
    var searchPill = node("div", "trtt-google-search-pill");
    var searchLens = node("span", "trtt-google-lens-icon", "🔍");
    searchPill.appendChild(searchLens);

    var searchInput = node("input", "trtt-google-search-input");
    searchInput.type = "text";
    searchInput.placeholder = "Search travel queries or ask Team MAGIC AI (e.g. flight delay €600, Sanluri routes, eSIM)...";
    searchInput.setAttribute("aria-label", "Search travel questions");
    searchPill.appendChild(searchInput);

    var searchActions = node("div", "trtt-google-pill-actions");
    var clearBtn = node("button", "trtt-google-clear-btn", "✕");
    clearBtn.type = "button";
    clearBtn.title = "Clear search";
    clearBtn.style.display = "none";
    clearBtn.addEventListener("click", function () {
      searchInput.value = "";
      clearBtn.style.display = "none";
      searchInput.focus();
    });
    searchActions.appendChild(clearBtn);

    var searchBtn = node("button", "trtt-google-ask-btn", "Ask AI ✨");
    searchBtn.type = "button";
    searchActions.appendChild(searchBtn);
    searchPill.appendChild(searchActions);
    engineWrap.appendChild(searchPill);

    searchInput.addEventListener("input", function () {
      clearBtn.style.display = searchInput.value.length > 0 ? "inline-block" : "none";
    });

    // Quick Suggestions / "People Also Ask"
    var quickWrap = node("div", "trtt-google-quick-wrap");
    quickWrap.appendChild(node("span", "trtt-google-quick-label", "Suggested searches:"));
    QUICK_PROMPTS.forEach(function (item) {
      var chip = node("button", "trtt-google-chip", item.label);
      chip.type = "button";
      chip.addEventListener("click", function () {
        searchInput.value = item.query;
        clearBtn.style.display = "inline-block";
        executeSearch(item.query);
      });
      quickWrap.appendChild(chip);
    });
    engineWrap.appendChild(quickWrap);

    // Google-style AI Overview Card (Container)
    var overviewCard = node("div", "trtt-google-overview-card");
    overviewCard.style.display = "none";

    // Overview Header
    var ovHeader = node("div", "trtt-overview-header");
    var ovLeft = node("div", "trtt-overview-left");
    ovLeft.appendChild(node("span", "trtt-overview-sparkle", "✨"));
    ovLeft.appendChild(node("strong", "trtt-overview-title", "AI Overview"));
    ovLeft.appendChild(node("span", "trtt-overview-badge", "Gemini 3.8 Flash & ChatGPT"));
    ovHeader.appendChild(ovLeft);

    var ovModel = node("span", "trtt-overview-model-tag", "Team MAGIC Grounded Intelligence");
    ovHeader.appendChild(ovModel);
    overviewCard.appendChild(ovHeader);

    // Overview Content Area
    var ovContent = node("div", "trtt-overview-content");
    overviewCard.appendChild(ovContent);

    // Google Sources Citation Carousel
    var ovSources = node("div", "trtt-overview-sources");
    overviewCard.appendChild(ovSources);

    // Overview Disclaimer Footer
    var ovFooter = node("div", "trtt-overview-footer");
    ovFooter.appendChild(node("small", "", "AI-generated overview grounded in European travel regulations & official sources. Verified marker: 787950."));
    overviewCard.appendChild(ovFooter);

    engineWrap.appendChild(overviewCard);
    modal.appendChild(engineWrap);

    function executeSearch(queryText) {
      var query = (queryText || searchInput.value).trim();
      if (!query) {
        searchInput.focus();
        return;
      }

      searchBtn.disabled = true;
      searchBtn.textContent = "Searching...";
      overviewCard.style.display = "block";
      ovContent.replaceChildren();
      ovSources.replaceChildren();

      var loadingBox = node("div", "trtt-overview-loading");
      loadingBox.appendChild(node("span", "trtt-google-spinner"));
      loadingBox.appendChild(node("span", "", "Generating Google-style AI Overview with Gemini & web grounding..."));
      ovContent.appendChild(loadingBox);

      // Call the production Vercel Answer Engine with proper question payload
      fetch("https://cocvghuj-trtt-news-bot.vercel.app/api/answer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: query })
      })
      .then(function (res) { return res.json(); })
      .then(function (data) {
        searchBtn.disabled = false;
        searchBtn.textContent = "Ask AI ✨";
        ovContent.replaceChildren();

        var aiText = "";
        var sources = [];

        if (data && data.ok && data.results) {
          var gem = data.results.gemini;
          var openr = data.results.openrouter;
          if (gem && gem.answer) {
            aiText = gem.answer;
            sources = gem.sources || [];
            ovModel.textContent = "Gemini 3.8 Flash (Grounding Enabled)";
          } else if (openr && openr.answer) {
            aiText = openr.answer;
            sources = openr.sources || [];
            ovModel.textContent = "ChatGPT (OpenRouter GPT-5.2)";
          }
        }

        if (!aiText) {
          var fb = getFallbackAnswer(query);
          aiText = fb.answer;
          sources = fb.sources;
          ovModel.textContent = "Team MAGIC Expert Travel Engine";
        }

        ovContent.appendChild(formatAnswerText(aiText));

        // Render Google-style Source Cards
        if (sources && sources.length > 0) {
          var srcTitle = node("div", "trtt-sources-title", "Verified Sources & Partner Tools:");
          ovSources.appendChild(srcTitle);

          var srcGrid = node("div", "trtt-sources-grid");
          sources.slice(0, 4).forEach(function (s) {
            var sc = node("a", "trtt-source-card");
            sc.href = s.url || "https://cocvghuj-trtt-news-bot.vercel.app/?marker=787950";
            sc.target = "_blank";
            sc.rel = "noopener noreferrer";

            var topRow = node("div", "trtt-source-top");
            var domain = s.domain || (s.url ? s.url.replace(/^https?:\/\//, "").split("/")[0] : "trtt-voyage.com");
            topRow.appendChild(node("span", "trtt-source-domain", domain));
            topRow.appendChild(node("span", "trtt-source-arrow", "↗"));

            var titleEl = node("div", "trtt-source-name", s.title || "Travel Partner Tool");
            sc.appendChild(topRow);
            sc.appendChild(titleEl);
            srcGrid.appendChild(sc);
          });
          ovSources.appendChild(srcGrid);
        }
      })
      .catch(function () {
        searchBtn.disabled = false;
        searchBtn.textContent = "Ask AI ✨";
        ovContent.replaceChildren();

        var fb = getFallbackAnswer(query);
        ovContent.appendChild(formatAnswerText(fb.answer));
        ovModel.textContent = "Team MAGIC Expert Travel Engine";

        if (fb.sources && fb.sources.length > 0) {
          var srcTitle = node("div", "trtt-sources-title", "Verified Sources & Partner Tools:");
          ovSources.appendChild(srcTitle);
          var srcGrid = node("div", "trtt-sources-grid");
          fb.sources.forEach(function (s) {
            var sc = node("a", "trtt-source-card");
            sc.href = s.url;
            sc.target = "_blank";
            sc.rel = "noopener noreferrer";

            var topRow = node("div", "trtt-source-top");
            topRow.appendChild(node("span", "trtt-source-domain", s.domain));
            topRow.appendChild(node("span", "trtt-source-arrow", "↗"));

            var titleEl = node("div", "trtt-source-name", s.title);
            sc.appendChild(topRow);
            sc.appendChild(titleEl);
            srcGrid.appendChild(sc);
          });
          ovSources.appendChild(srcGrid);
        }
      });
    }

    searchBtn.addEventListener("click", function () { executeSearch(); });
    searchInput.addEventListener("keydown", function (e) {
      if (e.key === "Enter") executeSearch();
    });

    // ==========================================
    // 21 VERIFIED TOOLS SECTION
    // ==========================================
    var toolsSection = node("div", "trtt-tools-section");
    var toolsHeading = node("div", "trtt-tools-heading");
    toolsHeading.appendChild(node("h3", "", "🚀 21 Verified Programs • TRTT VoyageHub SuperStore"));
    toolsHeading.appendChild(node("span", "", "Marker: 787950 Locked • 100% Verified Partners"));
    toolsSection.appendChild(toolsHeading);

    // Google-style Filter Tabs
    var tabsRow = node("div", "trtt-google-tabs");
    var categories = ["All", "Flights", "600€ Claim", "Taxi/Transfer", "Car Rental", "Global eSIM", "Tickets"];
    var activeTab = "All";

    var toolsGrid = node("div", "trtt-tools-grid");

    function renderTools(filterCat) {
      toolsGrid.replaceChildren();
      SERVICES_21.filter(function (s) {
        if (filterCat === "All") return true;
        if (filterCat === "Global eSIM") return s.cat.indexOf("eSIM") !== -1 || s.cat.indexOf("SIM") !== -1;
        return s.cat === filterCat;
      }).forEach(function (s) {
        var item = node("a", "trtt-tool-card");
        item.href = s.url;
        item.target = "_blank";
        item.rel = "noopener noreferrer";

        var top = node("div", "trtt-tool-card-top");
        top.appendChild(node("span", "trtt-tool-icon", s.icon));
        top.appendChild(node("span", "trtt-tool-cat-pill", s.cat));
        item.appendChild(top);

        var info = node("div", "trtt-tool-info");
        info.appendChild(node("strong", "trtt-tool-name", s.name));
        info.appendChild(node("p", "trtt-tool-desc", s.desc));
        item.appendChild(info);

        var btm = node("div", "trtt-tool-btm");
        btm.appendChild(node("span", "trtt-tool-marker", "Marker: 787950"));
        btm.appendChild(node("span", "trtt-tool-link-action", "Book / Check ↗"));
        item.appendChild(btm);

        toolsGrid.appendChild(item);
      });
    }

    categories.forEach(function (cat) {
      var tabBtn = node("button", "trtt-google-tab-btn" + (cat === activeTab ? " is-active" : ""), cat);
      tabBtn.type = "button";
      tabBtn.addEventListener("click", function () {
        tabsRow.querySelectorAll(".trtt-google-tab-btn").forEach(function (b) { b.classList.remove("is-active"); });
        tabBtn.classList.add("is-active");
        renderTools(cat);
      });
      tabsRow.appendChild(tabBtn);
    });

    toolsSection.appendChild(tabsRow);
    renderTools("All");
    toolsSection.appendChild(toolsGrid);
    modal.appendChild(toolsSection);

    // Footer
    var footer = node("div", "trtt-room-footer");
    footer.appendChild(node("p", "", "TRTT Voyage — Sanluri to World • Built with eternal love for Roksana, Taifa & Tasrif • Marker 787950"));
    modal.appendChild(footer);

    overlay.appendChild(modal);

    overlay.addEventListener("click", function (e) {
      if (e.target === overlay) closeRoom();
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeRoom();
    });

    return overlay;
  }

  function buildDoor() {
    var nav = node("nav", "trtt-control-nav");
    nav.id = "trtt-control-nav";
    nav.setAttribute("aria-label", "TRTT Voyage main menu");

    var brand = node("a", "trtt-control-brand", "TRTT VOYAGE");
    brand.href = "/";
    nav.appendChild(brand);

    var list = node("div", "trtt-route-list");
    ROUTES.forEach(function (item) { list.appendChild(makeRoute(item)); });
    nav.appendChild(list);

    var door = node("button", "trtt-thinking-room-trigger");
    door.type = "button";
    door.id = "trtt-thinking-room-trigger";
    door.setAttribute("aria-label", "Open Thinking Room");
    door.title = "Thinking Room & Google AI Engine — Click to open";

    door.appendChild(node("span", "trtt-door-icon", "✦"));

    var copy = node("span", "trtt-door-copy");
    copy.appendChild(node("strong", "", "THINKING ROOM"));
    copy.appendChild(node("small", "", "GOOGLE AI • 21 TOOLS"));
    door.appendChild(copy);

    door.appendChild(node("span", "trtt-door-arrow", "↗"));
    door.addEventListener("click", openRoom);
    nav.appendChild(door);

    return nav;
  }

  function mount() {
    if (!document.body) return false;
    if (document.getElementById("trtt-control-nav")) return true;

    var target = findMount();
    if (!target) return false;

    var nav = buildDoor();

    if (target.classList && target.classList.contains("header-menu")) {
      var oldMenu = target.querySelector("#main-menu") ||
        target.querySelector("#main-menu-nav");
      if (oldMenu && oldMenu.parentNode) {
        oldMenu.parentNode.replaceChild(nav, oldMenu);
      } else {
        target.appendChild(nav);
      }
    } else if (target.id === "main-menu") {
      target.parentNode.replaceChild(nav, target);
    }

    return true;
  }

  if (!mount()) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", function () { mount(); });
    } else {
      var tries = 0;
      var timer = setInterval(function () {
        tries++;
        if (mount() || tries >= 25) clearInterval(timer);
      }, 200);
    }
  }
})();
