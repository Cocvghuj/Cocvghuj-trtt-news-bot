# TRTT IMMUTABLE MASTER FILE — PROTECTION POLICY

**Status:** LOCKED / REFERENCE-ONLY  
**Project:** TRTT Voyage — DIAMOND RAJA / DIAMOND KING  
**Policy owner:** DIAMOND RAJA  
**Effective:** 2026-11-24

## 1. Protected identity

The following file is the immutable master and must be treated as read-only:

- **Public reference URL:** https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/diamond-king-v7-final.html
- **Repository:** `Cocvghuj/Cocvghuj-trtt-news-bot`
- **Canonical repository path observed:** `diamond-king-v7-final.html`
- **Verified copy:** GitHub `main` branch
- **Observed Git blob SHA (GitHub main):** `44d4a3092d43308062d1fbaf26b956aaefee9fb4`

The SHA above is a Git blob SHA, not a SHA-256 checksum. It identifies the copy fetched from GitHub `main` during the 2026-11-24 inspection.

## 2. Absolute no-touch rule

No contributor, automation, assistant, workflow, bot, or deployment process may:

- edit, overwrite, replace, truncate, reformat, or patch this file;
- delete, rename, move, or change its path;
- publish a modified copy over the public reference;
- use it as a working draft or test fixture that writes back to the same path;
- change its contents indirectly through a bulk commit, generated output, sync, or deployment.

If a task appears to require touching this file, STOP and report BLOCKED. Do not attempt a repair in place.

## 3. Safe development rule

All improvements must be additive and use a new filename (for example, `diamond-king-v8-preview.html`) on a non-default feature branch.

- Preserve the immutable file byte-for-byte.
- Never reuse the locked path for a new version.
- Keep changes isolated to a feature branch.
- Review the diff and run relevant tests before reporting PASS.
- Keep a separate backup of any new working artifact before risky transformations.
- Do not copy the master to another provider and claim it is a verified backup unless the bytes have been fetched and compared.

## 4. Mandatory pre-change verification

Before any repository write:

1. Fetch the locked path from its known source ref.
2. Compare its Git blob SHA with the recorded SHA above.
3. If the file is missing, the SHA differs, or the source ref is uncertain, STOP. Do not overwrite or restore automatically.
4. Confirm the target path for the new work does not already exist.
5. Confirm the target is a feature branch, not `main`, `gh-pages`, or another deployment branch.
6. After writing, fetch the locked file again and verify its SHA is unchanged.

## 5. Approval gates

Explicit DIAMOND RAJA approval is required before:

- live Blogger publishing or theme upload;
- merging into `main`;
- production deployment or changing a deployment source;
- DNS, domain, repository security, token, secret, or permission changes;
- changing or removing this policy.

Autonomous work is permitted only for safe, additive, non-production work on feature branches. The user's domain/DNS work is outside this task and must not be touched.

## 6. Provider records and observed limits (2026-11-24)

### GitHub
- Repository metadata confirms the default branch is `main`.
- The locked file was fetched successfully from GitHub `main` with blob SHA `44d4a3092d43308062d1fbaf26b956aaefee9fb4`.
- The same path was not found on the inspected `gh-pages` branch.
- GitHub branch-protection enforcement for `main` was not verified in this inspection.
- The public GitHub Pages URL could not be fetched by the available verifier; the exact bytes currently served at that URL are therefore NOT VERIFIED.

### GitLab
- Project: `trttnews24bd-group/Cocvghuj-trtt-news-bot`.
- GitLab `main` was reported as protected.
- The working branch `feature/trtt-voyage-diamond-theme-v1` was reported as not protected.
- The locked file path was not found on GitLab `main` during this inspection. Do not claim that GitLab holds a byte-identical backup of the master.
- This policy document is a rules record, not a technical access-control lock.

## 7. Honest status vocabulary

Use only:
- **PASS** — the exact operation was performed and verified.
- **FAIL** — the operation was attempted and failed.
- **NOT TESTED** — no test was performed.
- **BLOCKED** — a required permission, source, or prerequisite is missing.
- **TODO** — work remains.

Never describe a file as technically immutable or untouchable solely because this document says so. Enforced protection requires verified repository permissions/rules in the provider itself.

## 8. Change history

- 2026-11-24: Initial immutable-master policy recorded separately. The original HTML and MASTER-004 work-order file were not modified.
