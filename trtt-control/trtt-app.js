/* TRTT VOYAGE — THINKING ROOM | GitHub controlled */
(function () {
  "use strict";

  var MENU = [
    ["Muse", "CEO / Direction", "#muse"],
    ["ChatGPT", "AI Partner", "https://chatgpt.com/"],
    ["Gemini", "AI Partner", "https://gemini.google.com/"],
    ["GitHub", "Code Control", "https://github.com/Cocvghuj/Cocvghuj-trtt-news-bot"],
    ["Python", "Programming", "https://www.python.org/"],
    ["Java", "Programming", "https://www.java.com/"],
    ["CSS", "Design", "https://developer.mozilla.org/en-US/docs/Web/CSS"],
    ["CodePen", "Creative Lab", "https://codepen.io/"],
    ["Vlog", "TRTT Stories", "https://trttnews24bd.blogspot.com/search/label/Vlog"],
    ["Vercel", "Deployment", "https://cocvghuj-trtt-news-bot.vercel.app/"]
  ];

  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined && text !== null) node.textContent = text;
    return node;
  }

  function findMount() {
    return document.getElementById("main-menu") ||
      document.querySelector("#header-wrap .header-menu .main-menu") ||
      document.querySelector("#header-wrap .header-menu") ||
      document.querySelector(".header-menu") ||
      document.querySelector(".main-menu");
  }

  function build(mount) {
    if (document.getElementById("trtt-thinking-room")) return true;
    if (!mount) return false;

    var launcher = el("button", "trtt-launcher", "✦ THINKING ROOM");
    launcher.type = "button";
    launcher.setAttribute("aria-haspopup", "dialog");
    launcher.setAttribute("aria-expanded", "false");

    var overlay = el("div", "trtt-overlay");
    overlay.id = "trtt-thinking-room";
    overlay.setAttribute("aria-hidden", "true");

    var room = el("section", "trtt-room");
    room.setAttribute("role", "dialog");
    room.setAttribute("aria-modal", "true");
    room.setAttribute("aria-label", "TRTT Thinking Room");

    var header = el("header", "trtt-header");
    var title = el("div", "trtt-title");
    title.appendChild(el("small", "", "TRTT VOYAGE • SANLURI TO WORLD"));
    title.appendChild(el("h1", "", "Thinking Room"));
    title.appendChild(el("p", "", "A universe of ideas and creativity."));

    var close = el("button", "trtt-close", "×");
    close.type = "button";
    close.setAttribute("aria-label", "Close Thinking Room");
    header.appendChild(title);
    header.appendChild(close);

    var bubbles = el("div", "trtt-bubbles");
    MENU.forEach(function (item) {
      var a = el("a", "trtt-bubble");
      a.href = item[2];
      a.appendChild(el("strong", "", item[0]));
      a.appendChild(el("span", "", item[1]));

      if (item[2] === "#muse") {
        a.addEventListener("click", function (event) {
          event.preventDefault();
          var note = room.querySelector(".trtt-muse-note");
          if (!note) {
            note = el("p", "trtt-muse-note", "Muse — CEO / Direction");
            bubbles.insertAdjacentElement("afterend", note);
          } else {
            note.hidden = !note.hidden;
          }
        });
      } else {
        a.target = "_blank";
        a.rel = "noopener noreferrer";
      }
      bubbles.appendChild(a);
    });

    var footer = el("footer", "trtt-footer",
      "Made by MAC — Muse, Abu, ChatGPT, Gemini");

    room.appendChild(header);
    room.appendChild(bubbles);
    room.appendChild(footer);
    overlay.appendChild(room);
    document.body.appendChild(overlay);

    // Replace only the menu area selected above; no other Blogger sections or posts are touched.
    mount.replaceChildren(launcher);

    function openRoom() {
      overlay.classList.add("active");
      overlay.setAttribute("aria-hidden", "false");
      launcher.setAttribute("aria-expanded", "true");
      document.documentElement.classList.add("trtt-locked");
      close.focus();
    }

    function closeRoom() {
      overlay.classList.remove("active");
      overlay.setAttribute("aria-hidden", "true");
      launcher.setAttribute("aria-expanded", "false");
      document.documentElement.classList.remove("trtt-locked");
      launcher.focus();
    }

    launcher.addEventListener("click", openRoom);
    close.addEventListener("click", closeRoom);
    overlay.addEventListener("click", function (event) {
      if (event.target === overlay) closeRoom();
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && overlay.classList.contains("active")) closeRoom();
    });

    console.info("[TRTT] Thinking Room mounted at:", mount);
    return true;
  }

  function start() {
    if (build(findMount())) return;

    // Blogger may render its sections after the external script starts; watch briefly for them.
    var observer = new MutationObserver(function () {
      if (build(findMount())) observer.disconnect();
    });
    observer.observe(document.documentElement, { childList: true, subtree: true });

    window.setTimeout(function () {
      observer.disconnect();
      if (!document.getElementById("trtt-thinking-room")) {
        console.error("[TRTT] Could not find Blogger menu. Expected #main-menu or .header-menu.");
      }
    }, 10000);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start, { once: true });
  } else {
    start();
  }
})();
