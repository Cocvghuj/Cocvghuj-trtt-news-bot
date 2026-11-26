const { test, before, after } = require("node:test");
const assert = require("node:assert/strict");
const { chromium } = require("playwright");
const fs = require("node:fs");
const path = require("node:path");

const BASE_URL = process.env.TRtt_BASE_URL || "http://127.0.0.1:4173/index-v3-visual-fixed.html";
let browser;
let page;

function rgbChannels(cssColor) {
  const values = cssColor.match(/[\d.]+/g).map(Number);
  return values.slice(0, 3);
}
function luminance(cssColor) {
  const [r, g, b] = rgbChannels(cssColor).map(v => {
    const c = v / 255;
    return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}
function contrastRatio(a, b) {
  const values = [luminance(a), luminance(b)].sort((x, y) => y - x);
  return (values[0] + 0.05) / (values[1] + 0.05);
}
function columns(value) {
  return (value.match(/[0-9.]+px/g) || []).length;
}

before(async () => {
  browser = await chromium.launch({ headless: true });
  page = await browser.newPage({ viewport: { width: 1365, height: 900 } });
  await page.goto(BASE_URL, { waitUntil: "load" });
});
after(async () => { await browser?.close(); });

test("desktop and tablet/mobile widths have no horizontal overflow", async () => {
  const widths = [320, 360, 390, 540, 768, 900, 1024, 1280, 1440];
  const results = [];
  for (const width of widths) {
    await page.setViewportSize({ width, height: 900 });
    const metrics = await page.evaluate(() => ({
      viewport: document.documentElement.clientWidth,
      document: document.documentElement.scrollWidth,
      workspaceColumns: getComputedStyle(document.querySelector(".workspace")).gridTemplateColumns,
      layoutColumns: getComputedStyle(document.querySelector(".layout")).gridTemplateColumns,
      asideDisplay: getComputedStyle(document.querySelector("aside")).display,
      mainWidth: document.querySelector("main").getBoundingClientRect().width
    }));
    assert.ok(metrics.document <= metrics.viewport + 1,
      `Horizontal overflow at ${width}px: ${metrics.document}px document width`);
    if (width <= 900) {
      assert.equal(columns(metrics.workspaceColumns), 1, `Workspace should stack at ${width}px`);
      assert.equal(metrics.asideDisplay, "none", `Sidebar should hide at ${width}px`);
    } else {
      assert.equal(columns(metrics.workspaceColumns), 2, `Workspace should have two columns at ${width}px`);
    }
    results.push({ width, ...metrics });
  }
  fs.mkdirSync("test-results", { recursive: true });
  await page.setViewportSize({ width: 390, height: 844 });
  await page.screenshot({ path: "test-results/trtt-mobile-390.png", fullPage: true });
  await page.setViewportSize({ width: 768, height: 1024 });
  await page.screenshot({ path: "test-results/trtt-tablet-768.png", fullPage: true });
  await page.setViewportSize({ width: 1365, height: 900 });
  await page.screenshot({ path: "test-results/trtt-desktop-1365.png", fullPage: true });
  assert.equal(results.length, widths.length);
});

test("body copy and placeholders meet WCAG AA normal-text contrast", async () => {
  const measured = await page.evaluate(() => {
    const get = (selector, prop) => getComputedStyle(document.querySelector(selector))[prop];
    const bg = get("body", "backgroundColor");
    return {
      intro: { fg: get(".intro", "color"), bg },
      eyebrow: { fg: get(".eyebrow", "color"), bg },
      placeholder: {
        fg: getComputedStyle(document.querySelector("#toolName"), "::placeholder").color,
        bg: get("#toolName", "backgroundColor")
      },
      label: { fg: get('label[for="toolName"]', "color"), bg: get("#toolName", "backgroundColor") }
    };
  });
  for (const [name, pair] of Object.entries(measured)) {
    const ratio = contrastRatio(pair.fg, pair.bg);
    assert.ok(ratio >= 4.5, `${name} contrast ${ratio.toFixed(2)}:1 is below WCAG AA 4.5:1`);
  }
});

test("form controls and panels have visible boundaries", async () => {
  await page.locator("#toolName").focus();
  const data = await page.evaluate(() => ({
    inputBorder: getComputedStyle(document.querySelector("#toolName")).borderTopColor,
    panelBorder: getComputedStyle(document.querySelector(".panel")).borderTopColor,
    focusOutline: getComputedStyle(document.querySelector("#toolName")).outlineColor,
    focusBoxShadow: getComputedStyle(document.querySelector("#toolName")).boxShadow
  }));
  assert.ok(contrastRatio(data.inputBorder, "rgb(255, 255, 255)") >= 3,
    "Input boundary must reach 3:1 against white");
  assert.ok(contrastRatio(data.panelBorder, "rgb(255, 255, 255)") >= 3,
    "Panel boundary must reach 3:1 against white");
  assert.notEqual(data.focusBoxShadow, "none", "Focused form control must render a visible box-shadow ring");
  const ringColor = data.focusBoxShadow.match(/rgba?\\([^)]+\\)/)?.[0];
  assert.ok(ringColor, `Could not read the focus ring color from: ${data.focusBoxShadow}`);
  assert.ok(contrastRatio(ringColor, "rgb(255, 255, 255)") >= 3,
    "Keyboard focus ring must reach 3:1 against white");
});

test("page remains readable and primary controls stay within viewport", async () => {
  for (const width of [320, 390, 768, 1365]) {
    await page.setViewportSize({ width, height: 900 });
    const data = await page.evaluate(() => {
      const button = document.querySelector(".primary").getBoundingClientRect();
      const main = document.querySelector("main").getBoundingClientRect();
      return { buttonLeft: button.left, buttonRight: button.right, mainLeft: main.left, mainRight: main.right };
    });
    assert.ok(data.buttonLeft >= -1 && data.buttonRight <= width + 1,
      `Primary button clipped at viewport ${width}px`);
    assert.ok(data.mainLeft >= -1 && data.mainRight <= width + 1,
      `Main content clipped at viewport ${width}px`);
  }
});
