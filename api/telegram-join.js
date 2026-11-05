// TRTT Vercel API: public Telegram channel information only.
module.exports = function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "GET") return res.status(405).json({ success: false, error: "Method not allowed" });
  return res.status(200).json({
    success: true,
    channel: "t.me/trttnews24bd",
    url: "https://t.me/trttnews24bd",
    status: "Active"
  });
};
