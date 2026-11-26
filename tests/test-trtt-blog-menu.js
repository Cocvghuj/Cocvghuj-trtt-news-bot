"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");

const source = fs.readFileSync("trtt-blog-menu.js", "utf8");

class FakeElement {
  constructor(tagName) {
    this.tagName = tagName;
    this.children = [];
    this.attributes = {};
    this.textContent = "";
    this.href = "";
  }
  setAttribute(name, value) {
    this.attributes[name] = value;
  }
  appendChild(child) {
    this.children.push(child);
    return child;
  }
  removeChild(child) {
    const index = this.children.indexOf(child);
    if (index >= 0) this.children.splice(index, 1);
    return child;
  }
  get firstChild() {
    return this.children[0] || null;
  }
  cloneNode(deep) {
    const copy = new FakeElement(this.tagName);
    copy.attributes = { ...this.attributes };
    copy.textContent = this.textContent;
    copy.href = this.href;
    if (deep) this.children.forEach(child => copy.appendChild(child.cloneNode(true)));
    return copy;
  }
}

function makeContext(config, fetchFails) {
  const navs = [new FakeElement("ul"), new FakeElement("ul")];
  navs.forEach(nav => nav.appendChild(new FakeElement("legacy-link")));

  const document = {
    readyState: "complete",
    currentScript: { src: "https://cocvghuj-trtt-news-bot-git-main-trtt6.vercel.app/trtt-blog-menu.js" },
    querySelectorAll(selector) {
      assert.equal(selector, "#main-menu-nav");
      return navs;
    },
    createElement(tagName) {
      return new FakeElement(tagName);
    }
  };

  const window = { location: { origin: "https://www.trttvoyage.com" } };
  const fetch = async (url, options) => {
    assert.equal(url, "https://cocvghuj-trtt-news-bot-git-main-trtt6.vercel.app/blog-control.json");
    assert.equal(options.credentials, "omit");
    assert.equal(options.mode, "cors");
    if (fetchFails) throw new Error("simulated network failure");
    return { ok: true, json: async () => config };
  };

  vm.runInNewContext(source, { document, window, fetch, URL, Promise, Array });
  return navs;
}

async function flushPromises() {
  await new Promise(resolve => setImmediate(resolve));
}

async function main() {
  const menu = [
    { id: "home", label: "Home", href: "/" },
    { id: "news", label: "News", href: "/search/label/News" },
    { id: "travel", label: "Travel", href: "/search/label/Travel" },
    { id: "ai", label: "AI", href: "/search/label/AI" },
    { id: "tools", label: "Tools", href: "https://cocvghuj-trtt-news-bot-git-main-trtt6.vercel.app/" },
    { id: "about", label: "About", href: "/p/about-us.html" }
  ];

  const successNavs = makeContext({ menu }, false);
  await flushPromises();
  for (const nav of successNavs) {
    assert.equal(nav.children.length, 6);
    assert.deepEqual(nav.children.map(item => item.children[0].textContent),
      ["Home", "News", "Travel", "AI", "Tools", "About"]);
    assert.equal(nav.children[0].children[0].href, "https://www.trttvoyage.com/");
  }

  const failedNavs = makeContext({ menu: [{ label: "Unsafe", href: "javascript:alert(1)" }] }, false);
  await flushPromises();
  for (const nav of failedNavs) {
    assert.equal(nav.children.length, 1);
    assert.equal(nav.children[0].tagName, "legacy-link");
  }

  const offlineNavs = makeContext({ menu }, true);
  await flushPromises();
  for (const nav of offlineNavs) {
    assert.equal(nav.children.length, 1);
    assert.equal(nav.children[0].tagName, "legacy-link");
  }

  console.log("PASS: six-link desktop/mobile render; unsafe config and fetch failure preserve the existing menu.");
}

main().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
