# FlightScout Pro — Blogger Design Handoff

This is a separate student-led aviation publication owned by its own operator. It intentionally does not reuse TRTT's brand palette or Roksana Nila Vault.

## Design identity
- Brand: FlightScout Pro
- Positioning: Aviation & Flight Intelligence
- Palette: deep aviation navy, sky blue, cyan and runway orange
- Navigation: Home, Flight Search, Flight Deals, Passenger Rights, Airport & Transit, Travel Guides, eSIM & Connectivity, About, Contact
- Layout: responsive, readable editorial cards; accessible focus states; mobile-first spacing.

## Files
- `assets/css/flightscoutpro-theme.css` — complete Blogger styling layer.
- `flightscoutpro-control.json` — menu labels and destinations.
- `flightscoutpro-menu.js` — responsive menu loader.
- `assets/themes/flightscoutpro-ultra-clean-template.xml` — optional legacy standalone theme; do not upload it as part of this change.

## Connect the menu to Blogger (one-time step)
A GitHub push updates repository files and can create a Vercel Preview, but Blogger does not automatically read new files unless its Layout already contains a loader. To connect the new menu:
1. Open the FlightScout Pro Blogger dashboard.
2. Go to **Layout** → **Add a Gadget** → **HTML/JavaScript**.
3. Add this one line and save:
   `<script src="https://cocvghuj-trtt-news-bot.vercel.app/flightscoutpro-menu.js" defer></script>`
4. The loader fetches the menu configuration and CSS from the same Vercel project. No Blogger Theme XML replacement is required.

## Safety
- Existing posts and page URLs are preserved.
- Existing About, Contact, Privacy and Disclaimer pages are retained.
- No API keys, account credentials, or private contact details are added to the public menu configuration.
- No Blogger publishing action or Vercel production deployment is triggered by this repository change.
