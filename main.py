import os
import random
import requests
import google.generativeai as genai

def main():
    # এনভায়রনমেন্ট ভेरিয়েবল থেকে API কী (API Key) সংগ্রহ করা
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    
    # জেমিনাই কনফিগার করা
    genai.configure(api_key=api_key)
    
    # বর্তমান সচল মডেল ব্যবহার করা (কোনো পুরোনো বা ভুল নাম রাখা হয়নি)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # আপনার নিউজের জন্য প্রয়োজনীয় প্রম্পট
    prompt = "Write a short and engaging news update for trttnews24bd."
    
    # কন্টেন্ট জেনারেট করা
    response = model.generate_content(prompt)
    
    print("Response generated successfully:")
    print(response.text)

if __name__ == "__main__":
    main()
