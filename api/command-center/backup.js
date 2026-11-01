"use strict";
const { authorize } = require("../../lib/command-center/auth");
const { createDriveBackup } = require("../../lib/command-center/audit");

module.exports = async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed." });
  const auth = authorize(req, "COMMAND_CENTER_BACKUP_TOKEN");
  if (!auth.ok) return res.status(auth.status).json({ error: auth.error });
  try {
    const file = await createDriveBackup();
    return res.status(201).json({ backed_up: true, file_id: file.id, file_name: file.name });
  } catch (error) {
    return res.status(503).json({ backed_up: false, error: String(error.message || "Backup unavailable") });
  }
};