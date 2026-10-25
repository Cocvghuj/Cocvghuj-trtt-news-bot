import random
import json
from datetime import datetime

def generate_reels_script():
    celebs = [
        {"name": "Rahim", "city": "Rome", "earn": 7, "product": "Hotel + Flight"},
        {"name": "Anjali", "city": "Milan", "earn": 5, "product": "Express Train"},
        {"name": "Priya", "city": "Naples", "earn": 7, "product": "Sony Camera"},
        {"name": "Sujit", "city": "Venice", "earn": 5, "product": "Travel Bag"}
    ]
    c = random.choice(celebs)
    reel_text = f"🎬 15sec Reel: \"{c['name']} earned €{c['earn']} in {c['city']} on {c['product']} - Marker 787950 - Link in Bio\""
    
    output = {
        "reel": reel_text,
        "celeb": c,
        "generated_at": datetime.utcnow().isoformat()
    }
    
    with open("latest_reel.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
        
    print(f"✅ REEL GENERATED:\n{reel_text}")
    return reel_text

if __name__ == "__main__":
    generate_reels_script()
