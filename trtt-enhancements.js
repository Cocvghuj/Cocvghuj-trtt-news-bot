/* TRTT Voyage Enhancements
   Version: TRTT-ENHANCEMENTS-2026-11-08-03
   Separate enhancement layer. Does not edit the Blogger Theme, menu gadget, or Vercel deployment.
*/
(function () {
  "use strict";

  var VERSION = "TRTT-ENHANCEMENTS-2026-11-08-03";
  var MARKER = "787950";
  var BLOG = "https://trttnews24bd.blogspot.com";
  var FEED = BLOG + "/feeds/posts/default";
  var VERCEL = "https://cocvghuj-trtt-news-bot.vercel.app/?marker=787950";
  var DISCLOSURE = "Disclosure: As an Amazon Associate and Travelpayouts partner, TRTT Voyage earns from qualifying purchases.";
  var CREDIT = "Built by Cocvghuj on GitHub";
  var TEAM_CREDIT = "Made With Muse. Instruction from Muse. Fixed by ChatGPT.";

  var LABELS = [
    "Flight News",
    "Passenger Rights",
    "eSIM & Stay Connected",
    "Ride & Stay",
    "Tour & Experience",
    "Sanluri Diary"
  ];

  var CITIES = [
    "Cagliari", "Sanluri", "Rome", "Milan", "Bergamo", "London",
    "Paris", "Barcelona", "Dubai", "Dhaka", "Bangkok", "New York"
  ];

  function find(selectors, root) {
    root = root || document;
    for (var i = 0; i < selectors.length; i++) {
      var result = root.querySelector(selectors[i]);
      if (result) return result;
    }
    return null;
  }

  function element(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function isPostPage() {
    return document.body.classList.contains("item") ||
      /\/\d{4}\/\d{2}\/[^/?#]+\.html/i.test(location.pathname);
  }

  function isHomePage() {
    return location.pathname === "/" &&
      !document.body.classList.contains("item");
  }

  function getPostBody() {
    return find([".post-body", ".post-body-container", ".entry-content", ".post-content"]);
  }

  function fetchFeed() {
    return fetch(FEED + "?alt=json&max-results=150", {
      credentials: "omit",
      cache: "default"
    }).then(function (response) {
      if (!response.ok) throw new Error("Blogger feed unavailable");
      return response.json();
    });
  }

  function entries(data) {
    return data && data.feed && data.feed.entry ? data.feed.entry : [];
  }

  function entryUrl(entry) {
    var alternate = (entry.link || []).find(function (item) {
      return item.rel === "alternate";
    });
    if (!alternate || !alternate.href) return "";
    try {
      var url = new URL(alternate.href, BLOG);
      url.hash = "";
      return url.href.replace(/\/$/, "");
    } catch (_) {
      return alternate.href.split("#")[0].replace(/\/$/, "");
    }
  }

  function entryLabels(entry) {
    return (entry && entry.category ? entry.category : [])
      .map(function (category) { return category.term || ""; })
      .filter(Boolean);
  }

  /* Clean only the three explicitly approved visible entity wrappers.
     All surrounding article text and punctuation remain unchanged. */
  function cleanEntityText(root) {
    if (!root || !document.createTreeWalker) return 0;
    var pattern = /【entity-(facebook|visa|muse)¦canonical_name=[^】]*】/gi;
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        var parent = node.parentElement;
        if (!parent || parent.closest("script, style, textarea, code, pre, noscript")) {
          return NodeFilter.FILTER_REJECT;
        }
        pattern.lastIndex = 0;
        return pattern.test(node.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT;
      }
    });
    var nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    var count = 0;
    nodes.forEach(function (node) {
      pattern.lastIndex = 0;
      var next = node.nodeValue.replace(pattern, function (_, name) {
        count++;
        return name.charAt(0).toUpperCase() + name.slice(1).toLowerCase();
      });
      if (next !== node.nodeValue) node.nodeValue = next;
    });
    return count;
  }

  function watchForLateEntityText(root) {
    if (!root || !window.MutationObserver) return;
    var observer = new MutationObserver(function (records) {
      records.forEach(function (record) {
        if (record.type === "characterData" && record.target.parentElement) {
          cleanEntityText(record.target.parentElement);
        }
        Array.prototype.forEach.call(record.addedNodes || [], function (node) {
          if (node.nodeType === 1) cleanEntityText(node);
          else if (node.nodeType === 3 && node.parentElement) cleanEntityText(node.parentElement);
        });
      });
    });
    observer.observe(root, { childList: true, subtree: true, characterData: true });
  }

  function imageAtSize(url, size) {
    if (!url) return "";
    return url
      .replace(/\/s\d+(-c)?\//i, "/s" + size + "/")
      .replace(/=s\d+(-c)?(?=($|&))/i, "=s" + size);
  }

  function getEntryImage(entry) {
    var media = entry && entry.media$thumbnail && entry.media$thumbnail.url;
    if (media) return imageAtSize(media, 1200);
    var html = entry && entry.content && entry.content.$t ? entry.content.$t : "";
    var match = html.match(/<img[^>]+src=["']([^"']+)["']/i);
    return match ? imageAtSize(match[1], 1200) : "";
  }

  function plainExcerpt(entry) {
    var html = entry && entry.summary && entry.summary.$t
      ? entry.summary.$t
      : (entry && entry.content && entry.content.$t ? entry.content.$t : "");
    var box = document.createElement("div");
    box.innerHTML = html;
    return (box.textContent || box.innerText || "").replace(/\s+/g, " ").trim().slice(0, 145);
  }

  function formatDate(value) {
    if (!value) return "";
    var date = new Date(value);
    if (isNaN(date.getTime())) return "";
    return date.toLocaleDateString("en-GB", {
      day: "numeric", month: "short", year: "numeric"
    });
  }

  function buildFlightSearch() {
    var section = element("section", "trtt-home-flight");
    section.setAttribute("aria-labelledby", "trtt-flight-title");
    section.appendChild(element("p", "trtt-eyebrow", "PLAN YOUR NEXT JOURNEY"));
    var flightHeading = element("h2", "", "Where would you like to go?");
    flightHeading.id = "trtt-flight-title";
    section.appendChild(flightHeading);
    var form = element("form", "trtt-flight-form");
    form.setAttribute("role", "search");
    var fromWrap = element("label", "trtt-flight-field");
    fromWrap.appendChild(element("span", "", "FROM"));
    var from = element("input");
    from.type = "text";
    from.name = "from";
    from.placeholder = "Departure city";
    from.autocomplete = "off";
    from.required = true;
    fromWrap.appendChild(from);
    var toWrap = element("label", "trtt-flight-field");
    toWrap.appendChild(element("span", "", "TO"));
    var to = element("input");
    to.type = "text";
    to.name = "to";
    to.placeholder = "Destination";
    to.autocomplete = "off";
    to.required = true;
    toWrap.appendChild(to);
    var button = element("button", "trtt-flight-submit", "Search flights");
    button.type = "submit";
    form.append(fromWrap, toWrap, button);
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var origin = from.value.trim();
      var destination = to.value.trim();
      if (!origin || !destination) return;
      var query = "Flights from " + origin + " to " + destination;
      window.open("https://www.google.com/travel/flights?q=" + encodeURIComponent(query), "_blank", "noopener");
    });
    section.appendChild(form);
    section.appendChild(element("p", "trtt-flight-note", "Flight search opens Google Flights in a new tab."));
    return section;
  }

  function buildCategories() {
    var section = element("section", "trtt-home-categories");
    section.appendChild(element("p", "trtt-eyebrow", "EXPLORE TRTT VOYAGE"));
    section.appendChild(element("h2", "", "Travel smarter, wherever you go"));
    section.appendChild(element("p", "trtt-section-intro", "Practical travel news, rights and ideas for every part of your journey."));
    var grid = element("div", "trtt-category-grid");
    var descriptions = [
      "Airline updates, routes and travel alerts.",
      "Know your rights before and after a journey.",
      "Stay connected with eSIM guides and tips.",
      "Helpful ideas for transport and accommodation.",
      "Discover activities, places and experiences.",
      "Local notes and everyday life from Sanluri."
    ];
    var icons = ["✈", "⚖", "◉", "⌂", "◎", "☀"];
    LABELS.forEach(function (label, index) {
      var card = element("a", "trtt-category-card trtt-category-" + (index + 1));
      card.href = BLOG + "/search/label/" + encodeURIComponent(label);
      card.appendChild(element("span", "trtt-category-icon", icons[index]));
      card.appendChild(element("strong", "", label));
      card.appendChild(element("span", "trtt-category-description", descriptions[index]));
      card.appendChild(element("span", "trtt-category-arrow", "Explore stories →"));
      grid.appendChild(card);
    });
    section.appendChild(grid);
    return section;
  }

  function buildVoyageHub() {
    var section = element("section", "trtt-voyage-hub");
    section.appendChild(element("div", "trtt-hub-copy"));
    var copy = section.querySelector(".trtt-hub-copy");
    copy.appendChild(element("p", "trtt-eyebrow", "THE TRTT VOYAGE HUB"));
    copy.appendChild(element("h2", "", "Real places. Useful travel knowledge."));
    copy.appendChild(element("p", "", "Travel notes shaped by lived experience across Warsaw, Płońsk, Cagliari and Sanluri—shared with a wider world of travellers."));
    var link = element("a", "trtt-hub-link", "Read Sanluri Diary →");
    link.href = BLOG + "/search/label/" + encodeURIComponent("Sanluri Diary");
    copy.appendChild(link);
    var places = element("div", "trtt-hub-places");
    ["WARSAW", "PŁOŃSK", "CAGLIARI", "SANLURI"].forEach(function (place, index) {
      var item = element("div", "trtt-hub-place trtt-hub-place-" + (index + 1));
      item.appendChild(element("span", "", "0" + (index + 1)));
      item.appendChild(element("strong", "", place));
      places.appendChild(item);
    });
    section.appendChild(places);
    section.appendChild(element("p", "trtt-team-credit", TEAM_CREDIT));
    return section;
  }

  function buildRecentPosts() {
    var section = element("section", "trtt-home-recent");
    section.appendChild(element("p", "trtt-eyebrow", "FRESH FROM THE JOURNAL"));
    section.appendChild(element("h2", "", "Recent posts"));
    var grid = element("div", "trtt-recent-grid");
    grid.appendChild(element("p", "trtt-recent-loading", "Loading the latest TRTT Voyage stories…"));
    section.appendChild(grid);
    return { section: section, grid: grid };
  }

  function renderRecentPosts(grid, data) {
    var recent = entries(data).slice(0, 6);
    grid.textContent = "";
    recent.forEach(function (entry) {
      var url = entryUrl(entry);
      if (!url) return;
      var title = entry.title && entry.title.$t ? entry.title.$t : "Read story";
      var card = element("article", "trtt-recent-card");
      var link = element("a", "trtt-recent-image-link");
      link.href = url;
      var imageUrl = getEntryImage(entry);
      if (imageUrl) {
        var image = element("img", "trtt-recent-image");
        image.src = imageAtSize(imageUrl, 480);
        image.srcset = imageAtSize(imageUrl, 480) + " 480w, " + imageAtSize(imageUrl, 1200) + " 1200w";
        image.sizes = "(max-width: 600px) 88vw, 360px";
        image.alt = title;
        image.loading = "lazy";
        image.decoding = "async";
        link.appendChild(image);
      } else {
        link.appendChild(element("span", "trtt-recent-image-fallback", "TRTT VOYAGE"));
      }
      card.appendChild(link);
      var content = element("div", "trtt-recent-content");
      var date = formatDate(entry.published && entry.published.$t);
      if (date) content.appendChild(element("time", "trtt-recent-date", date));
      var heading = element("h3");
      var titleLink = element("a", "", title);
      titleLink.href = url;
      heading.appendChild(titleLink);
      content.appendChild(heading);
      var excerpt = plainExcerpt(entry);
      if (excerpt) content.appendChild(element("p", "trtt-recent-excerpt", excerpt));
      var read = element("a", "trtt-recent-read", "Read story →");
      read.href = url;
      content.appendChild(read);
      card.appendChild(content);
      grid.appendChild(card);
    });
    if (!grid.children.length) {
      grid.appendChild(element("p", "trtt-recent-loading", "New stories will appear here soon."));
    }
  }

  function addHomepageExperience() {
    if (document.querySelector(".trtt-home-experience")) return;
    var anchor = find([".blog-posts", ".blog-posts.hfeed", ".main .widget.Blog", "#Blog1", "main", "#main", "#content"]);
    if (!anchor) return;

    var page = element("div", "trtt-home-experience");
    var hero = element("section", "trtt-home-hero");
    var heroCopy = element("div", "trtt-home-hero-copy");
    heroCopy.appendChild(element("p", "trtt-eyebrow", "SANLURI TO WORLD"));
    heroCopy.appendChild(element("h1", "", "Your journey. Better informed."));
    heroCopy.appendChild(element("p", "trtt-home-hero-intro", "Travel news, passenger rights and practical guides—made clearer for the journey ahead."));
    var actions = element("div", "trtt-home-hero-actions");
    var explore = element("a", "trtt-button trtt-button-primary", "Explore travel stories");
    explore.href = BLOG + "/search";
    var local = element("a", "trtt-button trtt-button-secondary", "Discover Sanluri");
    local.href = BLOG + "/search/label/" + encodeURIComponent("Sanluri Diary");
    actions.append(explore, local);
    heroCopy.appendChild(actions);
    var heroVisual = element("div", "trtt-home-hero-visual");
    heroVisual.appendChild(element("span", "trtt-hero-orbit trtt-hero-orbit-one", "✈"));
    heroVisual.appendChild(element("span", "trtt-hero-orbit trtt-hero-orbit-two", "TRTT"));
    heroVisual.appendChild(element("span", "trtt-hero-stamp", "SANLURI TO WORLD"));
    hero.append(heroCopy, heroVisual);
    page.appendChild(hero);
    page.appendChild(buildFlightSearch());
    page.appendChild(buildCategories());
    page.appendChild(buildVoyageHub());
    var recent = buildRecentPosts();
    page.appendChild(recent.section);

    anchor.parentNode.insertBefore(page, anchor);
    fetchFeed().then(function (data) {
      renderRecentPosts(recent.grid, data);
      var isFeedAnchor = anchor.matches && anchor.matches(".blog-posts, #Blog1, .main .widget.Blog");
      if (isFeedAnchor) {
        anchor.classList.add("trtt-home-original-feed-hidden");
        var pager = find([".blog-pager", ".blog-pager-older", ".blog-pager-newer"]);
        if (pager) pager.classList.add("trtt-home-original-feed-hidden");
      }
    }).catch(function () {
      recent.grid.textContent = "";
      recent.grid.appendChild(element("p", "trtt-recent-loading", "Browse all stories from the TRTT Voyage archive."));
      var archive = element("a", "trtt-recent-read", "Open the story archive →");
      archive.href = BLOG + "/search";
      recent.grid.appendChild(archive);
    });
  }

  function addSearch(body) {
    if (document.querySelector(".trtt-enh-search")) return;
    var form = element("form", "trtt-enh-search");
    form.action = BLOG + "/search";
    form.method = "get";
    var label = element("span", "trtt-enh-search-label", "FIND YOUR NEXT JOURNEY");
    var row = element("div", "trtt-enh-search-row");
    var input = element("input");
    input.type = "search";
    input.name = "q";
    input.placeholder = "Search TRTT Voyage...";
    input.setAttribute("aria-label", "Search TRTT Voyage");
    var button = element("button", "", "Search");
    button.type = "submit";
    row.append(input, button);
    form.append(label, row);
    body.parentNode.insertBefore(form, body);
  }

  function styleArticle(body) {
    body.classList.add("trtt-enh-article");
    var images = body.querySelectorAll("img");
    Array.prototype.forEach.call(images, function (photo, index) {
      photo.loading = index === 0 ? "eager" : "lazy";
      photo.decoding = "async";
      if (index === 0) {
        photo.classList.add("trtt-enh-first-photo");
        photo.fetchPriority = "high";
        var upgraded = imageAtSize(photo.getAttribute("src") || photo.src, 1200);
        if (upgraded && upgraded !== photo.src) photo.src = upgraded;
      }
    });
    var firstParagraph = body.querySelector("p");
    if (firstParagraph) firstParagraph.classList.add("trtt-enh-hook");
  }

  function addTOC(body) {
    if (body.querySelector(".trtt-enh-toc")) return;
    var headings = Array.from(body.querySelectorAll("h2, h3"));
    if (headings.length < 2) return;
    var nav = element("nav", "trtt-enh-toc");
    nav.setAttribute("aria-label", "Table of contents");
    nav.appendChild(element("strong", "", "On this page"));
    var list = element("ol");
    headings.forEach(function (heading, index) {
      if (!heading.id) heading.id = "trtt-section-" + (index + 1);
      var item = element("li");
      if (heading.tagName === "H3") item.className = "trtt-enh-toc-sub";
      var link = element("a", "", heading.textContent.trim());
      link.href = "#" + heading.id;
      item.appendChild(link);
      list.appendChild(item);
    });
    nav.appendChild(list);
    body.insertBefore(nav, body.firstChild);
  }

  function getLabels() {
    var result = [];
    document.querySelectorAll(".post-labels a, .post-label a, .post-footer a[rel~='tag'], a[rel~='tag']").forEach(function (link) {
      var label = link.textContent.trim();
      if (label && result.indexOf(label) === -1) result.push(label);
    });
    return result;
  }

  function addRelated(body) {
    if (body.querySelector(".trtt-enh-related")) return;
    fetchFeed().then(function (data) {
      var allEntries = entries(data);
      var currentUrl = (function () {
        var canonical = document.querySelector('link[rel="canonical"]');
        var value = canonical && canonical.href ? canonical.href : location.href;
        try { var url = new URL(value, BLOG); url.hash = ""; return url.href.replace(/\/$/, ""); }
        catch (_) { return value.split("#")[0].replace(/\/$/, ""); }
      })();
      var currentEntry = allEntries.find(function (entry) { return entryUrl(entry) === currentUrl; });
      var labels = getLabels();
      entryLabels(currentEntry).forEach(function (label) {
        if (labels.indexOf(label) === -1) labels.push(label);
      });
      if (!labels.length) return;
      var matches = allEntries.filter(function (entry) {
        if (!entryUrl(entry) || entryUrl(entry) === currentUrl) return false;
        return entryLabels(entry).some(function (label) { return labels.indexOf(label) !== -1; });
      }).slice(0, 3);
      if (!matches.length) return;
      var section = element("section", "trtt-enh-related");
      section.appendChild(element("h2", "", "Related stories"));
      var list = element("ul");
      matches.forEach(function (entry) {
        var url = entryUrl(entry);
        if (!url) return;
        var item = element("li");
        var link = element("a", "", entry.title && entry.title.$t ? entry.title.$t : "Read article");
        link.href = url;
        item.appendChild(link);
        list.appendChild(item);
      });
      if (list.children.length) {
        section.appendChild(list);
        body.appendChild(section);
      }
    }).catch(function () {});
  }

  function addInternalLinks(body) {
    var walker = document.createTreeWalker(body, NodeFilter.SHOW_TEXT, {
      acceptNode: function (node) {
        var parent = node.parentElement;
        if (!parent) return NodeFilter.FILTER_REJECT;
        return parent.closest("a, h1, h2, h3, script, style, .trtt-enh-toc, .trtt-enh-related, .trtt-enh-search, .trtt-enh-vercel, .trtt-enh-disclosure, .trtt-enh-credit")
          ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
      }
    });
    var textNodes = [];
    while (walker.nextNode()) textNodes.push(walker.currentNode);
    fetchFeed().then(function (data) {
      var destinations = {};
      entries(data).forEach(function (entry) {
        var title = entry.title && entry.title.$t ? entry.title.$t : "";
        var url = entryUrl(entry);
        if (!url) return;
        CITIES.forEach(function (city) {
          if (!destinations[city] && title.toLowerCase().indexOf(city.toLowerCase()) !== -1) destinations[city] = url;
        });
      });
      var added = 0;
      textNodes.some(function (node) {
        if (added >= 2 || !node.parentNode) return added >= 2;
        var value = node.nodeValue;
        var lower = value.toLowerCase();
        var match = null;
        CITIES.forEach(function (city) {
          var position = lower.indexOf(city.toLowerCase());
          if (position >= 0 && destinations[city] && (!match || position < match.position)) {
            match = { city: city, position: position };
          }
        });
        if (!match) return false;
        var fragment = document.createDocumentFragment();
        fragment.appendChild(document.createTextNode(value.slice(0, match.position)));
        var link = element("a", "", match.city);
        link.href = destinations[match.city];
        fragment.appendChild(link);
        fragment.appendChild(document.createTextNode(value.slice(match.position + match.city.length)));
        node.parentNode.replaceChild(fragment, node);
        added++;
        return added >= 2;
      });
    }).catch(function () {});
  }

  function addVercelDisclosureCredit(body) {
    var exists = Array.from(body.querySelectorAll("a[href]")).some(function (link) {
      return link.href.indexOf("cocvghuj-trtt-news-bot.vercel.app") !== -1;
    });
    if (!exists) {
      var card = element("p", "trtt-enh-vercel");
      var link = element("a", "", "Open TRTT Voyage AI Playground");
      link.href = VERCEL;
      link.target = "_blank";
      link.rel = "noopener";
      card.appendChild(link);
      body.appendChild(card);
    }
    if (body.textContent.indexOf(DISCLOSURE) === -1) {
      body.appendChild(element("p", "trtt-enh-disclosure", DISCLOSURE));
    }
    if (body.textContent.indexOf(CREDIT) === -1) {
      body.appendChild(element("p", "trtt-enh-credit", CREDIT));
    }
  }

  function nightMode() {
    var dark;
    if (window.matchMedia) dark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    else {
      var hour = new Date().getHours();
      dark = hour >= 19 || hour < 7;
    }
    document.documentElement.classList.toggle("trtt-enh-dark", dark);
  }

  if (isHomePage()) addHomepageExperience();

  if (isPostPage()) {
    var postBody = getPostBody();
    if (!postBody) return;
    cleanEntityText(postBody);
    watchForLateEntityText(postBody);
    addSearch(postBody);
    styleArticle(postBody);
    addTOC(postBody);
    addRelated(postBody);
    addInternalLinks(postBody);
    addVercelDisclosureCredit(postBody);
    nightMode();
    if (window.matchMedia) {
      var preference = window.matchMedia("(prefers-color-scheme: dark)");
      if (preference.addEventListener) preference.addEventListener("change", nightMode);
    }
  }
})();