"use strict";

const POLICY = Object.freeze({
  read: "allow",
  research: "allow",
  create_code_change: "owner_approval_per_change",
  create_gmail_draft: "allow",
  send_email: "owner_approval_per_message",
  create_calendar_event: "owner_approval_per_event",
  write_google_drive: "owner_approval_per_action",
  update_notion: "owner_approval_per_action",
  deploy_vercel: "owner_approval_per_deployment",
  send_telegram_message: "owner_approval_per_message",
  delete_data: "explicit_owner_approval",
  change_permissions: "explicit_owner_approval",
  paid_api_usage: "blocked_by_default",
  paid_service_provisioning: "blocked",
  blogger_draft_publish: "blocked",
  blogger_workflow: "blocked",
  execute_main_py: "blocked"
});

function decisionFor(action, approved = false) {
  const rule = POLICY[action];
  if (!rule) return { allowed: false, reason: "Unknown action is denied by default." };
  if (rule === "allow") return { allowed: true, reason: "Allowed by policy." };
  if (rule === "blocked" || rule === "blocked_by_default") {
    return { allowed: false, reason: "This action is blocked by the current safety policy." };
  }
  if (approved === true) return { allowed: true, reason: "Explicit owner approval supplied." };
  return { allowed: false, reason: "Owner approval is required." };
}

module.exports = { POLICY, decisionFor };