/*! TRTT VOYAGE — THINKING ROOM DOOR / V105
 * Phase 1: navigation bar + Thinking Room entrance only.
 * The inner Thinking Room experience will be added in a later phase.
 */
(function () {
  "use strict";
  if (window.__TRTT_DOOR_V105__) return;
  window.__TRTT_DOOR_V105__ = true;

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

  function el(tag, cls, value) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (value != null) n.textContent = value;
    return n;
  }

  function makeRoute(item) {
    var a = el("a", "trtt-route-bubble");
    a.href = item[2];
    a.appendChild(el("strong", "", item[0]));
    a.appendChild(el("span", "", item[1]));
    return a;
  }

  function findMount() {
    var slot = document.querySelector(".header-menu, #main-menu, #main-menu-nav");
    if (slot) return slot;
    var header = document.querySelector("#header-wrap, #header-wrapper, #header, header");
    if (header && header.parentNode) return { parent: header.parentNode, after: header };
    var main = document.querySelector("#main-wrapper, #main, .blog-posts");
    if (main && main.parentNode) return { parent: main.parentNode, before: main };
    return { parent: document.body, before: document.body.firstChild };
  }

  function mount() {
    if (!document.body) return false;
    if (document.getElementById("trtt-control-nav")) return true;

    var nav = el("nav", "trtt-control-nav");
    nav.id = "trtt-control-nav";
    nav.setAttribute("aria-label", "TRTT Voyage main menu");

    var brand = el("a", "trtt-control-brand", "TRTT VOYAGE");
    brand.href = "/";
    nav.appendChild(brand);

    var list = el("div", "trtt-route-list");
    ROUTES.forEach(function (item) { list.appendChild(makeRoute(item)); });
    nav.appendChild(list);

    var door = el("button", "trtt-thinking-room-trigger");
    door.type = "button";
    door.id = "trtt-thinking-room-trigger";
    door.setAttribute("aria-label", "Thinking Room entrance — coming soon");
    door.title = "Thinking Room — opening soon";
    door.appendChild(el("span", "trtt-door-icon", "✦"));
    var copy = el("span", "trtt-door-copy");
    copy.appendChild(el("strong", "", "THINKING ROOM"));
    copy.appendChild(el("small", "", "ENTER THE IDEA SPACE"));
    door.appendChild(copy);
    door.appendChild(el("span", "trtt-door-arrow", "↗"));
    door.addEventListener("click", function () {
      var note = document.getElementById("trtt-door-note");
      if (!note) {
        note = el("div", "trtt-door-note", "Thinking Room is being prepared. The door is ready; the room comes next.");
        note.id = "trtt-door-note";
        note.setAttribute("role", "status");
        document.body.appendChild(note);
      }
      note.classList.add("is-visible");
      window.setTimeout(function () { note.classList.remove("is-visible"); }, 2600);
    });
    nav.appendChild(door);

    var target = findMount();
    if (target && target.parent && target.after) {
      target.parent.insertBefore(nav, target.after.nextSibling);
    } else if (target && target.parent && Object.prototype.hasOwnProperty.call(target, "before")) {
      target.parent.insertBefore(nav, target.before || null);
    } else if (target && target.appendChild) {
      target.appendChild(nav);
    } else {
      document.body.insertBefore(nav, document.body.firstChild);
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