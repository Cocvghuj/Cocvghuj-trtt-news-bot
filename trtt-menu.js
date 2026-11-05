/* TRTT responsive Blogger navigation — accessible, duplicate-safe */
(function () {
  "use strict";
  if (window.__TRTT_MENU_V2__) return;
  window.__TRTT_MENU_V2__ = true;

  var allowed = ["trttnews24bd.blogspot.com", "trttnews24bd.com", "www.trttnews24bd.com"];
  var host = location.hostname.toLowerCase();
  if (!allowed.some(function (domain) { return host === domain || host.endsWith("." + domain); })) return;

  function mount() {
    if (!document.body || document.getElementById("trtt-menu")) return;

    var style = document.createElement("style");
    style.id = "trtt-menu-responsive-style";
    style.textContent = [
      "#trtt-menu{position:sticky;top:0;z-index:99999;background:#fff;border-bottom:3px solid #ef476f;box-shadow:0 8px 24px rgba(20,33,61,.10);font-family:Arial,sans-serif}",
      "#trtt-menu *{box-sizing:border-box}",
      "#trtt-menu .menu-wrap{max-width:1240px;min-height:68px;margin:auto;padding:10px 20px;display:flex;align-items:center;justify-content:space-between;gap:18px}",
      "#trtt-menu .logo{display:flex;align-items:center;gap:9px;flex-shrink:0;color:#14213d;font-size:17px;font-weight:900;letter-spacing:.04em;text-decoration:none}",
      "#trtt-menu .logo-mark{width:36px;height:36px;display:grid;place-items:center;border-radius:11px;background:linear-gradient(135deg,#ef476f,#ffc857);color:#14213d;font-size:19px}",
      "#trtt-menu .links{display:flex;align-items:center;justify-content:flex-end;gap:5px}",
      "#trtt-menu .links a{display:block;padding:10px 13px;border-radius:10px;color:#33415c;text-decoration:none;font-size:13px;font-weight:750;transition:background .18s,color .18s,transform .18s}",
      "#trtt-menu .links a:hover,#trtt-menu .links a:focus-visible{background:#fff0f3;color:#d93660;outline:none}",
      "#trtt-menu .menu-toggle{display:none;align-items:center;justify-content:center;gap:9px;min-width:44px;min-height:44px;padding:9px 12px;border:1px solid #e7eaf1;border-radius:12px;background:#fff;color:#14213d;font-size:13px;font-weight:800;cursor:pointer}",
      "#trtt-menu .menu-toggle-icon{display:grid;gap:4px}",
      "#trtt-menu .menu-toggle-icon i{display:block;width:18px;height:2px;border-radius:2px;background:#14213d;transition:transform .2s,opacity .2s}",
      "#trtt-menu .menu-toggle[aria-expanded=true] .menu-toggle-icon i:first-child{transform:translateY(6px) rotate(45deg)}",
      "#trtt-menu .menu-toggle[aria-expanded=true] .menu-toggle-icon i:nth-child(2){opacity:0}",
      "#trtt-menu .menu-toggle[aria-expanded=true] .menu-toggle-icon i:last-child{transform:translateY(-6px) rotate(-45deg)}",
      "@media(max-width:760px){#trtt-menu .menu-wrap{min-height:64px;padding:9px 14px;flex-wrap:wrap;gap:8px}#trtt-menu .logo{font-size:15px}#trtt-menu .menu-toggle{display:flex}#trtt-menu .links{display:none;order:3;flex:0 0 100%;width:100%;padding:8px;background:#fff;border:1px solid #edf0f5;border-radius:15px;box-shadow:0 12px 28px rgba(20,33,61,.10);flex-direction:column;align-items:stretch;gap:3px}#trtt-menu .links.is-open{display:flex}#trtt-menu .links a{padding:13px 14px;border-radius:10px;font-size:14px}#trtt-menu .links a+a{border-top:1px solid #f3f4f7}}",
      "@media(prefers-reduced-motion:reduce){#trtt-menu *{transition:none!important}}"
    ].join("");
    document.head.appendChild(style);

    var nav = document.createElement("nav");
    nav.id = "trtt-menu";
    nav.setAttribute("aria-label", "TRTT main navigation");
    nav.innerHTML =
      '<div class="menu-wrap">' +
        '<a class="logo" href="/" aria-label="TRTT Voyage home"><span class="logo-mark">T</span><span>TRTT VOYAGE</span></a>' +
        '<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="trtt-menu-links">' +
          '<span class="menu-toggle-icon" aria-hidden="true"><i></i><i></i><i></i></span><span>Menu</span>' +
        '</button>' +
        '<div class="links" id="trtt-menu-links">' +
          '<a href="/">Home</a><a href="/search/label/TRTT%20News">TRTT News</a>' +
          '<a href="/search/label/Travel">Travel</a><a href="/search/label/Voyage">Voyage Hub</a>' +
          '<a href="/p/about.html">About</a>' +
        '</div>' +
      '</div>';
    document.body.insertBefore(nav, document.body.firstChild);

    var toggle = nav.querySelector(".menu-toggle");
    var links = nav.querySelector(".links");
    function closeMenu() {
      toggle.setAttribute("aria-expanded", "false");
      links.classList.remove("is-open");
    }
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") !== "true";
      toggle.setAttribute("aria-expanded", String(open));
      links.classList.toggle("is-open", open);
    });
    links.addEventListener("click", function (event) {
      if (event.target.closest("a")) closeMenu();
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") closeMenu();
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth > 760) closeMenu();
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount, { once: true });
  } else {
    mount();
  }
})();
