#!/usr/bin/env python3
"""Strict offline validation for the original TRTT Voyage Diamond Horizon Blogger theme."""
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
THEME = ROOT / "TRTT-Voyage-Generation-2-ULTIMATE.xml"
B = "{http://www.google.com/2005/gml/b}"
REQUIRED = {
    "Header1", "LinkList74", "Blog1", "PopularPosts1", "PopularPosts2",
    "Label1", "PageList1", "ContactForm1", "Profile1", "ReportAbuse1",
}
PRESERVED = {
    "LinkList70", "LinkList71", "LinkList75", "HTML1", "PopularPosts3",
    "HTML6", "Label3", "Image150", "LinkList78", "LinkList76",
}
PALETTE = {"#E98BAF", "#B77991", "#D6A542", "#11152D", "#FFFFFF", "#67E8F9", "#FFD700"}

def fail(message):
    print("FAIL:", message, file=sys.stderr)
    raise SystemExit(1)

if not THEME.is_file():
    fail("Theme XML is missing.")
raw = THEME.read_text(encoding="utf-8")
try:
    root = ET.fromstring(raw)
except ET.ParseError as exc:
    fail(f"XML is not well-formed: {exc}")

for token in ("eval(", "location.href", "deleted='true'", 'deleted="true"', "auto-publish", "window.location", "location.replace", "location.assign"):
    if token.lower() in raw.lower():
        fail(f"Forbidden behavior token: {token}")
for token in ("Mitti", "Way2Themes", "SoraTemplates", "LiveBlogger", "trttnews24bd.blogspot.com", "FlightScoutPro"):
    if token.lower() in raw.lower():
        fail(f"Third-party/legacy brand residue: {token}")
if "https://www.trttvoyage.com/" not in raw:
    fail("Canonical TRTT website link missing.")
for color in PALETTE:
    if color.lower() not in raw.lower():
        fail(f"Required brand color missing: {color}")

widgets = root.findall(".//" + B + "widget")
ids = [w.attrib.get("id", "") for w in widgets]
if len(ids) != len(set(ids)):
    fail("Duplicate widget IDs.")
missing = REQUIRED - set(ids)
if missing:
    fail("Required widgets missing: " + ", ".join(sorted(missing)))
missing_preserved = PRESERVED - set(ids)
if missing_preserved:
    fail("Existing widget IDs not preserved in candidate: " + ", ".join(sorted(missing_preserved)))

menu = root.find(".//" + B + "widget[@id='LinkList74']/" + B + "widget-settings")
if menu is None:
    fail("Main menu settings missing.")
settings = {x.attrib.get("name"): (x.text or "").strip() for x in menu.findall(B + "widget-setting")}
expected = {
    "text-0": "Home", "link-0": "/",
    "text-1": "News", "link-1": "/search/label/News",
    "text-2": "Travel", "link-2": "/search/label/Travel",
    "text-3": "AI", "link-3": "/search/label/AI",
    "text-4": "Tools", "link-4": "https://cocvghuj-trtt-news-bot.vercel.app/super-app",
    "text-5": "About", "link-5": "/p/about-us.html",
}
for key, value in expected.items():
    if settings.get(key) != value:
        fail(f"Main menu mismatch for {key}: {settings.get(key)!r}")

blog = root.find(".//" + B + "widget[@id='Blog1']/" + B + "widget-settings")
if blog is None:
    fail("Blog1 settings missing.")
blog_settings = {x.attrib.get("name"): (x.text or "").strip() for x in blog.findall(B + "widget-setting")}
for key in ("showAuthor", "showTimestamp", "showLabels", "showCommentLink"):
    if blog_settings.get(key) != "true":
        fail(f"Blog1 {key} must be true.")
if blog_settings.get("showShareButtons") != "false":
    fail("Blog1 share buttons must remain disabled.")

for forbidden_url in ("https://www.facebook.com/way2themes", "https://twitter.com/LiveBlogger1", "mitti-way2themes.blogspot.com"):
    if forbidden_url in raw:
        fail("Unverified third-party social/site URL remains.")
for private_pattern in (r"\+39\d{8,}", r"engrtaher2017@gmail\.com"):
    if re.search(private_pattern, raw, re.I):
        fail("Private contact detail found in theme.")
if "Thinking Room" in raw or "trtt-loader.js" in raw:
    fail("Thinking Room must remain separate from the public homepage.")
print(f"PASS: {THEME.name} passed XML well-formedness, required widgets, preserved IDs, menu, Blog1, palette, privacy and safety checks.")
