"use strict";
const { googleApi } = require("./google");

function validateGmailDraft(input = {}) {
  const to = String(input.to || "").trim();
  const subject = String(input.subject || "").trim();
  const body = String(input.body || "").trim();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(to)) throw new Error("A valid recipient email is required.");
  if (!subject || subject.length > 200) throw new Error("Email subject must contain 1–200 characters.");
  if (!body || body.length > 12000) throw new Error("Email body must contain 1–12000 characters.");
  return { to, subject, body };
}

function validateCalendarEvent(input = {}) {
  const summary = String(input.summary || "").trim();
  const start = input.start?.dateTime;
  const end = input.end?.dateTime;
  if (!summary || summary.length > 200) throw new Error("Event summary must contain 1–200 characters.");
  if (!start || !end || !Number.isFinite(Date.parse(start)) || !Number.isFinite(Date.parse(end))) {
    throw new Error("Calendar event requires valid start.dateTime and end.dateTime.");
  }
  if (Date.parse(end) <= Date.parse(start)) throw new Error("Calendar event end must be after start.");
  return { summary, description: String(input.description || "").slice(0, 4000), start: { dateTime: start }, end: { dateTime: end } };
}

async function createGmailDraft(input, env = process.env) {
  const draft = validateGmailDraft(input);
  const raw = [
    "To: " + draft.to,
    "Subject: " + draft.subject,
    "MIME-Version: 1.0",
    "Content-Type: text/plain; charset=UTF-8",
    "",
    draft.body
  ].join("\r\n");
  return googleApi("https://gmail.googleapis.com/gmail/v1/users/me/drafts", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: { raw: Buffer.from(raw, "utf8").toString("base64url") } })
  }, env);
}

async function listCalendarEvents({ timeMin, timeMax } = {}, env = process.env) {
  const start = timeMin || new Date().toISOString();
  const end = timeMax || new Date(Date.now() + 7 * 86400000).toISOString();
  if (!Number.isFinite(Date.parse(start)) || !Number.isFinite(Date.parse(end)) || Date.parse(end) <= Date.parse(start)) {
    throw new Error("Calendar range is invalid.");
  }
  const query = new URLSearchParams({ timeMin: start, timeMax: end, singleEvents: "true", orderBy: "startTime", maxResults: "100" });
  return googleApi("https://www.googleapis.com/calendar/v3/calendars/primary/events?" + query.toString(), {}, env);
}

async function createCalendarEvent(input, env = process.env) {
  const event = validateCalendarEvent(input);
  return googleApi("https://www.googleapis.com/calendar/v3/calendars/primary/events", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(event)
  }, env);
}

async function createGoogleDoc(title, textContent, env = process.env) {
  const safeTitle = String(title || "").trim().slice(0, 200);
  const content = String(textContent || "").slice(0, 30000);
  if (!safeTitle || !content) throw new Error("Document title and content are required.");
  const doc = await googleApi("https://docs.googleapis.com/v1/documents", {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ title: safeTitle })
  }, env);
  await googleApi("https://docs.googleapis.com/v1/documents/" + encodeURIComponent(doc.documentId) + ":batchUpdate", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ requests: [{ insertText: { location: { index: 1 }, text: content } }] })
  }, env);
  return { documentId: doc.documentId, title: doc.title };
}

async function createGoogleSlides(title, env = process.env) {
  const safeTitle = String(title || "").trim().slice(0, 200);
  if (!safeTitle) throw new Error("Presentation title is required.");
  const presentation = await googleApi("https://slides.googleapis.com/v1/presentations", {
    method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ title: safeTitle })
  }, env);
  return { presentationId: presentation.presentationId, title: presentation.title };
}

async function listGoogleTasks(env = process.env) {
  return googleApi("https://tasks.googleapis.com/tasks/v1/lists/@default/tasks?maxResults=100", {}, env);
}

async function createGoogleTask(title, notes = "", env = process.env) {
  const safeTitle = String(title || "").trim().slice(0, 200);
  if (!safeTitle) throw new Error("Task title is required.");
  return googleApi("https://tasks.googleapis.com/tasks/v1/lists/@default/tasks", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title: safeTitle, notes: String(notes || "").slice(0, 4000) })
  }, env);
}

async function createGoogleForm(title, env = process.env) {
  const safeTitle = String(title || "").trim().slice(0, 200);
  if (!safeTitle) throw new Error("Form title is required.");
  return googleApi("https://forms.googleapis.com/v1/forms", {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ info: { title: safeTitle, documentTitle: safeTitle } })
  }, env);
}

module.exports = { validateGmailDraft, validateCalendarEvent, createGmailDraft, listCalendarEvents, createCalendarEvent, createGoogleDoc, createGoogleSlides, listGoogleTasks, createGoogleTask, createGoogleForm };