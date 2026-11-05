#!/usr/bin/env python3
"""Single supported GitHub Actions entry point for the real Blogger draft engine."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import trtt_787950_master as engine


if __name__ == "__main__":
    raise SystemExit(engine.main())
