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

  // Never use a broad selector as a replacement target.
  // Replace only the exact Blogger menu section; otherwise preserve the header and append.
  function findMount() {
    var section = document.getElementById("main-menu");
    if (section) return { node: section, replace: true };

    var headerMenu = document.querySelector("#header-wrap .header-menu") ||
      document.querySelector(".header-menu");
    if (headerMenu) return { node: headerMenu, replace: false };

    // The old menu widget may have been deleted. Keep the launcher visible
    // by falling back to Blogger header containers without replacing them.
    var header = document.querySelector("#header-wrap") ||
      document.querySelector("#header-wrapper") ||
      document.querySelector("#header") ||
      document.querySelector("header") ||
      document.querySelector(".header-wrapper");
    if (header) return { node: header, replace: false, prepend: true };

    // Last-resort Blogger content anchors. Never replace their contents.
    var content = document.querySelector("#main-wrapper") ||
      document.querySelector("#main") ||
      document.querySelector(".main-wrapper") ||
      document.querySelector(".content-outer");
    if (content) return { node: content, replace: false, prepend: true };

    // Avoid silently failing if this theme has no recognizable wrapper.
    if (document.body) return { node: document.body, replace: false, prepend: true };

    return null;
  }

  function build(target) {
    if (document.getElementById("trtt-thinking-room")) return true;
    if (!target || !target.node) return false;

    var mount = target.node;
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

    var core = el("div", "trtt-core");
    core.appendChild(el("span", "trtt-core-orbit", "✦"));
    core.appendChild(el("strong", "", "TRTT MAC-787950"));
    core.appendChild(el("small", "", "IDEAS • PEOPLE • TECHNOLOGY"));

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

    var universe = el("div", "trtt-universe");
    universe.appendChild(core);
    universe.appendChild(bubbles);

    room.appendChild(header);
    room.appendChild(universe);
    room.appendChild(footer);
    overlay.appendChild(room);
    document.body.appendChild(overlay);

    if (target.replace) {
      mount.replaceChildren(launcher);
    } else {
      // Preserve all existing Blogger content and place the launcher first
      // inside a fallback container so it remains easy to find.
      if (!mount.querySelector(".trtt-launcher")) {
        if (target.prepend) mount.insertBefore(launcher, mount.firstChild);
        else mount.appendChild(launcher);
      }
    }

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

    console.info("[TRTT] Thinking Room mounted safely:", target.replace ? "#main-menu" : ".header-menu");
    return true;
  }

  function start() {
    if (build(findMount())) return;

    // Keep watching because Blogger can render header sections after external scripts load.
    var observer = new MutationObserver(function () {
      if (build(findMount())) observer.disconnect();
    });
    observer.observe(document.documentElement, { childList: true, subtree: true });
    console.warn("[TRTT] Waiting for Blogger menu mount point.");
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start, { once: true });
  } else {
    start();
  }
})();
