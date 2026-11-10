/* TRTT VOYAGE CONTROL SYSTEM — VERSION 103
 * One active implementation for Blogger navigation + Thinking Room.
 * Does not clear, replace, or rewrite Blogger's existing menu nodes.
 */
(function () {
  "use strict";
  if (window.__TRTT_CONTROL_V103__) return;
  window.__TRTT_CONTROL_V103__ = true;

  var ROUTES = [
    { name: "Home", detail: "Start here", href: "/" },
    { name: "My Diary", detail: "Personal journal", href: "/search/label/My%20Diary" },
    { name: "Flight", detail: "Flight services", href: "/search/label/Flight" },
    { name: "Ride", detail: "Ride services", href: "/search/label/Ride" },
    { name: "eSIM", detail: "Stay connected", href: "/search/label/eSIM" },
    { name: "Tour", detail: "Explore places", href: "/search/label/Tour" },
    { name: "Shop", detail: "TRTT Shop", href: "/search/label/Shop" },
    { name: "Night", detail: "Night services", href: "/search/label/Night" }
  ];

  var QUESTIONS = [
    "কোন জায়গাটি তোমার পরবর্তী ভ্রমণের স্বপ্ন?",
    "ভ্রমণে পরিকল্পনা বেশি জরুরি, নাকি অজানাকে আবিষ্কার?",
    "একটি নতুন শহরে পৌঁছে প্রথমে কী দেখতে চাও?",
    "তোমার কাছে আদর্শ ভ্রমণসঙ্গী কেমন?",
    "ভ্রমণের কোন স্মৃতিটি তুমি সারাজীবন মনে রাখতে চাও?",
    "একদিনের জন্য পৃথিবীর যেকোনো জায়গায় যেতে পারলে কোথায় যেতে?"
  ];

  function node(tag, className, text) {
    var el = document.createElement(tag);
    if (className) el.className = className;
    if (text !== undefined) el.textContent = text;
    return el;
  }

  function makeRoute(item, className) {
    var a = node("a", className || "trtt-route-bubble");
    a.href = item.href;
    a.appendChild(node("strong", "", item.name));
    a.appendChild(node("span", "", item.detail));
    return a;
  }

  function findMount() {
    return document.querySelector("#header-wrap > .container > .header-menu") ||
      document.querySelector("#header-wrap .header-menu") ||
      document.querySelector("#header-wrap #main-menu") ||
      document.querySelector("#main-menu") ||
      document.querySelector(".header-menu") ||
      document.querySelector("#header-wrap");
  }

  function buildRoom() {
    if (document.getElementById("trtt-thinking-room")) return;

    var overlay = node("div", "trtt-room-overlay");
    overlay.id = "trtt-thinking-room";
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-hidden", "true");
    overlay.setAttribute("aria-labelledby", "trtt-room-title");

    var panel = node("section", "trtt-room-panel");
    var head = node("header", "trtt-room-head");
    var heading = node("div", "trtt-room-heading");
    heading.appendChild(node("small", "", "TRTT VOYAGE • SANLURI TO WORLD"));
    var h = node("h2", "", "Thinking Room");
    h.id = "trtt-room-title";
    heading.appendChild(h);
    heading.appendChild(node("p", "", "Three perspectives. One shared space for ideas."));
    var close = node("button", "trtt-room-close", "×");
    close.type = "button";
    close.setAttribute("aria-label", "Close Thinking Room");
    head.appendChild(heading);
    head.appendChild(close);

    var identity = node("div", "trtt-identity-row");
    [
      { name: "Muse", role: "CEO • Direction", href: "#muse" },
      { name: "ChatGPT", role: "AI • Development", href: "https://chatgpt.com/" },
      { name: "Gemini", role: "AI • Research", href: "https://gemini.google.com/" }
    ].forEach(function (item) {
      var a = node("a", "trtt-identity-card");
      a.href = item.href;
      if (/^https:/.test(item.href)) { a.target = "_blank"; a.rel = "noopener noreferrer"; }
      a.appendChild(node("strong", "", item.name));
      a.appendChild(node("span", "", item.role));
      identity.appendChild(a);
    });

    var question = node("section", "trtt-question-panel");
    question.appendChild(node("small", "", "TODAY'S QUESTION"));
    var day = Math.floor(Date.now() / 86400000);
    question.appendChild(node("p", "", QUESTIONS[day % QUESTIONS.length]));

    var locked = node("div", "trtt-roksana-locked");
    locked.appendChild(node("span", "", "🔒"));
    var lockedText = node("div", "");
    lockedText.appendChild(node("strong", "", "ROKSANA LOCKED"));
    lockedText.appendChild(node("small", "", "Protected space • No access button"));
    locked.appendChild(lockedText);

    var roomRoutes = node("nav", "trtt-room-routes");
    roomRoutes.setAttribute("aria-label", "TRTT destinations");
    ROUTES.forEach(function (item) { roomRoutes.appendChild(makeRoute(item, "trtt-room-route")); });

    var footer = node("footer", "trtt-room-footer", "TRTT MAC-787950 LOCKED • Made by MAC — Muse, Abu, ChatGPT");
    panel.appendChild(head);
    panel.appendChild(identity);
    panel.appendChild(question);
    panel.appendChild(locked);
    panel.appendChild(node("h3", "trtt-destinations-title", "Explore TRTT Voyage"));
    panel.appendChild(roomRoutes);
    panel.appendChild(footer);
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

    var trigger = document.getElementById("trtt-thinking-room-trigger");
    if (trigger) {
      trigger.addEventListener("click", function () {
        overlay.classList.add("is-open");
        overlay.setAttribute("aria-hidden", "false");
        document.documentElement.classList.add("trtt-room-open");
        trigger.setAttribute("aria-expanded", "true");
        close.focus();
      });
    }
  }

  function mount() {
    if (!document.body) return false;
    if (document.getElementById("trtt-control-nav")) return true;

    var target = findMount();
    if (!target) return false;

    var nav = node("nav", "trtt-control-nav");
    nav.id = "trtt-control-nav";
    nav.setAttribute("aria-label", "TRTT Voyage main menu");

    var brand = node("a", "trtt-control-brand", "TRTT VOYAGE");
    brand.href = "/";
    nav.appendChild(brand);

    var routes = node("div", "trtt-route-list");
    ROUTES.forEach(function (item) { routes.appendChild(makeRoute(item)); });
    nav.appendChild(routes);

    var trigger = node("button", "trtt-thinking-room-trigger");
    trigger.id = "trtt-thinking-room-trigger";
    trigger.type = "button";
    trigger.setAttribute("aria-haspopup", "dialog");
    trigger.setAttribute("aria-controls", "trtt-thinking-room");
    trigger.setAttribute("aria-expanded", "false");
    trigger.appendChild(node("span", "trtt-door-icon", "✦"));
    var copy = node("span", "trtt-door-copy");
    copy.appendChild(node("strong", "", "THINKING ROOM"));
    copy.appendChild(node("small", "", "ENTER THE IDEA SPACE"));
    trigger.appendChild(copy);
    trigger.appendChild(node("span", "trtt-door-arrow", "↗"));
    nav.appendChild(trigger);

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