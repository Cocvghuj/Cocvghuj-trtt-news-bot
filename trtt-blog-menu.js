(function () {
  "use strict";

  var MENU_ID = "trtt-final-menu";
  var STYLE_ID = "trtt-final-menu-styles";

  function installMenu() {
    if (!document.body || document.getElementById(MENU_ID)) return;

    var style = document.createElement("style");
    style.id = STYLE_ID;
    style.textContent = [
      "#trtt-final-menu{position:sticky;top:0;z-index:99999;width:100%;background:#ff2e63;font-family:Arial,sans-serif;box-sizing:border-box}",
      "#trtt-final-menu *{box-sizing:border-box}",
      "#trtt-final-menu .trtt-bar{min-height:50px;padding:0 15px;display:flex;align-items:center;justify-content:space-between;gap:12px;position:relative}",
      "#trtt-final-menu .trtt-logo-txt{color:#fff;font-weight:800;font-size:16px;letter-spacing:1px;white-space:nowrap}",
      "#trtt-final-menu .trtt-ham{display:none;border:0;background:transparent;color:#fff;font-size:25px;line-height:1;padding:8px;cursor:pointer}",
      "#trtt-final-menu .trtt-links{display:flex;align-items:center;list-style:none;margin:0;padding:0;gap:0}",
      "#trtt-final-menu .trtt-links a{display:block;padding:17px 12px;color:#fff!important;text-decoration:none;font-weight:700;font-size:13px;white-space:nowrap}",
      "#trtt-final-menu .trtt-links a:hover,#trtt-final-menu .trtt-links a:focus-visible{background:rgba(0,0,0,.16);outline-offset:-3px}",
      "@media(max-width:768px){#trtt-final-menu .trtt-bar{padding:0 12px}#trtt-final-menu .trtt-ham{display:block}#trtt-final-menu .trtt-links{display:none;position:absolute;left:0;right:0;top:100%;width:100%;flex-direction:column;align-items:stretch;background:#ff5a8a;box-shadow:0 10px 20px rgba(0,0,0,.2)}#trtt-final-menu.open .trtt-links{display:flex}#trtt-final-menu .trtt-links a{padding:13px 16px;border-top:1px solid rgba(255,255,255,.16)}}",
      "@media(min-width:769px) and (max-width:950px){#trtt-final-menu .trtt-links a{padding-left:8px;padding-right:8px;font-size:12px}}"
    ].join("\n");
    document.head.appendChild(style);

    var menu = document.createElement("nav");
    menu.id = MENU_ID;
    menu.setAttribute("aria-label", "Main navigation");
    menu.innerHTML =
      '<div class="trtt-bar">' +
        '<a class="trtt-logo-txt" href="/" style="text-decoration:none">TRTT VOYAGE</a>' +
        '<button class="trtt-ham" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="trtt-main-links">☰</button>' +
        '<ul class="trtt-links" id="trtt-main-links">' +
          '<li><a href="/">Home</a></li>' +
          '<li><a href="/search/label/eSIM">eSIM Guide</a></li>' +
          '<li><a href="/search/label/Flights">Flights</a></li>' +
          '<li><a href="https://cocvghuj-trtt-news-bot.vercel.app/">Explore Life</a></li>' +
          '<li><a href="/p/about-us.html">About Us</a></li>' +
          '<li><a href="/p/contact.html">Contact</a></li>' +
        '</ul>' +
      '</div>';

    document.body.insertBefore(menu, document.body.firstChild);

    var toggle = menu.querySelector(".trtt-ham");
    function closeMenu() {
      menu.classList.remove("open");
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", "Open menu");
    }
    toggle.addEventListener("click", function () {
      var expanded = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!expanded));
      toggle.setAttribute("aria-label", expanded ? "Open menu" : "Close menu");
      menu.classList.toggle("open", !expanded);
    });
    menu.querySelectorAll(".trtt-links a").forEach(function (link) {
      link.addEventListener("click", closeMenu);
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") closeMenu();
    });
    document.addEventListener("click", function (event) {
      if (!menu.contains(event.target)) closeMenu();
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", installMenu, { once: true });
  } else {
    installMenu();
  }
})();
