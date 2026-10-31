body: JSON.stringify({
  model: "nvidia/nemotron-3.5-super-35b-vl:free",
  messages: [
    {
      role: "system",
      content: "You are TRTT Design Bot. You must output ONLY full HTML file with Tailwind CSS. No markdown. Marker 787950 locked."
    },
    {
      role: "user",
      content: `
TASK: PUSH DESIGN TO GITHUB

Create a complete index.html for https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/

REQUIREMENTS:
- Use Tailwind CSS CDN: https://cdn.tailwindcss.com
- Title: Cocvghuj TRTT News Bot - Sanluri Sardinia Live
- Hero: Roksana Boutique - Marker 787950 - Sanluri
- 3 product cards with Buy Now button linking to https://cocvghuj.github.io/
- SEO: meta description, alt tags, schema markup
- Footer: Last updated ${new Date().toISOString()} - Marker 787950
- Design: Modern, mobile responsive, gradient, Italian colors
- Push ready: Output must be full HTML from <!DOCTYPE html> to </html>

OUTPUT ONLY HTML, NO EXPLANATION.
`
    }
  ]
})
