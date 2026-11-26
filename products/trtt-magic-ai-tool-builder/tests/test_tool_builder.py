"""Dependency-free source-contract tests for the TRTT MAGIC AI Tool Builder.

Run from the repository root:
    python -m unittest discover -s products/trtt-magic-ai-tool-builder/tests -v

These tests inspect source contracts. They do not launch a browser or prove UI runtime behaviour.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest


PRODUCT_DIR = Path(__file__).resolve().parents[1]
HTML_FILE = PRODUCT_DIR / "trttmagic.html"


class SourceParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.elements = []
        self.template_names = set()
        self.external_scripts = []
        self.external_stylesheets = []
        self.meta = []
        self.script_parts = []
        self._inside_script = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.elements.append((tag, attrs))
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "button" and attrs.get("data-template"):
            self.template_names.add(attrs["data-template"])
        if tag == "script":
            self._inside_script = True
            if attrs.get("src"):
                self.external_scripts.append(attrs["src"])
        if tag == "link" and "stylesheet" in attrs.get("rel", "").lower():
            self.external_stylesheets.append(attrs.get("href", ""))
        if tag == "meta":
            self.meta.append(attrs)

    def handle_data(self, data):
        if self._inside_script:
            self.script_parts.append(data)

    def handle_endtag(self, tag):
        if tag == "script":
            self._inside_script = False


class ToolBuilderSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not HTML_FILE.is_file():
            raise FileNotFoundError(
                f"Expected {HTML_FILE}. Run this test from a complete repository checkout."
            )
        cls.html = HTML_FILE.read_text(encoding="utf-8")
        cls.parser = SourceParser()
        cls.parser.feed(cls.html)
        cls.parser.close()
        cls.script = "\n".join(cls.parser.script_parts)

    def test_document_and_mobile_viewport_exist(self):
        self.assertRegex(self.html.lower(), r"<!doctype\s+html>")
        self.assertRegex(self.html, r'<html\s+lang=["\']en["\']')
        viewport = [
            item for item in self.parser.meta
            if item.get("name", "").lower() == "viewport"
        ]
        self.assertTrue(viewport, "Viewport meta tag is required for mobile layout.")

    def test_required_builder_controls_exist(self):
        required_ids = {
            "toolForm", "toolName", "category", "audience", "task",
            "instructions", "tone", "format", "resetBtn", "emptyState",
            "previewContent", "promptPreview", "copyBtn", "exportBtn", "toast",
        }
        self.assertTrue(required_ids.issubset(self.parser.ids),
                        f"Missing IDs: {sorted(required_ids - self.parser.ids)}")

    def test_required_fields_are_validated(self):
        required_names = set()
        for tag, attrs in self.parser.elements:
            if tag in {"input", "textarea"} and "required" in attrs:
                required_names.add(attrs.get("name"))
        self.assertIn("toolName", required_names)
        self.assertIn("task", required_names)
        self.assertIn('form.reportValidity()', self.script)

    def test_all_three_starter_templates_are_wired(self):
        self.assertEqual(self.parser.template_names, {"seo", "blog", "faq"})
        self.assertIn('querySelectorAll("[data-template]")', self.script)
        self.assertIn("button.dataset.template", self.script)

    def test_prompt_is_generated_and_rendered_as_text(self):
        self.assertIn("function buildConfig()", self.script)
        self.assertIn("function buildPrompt(c)", self.script)
        self.assertIn("promptPreview.textContent=buildPrompt(currentConfig)", self.script)
        self.assertIn("Do not fabricate facts", self.script)

    def test_copy_action_has_a_safe_fallback(self):
        self.assertIn("navigator.clipboard.writeText", self.script)
        self.assertIn("Clipboard unavailable", self.script)

    def test_json_export_is_user_initiated(self):
        self.assertIn('new Blob([JSON.stringify(payload,null,2)]', self.script)
        self.assertIn('type:"application/json"', self.script)
        self.assertIn("URL.createObjectURL(blob)", self.script)
        self.assertIn("anchor.download=", self.script)

    def test_json_export_defers_object_url_revocation(self):
        self.assertRegex(
            self.script,
            r"setTimeout\\(\\(\\)=>URL\\.revokeObjectURL\\(url\\),\\s*1000\\)",
        )

    def test_responsive_and_keyboard_accessibility_rules_exist(self):
        self.assertIn(":focus-visible", self.html)
        self.assertRegex(self.html, r"@media\s*\(max-width:\s*900px\)")
        self.assertRegex(self.html, r"@media\s*\(max-width:\s*540px\)")
        self.assertIn("prefers-reduced-motion:reduce", self.html)
        self.assertIn("function invalidatePreview()", self.script)
        self.assertIn('form.querySelectorAll("input,textarea,select")', self.script)
        self.assertIn('control.addEventListener("input",invalidatePreview)', self.script)
        self.assertIn('control.addEventListener("change",invalidatePreview)', self.script)

    def test_no_external_assets_or_network_calls(self):
        self.assertEqual(self.parser.external_scripts, [])
        self.assertEqual(self.parser.external_stylesheets, [])
        for pattern in (r"\bfetch\s*\(", r"\bXMLHttpRequest\b",
                        r"\bWebSocket\b"):
            self.assertIsNone(re.search(pattern, self.html, re.I), pattern)

    def test_no_dynamic_code_or_browser_storage(self):
        for pattern in (r"\beval\s*\(", r"\bnew\s+Function\b",
                        r"\blocalStorage\b", r"\bsessionStorage\b"):
            self.assertIsNone(re.search(pattern, self.html, re.I), pattern)

    def test_brand_palette_uses_only_approved_hex_colours(self):
        found = {value.upper() for value in re.findall(r"#[0-9A-Fa-f]{3,8}", self.html)}
        approved = {"#E98BAF", "#B77991", "#D6A542", "#11152D", "#FFFFFF"}
        self.assertTrue(found.issubset(approved),
                        f"Unexpected colour values: {sorted(found - approved)}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
