#!/usr/bin/env python3
"""Create one unique, 300-word DRAFT for each TRTT Blogger site.

Safety: inserts are always isDraft=True. Existing LIVE posts are never changed.
"""
from __future__ import annotations

import html
import os
import re
import sys
from typing import Any

ARTICLES = {
    "trtt": {
        "blog_name": "TRTT News 24 BD",
        "blog_env": "BLOGGER_BLOG_ID",
        "title": "Google DeepMind Uses AI to Formally Verify Signal's Encryption Code",
        "source_url": "https://deepmind.google/blog/introducing-alphaproof-code/",
        "source_name": "Google DeepMind, November 10, 2026",
        "secondary_url": "https://www.axios.com/2026/11/10/google-code-verification-signal",
        "labels": ["Technology", "Artificial Intelligence", "Cybersecurity", "Google DeepMind"],
        "image_url": "https://images.squarespace-cdn.com/content/v1/667aeccd76a11f656cb108df/b630ca20-71f0-437f-ab03-fb695d64cbd0/Signal_3.png?format=2500w",
        "image_credit_url": "https://www.beneficialaifoundation.org/blog/signal-shot",
        "image_alt": "Illustration of engineers examining secure messaging and encryption systems",
        "paragraphs": [
            "Google DeepMind says it has used artificial intelligence agents to formally verify security properties in the code behind Signal, the secure messaging protocol used by millions. The research, announced on November 10, is a step in applying AI to software assurance rather than only code generation or vulnerability discovery.",
            "The system, called AlphaProof Code, combines human-guided specifications with AI proof agents. Researchers first defined the security properties that the code should satisfy. The agents then produced mathematical proofs, which were checked by Lean, a proof assistant. DeepMind reported generating more than six million lines of Lean proof code.",
            "The work examined libsignal, the reference implementation of Signal's protocol, at the code level. The proofs covered protections in the post-quantum PQXDH handshake and the Triple Ratchet, including forward secrecy, authentication and protection after a device compromise. DeepMind said the project took four weeks, a task that traditionally could require years.",
            "Researchers tested whether the framework could distinguish secure code from known-buggy code. They reintroduced two previously fixed vulnerabilities into an isolated version of Signal. In both tests, the system produced proofs showing that the altered implementation failed the specified security properties. The team released its verification materials for scrutiny.",
            "The result is not proof that every part of Signal, every messaging feature or all software is invulnerable. The work covered properties and one-to-one protocol sessions; formal proofs are only as broad as their specifications and assumptions. Human experts still need to decide what must be proved and review the claims.",
            "DeepMind sees possible applications in critical software, including healthcare, infrastructure and finance. Its ambition is to connect formal verification with AI-assisted software development, so changes can be checked before release. For now, AlphaProof Code is a research milestone, not a universal security guarantee or replacement for testing, audits and responsible engineering."
        ],
    },
    "flight": {
        "blog_name": "FlightScoutPro",
        "blog_env": "FLIGHTSCOUTPRO_BLOG_ID",
        "title": "Thai Airways Says Passenger Booking Data May Have Been Accessed in Amadeus Incident",
        "source_url": "https://www.thaiairways.com/fr-fr/content/actualites-et-communiques/amadeus-reports-unauthorized-access-to-thai-passenger-data/",
        "source_name": "Thai Airways International, November 9, 2026",
        "secondary_url": "https://www.nationthailand.com/news/40073323",
        "labels": ["Travel News", "Aviation", "Airline Technology", "Cybersecurity"],
        "image_url": "https://dovisa-cdn-assets.s3.eu-central-1.amazonaws.com/news/thailand-joins-australia-the-netherlands-new-zealand-and-the-uk-with-major-summer-2026-flight-schedule-offering-passengers-direct-flights-to-amsterdam-auckland-perth-and-more-content.jpg",
        "image_credit_url": "https://dovisa.com/news/thailand-joins-australia-the-netherlands-new-zealand-and-the-uk-with-major-summer-2026-flight-schedule-offering-passengers-direct-flights-to-amsterdam-auckland-perth-and-more",
        "image_alt": "Thai Airways passenger aircraft parked at an airport terminal",
        "paragraphs": [
            "Thai Airways International says passenger booking information may have been accessed without authorisation in a cybersecurity incident involving Amadeus, the technology company providing its passenger service systems. In a November 9 notice, the airline said the incident affected data stored in Amadeus systems, not its operational systems.",
            "Thai Airways said approximately 60,529 passenger records may have been accessed. Information potentially involved includes names, booking reference numbers, travel dates, flight routes and cabin class. About 376 additional records may include more sensitive details, such as email addresses, telephone numbers, passport numbers, nationality and frequent-flyer membership numbers.",
            "The access period identified by the airline ran from August 10, 2023, to September 23, 2026. Thai Airways said credit-card information was not affected and that it had found no evidence that accessed data had been disclosed. The airline is examining information supplied by Amadeus and has informed authorities.",
            "Amadeus told the airline that credentials used in the unauthorised access had been revoked and affected passwords reset. The provider also said it had strengthened monitoring and detection. Thai Airways said the incident had not affected flight operations or passenger services, and apologised for concern caused.",
            "For travellers, the case is a reminder that booking data can be held by technology suppliers as well as airlines. Passengers who receive a notification should check it comes from an official Thai Airways channel. Be cautious about unexpected messages referring to a booking, avoid unfamiliar links and never provide passwords or payment details in response to unsolicited requests.",
            "Thai Airways said it would contact affected passengers individually after verifying details. The airline has not described the incident as a flight disruption, and travellers should not assume their journeys are cancelled. Anyone with concerns should use the airline's official website or customer-service channels, not contact details in suspicious messages."
        ],
    },
}

def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))

def article_html(article: dict) -> str:
    image = (
        f'<p><img src="{html.escape(article["image_url"], quote=True)}" '
        f'alt="{html.escape(article["image_alt"], quote=True)}" /></p>'
        f'<p><small>Image credit: <a href="{html.escape(article["image_credit_url"], quote=True)}" '
        f'rel="nofollow noopener">image source</a></small></p>'
    )
    paragraphs = "\n".join(f"<p>{html.escape(p)}</p>" for p in article["paragraphs"])
    sources = (
        f'<p><strong>Primary source:</strong> <a href="{html.escape(article["source_url"], quote=True)}" '
        f'rel="nofollow noopener">{html.escape(article["source_name"])}</a>.</p>'
        f'<p><strong>Additional reporting:</strong> <a href="{html.escape(article["secondary_url"], quote=True)}" '
        f'rel="nofollow noopener">Read supporting coverage</a>.</p>'
    )
    return image + "\n" + paragraphs + "\n" + sources

def require_env() -> tuple[dict[str, str], str, str, str]:
    ids = {}
    for key, article in ARTICLES.items():
        env_name = article["blog_env"]
        value = os.environ.get(env_name, "").strip()
        if not value:
            raise RuntimeError(f"Missing required GitHub Actions secret: {env_name}")
        ids[key] = value
    if len(set(ids.values())) != 2:
        raise RuntimeError("The two Blogger blog IDs must be different.")
    names = ("BLOGGER_CLIENT_ID", "BLOGGER_CLIENT_SECRET", "BLOGGER_REFRESH_TOKEN")
    missing = [name for name in names if not os.environ.get(name, "").strip()]
    if missing:
        raise RuntimeError("Missing required GitHub Actions secrets: " + ", ".join(missing))
    return ids, *(os.environ[name].strip() for name in names)

def verify_draft(service: Any, blog_id: str, post_id: str, article: dict) -> None:
    # Drafts are only visible in the authenticated owner/admin view.
    post = service.posts().get(blogId=blog_id, postId=post_id, view="ADMIN").execute()
    if str(post.get("id", "")) != str(post_id):
        raise RuntimeError(f"Read-back ID mismatch for {article['blog_name']}.")
    if str(post.get("status", "")).upper() != "DRAFT":
        raise RuntimeError(f"Safety stop: {article['blog_name']} post is not DRAFT.")
    if post.get("title") != article["title"]:
        raise RuntimeError(f"Read-back title mismatch for {article['blog_name']}.")
    if article["image_url"] not in str(post.get("content", "")):
        raise RuntimeError(f"Image read-back check failed for {article['blog_name']}.")

def find_existing(service: Any, blog_id: str, article: dict) -> dict | None:
    token = None
    for _ in range(20):
        # ADMIN view is required to list unpublished drafts and expose status.
        args = {"blogId": blog_id, "maxResults": 100, "status": ["LIVE", "DRAFT"], "view": "ADMIN"}
        if token:
            args["pageToken"] = token
        response = service.posts().list(**args).execute()
        for item in response.get("items", []):
            if item.get("title") == article["title"]:
                status = str(item.get("status", "")).upper()
                if status == "LIVE":
                    raise RuntimeError(f"Matching article is already LIVE on {article['blog_name']}; no changes made.")
                if status != "DRAFT":
                    raise RuntimeError(f"Unexpected existing post status on {article['blog_name']}: {status!r}")
                return item
        token = response.get("nextPageToken")
        if not token:
            return None
    raise RuntimeError(f"Duplicate scan exceeded 20 pages for {article['blog_name']}.")

def create_or_confirm(service: Any, blog_id: str, article: dict) -> str:
    existing = find_existing(service, blog_id, article)
    if existing:
        post_id = str(existing.get("id", "")).strip()
        if not post_id:
            raise RuntimeError(f"Matching draft on {article['blog_name']} has no ID.")
        verify_draft(service, blog_id, post_id, article)
        print(f"CONFIRMED existing DRAFT: {article['blog_name']} | post_id={post_id}")
        return post_id
    result = service.posts().insert(
        blogId=blog_id,
        isDraft=True,
        body={
            "kind": "blogger#post",
            "title": article["title"],
            "content": article_html(article),
            "labels": article["labels"],
        },
    ).execute()
    post_id = str(result.get("id", "")).strip()
    if not post_id:
        raise RuntimeError(f"Blogger returned no post ID for {article['blog_name']}.")
    verify_draft(service, blog_id, post_id, article)
    print(f"VERIFIED DRAFT: {article['blog_name']} | post_id={post_id}")
    return post_id

def main() -> int:
    for article in ARTICLES.values():
        count = word_count(" ".join(article["paragraphs"]))
        if count != 300:
            raise RuntimeError(f"{article['blog_name']} article must be 300 words; found {count}.")
        if not article["source_url"].startswith("https://") or not article["image_url"].startswith("https://"):
            raise RuntimeError(f"Source or image URL validation failed for {article['blog_name']}.")
    ids, client_id, client_secret, refresh_token = require_env()

    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    credentials = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/blogger"],
    )
    service = build("blogger", "v3", credentials=credentials, cache_discovery=False)

    results = []
    for key, article in ARTICLES.items():
        results.append(create_or_confirm(service, ids[key], article))
    if len(results) != 2 or not all(results):
        raise RuntimeError("Both unique blog drafts must be verified before success.")
    print("SUCCESS: two different 300-word articles, with separate images, were read back and verified as DRAFTS.")
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
