
/* TRTT Voyage Enhancements
   Version: TRTT-ENHANCEMENTS-2026-11-08-02
   Blogger post pages only.
   Existing TRTT menu and Vercel deployment remain untouched.
*/
(function () {
  "use strict";

  var VERSION = "TRTT-ENHANCEMENTS-2026-11-07-01";
  var MARKER = "787950";
  var BLOG = "https://trttnews24bd.blogspot.com";
  var FEED = BLOG + "/feeds/posts/default";
  var VERCEL = "https://cocvghuj-trtt-news-bot.vercel.app/?marker=787950";

  var DISCLOSURE =
    "Disclosure: As an Amazon Associate and Travelpayouts partner, TRTT Voyage earns from qualifying purchases.";
  var CREDIT = "Built by Cocvghuj on GitHub";

  var LABELS = [
    "Flight News",
    "Passenger Rights",
    "eSIM & Stay Connected",
    "Ride & Stay",
    "Tour & Experience",
    "Sanluri Diary"
  ];

  var CITIES = [
    "Cagliari", "Sanluri", "Rome", "Milan",
    "Bergamo", "London", "Paris", "Barcelona",
    "Dubai", "Dhaka", "Bangkok", "New York"
  ];

  function isPostPage() {
    return document.body.classList.contains("item") ||
      /\/\d{4}\/\d{2}\/[^/?#]+\.html/i.test(location.pathname);
  }

  if (!isPostPage()) return;

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

  function getPostBody() {
    return find([
      ".post-body",
      ".post-body-container",
      ".entry-content",
      ".post-content"
    ]);
  }

  function fetchFeed() {
    return fetch(
      FEED + "?alt=json&max-results=150",
      { credentials: "omit" }
    ).then(function (response) {
      if (!response.ok) throw new Error("Feed unavailable");
      return response.json();
    });
  }

  function entryUrl(entry) {
    var alternate = (entry.link || []).find(function (item) {
      return item.rel === "alternate";
    });
    if (!alternate || !alternate.href) return "";
    try {
      var url = new URL(alternate.href, BLOG);
      url.hash = "";
      return url.href.replace(/\\/$/, "");
    } catch (_) {
      return alternate.href.split("#")[0].replace(/\\/$/, "");
    }
  }

  function currentPostUrl() {
    var canonical = document.querySelector('link[rel="canonical"]');
    var value = canonical && canonical.href ? canonical.href : location.href;
    try {
      var url = new URL(value, BLOG);
      url.hash = "";
      return url.href.replace(/\\/$/, "");
    } catch (_) {
      return value.split("#")[0].replace(/\\/$/, "");
    }
  }

  function entryLabels(entry) {
    return (entry && entry.category ? entry.category : [])
      .map(function (category) { return category.term || ""; })
      .filter(Boolean);
  }

  function entries(data) {
    return data && data.feed && data.feed.entry
      ? data.feed.entry
      : [];
  }

  function addSearch(body) {
    if (document.querySelector(".trtt-search")) return;

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

    var photo = body.querySelector("img");
    if (photo) {
      photo.classList.add("trtt-enh-first-photo");
      photo.loading = "eager";
      photo.fetchPriority = "high";
    }

    var firstParagraph = body.querySelector("p");
    if (firstParagraph) {
      firstParagraph.classList.add("trtt-enh-hook");
    }
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
      if (!heading.id) {
        heading.id = "trtt-section-" + (index + 1);
      }

      var item = element("li");
      if (heading.tagName === "H3") {
        item.className = "trtt-enh-toc-sub";
      }

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

    document.querySelectorAll(
      ".post-labels a, .post-label a, .post-footer a[rel~='tag'], a[rel~='tag']"
    ).forEach(function (link) {
      var label = link.textContent.trim();
      if (label && result.indexOf(label) === -1) result.push(label);
    });

    return result;
  }

  function addRelated(body) {
    if (body.querySelector(".trtt-enh-related")) return;

    fetchFeed().then(function (data) {
      var allEntries = entries(data);
      var currentUrl = currentPostUrl();
      var currentEntry = allEntries.find(function (entry) {
        return entryUrl(entry) === currentUrl;
      });

      var labels = getLabels();
      entryLabels(currentEntry).forEach(function (label) {
        if (labels.indexOf(label) === -1) labels.push(label);
      });

      if (!labels.length) return;

      var matches = allEntries.filter(function (entry) {
        if (!entryUrl(entry) || entryUrl(entry) === currentUrl) return false;
        return entryLabels(entry).some(function (label) {
          return labels.indexOf(label) !== -1;
        });
      }).slice(0, 3);

      if (!matches.length) return;

      var section = element("section", "trtt-enh-related");
      section.appendChild(element("h2", "", "Related stories"));

      var list = element("ul");
      matches.forEach(function (entry) {
        var alternate = (entry.link || []).find(function (item) {
          return item.rel === "alternate";
        });
        if (!alternate || !alternate.href) return;

        var item = element("li");
        var link = element(
          "a",
          "",
          entry.title ? entry.title.$t : "Read article"
        );
        link.href = alternate.href;
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
    var walker = document.createTreeWalker(
      body,
      NodeFilter.SHOW_TEXT,
      {
        acceptNode: function (node) {
          var parent = node.parentElement;

          if (!parent) return NodeFilter.FILTER_REJECT;

          return parent.closest(
            "a, h1, h2, h3, script, style, .trtt-toc, .trtt-related"
          )
            ? NodeFilter.FILTER_REJECT
            : NodeFilter.FILTER_ACCEPT;
        }
      }
    );

    var textNodes = [];
    while (walker.nextNode()) {
      textNodes.push(walker.currentNode);
    }

    fetchFeed().then(function (data) {
      var destinations = {};

      entries(data).forEach(function (entry) {
        var title = entry.title ? entry.title.$t : "";
        var alternate = (entry.link || []).find(function (item) {
          return item.rel === "alternate";
        });

        if (!alternate) return;

        CITIES.forEach(function (city) {
          if (
            !destinations[city] &&
            title.toLowerCase().indexOf(city.toLowerCase()) !== -1
          ) {
            destinations[city] = alternate.href;
          }
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

          if (
            position >= 0 &&
            destinations[city] &&
            (!match || position < match.position)
          ) {
            match = { city: city, position: position };
          }
        });

        if (!match) return false;

        var fragment = document.createDocumentFragment();

        fragment.appendChild(
          document.createTextNode(value.slice(0, match.position))
        );

        var link = element("a", "", match.city);
        link.href = destinations[match.city];
        fragment.appendChild(link);

        fragment.appendChild(
          document.createTextNode(
            value.slice(match.position + match.city.length)
          )
        );

        node.parentNode.replaceChild(fragment, node);
        added++;

        return added >= 2;
      });
    }).catch(function () {});
  }

  function addVercelDisclosureCredit(body) {
    var exists = Array.from(
      body.querySelectorAll("a[href]")
    ).some(function (link) {
      return link.href.indexOf(
        "cocvghuj-trtt-news-bot.vercel.app"
      ) !== -1;
    });

    if (!exists) {
      var card = element("p", "trtt-enh-vercel");
      var link = element(
        "a",
        "",
        "Open TRTT Voyage AI Playground"
      );

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

    if (window.matchMedia) {
      dark = window.matchMedia(
        "(prefers-color-scheme: dark)"
      ).matches;
    } else {
      var hour = new Date().getHours();
      dark = hour >= 19 || hour < 7;
    }

    document.documentElement.classList.toggle("trtt-enh-dark", dark);
  }

  /* Start enhancements: CSS is loaded separately by the Blogger gadget. */

  var postBody = getPostBody();
  if (!postBody) return;

  addSearch(postBody);
  styleArticle(postBody);
  addTOC(postBody);
  addRelated(postBody);
  addInternalLinks(postBody);
  addVercelDisclosureCredit(postBody);
  nightMode();

  if (window.matchMedia) {
    var preference = window.matchMedia(
      "(prefers-color-scheme: dark)"
    );

    if (preference.addEventListener) {
      preference.addEventListener("change", nightMode);
    }
  }
})();
