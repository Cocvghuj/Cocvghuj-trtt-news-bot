// Real Chromium end-to-end checks for the TRTT MAGIC AI Tool Builder.
// Uses Node's built-in test runner and Playwright installed by GitHub Actions.
const { test, before, after } = require("node:test");
const assert = require("node:assert/strict");
const { chromium } = require("playwright");

const BASE_URL = process.env.TRtt_BASE_URL || "http://127.0.0.1:4173";
let browser;
let context;
let page;

before(async () => {
  browser = await chromium.launch({ headless: true });
  context = await browser.newContext({
    acceptDownloads: true,
    permissions: ["clipboard-read", "clipboard-write"],
    viewport: { width: 1365, height: 900 }
  });
  page = await context.newPage();
  await page.goto(BASE_URL, { waitUntil: "load" });
});

after(async () => {
  await context?.close();
  await browser?.close();
});

test("page loads and shows the builder", async () => {
  await page.getByRole("heading", { name: "Build a useful AI tool." }).waitFor();
  await page.getByRole("heading", { name: "Tool configuration" }).waitFor();
  await page.getByRole("heading", { name: "Tool preview" }).waitFor();
  await assert.doesNotReject(() => page.locator("#emptyState").waitFor({ state: "visible" }));
});

test("starter template fills the configuration form", async () => {
  await page.getByRole("button", { name: "SEO brief" }).click();
  assert.equal(await page.locator("#toolName").inputValue(), "TRTT SEO Brief Assistant");
  assert.equal(await page.locator("#category").inputValue(), "Writing & content");
  assert.match(await page.locator("#task").inputValue(), /evidence-led SEO content brief/i);

  await page.getByRole("button", { name: "Blog outline" }).click();
  assert.equal(await page.locator("#toolName").inputValue(), "TRTT Blog Outline Builder");

  await page.getByRole("button", { name: "FAQ maker" }).click();
  assert.equal(await page.locator("#toolName").inputValue(), "TRTT FAQ Maker");
});

test("required fields block generation when empty", async () => {
  await page.locator("#resetBtn").click();
  await page.getByRole("button", { name: /Generate tool prompt/i }).click();
  assert.equal(await page.locator("#toolName").evaluate(el => el.validity.valueMissing), true);
  assert.equal(await page.locator("#previewContent").isVisible(), false);
});

test("custom tool configuration generates the expected prompt", async () => {
  await page.locator("#toolName").fill("TRTT E2E Demo Assistant");
  await page.locator("#audience").fill("TRTT test readers");
  await page.locator("#task").fill("Explain a supplied topic using verified information.");
  await page.locator("#instructions").fill("Never invent facts. State uncertainty.");
  await page.getByRole("button", { name: /Generate tool prompt/i }).click();

  const prompt = await page.locator("#promptPreview").innerText();
  assert.match(prompt, /TRTT E2E Demo Assistant/);
  assert.match(prompt, /Explain a supplied topic/);
  assert.match(prompt, /Never invent facts/);
  assert.equal(await page.locator("#previewContent").isVisible(), true);
  assert.equal(await page.locator("#emptyState").isVisible(), false);
});

test("editing a generated configuration invalidates stale preview and export", async () => {
  await page.locator("#task").fill("A revised task that must replace the previous prompt.");
  assert.equal(await page.locator("#previewContent").isVisible(), false);
  assert.equal(await page.locator("#emptyState").isVisible(), true);
  await page.getByRole("button", { name: /Generate tool prompt/i }).click();
  const updatedPrompt = await page.locator("#promptPreview").innerText();
  assert.match(updatedPrompt, /A revised task that must replace the previous prompt/);
  assert.doesNotMatch(updatedPrompt, /Explain a supplied topic using verified information/);
});

test("copy prompt writes the generated prompt to the clipboard", async () => {
  await page.getByRole("button", { name: "Copy prompt" }).click();
  await page.getByText("Prompt copied.", { exact: true }).waitFor();
  const clipboardText = await page.evaluate(() => navigator.clipboard.readText());
  assert.equal(clipboardText, await page.locator("#promptPreview").innerText());
});

test("JSON export downloads a valid tool definition", async () => {
  const [download] = await Promise.all([
    page.waitForEvent("download"),
    page.getByRole("button", { name: "Export tool JSON" }).click()
  ]);
  assert.match(download.suggestedFilename(), /trtt-e2e-demo-assistant\.json$/);
  const filePath = await download.path();
  assert.ok(filePath, "Expected a completed browser download");
  const fs = require("node:fs");
  const exported = JSON.parse(fs.readFileSync(filePath, "utf8"));
  assert.equal(exported.name, "TRTT E2E Demo Assistant");
  assert.match(exported.prompt, /Explain a supplied topic/);
  assert.equal(exported.schemaVersion, 1);
});

test("reset returns the page to its initial preview state", async () => {
  await page.locator("#resetBtn").click();
  assert.equal(await page.locator("#toolName").inputValue(), "");
  assert.equal(await page.locator("#previewContent").isVisible(), false);
  assert.equal(await page.locator("#emptyState").isVisible(), true);
});

test("mobile viewport has no horizontal overflow and stacks panels", async () => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.reload({ waitUntil: "load" });
  const metrics = await page.evaluate(() => ({
    viewportWidth: document.documentElement.clientWidth,
    documentWidth: document.documentElement.scrollWidth,
    form: document.querySelector("#toolForm").getBoundingClientRect().toJSON(),
    preview: document.querySelector(".workspace article:nth-child(2)").getBoundingClientRect().toJSON()
  }));
  assert.ok(metrics.documentWidth <= metrics.viewportWidth + 1,
    `Horizontal overflow: document ${metrics.documentWidth}px vs viewport ${metrics.viewportWidth}px`);
  assert.ok(metrics.preview.top > metrics.form.top,
    "Preview panel should stack below the form on mobile");
  assert.ok(metrics.form.width <= metrics.viewportWidth,
    "Form should fit within the mobile viewport");
});
