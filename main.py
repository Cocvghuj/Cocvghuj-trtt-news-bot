import os
import random
import requests
import google.generativeai as genai

def main():
    # এনভায়রনমেন্ট ভেরিয়েবল থেকে API কী (API Key) সংগ্রহ করা
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    
    # জেমিনাই কনফিগার করা
    genai.configure(api_key=api_key)
    
    # এই লাইব্রেরি ভার্সনের জন্য পরীক্ষিত এবং সমর্থিত মডেল নাম (gemini-pro)
    model = genai.GenerativeModel("gemini-pro")
    
    # আপনার নিউজের জন্য প্রয়োজনীয় প্রম্পট
    prompt = "Write a short and engaging news update for trttnews24bd."
    
    # কন্টেন্ট জেনারেট করা
    response = model.generate_content(prompt)
    
    print("Response generated successfully:")
    print(response.text)

if __name__ == "__main__":
    main()
