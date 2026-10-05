import os
import json
import telebot
import shutil
from datetime import datetime

# GitHub Secrets থেকে ডাটা নেওয়া হচ্ছে
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TOKEN or not ADMIN_CHAT_ID:
    print("ভুল: TELEGRAM_BOT_TOKEN বা TELEGRAM_CHAT_ID সেট করা নাই!")
    exit(1)

bot = telebot.TeleBot(TOKEN)

def start_automation():
    print("🚀 গিটহাব অটোমেশন টাস্ক শুরু হচ্ছে...")
    cur_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # ১. টেলিগ্রামে কাজ শুরুর নোটিফিকেশন পাঠানো
    try:
        bot.send_message(ADMIN_CHAT_ID, f"🚀 **GitHub Actions: নিউজ পোস্টের কাজ শুরু হয়েছে!**\n⏰ সময়: `{cur_time}`", parse_mode="Markdown")
    except Exception as e:
        print(f"টেলিগ্রামে মেসেজ পাঠানো যায়নি: {e}")

    # ২. আপনার মেইন পোস্টের ফাইলটি (যা ব্লগে পোস্ট করে এবং জিমিনি ব্যবহার করে) রান করা
    print("📦 ব্লগে পোস্ট দেওয়া হচ্ছে...")
    exit_code = os.system("python main.py")
    
    if exit_code == 0:
        bot.send_message(ADMIN_CHAT_ID, "✅ **আজকের নিউজ ব্লগে সফলভাবে পোস্ট করা হয়েছে বন্দু!**", parse_mode="Markdown")
    else:
        bot.send_message(ADMIN_CHAT_ID, f"⚠️ **ব্লগে পোস্ট দিতে সমস্যা হয়েছে! এক্সিট কোড:** `{exit_code}`", parse_mode="Markdown")

    # ৩. ডাটাবেজ (posted.json) ও কোড অটো-ব্যাকআপ নেওয়া
    print("⏳ ফাইলের ব্যকআপ নেওয়া হচ্ছে...")
    try:
        cur_date = datetime.now().strftime('%Y-%m-%d')
        
        # posted.json ব্যাকআপ পাঠানো
        if os.path.exists('posted.json'):
            with open('posted.json', 'rb') as f:
                bot.send_document(ADMIN_CHAT_ID, f, caption=f"📦 posted.json অটো-ব্যাকআপ ({cur_date})")
        
        # আপনার মেইন পোস্ট ফাইলের ব্যাকআপ পাঠানো
        if os.path.exists('main.py'):
            with open('main.py', 'rb') as f:
                bot.send_document(ADMIN_CHAT_ID, f, caption=f"📄 main.py ব্যাকআপ ({cur_date})")
                
        bot.send_message(ADMIN_CHAT_ID, "✅ **সব ফাইলের ব্যাকআপ তোমার টেলিগ্রামে পাঠিয়ে দেওয়া হয়েছে।**", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(ADMIN_CHAT_ID, f"❌ **ব্যাকআপ ফাইল পাঠানো ব্যর্থ হয়েছে:** `{e}`", parse_mode="Markdown")
    
    print("✅ গিটহাবের আজকের শিডিউলের কাজ শেষ!")

if __name__ == "__main__":
    start_automation()
