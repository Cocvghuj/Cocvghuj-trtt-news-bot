# 🇧🇩 TRTT NEWS 24 BD - Automated News Bot 🤖

> RSS to Facebook & Telegram & WhatsApp Auto Posting with AI Filter  
> **Founder in Milan, Italy | Future with Truth**

[![Python](https://img.shields.io/badge/Python-3.9-blue?style=flat&logo=python&logoColor=white)]()
[![Automation](https://img.shields.io/badge/GitHub-Actions-orange?style=flat&logo=githubactions&logoColor=white)]()
[![Platform](https://img.shields.io/badge/Blogger-News-success?style=flat&logo=blogger&logoColor=white)]()
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat)]()

---

## 💡 প্রযুক্তি ও কোডিং নিয়ে আমাদের ভাবনা
> *"কোডিং শুধু কম্পিউটারকে নির্দেশ দেওয়া নয়, কোডিং হলো নিজের কল্পনাশক্তিকে বাস্তবে রূপ দেওয়ার সবচেয়ে বড় হাতিয়ার।"*  

প্রযুক্তি কোনো জটিল বিষয় নয়—একটু পাইথন কোড আর সঠিক অটোমেশন জানা থাকলে পুরো পৃথিবীকে হাতের মুঠোয় নিয়ে আসা সম্ভব। এই প্রজেক্টটি তৈরি করা হয়েছে পাইথন, গিটহাব অ্যাকশন্স এবং এপিআই (API) ব্যবহার করে, যা মানুষের কষ্ট কমিয়ে মাত্র এক ক্লিকে পুরো নিউজ সিস্টেমকে সচল রাখে। আপনিও যদি কোডিং ভালোবাসেন, তবে ভয় দূর করে আজই কোড লেখা শুরু করুন!

---

### 🔥 এই বট কীভাবে কাজ করে?
এই বট `trttnews24bd.blogspot.com` থেকে নিয়মিত অটো নিউজ সংগ্রহ করে এবং শুধু মানুষের চাহিদাপূর্ণ ও গুরুত্বপূর্ণ খবরগুলো ফিল্টার করে স্বয়ংক্রিয়ভাবে প্রকাশ করে।

**প্রধান বৈশিষ্ট্যসমূহ (Features):**
- ✅ **Smart Filter:** শুধু জনপ্রিয় ক্যাটাগরি (ব্রেকিং, চাকরি, নিয়োগ, ফলাফল, টেক, এআই, আবহাওয়া, বাজারদর) ফিল্টার করে পোস্ট করে।
- ✅ **Multi-Platform:** এক ক্লিকে Facebook Page + Telegram Channel + WhatsApp Channel এ আপডেট পাঠিয়ে দেয়।
- ✅ **Auto Comment:** ফেসবুক পোস্টে স্বয়ংক্রিয়ভাবে ওয়েবসাইটের লিংকসহ কমেন্ট যুক্ত করে।
- ✅ **Auto Image:** ব্লগের ছবি অটো ডিটেক্ট করে HD কোয়ালিটিতে পোস্ট করে।
- ✅ **Spam Protection:** দিনে সর্বোচ্চ ৮টি পোস্ট এবং `posted.json` দিয়ে ডুপ্লিকেট চেক নিশ্চিত করে।
- ✅ **GitHub Actions:** ১০০% ফ্রি ক্লাউড অটোমেশন, আলাদা কোনো সার্ভারের প্রয়োজন হয় না।

---

### ⚙️ টেকনিক্যাল কার্যপদ্ধতি (How It Works)
1. `RSS Feed` -> `get_news()` -> ব্লগ থেকে লেটেস্ট খবরগুলো সংগ্রহ করে।
2. `is_high_demand_news()` -> খবরের শিরোনাম ও বিবরণ চেক করে ভাইরাল বা জরুরি কিনা যাচাই করে।
3. `post_to_telegram()` & `post_all()` -> টেলিগ্রাম এবং ফেসবুক পেজে স্বয়ংক্রিয়ভাবে পোস্ট ও অটো কমেন্ট করে।
4. `save_posted()` -> লিংকটি সেভ করে রাখে যাতে পরবর্তীতে ডুপ্লিকেট পোস্ট না হয়।

---

### 🤖 এআই ও প্রযুক্তি নিয়ে আমার নিজস্ব দৃষ্টিভঙ্গি (AI & Tech Perspective)
> *"ভবিষ্যতের দুনিয়ায় সেই এগিয়ে থাকবে, যে কোডিং এবং কৃত্রিম বুদ্ধিমত্তাকে (AI) নিজের কাজের সহায়ক শক্তি হিসেবে ব্যবহার করতে জানে।"*  

একজন এআই (AI) হিসেবে আমার বিশ্বাস—প্রযুক্তির আসল সৌন্দর্য লুকিয়ে আছে অটোমেশনের মধ্যে। মানুষ যখন ঘুমিয়ে থাকে বা নিজের সৃজনশীল অন্য কোনো কাজে ব্যস্ত থাকে, তখন একটি সুবিন্যস্ত কোড বা বট নিখুঁতভাবে ব্যাকগ্রাউন্ডে কাজ করে যেতে পারে। 

TRTT NEWS 24 BD প্রজেক্টটি শুধু কিছু কোডের সমষ্টি নয়; এটি হলো চিন্তা এবং প্রযুক্তির এমন এক মেলবন্ধন, যা প্রমাণ করে যে ইচ্ছা থাকলে একজন একা মানুষও গিটহাব ও পাইথনের সাহায্যে একটি পূর্ণাঙ্গ মিডিয়া প্ল্যাটফর্ম বা অটোমেটেড নিউজ নেটওয়ার্ক চালিয়ে নিতে পারে। কোডিংকে ভয় না পেয়ে একে নিজের বন্ধু বানিয়ে নিন, দেখবেন অসম্ভব বলে কিছু আর থাকবে না!

---

### 🔗 Connected Channels & Links
- 🌐 **Blogger:** [trttnews24bd.blogspot.com](https://trttnews24bd.blogspot.com)
- 📘 **Facebook Page:** [fb.com/trttnews24bd](https://facebook.com/trttnews24bd)
- ✈️ **Telegram:** [t.me/trttnews24bd](https://t.me/trttnews24bd)
- 📲 **WhatsApp Channel:** [Join WhatsApp](https://whatsapp.com/channel/0029Vb8co9VDeONEz0B5e51M)

---

### 🚀 Setup Environment Secrets
গিটহাব রিপোজিটরির Settings -> Secrets and variables -> Actions এ নিচের সিক্রেটগুলো যুক্ত করতে হবে:
- `FB_PAGE_ID`
- `FB_PAGE_ACCESS_TOKEN`
- `FB_USER_ACCESS_TOKEN`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHANNEL_ID`

---
<p align="center">
  <b>Made with ❤ in Milan, Italy for Bangladesh | TRTT NEWS 24 BD</b><br>
  <sub>#TRTTNEWS #BanglaNews #BreakingNews #Automation #PythonCoding #AI #FutureTech</sub>
</p>
