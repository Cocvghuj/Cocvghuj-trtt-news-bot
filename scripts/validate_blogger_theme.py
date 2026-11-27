#!/usr/bin/env python3
"""Static safety and structure checks for the TRTT Voyage Blogger theme candidate."""

from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

THEME = Path(__file__).resolve().parents[1] / "TRTT-Voyage-Generation-2-ULTIMATE.xml"
B_NS = "{http://www.google.com/2005/gml/b}"

def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)

if not THEME.is_file():
    fail(f"Theme file not found: {THEME}")

raw = THEME.read_text(encoding="utf-8")

# Parse the complete Blogger XML document; this catches malformed markup/entities.
try:
    root = ET.fromstring(raw)
except ET.ParseError as exc:
    fail(f"Theme XML is not well-formed: {exc}")

# Guardrails required for all TRTT Blogger theme candidates.
for forbidden in ("eval(", "location.href", "deleted='true'", 'deleted="true"', "auto-publish"):
    if forbidden in raw:
        fail(f"Forbidden pattern found: {forbidden}")

if "trttnews24bd.blogspot.com" in raw:
    fail("Legacy TRTT News 24 BD Blogger URL remains in the theme.")
if "FlightScoutPro" in raw:
    fail("Separate FlightScoutPro branding must not appear in the TRTT Voyage theme.")

widgets = root.findall(f".//{B_NS}widget")
widget_ids = [widget.attrib.get("id", "") for widget in widgets]
for required in ("Header1", "LinkList74", "Blog1", "Label1", "ContactForm1"):
    if required not in widget_ids:
        fail(f"Required existing Blogger widget is missing: {required}")
if len(widget_ids) != len(set(widget_ids)):
    fail("Duplicate Blogger widget IDs detected.")

menu = root.find(f".//{B_NS}widget[@id='LinkList74']/{B_NS}widget-settings")
if menu is None:
    fail("LinkList74 settings not found.")
settings = {item.attrib.get("name"): (item.text or "").strip() for item in menu.findall(f"{B_NS}widget-setting")}
for index, label in enumerate(("Home", "News", "Travel", "AI", "Tools", "About")):
    if settings.get(f"text-{index}") != label:
        fail(f"Menu item {index} should be {label!r}.")
expected_destinations = {
    "link-0": "/",
    "link-1": "/search/label/TRTT%20News24BD",
    "link-2": "/search?q=travel",
    "link-3": "/search/label/AI",
    "link-4": "https://cocvghuj-trtt-news-bot.vercel.app/super-app",
    "link-5": "/p/about-us.html",
}
for key, expected in expected_destinations.items():
    if settings.get(key) != expected:
        fail(f"Unexpected or unverified menu destination for {key}: {settings.get(key)!r}")

blog = root.find(f".//{B_NS}widget[@id='Blog1']/{B_NS}widget-settings")
if blog is None:
    fail("Blog1 settings not found.")
blog_settings = {item.attrib.get("name"): (item.text or "").strip() for item in blog.findall(f"{B_NS}widget-setting")}
if blog_settings.get("showShareButtons") != "false":
    fail("Blog1 share buttons must remain disabled.")

for page_path in ("/p/about-us.html", "/p/privacy-policy.html", "/p/disclaimer.html"):
    if page_path not in raw:
        fail(f"Footer page link missing: {page_path}")

for color in ("#E98BAF", "#B77991", "#D6A542", "#11152D", "#FFFFFF", "#67E8F9", "#FFD700"):
    if color.lower() not in raw.lower():
        fail(f"Approved TRTT palette token missing: {color}")

if "trtt-loader.js" not in raw:
    fail("Reviewed TRTT control loader reference is missing.")
if 'var hiddenLabels = ["my dairy", "diary"]' not in raw:
    fail("Personal diary isolation filter is missing.")
if "#PageList1,#Profile1{display:none!important}" not in raw:
    fail("Legacy PageList/Profile widgets must be hidden until their settings are reviewed.")
if "<a href='/p/contact-us.html'>Contact</a>" in raw:
    fail("Do not link the Contact page until the live Blogger page exists.")

print(f"PASS: {THEME.name} is well-formed XML and passed static safety, widget, menu, footer, and palette checks.")
