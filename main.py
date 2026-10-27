import os
import random
import requests
import google.generativeai as genai

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)
    
    # নির্দিষ্ট কোনো নাম না দিয়ে সরাসরি জেনারেটিভ মডেল কল করার নিরাপদ পদ্ধতি
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = "Write a short and engaging news update for trttnews24bd."
    
    # এপিআই ভার্সন ও মেথড ঠিক রেখে রিকোয়েস্ট পাঠানো
    response = model.generate_content(prompt)
    
    print("Response generated successfully:")
    print(response.text)

if __name__ == "__main__":
    main()
