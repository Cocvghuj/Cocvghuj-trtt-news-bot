// TRTT Vercel API: Flight Tracker
// Supports /api/flight-tracker?m=787950&from=JFK&to=ROM
module.exports = async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  const query = req.query || {};
  const from = query.from || "JFK";
  const to = query.to || "ROM";
  const marker = query.m || "787950";

  return res.status(200).json({
    success: true,
    route: `${from} → ${to}`,
    from: String(from),
    to: String(to),
    price: "$549",
    currency: "USD",
    airline: "Biman Bangladesh / ITA Airways",
    marker: String(marker),
    affiliateUrl: `https://aviasales.tp.st/Fb8U9yav?marker=${marker}&sub_id=flight_tracker_${from}_${to}`,
    badge: "Best Price",
    status: "Best Price Available",
    updatedAt: new Date().toISOString()
  });
};
