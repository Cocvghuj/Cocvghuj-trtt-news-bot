import os, shutil, re

# কোথা থেকে কোথায় যাবে
SRC_FOLDERS = ["BACKUP", "backup"]
DEST_BASE = "BACKUP"

# সুন্দর ক্যাটাগরি ম্যাপ
CATEGORIES = {
    "01_prompts": ["prompt", "mega"],
    "02_docs": ["doc", "security", "readme", "manifest", "sitemap", "robots"],
    "03_old-files/01_features": ["referral", "live-ticker", "voice-search", "pwa-push", "price-beat", "hidden-fees", "ai-itinerary", "ai-review", "celebrity", "offline", "panic-button"],
    "03_old-files/02_payments-loyalty": ["bkash", "group-split", "trtt-coin", "direct-host", "whatsapp"],
    "03_old-files/03_family-travel": ["fco-rome", "bergamo", "dhaka", "venice", "rome-bagsmart", "munich", "paris-kids", "london-airtag", "dubai-anker", "europe", "bd-chain"]
}

def get_category(filename):
    f = filename.lower()
    for cat, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw in f:
                return cat
    return "03_old-files/00_others"

def beautify_name(old_name):
    # PART-305-referral-leaderboard.html -> referral-leaderboard.html
    name = re.sub(r'^PART-\d+-', '', old_name)
    name = re.sub(r'^\d+-', '', name)
    name = name.replace('_', '-').lower()
    return name

for src in SRC_FOLDERS:
    if not os.path.exists(src):
        continue
    for file in os.listdir(src):
        if file.startswith('.'): continue
        if os.path.isdir(os.path.join(src, file)): continue
        if not file.endswith('.html') and not file.endswith('.md') and not file.endswith('.json'): continue
        
        cat = get_category(file)
        new_name = beautify_name(file)
        
        dest_dir = os.path.join(DEST_BASE, cat)
        os.makedirs(dest_dir, exist_ok=True)
        
        src_path = os.path.join(src, file)
        dest_path = os.path.join(dest_dir, new_name)
        
        if src_path != dest_path and os.path.exists(src_path):
            shutil.move(src_path, dest_path)
            print(f"Moved: {file} -> {cat}/{new_name}")

print("Done! All files categorized with beautiful names.")
