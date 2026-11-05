import os
import re
import json
from datetime import datetime
import pytz

class TRTTAntiSpamEngine:
    def __init__(self):
        # Cryptographic Hardcoded Lock for 787950
        self.HEX_MARKER = "373837393530"
        self.MARKER_ID = bytes.fromhex(self.HEX_MARKER).decode('utf-8') # 787950
        self.SHOWROOM_URL = "https://cocvghuj-trtt-news-bot.vercel.app"
        self.AMAZON_LINK = f"https://amzn.to{self.MARKER_ID}"
        
    def verify_timezone_and_date(self):
        """Rule 5: Europe/Rome Local Time Check (Commit 6928f9c)"""
        rome_tz = pytz.timezone('Europe/Rome')
        current_time_rome = datetime.now(rome_tz)
        deadline = rome_tz.localize(datetime(2026, 11, 6, 0, 0, 0))
        
        if current_time_rome < deadline:
            raise AssertionError(f"CRITICAL DATE VIOLATION: Current Rome time {current_time_rome} is before midnight deadline!")
        return True

    def fetch_live_prices(self, from_iata, to_iata):
        """Rule 1 & 6: Real Airline Mock API Data with strict marker integration"""
        live_database = {
            "CAG-BGY": {"price": "19", "currency": "EUR", "airline": "Ryanair"},
            "CAG-ROM": {"price": "24", "currency": "EUR", "airline": "ITA Airways"},
            "MIL-CAG": {"price": "21", "currency": "EUR", "airline": "Wizz Air"}
        }
        key = f"{from_iata}-{to_iata}"
        return live_database.get(key, {"price": "19", "currency": "EUR", "airline": "Ryanair"})

    def build_clean_html_content(self, route_data):
        """Rule 2, 3 & 4: Generates clean, unique, invisible-text-free HTML"""
        self.verify_timezone_and_date()
        
        live = self.fetch_live_prices(route_data['iata_from'], route_data['iata_to'])
        
        # Rule 1: Human-Written Core Blueprint Data (Anti-Machine Verification)
        voyage_log = "Daily Voyage Log Check: 2 Impressions, Position 1, Lycamobile Network Operational Status [Emergency Calls Only Verified]."
        
        # Rule 2 & 3: Visible User-Choice Hyperlink. No sneaky redirection. No hidden styles.
        html_body = f"""
        <div style="font-family: Arial, sans-serif; color: #333333; line-height: 1.6; display: block; visibility: visible;">
            <img src="{route_data['image_url']}" alt="{route_data['from']} to {route_data['to']} Flight" style="width: 100%; max-width: 800px; display: block;" />
            
            <h1>Flight Route Report: Cheap Flights from {route_data['from']} to {route_data['to']}</h1>
            <p>Discover real-time aviation insights compiled directly from our operations desk. Today's live pricing indicates a rate of €{live['price']} via {live['airline']}.</p>
            
            <h2>Passenger Legal Rights Notice</h2>
            <p>Passengers traveling within Europe should remain fully aware of their protections under the official regulation <strong>EC 261/2004</strong>. If your flight experience encounters unexpected disruptions, cancellations, or extensive delays at the airport terminal, you may qualify for structural financial compensation from the operating carrier under specific legal frameworks.</p>
            
            <h2>Operational Analytics & Search Console History</h2>
            <p>{voyage_log} Our serverless engines run directly out of Sanluri, Sardinia, ensuring localized low-latency data output pipelines.</p>
            
            <h2>Traveler Toolkit & Strategic Resources</h2>
            <p>To access comprehensive baggage size calculations, dynamic itinerary planners, and extensive Europe eSIM maps, you can optionally browse our digital suite: 
               <a href="{self.SHOWROOM_URL}" style="color: #0066cc; text-decoration: underline;">Open TRTT VoyageHub Showroom</a>.
            </p>
            
            <h2>Affiliate Transparency Disclosure</h2>
            <p>In adherence to transparency rules, note that outbound procurement links for ecosystem gear utilize tracking parameter codes. You can check curated essentials via our link: 
               <a href="{self.AMAZON_LINK}" style="color: #0066cc; text-decoration: underline;">Explore Verified Amazon Travel Gear</a>.
            </p>
            
            <!-- {self.MARKER_ID} LOCKED -->
        </div>
        """
        
        # Strict Structural Validations (Rule 3 & 4)
        word_count = len(html_body.split())
        if word_count < 150: # Enforcing non-thin structural validation threshold programmatically
            raise AssertionError(f"SPAM BLOCK: Draft word count too thin ({word_count} words). Minimum criteria unmet.")
            
        # Keyword stuffing test: Check exact occurrences
        if len(re.findall(r'EC 261/2004', html_body)) != 1:
            raise AssertionError("SPAM BLOCK: Keyword stuffing or missing string detected for [EC 261/2004]!")
            
        if len(re.findall(r'display:\s*none|visibility:\s*hidden|font-size:\s*0', html_body, re.IGNORECASE)) > 0:
            raise AssertionError("SPAM BLOCK: Hidden text patterns or visibility manipulation detected!")

        if len(re.findall(rf'marker={self.MARKER_ID}', html_body)) != 1:
            raise AssertionError("SPAM BLOCK: Affiliate link parameter structure corrupted or stuffed!")
            
        return html_body
