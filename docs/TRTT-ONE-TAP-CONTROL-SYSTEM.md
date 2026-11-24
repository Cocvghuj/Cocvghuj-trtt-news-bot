# TRTT One-Tap Control System

Status: FEATURE-BRANCH IMPLEMENTATION / NOT ACTIVE ON DEFAULT BRANCH

## Goal
Use ChatGPT as the conversational trigger and GitHub as the durable task queue, automation runner, and evidence log.

## Control flow
1. User sends TRTT START / STATUS / STOP in ChatGPT.
2. ChatGPT interprets the instruction and, for queued work, creates a GitHub Issue with the `trtt-queue` label.
3. The queue workflow validates the structured request and records QUEUED or BLOCKED in the issue.
4. ChatGPT performs permitted repository work through the GitHub connector, or a separately reviewed GitHub Action performs a narrowly scoped safe task.
5. Results are reported with commit/run links and PASS, FAIL, NOT TESTED, or BLOCKED.

## Queue contract
Every queued task must state:
- Task type
- Requested action
- Target branch
- Risk level
- Acceptance criteria
- Approval status

Allowed intake categories: Safe audit, Code change, Blogger draft, SEO/content review. "Other" is held for review. Intake does not itself authorize execution.

## Approval locks
- No merge to main without explicit DIAMOND RAJA approval for that specific merge.
- No live Blogger publish without explicit approval for that specific post.
- No DNS, secrets, OAuth, account permissions, or security-setting changes without explicit approval.
- No destructive deletion, mass edits, or changes to existing Blogger posts/widgets without explicit approval.
- Queue labels, workflow_dispatch, and scheduled runs are not approval.
- A queued task is not proof that work ran or passed.

## Scheduling
A daily queue summary is configured at 07:00 UTC. GitHub scheduled workflows run only from the default branch. This feature-branch copy is therefore dormant until separately reviewed and approved for the default branch. No merge is performed by this implementation.

## Stop / status
- STOP means do not start additional queued work; it does not cancel already-running external jobs unless explicitly cancelled.
- STATUS means inspect current open queue issues and recent workflow runs, then report evidence.
- Each work item must end with a status and links to its issue, commit, and workflow run where available.

## Existing workflow risks observed
- `trtt-master-control.yml` creates Blogger drafts from manual dispatch or an issue labeled `trtt-task`. It is a draft creator, not a general-purpose task runner.
- `trtt-safe-auto.yml` contains an auto-merge step when a PR carries the `auto` label. This conflicts with the project approval policy and requires a separate review before any default-branch activation.
- Several legacy autopilot/publish/sync workflows are disabled to avoid duplicate posts and conflicts.
- Blogger Theme XML and Layout gadget placement remain manual owner-side operations.

## Honest capability boundary
ChatGPT cannot keep itself awake or independently execute work continuously between conversations. GitHub Actions can run event-driven and scheduled jobs while enabled. ChatGPT can initiate and inspect tasks when the user returns or sends a trigger. A persistent button in every new ChatGPT chat cannot be installed by repository code; use the chat trigger phrase or a supported ChatGPT UI feature.
