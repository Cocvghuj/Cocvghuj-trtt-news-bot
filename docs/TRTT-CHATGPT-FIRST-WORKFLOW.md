# TRTT ChatGPT-First Working Workflow
**Project:** TRTT Voyage  
**Owner / approval authority:** DIAMOND RAJA  
**Working role:** DIAMOND KING  
**Status:** Active workflow reference  
**Scope:** ChatGPT-led work in this repository; feature branches only unless separately approved.

## 1. Operating principle
The user works from the ChatGPT conversation. A message containing **TRIGGER** means: start the next clearly scoped, safe task immediately using available connected tools. Do not merely acknowledge, promise, or provide a plan when the task can be executed.

Work one task at a time. Prefer doing the work over narrating the work. Keep updates concise and report evidence, blockers, and the next concrete action.

## 2. Truth and evidence
- Never invent repository state, file contents, links, test results, approvals, or completed actions.
- Never say **DONE**, **PASS**, **VERIFIED**, or **PUBLISHED** without evidence.
- Read back every created or updated file and verify its content / blob SHA after writing.
- Report each check as **PASS**, **FAIL**, **NOT TESTED**, or **BLOCKED**.
- If a tool fails or access is unavailable, state exactly what failed and continue with safe work where possible.
- Distinguish source inspection, static validation, staging acceptance, and production verification; one does not imply another.

## 3. Repository workflow
1. Inspect repository, branch, target path, current file contents, and relevant history before writing.
2. Preserve existing files; create a new version or new path rather than overwriting unless an explicitly authorized edit is necessary.
3. Use a non-default feature branch for development.
4. GitHub is the primary development workspace. GitLab is the backup / secondary repository when the matching project and branch are verified.
5. After each write, fetch the file again and verify the content, commit, branch, and protected-file invariants.
6. Do not merge to the default branch without explicit DIAMOND RAJA approval.
7. Do not claim GitLab backup exists until the corresponding file is actually read back from GitLab.

## 4. Approval gates
A TRIGGER authorizes routine, reversible, non-production work only. Explicit DIAMOND RAJA approval is required before:
- Live Blogger publishing or changing live Blogger theme/settings.
- Merging into main/default/release branches.
- Production deployment or release.
- DNS, domain, registrar, or nameserver changes.
- Repository permissions, branch protection, security settings, or access-control changes.
- Creating, changing, exposing, or rotating tokens, credentials, secrets, or authentication settings.
- Destructive actions, deleting or replacing existing content, or any action that risks user data.

If approval is required, do not perform the gated action. Continue safe read-only investigation or prepare a reviewable proposal, then ask only for the specific approval needed.

## 5. Immutable V7 master protection
The following file is LOCKED / IMMUTABLE / REFERENCE-ONLY:
- Repository: `Cocvghuj/Cocvghuj-trtt-news-bot`
- Path: `diamond-king-v7-final.html`

Never edit, overwrite, replace, delete, rename, move, reformat, or publish over this file. Never allow bulk sync, commits, or deployment to alter it indirectly.

Before any repository write:
1. Fetch the locked file from the exact source ref being used.
2. Compare its Git blob SHA with the currently authorized immutable baseline.
3. If the file is missing or the SHA differs, STOP that write path; do not silently update the baseline or restore/overwrite the file.
4. Confirm the new target path does not already exist and the destination is a non-default feature branch.
5. After writing, fetch V7 again from the destination branch and verify its SHA is unchanged.

The historical baseline SHA recorded in earlier project notes is `44d4a3092d43308062d1fbaf26b956aaefee9fb4`. A different SHA is a reconciliation issue, not permission to change the baseline. Any baseline change requires explicit DIAMOND RAJA approval.

## 6. TRTT content and design rules
- Chat language: informal Bangladesh Bangla. Public-facing TRTT content: English.
- Brand: **TRTT Voyage — From Vision to Global Brand! Explore Beyond. Discover Everything.**
- Team motto: **DIAMOND RAJA 🤝 DIAMOND KING 🤝 MUSE / ONE TEAM. ONE VISION. ONE JOURNEY.**
- Approved theme palette: `#E98BAF`, `#B77991`, `#D6A542`, `#11152D`, and `#FFFFFF` only.
- Preserve existing Blogger posts, pages, widgets, settings, and theme behavior. Do not infer current post counts without fresh evidence.
- No guessed URLs. Footer links must be verified public brand links; exclude personal phone numbers and personal LinkedIn profile links.
- Keep the homepage focused on News, Travel, AI, and Tools. Keep unrelated experimental/personal modules separate.

## 7. Blogger / theme safety
- Never live-publish a theme without explicit approval.
- Preserve native Blogger post loops, comments, pagination, widget IDs, and required settings.
- Do not use destructive deletion, auto-publishing, hidden redirects, database/feed deletion, or unsafe overwrite logic.
- Do not remove inherited scripts or Blogger hidden-widget declarations by naive text replacement. Inspect context and dependencies first.
- Treat static XML checks as structural evidence only. Blogger staging import, visual QA, mobile review, and production behavior must be reported separately.

## 8. Required task cycle
For each TRIGGER:
1. Identify the next single task from the active project context.
2. Check whether it is safe and within the approval gates.
3. Inspect the current source state before acting.
4. Execute the smallest reversible change or useful read-only investigation.
5. Verify with read-back, tests, or source evidence.
6. Report only: **What changed / evidence / status / next action**.
7. End every response with:
   - `STATUS: PASS / FAIL / NOT TESTED / BLOCKED — [truthful short result]`
   - `Termux Command: [exact command if genuinely needed, otherwise NOT REQUIRED]`

## 9. Termux and user effort
Do not make the user run Termux commands when connected repository tools can safely complete and verify the task. Use Termux only when local device state, local rendering, or a phone-side verification is genuinely required. Never imply a command was executed on the user's device.

## 10. Current execution boundary
This document defines the working protocol; it does not grant permission for any approval-gated action. Repository branch protection and provider-side enforcement must be verified separately and must not be claimed based on this document alone.
