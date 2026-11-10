/*! TRTT VOYAGE — THINKING ROOM DOOR / V106
 * GitHub-controlled door. No Blogger theme edits required.
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

  // Exact insertion point from the saved TRTT Blogger layout:
  // #header-wrap > .container > .header-menu > #main-menu
  function findMount() {
    return document.querySelector("#header-wrap .header-menu") ||
      document.querySelector("#header-wrap #main-menu") ||
      document.querySelector("#header-wrap");
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
    door.title = "Thinking Room";
    door.appendChild(node("span", "trtt-door-icon", "✦"));

    var copy = node("span", "trtt-door-copy");
    copy.appendChild(node("strong", "", "THINKING ROOM"));
    copy.appendChild(node("small", "", "ENTER THE IDEA SPACE"));
    door.appendChild(copy);
    door.appendChild(node("span", "trtt-door-arrow", "↗"));

    door.addEventListener("click", function () {
      var note = document.getElementById("trtt-door-note");
      if (!note) {
        note = node("div", "trtt-door-note",
          "Thinking Room is being prepared. The door is ready; the room comes next.");
        note.id = "trtt-door-note";
        note.setAttribute("role", "status");
        document.body.appendChild(note);
      }
      note.classList.add("is-visible");
      window.clearTimeout(window.__TRTT_DOOR_NOTE_TIMER__);
      window.__TRTT_DOOR_NOTE_TIMER__ = window.setTimeout(function () {
        note.classList.remove("is-visible");
      }, 2600);
    });

    nav.appendChild(door);
    return nav;
  }

  function mount() {
    if (!document.body) return false;
    var target = findMount();
    if (!target) return false;

    var old = document.getElementById("trtt-control-nav");
    if (old) old.remove();

    var nav = buildDoor();

    if (target.classList && target.classList.contains("header-menu")) {
      // The old menu lives in this exact header slot; replace only its contents.
      while (target.firstChild) target.removeChild(target.firstChild);
      target.appendChild(nav);
    } else if (target.id === "main-menu") {
      while (target.firstChild) target.removeChild(target.firstChild);
      target.appendChild(nav);
    } else {
      // Last-resort fallback stays inside the header, never at the bottom of the page.
      target.appendChild(nav);
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