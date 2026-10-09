import os
import json
from google.oauth2.credentials import Credentials

def get_blogger():
    # গিটহাব সিক্রেটস থেকে টোকেন ডেটা পড়া হচ্ছে
    s = os.environ.get("BLOGGER_TOKEN_JSON")
    
    # ১. ভেরিয়েবলটি খালি বা None কিনা তা চেক করা
    if s is None:
        print("Error: 'BLOGGER_TOKEN_JSON' এনভায়রনমেন্ট ভেরিয়েবলটি খুঁজে পাওয়া যায়নি।")
        print("অনুগ্রহ করে আপনার GitHub Repository Settings > Secrets-এ এটি সেট করুন।")
        return None
        
    # ২. ভেরিয়েবলটিতে কোনো ডেটা না থাকলে বা শুধু স্পেস থাকলে হ্যান্ডেল করা
    s_stripped = s.strip()
    if not s_stripped:
        print("Error: 'BLOGGER_TOKEN_JSON' সিক্রেটটি খালি (Empty) অবস্থায় আছে।")
        return None
        
    try:
        # ৩. ডেটা সঠিকভাবে JSON ডিকোড করা
        token_info = json.loads(s_stripped)
        
        # গুগল ক্রেডেনশিয়াল জেনারেট করা
        creds = Credentials.from_authorized_user_info(token_info)
        
        # এখানে আপনার সার্ভিসের বাকি কোড থাকবে (যেমন: service = build('blogger', 'v3', ...))
        # return service
        return creds # অথবা আপনার বর্তমান রিটার্ন স্টেটমেন্ট রাখুন
        
    except json.JSONDecodeError as e:
        # JSON ফরম্যাটে কোনো ভুল থাকলে এই ব্লকটি কাজ করবে
        print(f"Error: JSON ডিকোড করতে সমস্যা হয়েছে। আপনার সিক্রেটটি সঠিক JSON ফরম্যাটে নেই।")
        print(f"মূল ভুল: {e}")
        print(f"সিক্রেটের প্রথম ২০টি ক্যারেক্টার (পরীক্ষার জন্য): {s_stripped[:20]}")
        return None
