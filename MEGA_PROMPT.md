# 🚀 TRTT SUPER APP 2026 — MASTER ARCHITECTURE & SYSTEM SPECIFICATION
**Project Name:** TRTT Super App 2026 (EuroHub Voyage & Logistics)  
**Primary Affiliate Marker:** #787950 (Travelpayouts) & Amazon Tag: trtt-21  
**Target Architecture:** Single-File HTML5 Client-Side Web App (`index.html`) + GitHub Actions Serverless Cron  
**Primary Objective:** Deliver a Million-Dollar Travel Super App integrating Hotel/Flight Booking, Airport Ground Transport Control, Multi-Language Localizations, Cashback Verifications, and Social Proof (Celebrity Wall) without server dependencies.

---

## 1. PERSISTENCE & STORAGE GUARANTEE (ANTI-DATA LOSS)
- **Zero External Backend / Zero FileReader Blobs:** Eliminates client-side file reading and unsafe API crashes. Photos are handled purely via URL input strings (`<input type="url">`) or repository-relative image paths (`images/customers/...`).
- **localStorage Fallback Chain:**
  - `trtt_gmail`: Verification status flag (Default: `true`).
  - `trtt_pass`: Passport verification flag (Default: `true`).
  - `trtt_email`: Active user email.
  - `discount_code`: Uniquely generated discount voucher (`TRTT-VERIFIED-3OFF-XXXX`).
  - `trtt_verified_bookings`: Array of submitted cashback verification objects.
  - `trtt_airport_control`: Transport DB cache status.
  - `trtt_auto_lang`: System auto-detected language code.
- **30-Second Heartbeat Auto-Save:** Background `setInterval` executes state sync every 30,000ms, updating UI state indicators and outputting console telemetry: `"✅ 8 HOURS PROMO SAVED BY TEACHER META AI - WILL NOT DELETE"`.
- **Image Failure Resilience:** All `<img>` elements enforce an `onerror` fallback string pointing to `https://picsum.photos/seed/fallback/400/300`.

---

## 2. AIRPORT & TRANSPORT CONTROL HUB (LOGISTICS ENGINE)
Unlike standard booking platforms that only display distances, TRTT integrates a localized airport ground transport and connectivity matrix (`AIRPORTS_DB`):
- **FCO (Rome, Italy):** Leonardo Express Rail (32m, €14) | Terravision Bus (55m, €6) | TIM 5GB eSIM (€5)
- **MXP (Milan, Italy):** Malpensa Express (50m, €13) | Autostradale Bus (60m, €10) | Vodafone eSIM (€5)
- **NAP (Naples, Italy):** Alibus Airport Shuttle (€5) | Curreri Bus (€10) | Iliad eSIM (€5)
- **DAC (Dhaka, Bangladesh):** Express Rail (25m) | BRTC Shuttle Bus (€1) | Grameenphone 5GB eSIM (€3) | ~7,400 km Route Link to FCO
- **DEL (Delhi, India):** Airport Express Metro (€0.5) | DTC AC Bus (€1) | Jio 5G eSIM (€2)
- **CDG (Paris, France):** RER B Rail (35m, €11) | Roissybus (60m, €16) | Orange France eSIM (€6)

---

## 3. AWIN-STYLE GLOBAL AUTO-LANGUAGE SELECTOR
- **Detection Algorithm:** Examines `navigator.language` combined with client timezone (`Intl.DateTimeFormat().resolvedOptions().timeZone`).
  - Timezone matching `Dhaka` $\rightarrow$ Bengali (`bn`)
  - Timezone matching `Kolkata` $\rightarrow$ Hindi (`hi`)
  - Timezone matching `Rome` or `Milan` $\rightarrow$ Italian (`it`)
  - Default fallback $\rightarrow$ English (`en`)
- **Global Header UI:** Displays top banner `"Choose another country or region to see content specific to your location - Global"` with a real-time language dropdown selector that dynamically re-renders UI headings and search placeholders.

---

## 4. DISCOUNT VERIFICATION & CASHBACK ENGINE
- **Affiliate Integration:** Routes bookings through Travelpayouts marker `#787950` (Economybookings, Aviasales, Airalo) and Amazon Affiliate links (`trtt-21`).
- **Flow:**
  1. System checks `trtt_gmail` and `trtt_pass` status flags.
  2. Auto-generates unique discount voucher: `TRTT-VERIFIED-3OFF-XXXX`.
  3. User submits Booking ID / Amazon Order ID alongside a Screenshot Image URL.
  4. Submission pushes record into `trtt_verified_bookings` in `localStorage` marked as `Pending Admin Check via Marker 787950`.
  5. Entitles user to €3 (Travelpayouts) or €5–€7 (Amazon) manual cashback payout via PayPal/bKash.

---

## 5. INSTAGRAM-STYLE CELEBRITY WALL & GITHUB ACTIONS CRON
- **Social Proof Layout:** Dual-column Instagram-style cards with gradient borders.
  - **Left Card (Celebrity of the Day):** Seeded deterministically using current Julian date (`today.toordinal()`).
  - **Right Card (Celebrity of the Week):** Seeded using ISO calendar week number from top-liked customer list.
- **Root Repository Files:**
  - `customers.json`: Array of customer objects containing name, destination, booking type, product details, photo path, promo code, cashback amount, and likes.
  - `airports.json`: Database of airport ground transport metrics.
  - `celebrity.json`: JSON output containing selected daily and weekly celebrities.
  - `.github/workflows/celebrity.yml`: Daily automated Python script running at `0 0 * * *` UTC to generate `celebrity.json` and push updates via `TRTT Bot`.

---

## 6. BOOKING.COM PREMIUM UI REPLICATION
- **Color Palette:** Dark Navy (`#003580` / `#0f172a`), Accent Blue (`#006ce4`), and Highlight Yellow (`#ffb700`).
- **Core Visual Sections:**
  - **Explore Italy Grid:** City cards showing property counts and distance indicators (e.g., *Rome - 23,997 properties*, *Milan - 15,391 properties*).
  - **Quick & Easy Trip Planner:** Interactive category chips (*Shopping & Outlets*, *Markets*, *Road Trips*, *Festive*, *Art & Music*).
  - **Homes Guests Love:** Hotel cards featuring favorite icons, rating badges (e.g., *9.7 Exceptional*), review counts, and base pricing.
  - **Genius Loyalty Tier:** Banner highlighting Genius Level 1 benefits (10% property and car rental discounts).
  - **AI Recommendation Engine:** Interactive prompt field generating immediate itinerary breakdowns.
  - **Footer Links:** Replaces generic affiliate link with *"Become a TRTT Celebrity - Earn €3-€7 Cashback (Marker 787950)"*.
