// TRTT News Blogger menu — Vercel-backed, with only verified tool pages.
(function () {
  "use strict";

  if (window.__TRTT_VERCEL_MENU_V2__) return;
  window.__TRTT_VERCEL_MENU_V2__ = true;

  var BASE = "https://cocvghuj-trtt-news-bot.vercel.app";
  var MARKER = "787950";
  var TELEGRAM = "https://t.me/trttnews24bd";
  var TOOLS = [
    { id: "flight", name: "Flight Search", detail: "Compare available flight routes", icon: "✈️", page: "/tools/flight-search.html" },
    { id: "baggage", name: "Baggage Size Checker", detail: "Check cabin-bag dimensions", icon: "🧳", page: "/tools/baggage-size-checker.html" },
    { id: "delay", name: "Flight Delay Calculator", detail: "Review possible EU261 compensation", icon: "⏱️", page: "/tools/delay-calculator.html" },
    { id: "esim", name: "eSIM Comparator", detail: "Compare travel eSIM providers", icon: "📱", page: "/tools/esim-compare.html" },
    { id: "taxi", name: "Airport Transfer Calculator", detail: "Review airport transfer options", icon: "🚕", page: "/tools/taxi-calculator.html" }
  ];

  var overlay, frame, status, log, title, openLink;

  function addLog(message) {
    if (!log) return;
    var item = document.createElement("div");
    item.textContent = "[" + new Date().toLocaleTimeString() + "] " + message;
    log.appendChild(item);
    log.scrollTop = log.scrollHeight;
  }

  function setStatus(message, good) {
    if (!status) return;
    status.textContent = message;
    status.classList.toggle("is-good", !!good);
    status.classList.toggle("is-bad", !good);
  }

  function checkApi() {
    fetch(BASE + "/api/health", { method: "GET", mode: "cors", cache: "no-store" })
      .then(function (response) {
        if (!response.ok) throw new Error("HTTP " + response.status);
        return response.json();
      })
      .then(function (data) {
        if (!data || data.ok !== true) throw new Error("Health response invalid");
        setStatus("Vercel API online", true);
        addLog("Vercel health check passed (HTTP 200).");
      })
      .catch(function (error) {
        setStatus("Vercel API unavailable", false);
        addLog("Vercel health check failed: " + error.message);
      });
  }

  function track(eventName, toolId) {
    var query = new URLSearchParams({
      m: MARKER,
      src: eventName,
      tool: toolId || "menu",
      t: String(Date.now())
    });
    fetch(BASE + "/api/vault-click?" + query.toString(), {
      method: "GET",
      mode: "cors",
      cache: "no-store",
      keepalive: true
    }).then(function (response) {
      if (!response.ok) throw new Error("HTTP " + response.status);
      return response.json();
    }).then(function (data) {
      if (!data || data.success !== true) throw new Error("API rejected event");
      addLog("Tracking API accepted event (not stored as analytics).");
    }).catch(function (error) {
      addLog("Tracking request failed: " + error.message);
    });
  }

  function loadTool(tool) {
    if (!tool || !frame) return;
    title.textContent = tool.icon + " " + tool.name;
    frame.onload = function () {
      addLog(tool.name + " page response loaded.");
    };
    frame.onerror = function () {
      addLog(tool.name + " page failed to load.");
    };
    frame.src = BASE + tool.page + "?m=" + encodeURIComponent(MARKER);
    openLink.href = BASE + tool.page;
    openLink.hidden = false;
    addLog("Opening verified page: " + tool.page);
    track("tool_select", tool.id);

    overlay.querySelectorAll("[data-tool]").forEach(function (button) {
      button.classList.toggle("active", button.getAttribute("data-tool") === tool.id);
      button.setAttribute("aria-pressed", button.getAttribute("data-tool") === tool.id ? "true" : "false");
    });
  }

  function closeMenu() {
    overlay.classList.remove("open");
    overlay.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
  }

  function build() {
    if (document.getElementById("trtt-vercel-overlay")) return;

    var style = document.createElement("style");
    style.id = "trtt-vercel-menu-style";
    style.textContent = [
      "#trtt-vercel-overlay{position:fixed;inset:0;z-index:2147483647;display:none;flex-direction:column;background:#0b1020;color:#f8fafc;font:14px/1.45 system-ui,-apple-system,Segoe UI,sans-serif;overflow:hidden}",
      "#trtt-vercel-overlay.open{display:flex}",
      "#trtt-vercel-overlay *{box-sizing:border-box}",
      "#trtt-vercel-overlay .trtt-top{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 16px;background:#121b34;border-bottom:1px solid #c9a84c}",
      "#trtt-vercel-overlay .trtt-brand{font-weight:800;color:#f8d879}",
      "#trtt-vercel-overlay .trtt-status{font-size:12px;padding:5px 9px;border-radius:20px;background:#29334b;color:#e2e8f0}",
      "#trtt-vercel-overlay .trtt-status.is-good{background:#123b2b;color:#9df0bd}",
      "#trtt-vercel-overlay .trtt-status.is-bad{background:#4a2026;color:#ffc2c2}",
      "#trtt-vercel-overlay .trtt-close{border:1px solid #475569;background:#202b43;color:white;border-radius:8px;padding:7px 11px;cursor:pointer}",
      "#trtt-vercel-overlay .trtt-body{display:grid;grid-template-columns:minmax(190px,230px) minmax(0,1fr) minmax(250px,310px);gap:10px;padding:10px;min-height:0;flex:1;overflow:hidden}",
      "#trtt-vercel-overlay .trtt-panel{min-width:0;min-height:0;overflow:auto;background:#121a2c;border:1px solid #34415b;border-radius:12px;padding:12px}",
      "#trtt-vercel-overlay .trtt-tool{display:flex;width:100%;align-items:center;gap:10px;text-align:left;padding:11px;margin:5px 0;border:1px solid #34415b;border-radius:9px;background:#18233a;color:#f8fafc;cursor:pointer}",
      "#trtt-vercel-overlay .trtt-tool:hover,#trtt-vercel-overlay .trtt-tool.active{border-color:#f1c75b;background:#27334b}",
      "#trtt-vercel-overlay .trtt-tool small{display:block;color:#b7c2d5;font-size:11px}",
      "#trtt-vercel-overlay .trtt-stage{display:flex;flex-direction:column;padding:0;overflow:hidden}",
      "#trtt-vercel-overlay .trtt-stage-head{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:10px;border-bottom:1px solid #34415b}",
      "#trtt-vercel-overlay .trtt-iframe{width:100%;height:100%;min-height:300px;border:0;background:white;flex:1}",
      "#trtt-vercel-overlay .trtt-log{font:11px/1.5 ui-monospace,monospace;color:#c8d5e8;overflow-wrap:anywhere}",
      "#trtt-vercel-overlay .trtt-log div{padding:5px 0;border-bottom:1px solid #29354c}",
      "#trtt-vercel-overlay .trtt-link{color:#f4d16f;font-size:12px}",
      "#trtt-vercel-fab{position:fixed;left:14px;bottom:14px;z-index:2147483646;width:54px;height:54px;border:2px solid white;border-radius:50%;background:linear-gradient(135deg,#f6d36b,#ef476f);color:#101827;font-size:24px;font-weight:900;box-shadow:0 5px 22px #0008;cursor:pointer}",
      "@media(max-width:900px){#trtt-vercel-overlay{overflow-y:auto}#trtt-vercel-overlay .trtt-top{position:sticky;top:0;z-index:2;flex-wrap:wrap}#trtt-vercel-overlay .trtt-body{display:flex;flex-direction:column;overflow:visible;min-height:auto}#trtt-vercel-overlay .trtt-panel{overflow:visible}#trtt-vercel-overlay .trtt-stage{min-height:62vh}#trtt-vercel-overlay .trtt-iframe{min-height:55vh}#trtt-vercel-overlay .trtt-tools{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:5px}#trtt-vercel-overlay .trtt-tool{margin:0}}",
      "@media(max-width:480px){#trtt-vercel-overlay .trtt-tools{grid-template-columns:1fr}#trtt-vercel-overlay .trtt-top{align-items:flex-start}#trtt-vercel-overlay .trtt-stage{min-height:65vh}}"
    ].join("\n");
    document.head.appendChild(style);

    overlay = document.createElement("div");
    overlay.id = "trtt-vercel-overlay";
    overlay.setAttribute("aria-hidden", "true");
    overlay.innerHTML =
      '<div class="trtt-top"><div><div class="trtt-brand">TRTT NEWS • TRAVEL TOOLS</div><div style="font-size:11px;color:#cbd5e1">Blogger menu connected to Vercel</div></div><div style="display:flex;align-items:center;gap:8px"><span class="trtt-status" id="trtt-vercel-status">Checking API…</span><button type="button" class="trtt-close" id="trtt-vercel-close" aria-label="Close menu">✕</button></div></div>' +
      '<div class="trtt-body"><section class="trtt-panel"><b>Available tools</b><div class="trtt-tools" id="trtt-vercel-tools"></div><p style="font-size:11px;color:#b7c2d5">Only pages present in the deployed project are listed.</p><a class="trtt-link" href="' + TELEGRAM + '" target="_blank" rel="noopener noreferrer">Join TRTT Telegram ↗</a></section>' +
      '<section class="trtt-panel trtt-stage"><div class="trtt-stage-head"><b id="trtt-vercel-title">Choose a tool</b><a class="trtt-link" id="trtt-vercel-open" href="#" target="_blank" rel="noopener noreferrer" hidden>Open separately ↗</a></div><iframe class="trtt-iframe" id="trtt-vercel-iframe" title="TRTT travel tool" src="about:blank" loading="lazy"></iframe></section>' +
      '<section class="trtt-panel"><b>Connection log</b><div class="trtt-log" id="trtt-vercel-log" aria-live="polite"></div></section></div>';
    document.body.appendChild(overlay);

    frame = document.getElementById("trtt-vercel-iframe");
    status = document.getElementById("trtt-vercel-status");
    log = document.getElementById("trtt-vercel-log");
    title = document.getElementById("trtt-vercel-title");
    openLink = document.getElementById("trtt-vercel-open");

    var toolContainer = document.getElementById("trtt-vercel-tools");
    TOOLS.forEach(function (tool) {
      var button = document.createElement("button");
      button.type = "button";
      button.className = "trtt-tool";
      button.setAttribute("data-tool", tool.id);
      button.setAttribute("aria-pressed", "false");
      var icon = document.createElement("span");
      icon.textContent = tool.icon;
      icon.setAttribute("aria-hidden", "true");
      var copy = document.createElement("span");
      copy.innerHTML = "<b></b><small></small>";
      copy.querySelector("b").textContent = tool.name;
      copy.querySelector("small").textContent = tool.detail;
      button.appendChild(icon);
      button.appendChild(copy);
      button.addEventListener("click", function () { loadTool(tool); });
      toolContainer.appendChild(button);
    });

    document.getElementById("trtt-vercel-close").addEventListener("click", closeMenu);
    overlay.addEventListener("click", function (event) {
      if (event.target === overlay) closeMenu();
    });

    checkApi();
  }

  function addLauncher() {
    if (document.getElementById("trtt-vercel-fab")) return;
    var launcher = document.createElement("button");
    launcher.type = "button";
    launcher.id = "trtt-vercel-fab";
    launcher.textContent = "⋯";
    launcher.setAttribute("aria-label", "Open TRTT travel tools menu");
    launcher.addEventListener("click", function () {
      overlay.classList.add("open");
      overlay.setAttribute("aria-hidden", "false");
      document.body.style.overflow = "hidden";
      track("menu_open", "menu");
      checkApi();
      if (!frame.src || frame.src === "about:blank") loadTool(TOOLS[0]);
    });
    document.body.appendChild(launcher);
  }

  function init() {
    build();
    addLauncher();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();