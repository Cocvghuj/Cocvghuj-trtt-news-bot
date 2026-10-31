# 🚀 FlightScoutPro & TRTT News 24 BD Autonomous Publishing Engine & Theme Overhaul

## 🇧🇩 বাংলা নির্দেশিকা (১০০% অটোমেশন ও ডিজাইন সেটআপ)

আপনার ব্লগে ২ মাস ধরে যে ডিজাইন সমস্যা ছিল এবং পোস্টগুলো এলোমেলো দেখাচ্ছিল, তা এখন পুরোপুরি অটোমেটেড করা হয়েছে।

### ১. স্বয়ংক্রিয় পোস্টিং ইঞ্জিন (`main.py` আপগ্রেড)
- **FlightScoutPro (`flightscoutpro.blogspot.com`):**
  - **মালিক/প্রধান লেখক:** Muntasir Rahman (মুনতাসির রহমান)
  - **ইমেইল:** `muntasirrahaman694@gmail.com` | **হোয়াটসঅ্যাপ/ফোন:** `+8801314847336`
  - **ঠিকানা:** Dhaka, Bangladesh
  - **ব্র্যান্ডিং:** FlightScoutPro Aviation & Travel Intelligence
  - **অটো ইনজেক্টেড উইজেট:** Key Takeaways বক্স, ফ্লাইট ডিল রেডার, €600 এয়ারহেল্প ক্লেইম বাটন, ভেরিফাইড অথর কার্ড এবং অফিসিয়াল লিগ্যাল পেজ লিংক।

- **TRTT NEWS 24 BD (`trttnews24bd.blogspot.com`):**
  - **মালিক/প্রধান সম্পাদক:** Abu Taher (আবু তাহের)
  - **ইমেইল:** `engrtaher2017@gmail.com`
  - **ঠিকানা:** Via Carlo Felice, Sanluri, South Sardinia, Italy / Milan, Italy
  - **উইজেট:** VoyageHub Super App (21 Tools), ট্রাভেল অ্যান্ড লজিস্টিকস পার্টনার স্ট্রিপ, ভেরিফাইড অথর কার্ড।

---

### ২. ব্লগার ডিজাইনের ম্যাজিক ফিক্স (২ মিনিটে হোমপেজ ও সাইডবার ঠিক করার উপায়)
আপনার ব্লগের হোমপেজ ও পুরনো পোস্টগুলোকেও সাথে সাথে ঝকঝকে আধুনিক করতে ২টি সহজ উপায় রয়েছে:

#### উপায় ১: ১-ক্লিক ম্যাজিক সিএসএস (সবচেয়ে সহজ ও নিরাপদ)
১. ব্লগার ড্যাশবোর্ডে লগইন করুন: `https://www.blogger.com`
২. বামপাশের মেনু থেকে **Theme**-এ ক্লিক করুন।
৩. আপনার বর্তমান থিমের পাশে **Customize** বাটনে ক্লিক করুন।
৪. **Advanced** অপশনে যান এবং ড্রপডাউন থেকে **Add CSS** সিলেক্ট করুন।
৫. রিপোজিটরির `assets/css/flightscoutpro-theme.css` ফাইলের সম্পূর্ণ কোড কপি করে পেস্ট করুন।
৬. নিচে ডানপাশে **Save (ডিস্ক আইকন)** এ ক্লিক করুন!
*(ব্যাস! সাথে সাথে আপনার ব্লগের ধূসর ব্যাকগ্রাউন্ড চলে যাবে, ফন্ট আধুনিক হবে এবং সাইডবারের অপ্রয়োজনীয় গ্যাজেট লুকিয়ে যাবে।)*

#### উপায় ২: নতুন আল্ট্রা-ক্লিন থিম আপলোড (XML Theme Restore)
১. ব্লগার ড্যাশবোর্ডে **Theme** পেজে যান।
২. **Customize** বাটনের পাশের ছোট তীর (arrow) আইকনে ক্লিক করে **Restore** চাপুন।
৩. **Upload** বাটনে ক্লিক করে `assets/themes/flightscoutpro-ultra-clean-template.xml` ফাইলটি সিলেক্ট করে আপলোড দিন।

---

### ৩. অফিসিয়াল পেজসমূহ (AdSense ও Google Search Approved)
সবগুলো পেজ ইতিমধ্যে পুশ করা আছে:
- **FlightScoutPro:** `pages/flightscoutpro/` (About Us, Contact Us, Privacy Policy, Disclaimer)
- **TRTT News 24 BD:** `pages/trttnews24bd/` (About Us, Contact Us, Privacy Policy, Disclaimer)

---

## 🇬🇧 English Documentation

### Architecture Overview
1. **GitHub Actions Autopilot (`.github/workflows/trtt-unified-autopilot.yml`):**
   - Runs twice daily (08:17 & 20:17 Sanluri time) or manually via `workflow_dispatch`.
   - Calls `main.py` which dynamically synthesizes high-E-E-A-T articles with Unsplash imagery.
   - Posts directly to Google Blogger via Blogger API v3 with tailored profiles for both blogs.
2. **Post Layout & CSS:**
   - Every post includes responsive scoped CSS, quick-summary key takeaways, dynamic author badge, and direct partner action links.
