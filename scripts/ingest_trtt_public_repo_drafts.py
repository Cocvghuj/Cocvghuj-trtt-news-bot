#!/usr/bin/env python3
"""Import explicitly opted-in HTML drafts from the public TRTT repo allowlist.

Only this central repository owns Blogger credentials. Source repositories are
read-only inputs; no secrets are requested or written there.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "config" / "trtt-source-repositories.json"
DRAFT_DIR = ROOT / "blog" / "drafts"
BRIDGE = ROOT / "scripts" / "create_blogger_html_draft.py"
MARKER_RE = re.compile(r"<!--\s*TRTT_BLOGGER_DRAFT:\s*true\s*-->", re.I)
USER_AGENT = "TRTT-Central-Draft-Ingest/1.0"


def is_allowed_path(path: str, allowed_directories: list[str]) -> bool:
    parts = path.split("/")
    parent = "/".join(parts[:-1])
    return (
        parent in allowed_directories
        and len(parts) == len(parent.split("/")) + 1
        and parts[-1].lower().endswith(".html")
        and parts[-1] not in {"", ".", ".."}
    )


def has_opt_in_marker(content: str) -> bool:
    return bool(MARKER_RE.search(content))


def is_approved_legacy_source(repo: str, path: str, blob_sha: str, approvals: dict) -> bool:
    """Allow only centrally pinned, previously owner-approved source files."""
    approved = approvals.get(repo, {}).get(path)
    return bool(approved and approved == blob_sha)


def github_json(url: str):
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": USER_AGENT,
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_raw(repo: str, branch: str, path: str) -> str:
    url = (
        "https://raw.githubusercontent.com/"
        + repo + "/" + quote(branch, safe="")
        + "/" + quote(path, safe="/")
    )
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=20) as response:
        raw = response.read(1_000_001)
    if len(raw) > 1_000_000:
        raise RuntimeError(f"Source article exceeds 1 MB: {repo}/{path}")
    return raw.decode("utf-8")


def source_articles(repo: str, allowed_directories: list[str], approved_legacy_sources: dict):
    metadata = github_json("https://api.github.com/repos/" + repo)
    if metadata.get("private") is not False:
        raise RuntimeError(f"Source repository is not confirmed public: {repo}")
    branch = metadata.get("default_branch")
    if not branch:
        raise RuntimeError(f"Default branch is unavailable: {repo}")
    tree = github_json(
        "https://api.github.com/repos/" + repo
        + "/git/trees/" + quote(branch, safe="") + "?recursive=1"
    )
    if tree.get("truncated"):
        raise RuntimeError(f"Repository tree was truncated; refusing partial scan: {repo}")
    for item in tree.get("tree", []):
        path = item.get("path", "")
        if item.get("type") != "blob" or not is_allowed_path(path, allowed_directories):
            continue
        explicitly_pinned = is_approved_legacy_source(
            repo, path, str(item.get("sha", "")), approved_legacy_sources
        )
        if not explicitly_pinned:
            content = fetch_raw(repo, branch, path)
            if not has_opt_in_marker(content):
                continue
        else:
            content = fetch_raw(repo, branch, path)
        yield path, content


def local_draft_path(repo: str, source_path: str) -> Path:
    identity = hashlib.sha256((repo + "/" + source_path).encode("utf-8")).hexdigest()[:12]
    repo_slug = re.sub(r"[^a-zA-Z0-9-]+", "-", repo.split("/", 1)[-1]).strip("-").lower()
    return DRAFT_DIR / f"hub-{repo_slug}-{identity}.html"


def ingest(dry_run: bool = False) -> int:
    config = json.loads(REGISTRY.read_text(encoding="utf-8"))
    repositories = config["repositories"]
    allowed = config["allowed_directories"]
    approved_legacy_sources = config.get("approved_legacy_sources", {})
    max_articles = int(config.get("max_articles_per_run", 20))
    if not repositories or len(repositories) != len(set(repositories)):
        raise RuntimeError("Repository allowlist is empty or contains duplicates.")
    DRAFT_DIR.mkdir(parents=True, exist_ok=True)
    processed = 0
    failures = 0

    for repo in repositories:
        print(f"Scanning public source: {repo}")
        try:
            for source_path, content in source_articles(repo, allowed, approved_legacy_sources):
                processed += 1
                if processed > max_articles:
                    raise RuntimeError("Maximum articles per run exceeded; refusing an unbounded import.")
                local_path = local_draft_path(repo, source_path)
                local_path.write_text(content, encoding="utf-8")
                try:
                    relative_path = local_path.relative_to(ROOT).as_posix()
                    command = [sys.executable, str(BRIDGE)]
                    if dry_run:
                        command.append("--validate-only")
                    command.append(relative_path)
                    result = subprocess.run(command, cwd=ROOT, check=False)
                    if result.returncode != 0:
                        failures += 1
                        print(f"FAIL: {repo}/{source_path} was rejected by the Blogger safety bridge.")
                    else:
                        print(f"PASS: {repo}/{source_path} {'validated' if dry_run else 'processed'} by central hub.")
                finally:
                    local_path.unlink(missing_ok=True)
        except (urllib.error.URLError, urllib.error.HTTPError, UnicodeDecodeError, RuntimeError, KeyError, ValueError) as exc:
            failures += 1
            print(f"FAIL: source scan {repo}: {type(exc).__name__}: {exc}", file=sys.stderr)

    if processed == 0:
        print("No explicitly opted-in Blogger HTML drafts were found.")
    print(f"Central ingest summary: candidates={processed}, failures={failures}, dry_run={dry_run}")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Validate eligible files without calling Blogger.")
    args = parser.parse_args()
    return ingest(dry_run=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
