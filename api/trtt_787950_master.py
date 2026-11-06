"""Read-only TRTT status endpoint; Blogger writes use one entry point only.

The sole supported Blogger draft publisher is scripts/publish_news.py, which
delegates to trtt_787950_master.main(). This module never inserts or publishes.
"""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler
from typing import Any

from trtt_787950_master import (
    build_content,
    build as build_blogger_service,
    find_duplicate_post,
)

# Compatibility export for callers that need the configured Blogger client.
build = build_blogger_service


def main() -> int:
    """Read-only module entry point; deliberately does not run the publisher."""
    return 0


class handler(BaseHTTPRequestHandler):
    def _send(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        self._send(200, {
            "service": "TRTT Blogger draft status",
            "marker": "787950 LOCKED",
            "mode": "read-only",
            "publisher": "scripts/publish_news.py",
        })

    def do_POST(self) -> None:
        self._send(405, {
            "error": "This endpoint is read-only.",
            "publisher": "scripts/publish_news.py",
        })

    def log_message(self, format: str, *args: Any) -> None:
        return
