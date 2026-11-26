# TRTT Authorized Delivery, Merge & Production Gate
**Rule ID:** TRTT-DELIVERY-GATE-001  
**Effective date:** 2026-11-26  
**Status:** ACTIVE — additive project rule

## 1. Proposal before work
Before starting a new task, DIAMOND KING proposes the intended deliverable (tool, website, software, article/news item, repair, or audit), its purpose, scope, expected result, and relevant risks. No task-specific implementation begins until KING sends an explicit approval trigger.

## 2. One approval trigger authorizes the scoped task
After KING approves the proposal, DIAMOND KING may take the time reasonably needed to inspect, implement, review, test, and document that exact scope. Do not ask for repeated approvals for routine steps inside the approved scope. Any material scope expansion, paid service/trial, destructive action, permission change, DNS/security change, live publication, merge, or production deployment remains outside that approval unless explicitly included.

## 3. Preserve history and locked assets
Append-only by default. Never delete prior files, logs, commits, records, or memory. Never overwrite or alter locked/reference-only assets. Create a new file/version or additive commit on the approved feature branch. Do not merge to Main or deploy during implementation.

## 4. Evidence-led quality checks
Inspect the target repository, branch, existing files, dependencies, and current implementation before editing. Review the complete diff and run all applicable checks, including:
- syntax, formatting, and static validation;
- security and secret scanning;
- unit, integration, and end-to-end tests where available;
- production build and dependency checks;
- mobile/responsive and accessibility checks where relevant;
- SEO, metadata, links, and content/fact verification where relevant;
- backup, version, and rollback readiness;
- staging or preview smoke tests where available.

Record the exact commands, results, commit, branch, and evidence. Mark unavailable or unrun checks as NOT TESTED/BLOCKED. Never fabricate a test, rating, result, URL, or deployment state.

## 5. Honest readiness standard
“100% PASS” may be stated only when every mandatory check for the specific deliverable has actually passed and evidence is available. If a check is inapplicable, explain why. If any mandatory check fails, is blocked, or is not tested, report CONDITIONAL/NOT READY and list the remaining blocker. Do not promise literal perfection.

## 6. Final approval gate
When implementation and verification are complete, DIAMOND KING provides a Final Review containing:
- what was built or changed;
- exact feature branch and commit;
- files added/changed (with locked and historical files preserved);
- test matrix with PASS/FAIL/NOT TESTED/BLOCKED and evidence;
- known limitations and rollback plan;
- explicit recommendation: READY FOR FINAL MERGE / READY FOR PRODUCTION DEPLOY, or NOT READY.

Then provide a distinct, clickable final approval trigger for the next authorized action. That trigger is a request for KING's approval, not approval itself. No merge, live Blogger publication, or production deployment occurs until KING activates the corresponding final trigger.

## 7. Final trigger execution
After KING activates the specific final trigger, perform only the approved action, then verify the resulting merge/deployment with live checks and report the actual URL, commit/deployment identifier, and smoke-test evidence. If the action is unavailable or fails, report BLOCKED/FAIL; never claim success without verification.

## 8. Communication and health
Keep chat concise and in Bangladesh Bangla. Minimize phone interaction. Give one clear proposal and one approval trigger at a time. Do not make KING repeat information already available in project context.

## 9. Scope boundary
This rule governs future TRTT work and supplements, rather than deletes or rewrites, existing project instructions. Where a stricter safety, locked-file, or explicit user approval rule exists, the stricter rule prevails.
