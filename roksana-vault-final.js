
/* =========================================================
   ROKSANA NILLA — TRTT FINAL VAULT
   Strict 3-domain allowlist | 12-color rotation
   Responsive cards | Live clock | Duplicate protection
   ========================================================= */

(function () {
  "use strict";

  var ROOT_ID = "RoksanaFinalVault";
  var STYLE_ID = "roksana-final-vault-style";
  var ALLOWED = [
    "trttnews24bd.blogspot.com",
    "trttnews24bd.com",
    "www.trttnews24bd.com"
  ];

  var host = window.location.hostname.toLowerCase().trim();

  /* Strict domain lock */
  if (!ALLOWED.includes(host)) {
    var blocked = document.getElementById(ROOT_ID);
    if (blocked) blocked.remove();
    console.warn("[Roksana Vault] Domain not allowed:", host);
    return;
  }

  /* Prevent duplicate initialization */
  if (window.__ROKSANA_VAULT_INITIALIZED__) return;
  window.__ROKSANA_VAULT_INITIALIZED__ = true;

  var colors = [
    "#FF2E63", "#FFC300", "#AF7AC5", "#E8A0A8",
    "#967BB6", "#FF7F70", "#8E44AD", "#FFB38A",
    "#D946A6", "#F4D58D", "#6C3483", "#F7A8C4"
  ];

  var cards = [
    { title: "TRTT Voyage", subtitle: "Travel & Discovery", query: "TRTT Voyage" },
    { title: "Bangladesh", subtitle: "দেশের খবর", query: "Bangladesh" },
    { title: "World News", subtitle: "বিশ্ব সংবাদ", query: "World News" },
    { title: "Technology", subtitle: "প্রযুক্তির খবর", query: "Technology" },
    { title: "Lifestyle", subtitle: "জীবনযাপন", query: "Lifestyle" },
    { title: "Entertainment", subtitle: "বিনোদন", query: "Entertainment" },
    { title: "Travel Stories", subtitle: "ভ্রমণ কাহিনি", query: "Travel Stories" },
    { title: "Food & Culture", subtitle: "খাবার ও সংস্কৃতি", query: "Food Culture" },
    { title: "Business", subtitle: "ব্যবসা-বাণিজ্য", query: "Business" },
    { title: "Education", subtitle: "শিক্ষা", query: "Education" },
    { title: "Health & Life", subtitle: "স্বাস্থ্য ও জীবন", query: "Health Life" },
    { title: "All Articles", subtitle: "সব প্রকাশনা", query: "" }
  ];

  function addStyles() {
    if (document.getElementById(STYLE_ID)) return;

    var css = document.createElement("style");
    css.id = STYLE_ID;
    css.textContent = `
      #${ROOT_ID} {
        box-sizing: border-box;
        width: calc(100% - 20px);
        margin: 12px auto;
        padding: 20px;
        border: 2px solid #FF2E63;
        border-radius: 17px;
        background: linear-gradient(135deg,#fff,#fff0f5);
        box-shadow: 0 5px 20px rgba(255,46,99,.13);
        color: #292929;
        font-family: Arial, sans-serif;
        position: relative;
        z-index: 1;
      }
      #${ROOT_ID} * { box-sizing: border-box; }
      #${ROOT_ID} .rv-heading {
        margin: 0 0 8px;
        color: #FF2E63;
        font-size: clamp(19px,4vw,27px);
        font-weight: 800;
        text-align: center;
      }
      #${ROOT_ID} .rv-subtitle {
        margin: 0 0 12px;
        text-align: center;
        font-size: 14px;
        line-height: 1.6;
      }
      #${ROOT_ID} .rv-clock {
        text-align: center;
        font-size: 13px;
        font-weight: 700;
        margin: 10px 0 17px;
      }
      #${ROOT_ID} .rv-grid {
        display: grid;
        grid-template-columns: repeat(4,minmax(0,1fr));
        gap: 11px;
      }
      #${ROOT_ID} .rv-card {
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-height: 88px;
        padding: 13px 8px;
        border-radius: 12px;
        text-align: center;
        text-decoration: none;
        color: #fff !important;
        background: var(--rv-color);
        box-shadow: 0 3px 9px rgba(0,0,0,.12);
        transition: transform .2s ease, box-shadow .2s ease;
      }
      #${ROOT_ID} .rv-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(0,0,0,.18);
      }
      #${ROOT_ID} .rv-card strong {
        font-size: 14px;
        line-height: 1.4;
      }
      #${ROOT_ID} .rv-card span {
        margin-top: 4px;
        font-size: 11px;
        opacity: .95;
      }
      #${ROOT_ID} .rv-footer {
        margin: 17px 0 0;
        text-align: center;
        color: #666;
        font-size: 10px;
      }
      @media(max-width:700px) {
        #${ROOT_ID} .rv-grid {
          grid-template-columns: repeat(3,minmax(0,1fr));
        }
      }
      @media(max-width:420px) {
        #${ROOT_ID} { padding: 13px; }
        #${ROOT_ID} .rv-grid {
          grid-template-columns: repeat(2,minmax(0,1fr));
          gap: 8px;
        }
        #${ROOT_ID} .rv-card { min-height: 78px; }
      }
      @media(prefers-reduced-motion:reduce) {
        #${ROOT_ID} .rv-card { transition: none; }
      }
    `;
    document.head.appendChild(css);
  }

  function createVault() {
    var existing = document.getElementById(ROOT_ID);
    if (existing) return existing;

    var root = document.createElement("section");
    root.id = ROOT_ID;
    root.setAttribute("aria-label", "Roksana Nilla Final Vault");

    var heading = document.createElement("h2");
    heading.className = "rv-heading";
    heading.textContent = "✨ ROKSANA NILLA'S FINAL VAULT ✨";

    var subtitle = document.createElement("p");
    subtitle.className = "rv-subtitle";
    subtitle.textContent =
      "Tomar Jonno — This Vault is for You | TRTT VOYAGE";

    var clock = document.createElement("div");
    clock.className = "rv-clock";
    clock.setAttribute("aria-live", "off");

    var grid = document.createElement("div");
    grid.className = "rv-grid";

    cards.forEach(function (item, index) {
      var link = document.createElement("a");
      link.className = "rv-card";
      link.style.setProperty("--rv-color", colors[index]);

      var query = item.query
        ? "?q=" + encodeURIComponent(item.query)
        : "";

      link.href =
        "https://trttnews24bd.blogspot.com/search" + query;

      var title = document.createElement("strong");
      title.textContent = item.title;

      var description = document.createElement("span");
      description.textContent = item.subtitle;

      link.appendChild(title);
      link.appendChild(description);
      grid.appendChild(link);
    });

    var footer = document.createElement("p");
    footer.className = "rv-footer";
    footer.textContent = "ROKSANA VAULT • TRTT VOYAGE";

    root.appendChild(heading);
    root.appendChild(subtitle);
    root.appendChild(clock);
    root.appendChild(grid);
    root.appendChild(footer);

    addStyles();

    return root;
  }

  /* Find Blogger header and insert Vault beneath it */
  function placeVault() {
    var root = document.getElementById(ROOT_ID);
    if (!root) root = createVault();

    var header = document.querySelector(
      "header, .header, .Header, #header, #Header, .centered-top-container"
    );

    var feed = document.querySelector(
      "#Blog1, .blog-posts, .blog-posts.hfeed, main"
    );

    if (header && header.parentNode) {
      if (header.nextElementSibling !== root) {
        header.parentNode.insertBefore(root, header.nextSibling);
      }
      return true;
    }

    if (feed && feed.parentNode) {
      if (feed.previousElementSibling !== root) {
        feed.parentNode.insertBefore(root, feed);
      }
      return true;
    }

    return false;
  }

  /* Live local clock */
  function updateClock() {
    var clock = document.querySelector(
      "#" + ROOT_ID + " .rv-clock"
    );
    if (!clock) return;

    clock.textContent = new Intl.DateTimeFormat("en-GB", {
      dateStyle: "medium",
      timeStyle: "medium"
    }).format(new Date());
  }

  var colorIndex = 0;

  function rotateColors() {
    var elements = document.querySelectorAll(
      "#" + ROOT_ID + " .rv-card"
    );

    elements.forEach(function (element, index) {
      element.style.setProperty(
        "--rv-color",
        colors[(index + colorIndex) % colors.length]
      );
    });

    colorIndex = (colorIndex + 1) % colors.length;
  }

  function start() {
    placeVault();
    updateClock();
    rotateColors();

    if (!window.__ROKSANA_VAULT_CLOCK__) {
      window.__ROKSANA_VAULT_CLOCK__ =
        window.setInterval(updateClock, 1000);
    }

    if (!window.__ROKSANA_VAULT_COLORS__) {
      window.__ROKSANA_VAULT_COLORS__ =
        window.setInterval(rotateColors, 2800);
    }

    if (!window.__ROKSANA_VAULT_OBSERVER__) {
      var observer = new MutationObserver(function () {
        if (!document.getElementById(ROOT_ID)) {
          placeVault();
        }
      });

      observer.observe(document.body, {
        childList: true,
        subtree: true
      });

      window.__ROKSANA_VAULT_OBSERVER__ = observer;
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start, {
      once: true
    });
  } else {
    start();
  }

})();
