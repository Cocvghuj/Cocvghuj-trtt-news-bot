# TRTT Million Dollar English News Drafts Architecture

## Overview
The **TRTT MILLION DOLLAR English News Drafts** engine is an enterprise automated content pipeline designed for high Google Search indexation, strict E-E-A-T compliance, multi-network affiliate conversion, and zero-duplicate draft generation.

---

## Key Pillars

### 1. Google Search Compliance (E-E-A-T)
- **Title Bounds:** Strict 1-100 characters, English Latin characters only.
- **Search Description:** Strict 120-160 characters for optimal Google Rich Snippets without clipping.
- **Labels / Tags:** Maximum 5 unique, English Latin labels (each under 50 characters).
- **Grounding & Authenticity:** Articles are anchored in real ground handling experience in Sanluri, Sardinia, Italy (Via Carlo Felice ARST 08:17, 39.5613° N, 8.6332° E) and Cagliari Airport (CAG).

### 2. Multi-Network Commercial Integrity
- **Travelpayouts Marker:** Permanent lock on Marker `787950`.
- **Kiwitaxi Transfer:** Permanent fix on `tIZcbMOB` (zero bug, fixed airport rates).
- **SubID Auto-Tracking:** `subid=trtt_lock_it` for geo-targeted European conversion.
- **Real Direct Partnerships:** Direct link to authentic Italian hotel `hotel-bernini.it` (3-5% direct booking model vs. 20% OTA commission).
- **GDPR & Privacy:** Full compliance with `trtt_cookie_consent_esim` notice.

### 3. Execution Schedule & Workflow Hardening
- **Cron Trigger:** Runs 3x daily at `07:00`, `13:00`, and `19:00` UTC (corresponding to 09:00, 15:00, and 21:00 Italian local time).
- **Manual Trigger:** Supports full `workflow_dispatch` with custom news topic and HTTPS primary source validation.
- **Blogger API Synchronization:** Drafts are delivered directly to:
  - `TRTT News 24 BD` (`trttnews24bd.blogspot.com`)
  - `FlightScoutPro` (`flightscoutpro.blogspot.com`)
  - Configured partner networks (`PARTNER_BLOG_IDS`)

---

## File Manifest
1. `.github/workflows/trtt-english-news-drafts.yml` - Hardened GitHub Actions orchestrator with 3x daily cron, strict unit validation, and Blogger draft dispatcher.
2. `scripts/draft_news.py` - Core Python generation & validation engine with Latin filtering, traffic injection, and Vercel/GitHub cross-referencing.
3. `tests/test_draft_news.py` - Comprehensive unit test suite covering metadata validation, URL security, Latin enforcement, and idempotent traffic injection.
4. `NEWS_DRAFT_WORKFLOW.md` - Technical and operational documentation.
