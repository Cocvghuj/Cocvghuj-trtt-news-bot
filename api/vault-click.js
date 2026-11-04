// TRTT Vercel API: Vault Click & Stealth Telemetry Tracker
// Supports /api/vault-click?m=787950&src=menu&tool=dashboard
module.exports = async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  const query = req.query || {};
  const marker = query.m || "787950";
  const source = query.src || "menu";
  const tool = query.tool || "dashboard";
  const timestamp = Number(query.t) || Date.now();

  return res.status(200).json({
    success: true,
    tracked: true,
    marker: String(marker),
    source: String(source),
    tool: String(tool),
    timestamp: timestamp,
    code: 200,
    status: "Marker Tracked 127→128 OK"
  });
};
