// TRTT Vercel API: Telegram VIP Club Redirect Tracker
// Supports /api/telegram-join?m=787950
module.exports = async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  const query = req.query || {};
  const marker = query.m || "787950";

  return res.status(200).json({
    success: true,
    channel: "t.me/trttnews24bd",
    url: "https://t.me/trttnews24bd",
    marker: String(marker),
    memberBenefits: "Exclusive $99 Deals • Daily European Flight Alerts • 24/7 Transit Support",
    status: "Active"
  });
};
