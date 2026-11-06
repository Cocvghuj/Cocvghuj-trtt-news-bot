"""Workflow entry point for the canonical, verified Blogger DRAFT engine."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import trtt_787950_master as engine

if __name__ == "__main__":
    raise SystemExit(engine.main())
