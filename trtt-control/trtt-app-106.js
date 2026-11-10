/*! TRTT VOYAGE — THINKING ROOM / V106 — TEAM MAGIC ROKSANA EDITION
 * Marker: TRTT MAGIC-787950 ROKSANA LOCKED
 * Team: Muse (CEO), Abu Taher (Publisher), ChatGPT & Gemini / AI Studio (Developers)
 */
(function () {
  "use strict";
  if (window.__TRTT_DOOR_V106__) return;
  window.__TRTT_DOOR_V106__ = true;

  var ROUTES = [
    ["Home", "Start here", "/"],
    ["My Diary", "Personal journal", "/search/label/My%20Diary"],
    ["Flight", "Flight services", "/search/label/Flight"],
    ["Ride", "Ride services", "/search/label/Ride"],
    ["eSIM", "Stay connected", "/search/label/eSIM"],
    ["Tour", "Explore places", "/search/label/Tour"],
    ["Shop", "TRTT Shop", "/search/label/Shop"],
    ["Night", "Night services", "/search/label/Night"]
  ];

  var SERVICES_21 = [
    { name: "Aviasales", cat: "Flights", icon: "✈️", url: "https://aviasales.tpo.lv/Fb8U9yav?marker=787950" },
    { name: "AirHelp", cat: "600€ Claim", icon: "⚖️", url: "https://airhelp.tpo.lv/3ItXS0E4?marker=787950" },
    { name: "Compensair", cat: "EU Claim", icon: "🛡️", url: "https://compensair.tpo.lv/YgVXgRnB?marker=787950" },
    { name: "Kiwitaxi", cat: "Taxi/Transfer", icon: "🚕", url: "https://kiwitaxi.tpo.lv/tIZcbMOB?marker=787950" },
    { name: "GetTransfer", cat: "Chauffeured", icon: "🚘", url: "https://gettransfer.tpo.lv/1u8zRU5s?marker=787950" },
    { name: "Intui.travel", cat: "Airport Ride", icon: "🚐", url: "https://intui.tpo.lv/tiSkz4Yq?marker=787950" },
    { name: "Welcome Pickups", cat: "Pickups", icon: "📍", url: "https://tpo.lv/h3LrTZcS?marker=787950" },
    { name: "Localrent", cat: "Car Rental", icon: "🚗", url: "https://localrent.tpo.lv/4jd1IRQG?marker=787950" },
    { name: "EconomyBookings", cat: "Car Rental", icon: "🚙", url: "https://economybookings.tpo.lv/pyHqRiOo?marker=787950" },
    { name: "QEEQ", cat: "Deals & Cars", icon: "🏎️", url: "https://qeeq.tpo.lv/HKhCeDhY?marker=787950" },
    { name: "Airalo", cat: "Global eSIM", icon: "📶", url: "https://airalo.tpo.lv/ZZoQC7Mz?marker=787950" },
    { name: "Yesim", cat: "Travel eSIM", icon: "📲", url: "https://yesim.tpo.lv/krzFKLpg?marker=787950" },
    { name: "Drimsim", cat: "Universal SIM", icon: "🌐", url: "https://drimsim.tpo.lv/Ly7ywlY8?marker=787950" },
    { name: "Saily", cat: "Nord eSIM", icon: "🛡️", url: "https://saily.tpo.lv/ssekmS4X?marker=787950" },
    { name: "Tiqets", cat: "Tickets", icon: "🎟️", url: "https://tiqets.tpo.lv/bnx8pnF6?marker=787950" },
    { name: "Klook", cat: "Tours & Transit", icon: "🎢", url: "https://klook.tpo.lv/TWKnemhz?marker=787950" },
    { name: "Go City", cat: "City Passes", icon: "🎫", url: "https://gocity.tpo.lv/QSQw8FwU?marker=787950" },
    { name: "KKday", cat: "Experiences", icon: "🗺️", url: "https://kkday.tpo.lv/JaAfTgGF?marker=787950" },
    { name: "Radical Storage", cat: "Luggage", icon: "🧳", url: "https://radicalstorage.tpo.lv/WkGqxIsD?marker=787950" },
    { name: "Amazon Flight Gear", cat: "Travel Gear", icon: "🎒", url: "https://amzn.to/4shg6Hn?marker=787950" },
    { name: "SuperStore Portal", cat: "21-in-1 Hub", icon: "🚀", url: "https://cocvghuj-trtt-news-bot.vercel.app/?marker=787950" }
  ];

  function node(tag, className, value) {
    var el = document.createElement(tag);
    if (className) el.className = className;
    if (value !== undefined && value !== null) el.textContent = value;
    return el;
  }

  function makeRoute(item) {
    var a = node("a", "trtt-route-bubble");
    a.href = item[2];
    a.appendChild(node("strong", "", item[0]));
    a.appendChild(node("span", "", item[1]));
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
  }

  function closeRoom() {
    var overlay = document.getElementById("trtt-room-overlay-106");
    if (overlay) {
      overlay.classList.remove("is-active");
      document.documentElement.classList.remove("trtt-room-open");
    }
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
    var h2 = node("h2", "trtt-room-title", "THINKING ROOM & SUPERSTORE");
    var sub = node("p", "trtt-room-subtitle", "Team MAGIC: Muse (CEO) • Abu Taher (Publisher) • ChatGPT & Gemini (Developer) • Sanluri to World");
    titleBox.appendChild(badge);
    titleBox.appendChild(h2);
    titleBox.appendChild(sub);

    var closeBtn = node("button", "trtt-room-close", "✕");
    closeBtn.setAttribute("aria-label", "Close Thinking Room");
    closeBtn.addEventListener("click", closeRoom);
    header.appendChild(titleBox);
    header.appendChild(closeBtn);
    modal.appendChild(header);

    // Primary Interactive Core: Ask Team MAC AI (ChatGPT & AI Studio)
    var aiCore = node("div", "trtt-room-ai-core");
    var aiTitle = node("div", "trtt-ai-core-header");
    aiTitle.appendChild(node("span", "trtt-ai-pulse-dot"));
    aiTitle.appendChild(node("strong", "", "প্রধান এআই বাটন • Ask Team MAC AI (ChatGPT & AI Studio)"));
    aiCore.appendChild(aiTitle);

    var aiActionRow = node("div", "trtt-ai-action-row");
    var aiInput = node("input", "trtt-ai-input");
    aiInput.type = "text";
    aiInput.placeholder = "ভ্রমণ বা রুট সম্পর্কে যেকোনো প্রশ্ন লিখুন (যেমন: 600€ claim, Sanluri route, eSIM)...";

    var aiBtn = node("button", "trtt-ai-ask-btn", "জিজ্ঞাসা করুন ⚡");
    aiBtn.type = "button";

    var aiResponseBox = node("div", "trtt-ai-response-box");
    aiResponseBox.style.display = "none";

    aiBtn.addEventListener("click", function () {
      var query = aiInput.value.trim();
      if (!query) {
        aiInput.focus();
        return;
      }
      aiBtn.disabled = true;
      aiBtn.textContent = "খোঁজা হচ্ছে...";
      aiResponseBox.style.display = "block";
      aiResponseBox.textContent = "টিম ম্যাক এআই সংযোগ নিচ্ছে...";

      fetch("https://cocvghuj-trtt-news-bot.vercel.app/api/answer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: query })
      })
      .then(function (res) { return res.json(); })
      .then(function (data) {
        aiBtn.disabled = false;
        aiBtn.textContent = "জিজ্ঞাসা করুন ⚡";
        if (data && data.answer) {
          aiResponseBox.textContent = data.answer;
        } else {
          aiResponseBox.textContent = "টিম ম্যাক পরামর্শ: " + query + " এর সেরা তথ্যের জন্য Aviasales (ফ্লাইট) ও AirHelp (ক্ষতিপূরণ) সরাসরি চেক করুন।";
        }
      })
      .catch(function () {
        aiBtn.disabled = false;
        aiBtn.textContent = "জিজ্ঞাসা করুন ⚡";
        aiResponseBox.textContent = "টিম ম্যাক নোট: সরাসরি Super App বা Vercel Answer Engine-এ প্রশ্নটি দেখতে নিচে ক্লিক করুন।";
      });
    });

    aiActionRow.appendChild(aiInput);
    aiActionRow.appendChild(aiBtn);
    aiCore.appendChild(aiActionRow);
    aiCore.appendChild(aiResponseBox);
    modal.appendChild(aiCore);

    // 21 Verified Tools Section
    var toolsHeading = node("div", "trtt-tools-heading");
    toolsHeading.appendChild(node("h3", "", "🚀 ২১টি ভেরিফাইড প্রোগ্রাম • TRTT VoyageHub SuperStore"));
    toolsHeading.appendChild(node("span", "", "Marker 787950 Locked • 100% Verified"));
    modal.appendChild(toolsHeading);

    var toolsGrid = node("div", "trtt-tools-grid");
    SERVICES_21.forEach(function (s) {
      var item = node("a", "trtt-tool-card");
      item.href = s.url;
      item.target = "_blank";
      item.rel = "noopener noreferrer";

      var icon = node("span", "trtt-tool-icon", s.icon);
      var info = node("div", "trtt-tool-info");
      info.appendChild(node("strong", "", s.name));
      info.appendChild(node("small", "", s.cat));

      item.appendChild(icon);
      item.appendChild(info);
      toolsGrid.appendChild(item);
    });
    modal.appendChild(toolsGrid);

    // Footer
    var footer = node("div", "trtt-room-footer");
    footer.appendChild(node("p", "", "TRTT Voyage — Sanluri to World • Built with Love for Roksana, Taifa & Tasrif • Marker 787950"));
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
    door.setAttribute("aria-label", "Thinking Room entrance");
    door.title = "Thinking Room — Click to enter";
    door.appendChild(node("span", "trtt-door-icon", "✦"));

    var copy = node("span", "trtt-door-copy");
    copy.appendChild(node("strong", "", "THINKING ROOM"));
    copy.appendChild(node("small", "", "TEAM MAGIC • 21 TOOLS"));
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

  function start() {
    if (mount()) return;
    var observer = new MutationObserver(function () {
      if (mount()) observer.disconnect();
    });
    observer.observe(document.documentElement, { childList: true, subtree: true });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start, { once: true });
  } else {
    start();
  }
})();
