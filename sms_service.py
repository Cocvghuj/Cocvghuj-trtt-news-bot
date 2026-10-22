import os
from twilio.rest import Client

def send_abandoned_cart_sms(phone, destination="FCO"):
    sid = os.getenv("TWILIO_ACCOUNT_SID")
    token = os.getenv("TWILIO_AUTH_TOKEN")
    from_phone = os.getenv("TWILIO_PHONE")
    
    client = Client(sid, token)
    body = f"বন্ধু, তোর {destination} ট্রিপের €7 ক্যাশব্যাক মিস করছিস! বুক কর TRTT Marker 787950 দিয়ে: https://cocvghuj.github.io/Cocvghuj-trtt-news-bot/?to={destination}"
    
    msg = client.messages.create(body=body, from_=from_phone, to=phone)
    print(f"✅ SMS সফলভাবে পাঠানো হয়েছে - ID: {msg.sid}")
    return msg.sid
