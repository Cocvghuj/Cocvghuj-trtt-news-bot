#!/usr/bin/env python3
"""Compatibility entry point; the single-draft engine owns all Blogger writes."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import trtt_787950_master as engine


def main() -> int:
    return engine.main()


if __name__ == "__main__":
    raise SystemExit(main())
