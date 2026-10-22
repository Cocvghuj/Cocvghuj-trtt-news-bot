import os, random, requests, smtplib, traceback
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- SECURE CONFIGURATION ---
MARKER = os.environ.get("TRAVEL_PAYOUT_MARKER", "787950")
AMAZON = os.environ.get("AMAZON_LINK", "https://amzn.to/4shg6Hn")

BLOGGER_BLOG_ID = os.environ.get("BLOGGER_BLOG_ID")
BLOGGER_CLIENT_ID = os.environ.get("BLOGGER_CLIENT_ID")
BLOGGER_CLIENT_SECRET = os.environ.get("BLOGGER_CLIENT_SECRET")
BLOGGER_REFRESH_TOKEN = os.environ.get("BLOGGER_REFRESH_TOKEN")

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
GMAIL_EMAIL = os.environ.get("GMAIL_EMAIL")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")
CUSTOMER_EMAILS = os.environ.get("CUSTOMER_EMAILS", "")

# --- DYNAMIC CONTENT DATABASE ---
TOPICS = [
    {
        "title": "Building a Remote Travel Consulting Business in Europe",
        "cat": "BUSINESS & FREEDOM",
        "subtitle": "Turn your travel passion into a high-paying remote consulting practice across EU hubs.",
        "read_time": "6 min read",
        "highlights": [
            "Setting up your digital nomad tax residency in Portugal or Spain",
            "Essential SaaS tools for remote itinerary planning",
            "Monetizing specialized European travel routes in 2026"
        ]
    },
    {
        "title": "Schengen Travel Blueprint: Low-Cost Routes & Smart Planning",
        "cat": "DESTINATION GUIDE",
        "subtitle": "Discover budget-friendly train routes, hiddenআপনার বর্তমান কোডটিকে সম্পূর্ণ **আধুনিক, আন্তর্জাতিক মানের প্রফেশনাল আর্কিটেকচারে (Enterprise/Modular standard)** রূপান্তর করা হয়েছে। 

পুরোনো ইনলাইন স্টাইল, মনোলিথিক স্ট্রাকচার এবং প্লেইন ডিজাইনের পরিবর্তন করে এতে **Jinja2 টেমপ্লেটিং, মডুলার আর্কিটেকচার, ডাইনামিক ডেটা ফিল্টারিং এবং মডার্ন কালার প্যালেট (Tailwind-inspired)** ব্যবহার করা হয়েছে, যা যেকোনো ট্রাভেলারের চোখে বিশ্বস্ততা ও আকর্ষণ তৈরি করবে।

---

## 🛠️ আর্কিটেকচার পুনর্গঠন (Project Structure)

আপনার পুরো প্রজেক্টকে ১টি ফাইলের বদলে ৩টি প্রফেশনাল ফাইলে ভাগ করে দেয়া হলো:

```text
├── config.py             # সমস্ত কনফিগারেশন, এনভায়রনমেন্ট ভেরিয়েবল ও অ্যাফিলিয়েট লিংক
├── email_service.py      # আধুনিক ট্রানজেকশনাল ইমেইল সার্ভিস মডিউল
└── main.py               # মূল এক্সিকিউশন ও সার্ভিস ইন্টিগ্রেশন ফাইল
