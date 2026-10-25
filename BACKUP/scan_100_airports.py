# MULTI-TRILLION REAL SCANNER - NO FAKE - Marker 787950
import os, requests, json, datetime
from pathlib import Path

# GitHub Secret থেকে Token নেবে - ফেক না!
AVIA_TOKEN = os.getenv("AVIASALES_TOKEN")  # Travelpayouts থেকে নেবে
MARKER = os.getenv("TRAVEL_MARKER", "787950")

AIRPORTS_100 = ["FCO","BGY","LIN","CAG","MXP","VCE","BLQ","NAP","DAC","JFK","LHR","CDG","BCN","DXB","IST"] # 100 টা তোমার লিস্ট

def real_price_scan(origin):
    """Real Aviasales API - No Fake"""
    if not AVIA_TOKEN:
        print("AVIASALES_TOKEN Secret নাই - GitHub Settings -> Secrets এ বসাও")
        return None
    
    # Travelpayouts Cheap Flights API - Real Price
    url = f"https://api.travelpayouts.com/v1/prices/cheap?origin={origin}&token={AVIA_TOKEN}&currency=EUR"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        if data.get("success") and data.get("data"):
            # First destination price
            for dest, flights in data["data"].items():
                for flight in flights.values():
                    return flight.get("price"), dest
    except Exception as e:
        print(f"Error {origin}: {e}")
    return None, None

def generate_real():
    results = {}
    for apt in AIRPORTS_100:
        price, dest = real_price_scan(apt)
        if price:
            results[apt] = {"price": price, "to": dest, "link": f"https://aviasales.tpo.lv/Fb8U9yav?marker={MARKER}&origin={apt}&destination={dest}"}
            print(f"REAL: {apt} -> {dest} = €{price}")
    
    Path("data").mkdir(exist_ok=True)
    with open("data/100_airports_REAL_787950.json","w") as f:
        json.dump({"date": str(datetime.datetime.now()), "real": True, "marker": MARKER, "prices": results}, f, indent=2)
    
    print(f"DONE: {len(results)} Real Prices - No Fake - Marker {MARKER}")

if __name__ == "__main__":
    generate_real()
