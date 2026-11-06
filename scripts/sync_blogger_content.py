#!/usr/bin/env python3
"""Disabled legacy sync; Blogger API access is centralized in scripts/publish_news.py."""
# Legacy sync policy marker: isDraft=True. This script performs no Blogger request.
raise SystemExit("Disabled: only scripts/publish_news.py may access Blogger under the DRAFT-only policy.")
