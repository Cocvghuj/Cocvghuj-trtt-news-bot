#!/usr/bin/env python3
"""The sole Blogger API entry point. Creates and verifies DRAFTS only."""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import trtt_787950_master as engine


def _require_configuration() -> tuple[str, str]:
    names = (
        "BLOGGER_BLOG_ID",
        "FLIGHTSCOUTPRO_BLOG_ID",
        "BLOGGER_CLIENT_ID",
        "BLOGGER_CLIENT_SECRET",
        "BLOGGER_REFRESH_TOKEN",
    )
    missing = [key for key in names if not os.environ.get(key, "").strip()]
    if missing:
        raise RuntimeError("Missing required Blogger configuration: " + ", ".join(missing))
    primary = os.environ["BLOGGER_BLOG_ID"].strip()
    partner = os.environ["FLIGHTSCOUTPRO_BLOG_ID"].strip()
    if primary == partner:
        raise RuntimeError("The two Blogger blog IDs must be different.")
    return primary, partner


def _build_service() -> Any:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    credentials = Credentials(
        token=None,
        refresh_token=os.environ["BLOGGER_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["BLOGGER_CLIENT_ID"],
        client_secret=os.environ["BLOGGER_CLIENT_SECRET"],
        scopes=["https://www.googleapis.com/auth/blogger"],
    )
    return build("blogger", "v3", credentials=credentials, cache_discovery=False)


def _verify_post_draft(service: Any, blog_id: str, post_id: str) -> dict[str, Any]:
    """Read the post back from Blogger and fail closed unless its server status is DRAFT."""
    verified = service.posts().get(blogId=blog_id, postId=post_id).execute()
    returned_id = str(verified.get("id", "")).strip()
    status = str(verified.get("status", "")).upper()
    if not returned_id:
        raise RuntimeError(
            f"Blogger safety failure: read-back for post {post_id} returned no post ID."
        )
    if returned_id != post_id:
        raise RuntimeError(
            f"Blogger safety failure: requested post {post_id}, received {returned_id}."
        )
    if status != "DRAFT":
        raise RuntimeError(
            f"Blogger safety failure: post {post_id} returned "
            f"{status or 'UNKNOWN'}; expected DRAFT."
        )
    print(f"Post ID: {post_id} - Status: {status} - DRAFT Verified")
    return verified


def find_duplicate_post(
    service: Any,
    blog_id: str,
    title: str,
    content: str,
    topic_key: str | None = None,
    max_pages: int | None = None,
    context: Any = None,
) -> dict[str, Any] | None:
    """Scan LIVE and DRAFT posts; any uncertainty aborts creation (fail closed)."""
    if context is None:
        import main as context

    from difflib import SequenceMatcher

    new_title = context.normalize_article_text(title)
    new_body = context.normalize_article_text(content)
    recovery_marker = context.topic_draft_marker(topic_key) if topic_key else None
    limit = max_pages if max_pages is not None else context.DUPLICATE_CHECK_MAX_PAGES
    if limit < 1:
        raise ValueError("Duplicate scan page limit must be at least one.")

    page_token = None
    seen_tokens: set[str] = set()
    try:
        for _ in range(limit):
            args = {
                "blogId": blog_id,
                "maxResults": context.DUPLICATE_CHECK_PAGE_SIZE,
                "fetchBodies": True,
                "status": ["LIVE", "DRAFT"],
            }
            if page_token:
                args["pageToken"] = page_token
            response = service.posts().list(**args).execute()

            for existing in response.get("items", []):
                old_content = str(existing.get("content", ""))
                if recovery_marker and recovery_marker in old_content:
                    return existing

                old_title = context.normalize_article_text(existing.get("title", ""))
                old_body = context.normalize_article_text(old_content)
                if old_title and old_title == new_title:
                    return existing

                if len(new_body) >= 500 and len(old_body) >= 500:
                    if new_body in old_body:
                        return existing
                    matcher = SequenceMatcher(None, new_body, old_body, autojunk=False)
                    coverage = sum(block.size for block in matcher.get_matching_blocks()) / len(new_body)
                    if coverage >= 0.88:
                        return existing

            next_token = response.get("nextPageToken")
            if not next_token:
                return None
            if next_token in seen_tokens:
                raise RuntimeError("Blogger duplicate scan returned a repeated page token.")
            seen_tokens.add(next_token)
            page_token = next_token

        raise RuntimeError(
            f"Duplicate scan exceeded {limit} pages; refusing to create a potentially repeated draft."
        )
    except Exception as exc:
        raise RuntimeError(
            f"Duplicate check could not be completed for blog {blog_id}: {exc}"
        ) from exc


def _build_search_description(route: dict[str, Any]) -> str:
    """Build a concise, route-specific Blogger search description from queue fields."""
    from datetime import datetime

    travel_date = datetime.strptime(str(route["date"]), "%Y-%m-%d").strftime("%d %B %Y").lstrip("0")
    description = (
        f"Plan {route['from']} ({route['iata_from']}) to {route['to']} "
        f"({route['iata_to']}) for {travel_date}. Compare baggage costs, airport "
        "transfers, schedules and EU passenger rights before booking."
    )
    if len(description) > 160:
        description = description[:157].rsplit(" ", 1)[0].rstrip(" ,;:") + "..."
    return description


def create_or_verify_draft(
    service: Any,
    blog_id: str,
    title: str,
    content: str,
    topic_key: str | None = None,
    context: Any = None,
    search_description: str | None = None,
) -> tuple[dict[str, Any], bool]:
    """Recover an existing draft or create one; never retry a non-idempotent insert."""
    if context is None:
        import main as context

    marked_content = context.add_topic_draft_marker(content, topic_key)
    duplicate = find_duplicate_post(
        service,
        blog_id,
        title,
        marked_content,
        topic_key=topic_key,
        context=context,
    )

    if duplicate:
        post_id = str(duplicate.get("id", "")).strip()
        if not post_id:
            raise RuntimeError("Matching Blogger record has no ID; refusing to continue.")
        if str(duplicate.get("status", "")).upper() == "LIVE":
            raise AssertionError(
                f"Matching Blogger post {post_id} is LIVE; refusing unsafe action."
            )
        return _verify_post_draft(service, blog_id, post_id), False

    # Do not automatically retry insert: if the network times out after Blogger
    # accepts it, the next run recovers this deterministic marker before inserting.
    result = service.posts().insert(
        blogId=blog_id,
        body={
            "kind": "blogger#post",
            "title": title,
            "content": marked_content,
            "labels": ["TRTT", "Flight Guide", "Sardinia", "787950"],
            **({"customMetaData": search_description} if search_description else {}),
        },
        isDraft=True,
    ).execute()
    post_id = str(result.get("id", "")).strip()
    if not post_id:
        raise RuntimeError("Blogger insert returned no post ID; workflow failed closed.")
    return _verify_post_draft(service, blog_id, post_id), True


def _create_or_recover_draft(
    service: Any, blog_id: str, title: str, content: str
) -> tuple[dict[str, Any], bool]:
    """Backward-compatible wrapper for the single authoritative DRAFT routine."""
    return create_or_verify_draft(service, blog_id, title, content)


def create_drafts_on_blogs(
    title: str,
    html_content: str,
    meta: dict,
    article_data: dict = None,
    photo: dict = None,
    topic: str = None,
    context: Any = None,
    credentials_factory: Any = None,
    builder: Any = None,
) -> list[dict]:
    """Compatibility adapter; Blogger API resource calls remain in this module."""
    if context is None:
        import main as context

    if not all(
        [context.BLOGGER_CLIENT_ID, context.BLOGGER_CLIENT_SECRET, context.BLOGGER_REFRESH_TOKEN]
    ):
        raise RuntimeError(
            "Blogger OAuth credentials are incomplete. Refusing to report a successful no-op run."
        )

    targets = []
    if context.BLOGGER_BLOG_ID:
        targets.append(("TRTT News 24 BD (Main Hub)", context.BLOGGER_BLOG_ID))
    if context.FLIGHTSCOUTPRO_BLOG_ID:
        targets.append(("FlightScoutPro (Partner Blog)", context.FLIGHTSCOUTPRO_BLOG_ID))

    for index, raw in enumerate(context.PARTNER_BLOG_IDS.split(","), 1):
        value = raw.strip()
        if value and value not in [item[1] for item in targets]:
            targets.append((f"Partner Network Blog #{index}", value))

    if context.os.path.exists("partners.json"):
        try:
            with open("partners.json", "r", encoding="utf-8") as handle:
                for partner in context.json.load(handle):
                    blog_id = partner.get("blog_id")
                    if blog_id and blog_id not in [item[1] for item in targets]:
                        targets.append((partner.get("site_name", "Partner Blog"), blog_id))
        except Exception as exc:
            print(f"partners.json read notice: {exc}")

    if not targets:
        raise RuntimeError("No Blogger target blog IDs are configured.")

    if credentials_factory is None or builder is None:
        from google.oauth2.credentials import Credentials as credentials_factory
        from googleapiclient.discovery import build as builder

    credentials = credentials_factory(
        None,
        refresh_token=context.BLOGGER_REFRESH_TOKEN,
        client_id=context.BLOGGER_CLIENT_ID,
        client_secret=context.BLOGGER_CLIENT_SECRET,
        token_uri="https://oauth2.googleapis.com/token",
    )
    service = builder("blogger", "v3", credentials=credentials)
    topic_key = context.topic_history_key(topic) if topic else None
    source_content = (article_data or {}).get("content", html_content)
    outcomes = []

    for blog_name, blog_id in targets:
        try:
            duplicate = find_duplicate_post(
                service,
                blog_id,
                title,
                source_content,
                topic_key=topic_key,
                context=context,
            )
            if duplicate:
                post_id = str(duplicate.get("id", "")).strip()
                if not post_id:
                    raise RuntimeError("Duplicate post found without a post ID.")
                if str(duplicate.get("status", "")).upper() == "LIVE":
                    raise RuntimeError("Matching Blogger post is LIVE; refusing unsafe action.")
                _verify_post_draft(service, blog_id, post_id)
                edit_url = f"https://www.blogger.com/blog/post/edit/{blog_id}/{post_id}"
                outcomes.append(
                    {
                        "blog_name": blog_name,
                        "blog_id": blog_id,
                        "post_id": post_id,
                        "edit_url": edit_url,
                        "status": "already_exists",
                    }
                )
                continue

            profile = context.get_blog_profile(blog_name, blog_id)
            tailored = (
                context.build_enterprise_html(article_data, photo, profile)
                if article_data and photo
                else html_content
            )
            body = {
                "title": title,
                "content": context.add_topic_draft_marker(tailored, topic_key),
                "labels": meta.get("labels", []),
                "customMetaData": meta.get("search_description", ""),
                "location": {"name": profile["author_location"]},
            }
            inserted = service.posts().insert(blogId=blog_id, body=body, isDraft=True).execute()
            post_id = str(inserted.get("id", "")).strip()
            if not post_id:
                raise RuntimeError("Blogger insert response did not contain a post ID.")
            _verify_post_draft(service, blog_id, post_id)
            edit_url = f"https://www.blogger.com/blog/post/edit/{blog_id}/{post_id}"
            outcomes.append(
                {
                    "blog_name": blog_name,
                    "blog_id": blog_id,
                    "post_id": post_id,
                    "edit_url": edit_url,
                    "status": "created",
                }
            )
            print(f"SUCCESS: Draft created - {blog_name} - Post ID: {post_id}")
        except Exception as exc:
            outcomes.append(
                {"blog_name": blog_name, "blog_id": blog_id, "status": "failed", "error": str(exc)}
            )
            print(f"Notice posting to {blog_name} (ID: {blog_id}): {exc}")

    return outcomes


def _load_queued_route() -> tuple[dict[str, Any], dict[str, Any]]:
    """Require one real queued route; an empty queue is a hard failure, never a fake pass."""
    import json
    from datetime import datetime

    queue_path = engine.QUEUE_FILE
    if not queue_path.is_file() or queue_path.stat().st_size == 0:
        raise RuntimeError(f"Queue is empty or missing: {queue_path}; refusing to report success.")

    try:
        queue = json.loads(queue_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Queue cannot be read: {exc}") from exc

    if not isinstance(queue, dict):
        raise RuntimeError("Queue must be a JSON object.")
    if queue.get("isDraft") is not True:
        raise RuntimeError("Queue policy failure: isDraft must be true.")
    if queue.get("batch_size") != 1:
        raise RuntimeError("Queue policy failure: batch_size must equal 1.")
    if queue.get("require_image") is not True:
        raise RuntimeError("Queue policy failure: require_image must be true.")
    if queue.get("require_marker") != engine.MARKER:
        raise RuntimeError("Queue policy failure: marker mismatch.")

    routes = queue.get("routes")
    if not isinstance(routes, list) or len(routes) != 1 or not isinstance(routes[0], dict):
        raise RuntimeError(
            f"Queue must contain exactly one route object; found "
            f"{len(routes) if isinstance(routes, list) else 'invalid'}."
        )

    route = dict(routes[0])
    required = ("from", "to", "iata_from", "iata_to", "date", "price", "airline")
    missing = [key for key in required if not str(route.get(key, "")).strip()]
    if missing:
        raise RuntimeError("Queued route is missing required fields: " + ", ".join(missing))
    if route.get("isDraft") is not True:
        raise RuntimeError("Route policy failure: route.isDraft must be true.")
    try:
        route_date = datetime.strptime(str(route["date"]), "%Y-%m-%d").date()
    except ValueError as exc:
        raise RuntimeError("Queued route date must use YYYY-MM-DD.") from exc
    if route_date < engine.publish_date().date():
        raise RuntimeError("Queued route date is in the past; refusing to create a stale draft.")

    print(
        f"Queue verified: version={queue.get('version', route['date'])}; "
        f"routes=1; date={route['date']}; isDraft=True"
    )
    return queue, route


def _affiliate_links_are_disclosed(content: str) -> bool:
    """Require every configured affiliate URL in content to use a sponsored/nofollow anchor."""
    for url in engine.AFFILIATES.values():
        if url not in content:
            continue
        href = f'href="{url}"'
        position = content.find(href)
        if position < 0:
            return False
        tag_start = content.rfind("<a", 0, position)
        tag_end = content.find(">", position)
        if tag_start < 0 or tag_end < 0:
            return False
        opening_tag = content[tag_start:tag_end + 1]
        if 'rel="sponsored nofollow noopener"' not in opening_tag:
            return False
    return True


def main(service_factory: Any = None) -> int:
    started = time.monotonic()
    primary, partner = _require_configuration()
    print("Republish allowed - today's date override (DRAFT-only; no live publishing).")
    queue, route = _load_queued_route()
    route_key = engine.route_key(route)
    title = f"{route['from']} to {route['to']} flight guide - {route['date']} - TRTT"
    content = engine.build_content(route)

    checks = {
        "800+ words": engine._plain_word_count(content) >= 800,
        "image": "<img src=" in content,
        "marker": engine.MARKER in content,
        "Vercel hub": engine.LIVE_APP in content,
        "affiliate links disclosed": _affiliate_links_are_disclosed(content),
    }
    for label, passed in checks.items():
        print(f"{label}: {'PASS' if passed else 'FAIL'}")
        if not passed:
            raise RuntimeError(f"Draft content validation failed: {label}")

    import main as editorial_context

    service = service_factory() if service_factory else _build_service()
    verified = []
    for blog_id, blog_name in (
        (primary, "trttnews24bd"),
        (partner, "flightscoutpro"),
    ):
        post, created = create_or_verify_draft(
            service,
            blog_id,
            title,
            content,
            topic_key=route_key,
            context=editorial_context,
            search_description=_build_search_description(route),
        )
        post_id = str(post.get("id", "")).strip()
        if not post_id:
            raise RuntimeError(f"{blog_name}: Blogger returned no Post ID.")
        # create_or_verify_draft performs posts().get() and fails unless Blogger returns DRAFT.
        status = str(post.get("status", "")).upper()
        if status != "DRAFT":
            raise RuntimeError(f"{blog_name}: read-back status was {status or 'UNKNOWN'}, not DRAFT.")
        if created:
            print(f"SUCCESS: Draft created - {blog_name} - Post ID: {post_id}")
        else:
            print(f"CONFIRMED: Existing Blogger DRAFT - {blog_name} - Post ID: {post_id}")
        print(f"{blog_name}: Post ID: {post_id} | Status: DRAFT VERIFIED")
        verified.append((blog_name, post_id))

    if len(verified) != 2:
        raise RuntimeError("Both Blogger sites must be verified before success.")
    engine.append_history(route_key)
    print(f"SUCCESS: {len(verified)} Blogger DRAFT posts verified; no LIVE posts created.")
    print(f"Elapsed: {time.monotonic() - started:.2f}s")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
