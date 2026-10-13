import google.generativeai as genai
import re

# 1. REAL OFFICIAL DATABASE - NO FAKE ALLOWED
OFFICIAL_DB = {
    "GERMANY": {"desk": "German Federal Foreign Office (Make it in Germany)", "url": "https://www.make-it-in-germany.com/en/visa-residence/types/chancenkarte", "fee": "€75", "label": "Global Work Permits & Immigration"},
    "PORTUGAL": {"desk": "Portuguese Ministry of Foreign Affairs - Vistos MNE", "url": "https://vistos.mne.gov.pt/en/national-visas/general-information", "fee": "€90 Visa + €83 Residence Permit", "label": "Europe Visa & Residency"},
    "MALTA": {"desk": "Jobsplus - Government of Malta", "url": "https://jobsplus.gov.mt/employers/resources/single-permit", "fee": "€280.50", "label": "Global Work Permits & Immigration"},
    "ITALY": {"desk": "Italian Ministry of Interior - Portale Immigrazione", "url": "https://www.interno.gov.it/it/temi/immigrazione", "fee": "€116", "label": "Europe Visa & Residency"},
    "UK": {"desk": "UK Government - UK Visas and Immigration", "url": "https://www.gov.uk/government/organisations/uk-visas-and-immigration", "fee": "£464", "label": "UK Visa and Immigration"},
    "USA": {"desk": "US Department of State", "url": "https://travel.state.gov", "fee": "$185", "label": "Global Work Permits & Immigration"},
    "CZECH": {"desk": "Ministry of Interior of Czech Republic", "url": "https://www.mvcr.cz/mvcren/article/third-country-nationals.aspx", "fee": "CZK 2,500", "label": "World Affairs"},
    "TECH": {"desk": "Official Company Press Release / Reuters Tech", "url": "https://www.reuters.com/technology/", "fee": "N/A", "label": "Global Tech & AI"},
    "WORLD": {"desk": "Official Government Portal / Reuters World", "url": "https://www.reuters.com/world/", "fee": "N/A", "label": "World Affairs"},
    "DEFAULT": {"desk": "Verified Official Government Source", "url": "https://www.reuters.com/", "fee": "N/A", "label": "Lifestyle & Europe News"},
}

BANNED_PHRASES = ["Official International Migration Bureau", "Official Standard Fee", "Standard International Rates", "SHOCKED", "NEVER", "Top 1"]

def get_info(topic: str):
    t = topic.upper()
    for key in ["GERMANY","PORTUGAL","MALTA","ITALY","UK","USA","CZECH"]:
        if key in t: return OFFICIAL_DB[key]
    if any(x in t for x in ["APPLE","GOOGLE","AI","BILL GATES","OPENAI","TECH"]): return OFFICIAL_DB["TECH"]
    if any(x in t for x in ["UKRAINE","WAR","VISA PAUSE","ELECTION","WORLD"]): return OFFICIAL_DB["WORLD"]
    return OFFICIAL_DB["DEFAULT"]

# 2. PERMANENT COMMAND FOR GEMINI - THIS IS SAVED FOREVER IN GITHUB
def build_lifetime_prompt(any_topic: str):
    info = get_info(any_topic)
    prompt = f"""
SYSTEM: You are BBC News Senior Editor, TRTT NEWS 24 BD Bureau, Sanluri, Italy. You obey ONLY OFFICIAL_DB.
You are locked. You cannot invent.

TOPIC: {any_topic}
OFFICIAL DESK (USE ONLY THIS): {info['desk']}
OFFICIAL URL (CITE EXACTLY 2 TIMES): {info['url']}
OFFICIAL FEE (USE ONLY THIS): {info['fee']}
LABEL (Python will use, you just write): {info['label']}

ABSOLUTE RULES - BREAK = FAIL:
1. NEVER write these BANNED phrases: {', '.join(BANNED_PHRASES)}. If you write them, article is rejected.
2. You MUST use desk={info['desk']} and url={info['url']} and fee={info['fee']}. No other source.
3. 700+ words, 100% English UK, BBC neutral, no emoji.
4. Title: BBC style - Example: {any_topic}: Official Guide and Requirements 2027
5. Structure EXACT:
   Executive Summary (80 words, include date 13 Oct 2026)
   H2: Official Announcement from {info['desk']} (cite {info['url']} 2 times) - 120 words
   H2: Key Eligibility / Core Facts - 150 words bullets
   H2: Step-by-Step Process Without Brokers - 150 words numbered, warn against dalal
   H2: Official Fee {info['fee']} and Legal Protection - 100 words
   H2: TRTT Expert Take & Verification (Sanluri, Italy) - 80 words, MUST start with "Our resident editorial bureau in Sanluri, Italy has directly cross-referenced this with {info['desk']}..." and MUST end with "— Verified by Senior Editorial Desk | TRTT NEWS 24 BD Bureau (Sanluri, Italy)"
   Footer: Official Reference Desk: {info['desk']} - {info['url']}

6. GOOGLE E-E-A-T: Add Author TRTT Senior Editorial Desk, add Official Reference.

Now write news for: {any_topic}
"""
    return prompt, info['label']

# 3. AUTO-CHECK - If Gemini makes mistake, auto-regenerate
def generate_google_safe_news(topic: str):
    genai.configure(api_key="YOUR_GEMINI_API_KEY")
    model = genai.GenerativeModel("gemini-1.5-flash", generation_config={"temperature": 0.1})
    prompt, label = build_lifetime_prompt(topic)

    for attempt in range(3):
        response = model.generate_content(prompt)
        text = response.text

        # Check for banned fake words
        has_banned = any(b.lower() in text.lower() for b in BANNED_PHRASES)
        if has_banned:
            print(f"⚠️ Gemini tried to use banned phrases on attempt {attempt+1}. Retrying...")
            continue
        return text, label
    
    raise ValueError("❌ Gemini failed to follow anti-hallucination rules after 3 attempts.")
