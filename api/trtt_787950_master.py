"""Read-only Vercel status endpoint; Blogger draft publishing runs only in GitHub Actions."""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler

from trtt_787950_master import build, build_content, find_duplicate_post, main

MARKER = "787950 LOCKED"
PUBLISHER_ENTRYPOINT = "scripts/publish_news.py"


class handler(BaseHTTPRequestHandler):
    """Status-only endpoint. POST is rejected; it never creates or publishes Blogger posts."""

    def do_GET(self):
        payload = json.dumps({
            "status": "ready",
            "marker": MARKER,
            "publishing_mode": "DRAFT_ONLY",
            "publisher": PUBLISHER_ENTRYPOINT,
            "message": "Run the GitHub Actions draft workflow; review Blogger drafts manually before publication.",
        }).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self):
        self.send_response(405)
        self.send_header("Allow", "GET")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
