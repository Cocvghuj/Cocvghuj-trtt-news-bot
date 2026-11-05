// General information endpoint only; not a personalised visa eligibility decision.
module.exports = function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "GET") return res.status(405).json({ success: false, error: "Method not allowed" });
  const query = req.query || {};
  return res.status(200).json({
    success: true,
    dataMode: "general-information",
    verifiedForTraveller: false,
    destination: String(query.country || "Italy"),
    nationality: query.nationality ? String(query.nationality) : null,
    message: "Visa requirements depend on passport nationality, residence status, purpose and dates. Confirm with the destination's official immigration authority before travel."
  });
};