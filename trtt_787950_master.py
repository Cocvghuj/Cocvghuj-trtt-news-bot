# TRTT 500 Quality Master - Marker 787950 HIDDEN
import json, os, time

MARKER = os.getenv("TRAVEL_MARKER", "787950")  # Hidden - env থেকে
QUEUE_FILE = "news/queue/latest.json"
HISTORY_FILE = "drafted_history.txt"
BATCH_SIZE = 20  # Blogger safe - 50 না, 20
SLEEP_BETWEEN = 60  # 20 sec না, 60 sec - Blogger API safe

REAL_ROUTES = [
    "Dhaka to Rome", "Dhaka to Milan", "Chittagong to Rome",
    "Rome to Dhaka", "Milan to Dhaka", "Sanluri to Dhaka",
    "Cagliari to Rome", "Rome to Cagliari", "Milan to Cagliari",
    "Rome to Paris", "Paris to Rome", "Rome to London",
    # ... তোমার 380 টা real route এখানে - Origin0 না
]

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return set()
    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f)

def build_content(city):
    # Marker CONTENT এ নাই - শুধু API link এ
    # Ghost-SIM = eSIM logic - আলাদা function
    return f"""
    <h2>Live Travel Guide: {city}</h2>
    <div id="roksana-vault-flight" data-city="{city}"></div>
    <div id="ghost-esim" data-city="{city}"></div>
    <p>Last updated: 4 times daily - Live from TRTT</p>
    <script>
      // Flight API call with hidden marker will be injected by roksana-vault.js
      // eSIM price via Ghost Protocol
    </script>
    """

def run_batch():
    history = load_history()
    queue = json.load(open(QUEUE_FILE, 'r', encoding='utf-8')) if os.path.exists(QUEUE_FILE) else REAL_ROUTES
    
    done = 0
    for city in queue:
        if city in history: continue
        if done >= BATCH_SIZE: break
        
        content = build_content(city)
        print(f"[{done+1}] Drafting: {city} - Marker HIDDEN in API only")
        # blogger_post_draft(content)  # এখানে API call
        
        open(HISTORY_FILE, 'a', encoding='utf-8').write(city + "\n")
        done += 1
        time.sleep(SLEEP_BETWEEN)
    
    print(f"✅ Batch Done: {done}")

if __name__ == "__main__":
    run_batch()
