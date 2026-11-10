/*! TRTT VOYAGE CONTROL — V104
 * GitHub-managed replacement menu + Thinking Room.
 * Mounts directly into the Blogger header menu slot; no theme edits required.
 */
(function () {
  "use strict";
  if (window.__TRTT_CONTROL_V104__) return;
  window.__TRTT_CONTROL_V104__ = true;

  var ROUTES = [
    ["Home","Start here","/"],
    ["My Diary","Personal journal","/search/label/My%20Diary"],
    ["Flight","Flight services","/search/label/Flight"],
    ["Ride","Ride services","/search/label/Ride"],
    ["eSIM","Stay connected","/search/label/eSIM"],
    ["Tour","Explore places","/search/label/Tour"],
    ["Shop","TRTT Shop","/search/label/Shop"],
    ["Night","Night services","/search/label/Night"]
  ];
  var QUESTIONS = [
    "কোন জায়গাটি তোমার পরবর্তী ভ্রমণের স্বপ্ন?",
    "ভ্রমণে পরিকল্পনা বেশি জরুরি, নাকি অজানাকে আবিষ্কার?",
    "একটি নতুন শহরে পৌঁছে প্রথমে কী দেখতে চাও?",
    "তোমার কাছে আদর্শ ভ্রমণসঙ্গী কেমন?",
    "ভ্রমণের কোন স্মৃতিটি তুমি সারাজীবন মনে রাখতে চাও?",
    "একদিনের জন্য পৃথিবীর যেকোনো জায়গায় যেতে পারলে কোথায় যেতে?"
  ];

  function el(tag, cls, value) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (value != null) n.textContent = value;
    return n;
  }
  function routeLink(data, cls) {
    var a = el("a", cls);
    a.href = data[2];
    a.appendChild(el("strong", "", data[0]));
    a.appendChild(el("span", "", data[1]));
    return a;
  }
  function buildRoom() {
    var old = document.getElementById("trtt-thinking-room");
    if (old) old.remove();

    var overlay = el("div", "trtt-room-overlay");
    overlay.id = "trtt-thinking-room";
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-hidden", "true");
    overlay.setAttribute("aria-labelledby", "trtt-room-title");

    var panel = el("section", "trtt-room-panel");
    var head = el("header", "trtt-room-head");
    var titleWrap = el("div", "trtt-room-heading");
    titleWrap.appendChild(el("small", "", "TRTT VOYAGE • SANLURI TO WORLD"));
    var title = el("h2", "", "Thinking Room");
    title.id = "trtt-room-title";
    titleWrap.appendChild(title);
    titleWrap.appendChild(el("p", "", "Three perspectives. One shared space for ideas."));
    var close = el("button", "trtt-room-close", "×");
    close.type = "button";
    close.setAttribute("aria-label", "Close Thinking Room");
    head.append(titleWrap, close);

    var identities = el("div", "trtt-identity-row");
    [
      ["Muse","CEO • Direction","#muse"],
      ["ChatGPT","AI • Development","https://chatgpt.com/"],
      ["Gemini","AI • Research","https://gemini.google.com/"]
    ].forEach(function (item) {
      var a = el("a", "trtt-identity-card");
      a.href = item[2];
      if (/^https:/.test(item[2])) { a.target = "_blank"; a.rel = "noopener noreferrer"; }
      a.append(el("strong", "", item[0]), el("span", "", item[1]));
      identities.appendChild(a);
    });

    var q = el("section", "trtt-question-panel");
    q.appendChild(el("small", "", "TODAY'S QUESTION"));
    q.appendChild(el("p", "", QUESTIONS[Math.floor(Date.now() / 86400000) % QUESTIONS.length]));

    var locked = el("div", "trtt-roksana-locked");
    locked.appendChild(el("span", "", "🔒"));
    var lockedCopy = el("div", "");
    lockedCopy.append(el("strong", "", "ROKSANA LOCKED"), el("small", "", "Protected space • No access button"));
    locked.appendChild(lockedCopy);

    var routes = el("nav", "trtt-room-routes");
    routes.setAttribute("aria-label", "TRTT destinations");
    ROUTES.forEach(function (r) { routes.appendChild(routeLink(r, "trtt-room-route")); });

    panel.append(
      head, identities, q, locked,
      el("h3", "trtt-destinations-title", "Explore TRTT Voyage"),
      routes,
      el("footer", "trtt-room-footer", "TRTT MAC-787950 LOCKED • Made by MAC — Muse, Abu, ChatGPT")
    );
    overlay.appendChild(panel);
    document.body.appendChild(overlay);

    function closeRoom() {
      overlay.classList.remove("is-open");
      overlay.setAttribute("aria-hidden", "true");
      document.documentElement.classList.remove("trtt-room-open");
      var trigger = document.getElementById("trtt-thinking-room-trigger");
      if (trigger) trigger.setAttribute("aria-expanded", "false");
    }
    close.addEventListener("click", closeRoom);
    overlay.addEventListener("click", function (event) {
      if (event.target === overlay) closeRoom();
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && overlay.classList.contains("is-open")) closeRoom();
    });
  }

  function makeMenu() {
    var nav = el("nav", "trtt-control-nav");
    nav.id = "trtt-control-nav";
    nav.setAttribute("aria-label", "TRTT Voyage main menu");

    var brand = el("a", "trtt-control-brand", "TRTT VOYAGE");
    brand.href = "/";
    nav.appendChild(brand);

    var list = el("div", "trtt-route-list");
    ROUTES.forEach(function (r) { list.appendChild(routeLink(r, "trtt-route-bubble")); });
    nav.appendChild(list);

    var trigger = el("button", "trtt-thinking-room-trigger", "✦ Thinking Room");
    trigger.id = "trtt-thinking-room-trigger";
    trigger.type = "button";
    trigger.setAttribute("aria-haspopup", "dialog");
    trigger.setAttribute("aria-controls", "trtt-thinking-room");
    trigger.setAttribute("aria-expanded", "false");
    trigger.addEventListener("click", function () {
      var overlay = document.getElementById("trtt-thinking-room");
      if (!overlay) return;
      overlay.classList.add("is-open");
      overlay.setAttribute("aria-hidden", "false");
      document.documentElement.classList.add("trtt-room-open");
      trigger.setAttribute("aria-expanded", "true");
      var close = overlay.querySelector(".trtt-room-close");
      if (close) close.focus();
    });
    nav.appendChild(trigger);
    return nav;
  }

  function mount() {
    if (!document.body) return false;
    var nav = makeMenu();

    // Prefer the exact Blogger menu container used by the TRTT theme.
    var slot = document.querySelector(".header-menu");
    if (slot) {
      slot.replaceChildren(nav);
    } else {
      var section = document.querySelector("#main-menu");
      if (section) {
        section.replaceChildren(nav);
      } else {
        var list = document.querySelector("#main-menu-nav");
        if (list && list.parentNode) {
          list.parentNode.replaceChildren(nav);
        } else {
          var header = document.querySelector("#header-wrap, #header-wrapper, #header, header");
          var search = document.querySelector("#nav-search, .show-search");
          if (header && search && search.parentNode === header) {
            header.insertBefore(nav, search);
          } else if (header) {
            header.appendChild(nav);
          } else {
            document.body.insertBefore(nav, document.body.firstChild);
          }
        }
      }
    }
    buildRoom();
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
