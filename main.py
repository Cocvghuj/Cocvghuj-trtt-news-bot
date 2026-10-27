import os
import random
import requests
import google.generativeai as genai

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)
    
    # বর্তমান জেমিনাই লাইব্রেরির জন্য সঠিক স্টাইলের মডেল কল
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = "Write a short and engaging news update for trttnews24bd."
    
    response = model.generate_content(prompt)
    
    print("Response generated successfully:")
    print(response.text)

if __name__ == "__main__":
    main()
