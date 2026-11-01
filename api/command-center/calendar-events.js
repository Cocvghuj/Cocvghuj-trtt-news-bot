"use strict";
const { authorize } = require("../../lib/command-center/auth");
const { appendAuditEvent } = require("../../lib/command-center/audit");
const { listCalendarEvents, createCalendarEvent } = require("../../lib/command-center/google-services");

module.exports = async function handler(req, res) {
  const auth = authorize(req);
  if (!auth.ok) return res.status(auth.status).json({ error: auth.error });
  try {
    if (req.method === "GET") {
      const url = new URL(req.url, "https://command-center.local");
      const data = await listCalendarEvents({ timeMin: url.searchParams.get("timeMin"), timeMax: url.searchParams.get("timeMax") });
      return res.status(200).json({ items: data.items || [] });
    }
    if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed." });
    const body = typeof req.body === "string" ? (() => { try { return JSON.parse(req.body); } catch { return {}; } })() : (req.body || {});
    if (body.owner_approved !== true) return res.status(403).json({ error: "Explicit owner approval is required to create a calendar event." });
    await appendAuditEvent({ action: "calendar.event_requested", resource: "Google Calendar", status: "approved", summary: "Owner approved a calendar event; event details are not logged." });
    const event = await createCalendarEvent(body);
    try {
      await appendAuditEvent({ action: "calendar.event_created", resource: event.id || "Google Calendar event", status: "completed", summary: "Calendar event created after explicit owner approval." });
      return res.status(201).json({ created: true, audit_recorded: true, event_id: event.id, html_link: event.htmlLink });
    } catch {
      return res.status(202).json({ created: true, audit_recorded: false, audit_status: "pending", event_id: event.id, html_link: event.htmlLink });
    }
  } catch (error) {
    return res.status(503).json({ created: false, error: String(error.message || "Calendar operation failed") });
  }
};
