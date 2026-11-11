/*! TRTT VOYAGE — THINKING ROOM DOOR ONLY / V106 */
(function () {
  "use strict";
  if (window.__TRTT_DOOR_V106_ONLY__) return;
  window.__TRTT_DOOR_V106_ONLY__ = true;

  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text != null) node.textContent = text;
    return node;
  }

  function buildDoor() {
    if (!document.body || document.getElementById("trtt-thinking-room-trigger")) return;

    var door = el("button", "trtt-thinking-room-trigger");
    door.id = "trtt-thinking-room-trigger";
    door.type = "button";
    door.setAttribute("aria-label", "Open Thinking Room");
    door.setAttribute("aria-controls", "trtt-room-overlay");
    door.setAttribute("aria-expanded", "false");
    door.appendChild(el("span", "trtt-door-symbol", "✦"));

    var label = el("span", "trtt-door-label");
    label.appendChild(el("strong", "", "THINKING ROOM"));
    label.appendChild(el("small", "", "ENTER THE ROOM"));
    door.appendChild(label);
    door.appendChild(el("span", "trtt-door-arrow", "↗"));

    var overlay = el("section", "trtt-room-overlay");
    overlay.id = "trtt-room-overlay";
    overlay.setAttribute("role", "dialog");
    overlay.setAttribute("aria-modal", "true");
    overlay.setAttribute("aria-hidden", "true");
    overlay.setAttribute("aria-labelledby", "trtt-room-title");

    var panel = el("div", "trtt-room-panel");
    var header = el("header", "trtt-room-header");
    var identity = el("div", "trtt-room-identity");
    identity.appendChild(el("span", "trtt-room-eyebrow", "TRTT VOYAGE • SANLURI TO WORLD"));
    var title = el("h2", "", "THINKING ROOM");
    title.id = "trtt-room-title";
    identity.appendChild(title);
    identity.appendChild(el("p", "", "A quiet room for clear thinking and building."));
    var close = el("button", "trtt-room-close", "×");
    close.type = "button";
    close.setAttribute("aria-label", "Close Thinking Room");
    header.appendChild(identity);
    header.appendChild(close);
    panel.appendChild(header);

    panel.appendChild(el("div", "trtt-room-lock", "ROKSANA — LOCKED"));
    var main = el("main", "trtt-room-main");
    main.appendChild(el("span", "trtt-room-eyebrow", "ONE TASK AT A TIME"));
    main.appendChild(el("h3", "", "Think. Build. Move forward."));
    main.appendChild(el("p", "trtt-room-description",
      "This room is for focused work on TRTT Voyage. No extra menus. No distractions."));
    panel.appendChild(main);
    panel.appendChild(el("footer", "trtt-room-footer",
      "TRTT MAC-787950 LOCKED • Made by MAC — Muse, Abu, ChatGPT"));
    overlay.appendChild(panel);

    function openRoom() {
      overlay.classList.add("is-open");
      overlay.setAttribute("aria-hidden", "false");
      document.documentElement.classList.add("trtt-room-open");
      door.setAttribute("aria-expanded", "true");
      close.focus();
    }
    function closeRoom() {
      overlay.classList.remove("is-open");
      overlay.setAttribute("aria-hidden", "true");
      document.documentElement.classList.remove("trtt-room-open");
      door.setAttribute("aria-expanded", "false");
      door.focus();
    }

    door.addEventListener("click", openRoom);
    close.addEventListener("click", closeRoom);
    overlay.addEventListener("click", function (event) {
      if (event.target === overlay) closeRoom();
    });
    document.addEventListener("keydown", function (event) {
      if (overlay.classList.contains("is-open") && event.key === "Escape") {
        event.preventDefault();
        closeRoom();
      }
    });

    document.body.appendChild(overlay);
    document.body.appendChild(door);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", buildDoor, { once: true });
  } else {
    buildDoor();
  }
})();