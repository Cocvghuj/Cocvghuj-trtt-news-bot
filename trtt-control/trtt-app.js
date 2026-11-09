/* TRTT VOYAGE — THINKING ROOM */
(function () {
  "use strict";

  const MENU = [
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

  function create(tag, cls, text) {
    const el = document.createElement(tag);
    if (cls) el.className = cls;
    if (text) el.textContent = text;
    return el;
  }

  function init() {
    if (document.getElementById("trtt-thinking-room")) return;

    const menu = document.getElementById("main-menu");

    if (!menu) {
      console.error("TRTT: Blogger main-menu not found.");
      return;
    }

    menu.replaceChildren();

    const launcher = create("button", "trtt-launcher", "✦ THINKING ROOM");
    launcher.type = "button";
    menu.appendChild(launcher);

    const overlay = create("div", "trtt-overlay");
    overlay.id = "trtt-thinking-room";

    const room = create("div", "trtt-room");

    const header = create("header", "trtt-header");
    const title = create("div", "trtt-title");
    title.appendChild(create("small", "", "TRTT VOYAGE • SANLURI TO WORLD"));
    title.appendChild(create("h1", "", "Thinking Room"));
    title.appendChild(create("p", "", "A universe of ideas and creativity."));

    const close = create("button", "trtt-close", "×");
    close.type = "button";
    close.setAttribute("aria-label", "Close");

    header.append(title, close);

    const bubbles = create("div", "trtt-bubbles");

    MENU.forEach(([name, detail, url]) => {
      const bubble = create("a", "trtt-bubble");
      bubble.href = url;
      bubble.appendChild(create("strong", "", name));
      bubble.appendChild(create("span", "", detail));

      if (url.startsWith("http")) {
        bubble.target = "_blank";
        bubble.rel = "noopener noreferrer";
      } else {
        bubble.addEventListener("click", event => {
          event.preventDefault();
          alert("Muse — CEO / Direction");
        });
      }

      bubbles.appendChild(bubble);
    });

    const footer = create(
      "footer",
      "trtt-footer",
      "Made by MAC — Muse, Abu, ChatGPT, Gemini"
    );

    room.append(header, bubbles, footer);
    overlay.appendChild(room);
    document.body.appendChild(overlay);

    function open() {
      overlay.classList.add("active");
      document.documentElement.classList.add("trtt-locked");
      launcher.setAttribute("aria-expanded", "true");
    }

    function shut() {
      overlay.classList.remove("active");
      document.documentElement.classList.remove("trtt-locked");
      launcher.setAttribute("aria-expanded", "false");
    }

    launcher.addEventListener("click", open);
    close.addEventListener("click", shut);

    overlay.addEventListener("click", event => {
      if (event.target === overlay) shut();
    });

    document.addEventListener("keydown", event => {
      if (event.key === "Escape") shut();
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
