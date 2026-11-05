// Lightweight event acknowledgement endpoint. Events are not persisted.
module.exports = function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  res.setHeader("Cache-Control", "no-store");
  if (req.method === "OPTIONS") return res.status(204).end();
  if (req.method !== "GET") return res.status(405).json({ success: false, error: "Method not allowed" });

  const query = req.query || {};
  return res.status(200).json({
    success: true,
    accepted: true,
    persisted: false,
    marker: String(query.m || ""),
    source: String(query.src || "menu"),
    tool: String(query.tool || "menu"),
    timestamp: Number(query.t) || Date.now(),
    message: "Request accepted; persistent analytics storage is not configured."
  });
};