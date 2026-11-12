/*! TRTT UNIVERSE — THINKING ROOM ENTRY / V106 */
(function () {
  "use strict";
  if (window.__TRTT_UNIVERSE_ROOM_V106__) return;
  window.__TRTT_UNIVERSE_ROOM_V106__ = true;

  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function build() {
    if (!document.body || document.getElementById("trtt-thinking-room-trigger")) return;

    var door = el("button", "trtt-cr-door");
    door.id = "trtt-thinking-room-trigger";
    door.type = "button";
    door.setAttribute("aria-label", "Enter the TRTT Thinking Room");
    door.setAttribute("aria-controls", "trtt-room-overlay");
    door.setAttribute("aria-expanded", "false");
    door.appendChild(el("span", "trtt-cr-door-mark", "✦"));

    var label = el("span", "trtt-cr-door-label");
    label.appendChild(el("strong", "", "THINKING ROOM"));
    label.appendChild(el("small", "", "ENTER THE UNIVERSE"));
    door.appendChild(label);
    door.appendChild(el("span", "trtt-cr-door-arrow", "↗"));

    var overlay = el("div", "trtt-cr-overlay");
    overlay.id = "trtt-room-overlay";
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-hidden", "true");
    overlay.setAttribute("aria-label", "TRTT Universe Thinking Room");

    var shell = el("div", "trtt-cr-shell");
    var close = el("button", "trtt-cr-close", "×");
    close.type = "button";
    close.setAttribute("aria-label", "Close Thinking Room");

    var frame = el("iframe", "trtt-universe-frame");
    frame.id = "trtt-universe-frame";
    frame.title = "TRTT Universe — Team Magic";
    frame.loading = "eager";
    frame.referrerPolicy = "strict-origin-when-cross-origin";
    frame.setAttribute("allow", "clipboard-write");
    frame.src = "https://cdn.jsdelivr.net/gh/Cocvghuj/Cocvghuj-trtt-news-bot@trtt-control-v106/trtt-control/trtt-universe-thinking-room-106.html?v=106-universe-room-20261112";

    shell.appendChild(frame);
    shell.appendChild(close);
    overlay.appendChild(shell);

    function open() {
      overlay.classList.add("is-open");
      overlay.setAttribute("aria-hidden", "false");
      document.documentElement.classList.add("trtt-cr-open");
      door.setAttribute("aria-expanded", "true");
      close.focus();
    }

    function shut() {
      overlay.classList.remove("is-open");
      overlay.setAttribute("aria-hidden", "true");
      document.documentElement.classList.remove("trtt-cr-open");
      door.setAttribute("aria-expanded", "false");
      door.focus();
    }

    door.addEventListener("click", open);
    close.addEventListener("click", shut);
    overlay.addEventListener("click", function (event) {
      if (event.target === overlay) shut();
    });
    document.addEventListener("keydown", function (event) {
      if (overlay.classList.contains("is-open") && event.key === "Escape") {
        event.preventDefault();
        shut();
      }
    });

    document.body.appendChild(overlay);
    document.body.appendChild(door);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", build, { once: true });
  } else {
    build();
  }
})();