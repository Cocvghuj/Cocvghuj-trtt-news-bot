import os
import google.generativeai as genai
import requests

# 1. Groq & Gemini Dual Fallback Execution
def generate_safe_news_with_fallback(topic: str, prompt: str):
    # প্রথমে Gemini দিয়ে চেষ্টা করা যাক
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        try:
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-1.5-flash", generation_config={"temperature": 0.1})
            response = model.generate_content(prompt)
            if response and response.text:
                print("✅ Generated successfully using Gemini AI.")
                return response.text
        except Exception as e:
            print(f"⚠️ Gemini Failed: {e}. Switching to Groq fallback...")

    # যদি Gemini ফেইল করে, তবে Groq (Llama-3) দিয়ে জেনারেট করবে
    groq_key = os.environ.get("GROQ_API_KEY")
    if groq_key:
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {groq_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1
            }
            r = requests.post(url, json=payload, headers=headers, timeout=60)
            if r.status_code == 200:
                res_json = r.json()
                text = res_json['choices'][0]['message']['content']
                print("✅ Generated successfully using Groq (Llama-3) Fallback.")
                return text
        except Exception as e:
            print(f"⚠️ Groq Fallback Failed: {e}")

    raise ValueError("❌ Both Gemini and Groq APIs failed to generate content.")
