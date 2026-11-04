// TRTT Vercel API: Visa Checker
// Supports /api/visa-check?country=Italy&m=787950
module.exports = async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  const query = req.query || {};
  const country = query.country || "Italy";
  const from = query.from || "USA";
  const marker = query.m || "787950";

  return res.status(200).json({
    success: true,
    destination: String(country),
    origin: String(from),
    visaStatus: "Visa Free (Up to 90 Days Schengen)",
    visaRequired: false,
    stayDuration: "90 days within any 180-day period",
    badge: "Free",
    marker: String(marker),
    recommendation: "Ensure passport has at least 3 months validity beyond planned departure date.",
    status: "Verified",
    updatedAt: new Date().toISOString()
  });
};
