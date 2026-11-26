# TRTT MAGIC — Release Candidate Fix Memory

**Date:** 2026-11-26  
**Repository:** `Cocvghuj/Cocvghuj-trtt-news-bot`  
**Branch:** `feature/trtt-magic-ai-tool-builder-mvp-v1`

## আজকে কি করলাম
- পূর্বের V3 visual-QA HTML-কে additive release file `trttmagic.html` হিসেবে promote করা হয়েছে; পুরোনো V2 এবং V3 source file অক্ষত।
- Source-contract test এখন `trttmagic.html` পরীক্ষা করে, পুরোনো V2 target নয়।
- Form input/change হলে generated preview invalidates হয়; template বদলালেও পুরোনো preview আর copy/export করা যায় না।
- Stale-preview regression test যোগ করা হয়েছে।
- Visual QA focus test এখন computed `outlineColor` নয়, বাস্তবে render হওয়া `box-shadow` focus ring ও তার contrast পরীক্ষা করে।
- README-তে prototype সীমাবদ্ধতা ও release-candidate validation status হালনাগাদ করা হয়েছে।
- এই addendum পুরোনো Step-4 memory-কে replace করে না; এটি append-only ইতিহাস।

## Release validation status
- এই commit-এর পর GitHub Actions workflow ফলাফল যাচাই করতে হবে; ফলাফল না আসা পর্যন্ত নতুন RC validation = NOT TESTED.
- পূর্বের V3 baseline visual QA: 12/12 Chromium checks PASS (আগের commit/run)।
- Physical Android Chrome: NOT TESTED.
- AI API/backend/auth/database: NOT IMPLEMENTED.
- Main merge, production deployment, Blogger publish: NOT ATTEMPTED.

## কালকে কি করবো
- নতুন GitHub Actions run-এর source tests ও Chromium E2E/visual QA ফলাফল পরীক্ষা।
- সব pass হলে README ও এই memory-তে run URL/সংখ্যা append/update করে final RC status নির্ধারণ।
- Android physical browser test আলাদা করে করা; না হলে NOT TESTED রাখা।
- পরবর্তী merge/deploy/blog action-এর আগে আলাদা অনুমতি নিতে হবে।

## Validation update — 2026-11-26
- GitHub Actions source-contract tests for the release branch passed: **11/11**.
- Run: https://github.com/Cocvghuj/Cocvghuj-trtt-news-bot/actions/runs/45758872204
- Chromium E2E/visual QA against `trttmagic.html` is still in progress at run 45758872131; do not mark browser validation PASS until it completes.
- Earlier E2E attempt found one regression-test failure and one source-test expectation mismatch; both were corrected in later commits. Historical failed runs remain visible and were not deleted.

## Final RC validation — 2026-11-26
- PASS — source-contract suite: **11/11**, run https://github.com/Cocvghuj/Cocvghuj-trtt-news-bot/actions/runs/45758872204
- PASS — Chromium E2E + visual QA: **13/13**, run https://github.com/Cocvghuj/Cocvghuj-trtt-news-bot/actions/runs/45758872131
- The 13 checks include stale-preview invalidation, copy, JSON export, required-field validation, template behavior, mobile stacking/no overflow, 9 responsive viewport widths (320–1440px), WCAG AA normal-text contrast, visible input/panel boundaries, and focus-ring box-shadow contrast.
- Screenshot artifact: https://github.com/Cocvghuj/Cocvghuj-trtt-news-bot/actions/runs/45758872131/artifacts/15088931243
- Physical Android Chrome remains NOT TESTED. API/backend/auth/database/production hosting remain NOT IMPLEMENTED.
- No merge, deployment, Blogger publish, or Main write was performed.
