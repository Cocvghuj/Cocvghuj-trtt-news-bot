// Sample endpoint only; it does not query live fares.
module.exports = function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "GET") return res.status(405).json({ success: false, error: "Method not allowed" });
  const query = req.query || {};
  const from = String(query.from || "JFK");
  const to = String(query.to || "ROM");
  return res.status(200).json({
    success: true,
    dataMode: "sample",
    liveAvailability: false,
    from,
    to,
    samplePrice: "$549",
    currency: "USD",
    message: "Illustrative sample only. Check the flight-search page for current options."
  });
};