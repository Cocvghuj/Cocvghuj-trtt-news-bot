#!/usr/bin/env python3
"""Disabled legacy Blogger admin entry point; no Blogger API access is permitted here."""
raise SystemExit(
    "Disabled: Blogger API access is centralized in scripts/publish_news.py. "
    "Admin, moderation, and deletion actions are not authorized by the DRAFT-only workflow."
)
