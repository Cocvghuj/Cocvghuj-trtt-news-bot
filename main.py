import os
import google.generativeai as genai

def ensure_public_guides_dir():
    os.makedirs("public/guides", exist_ok=True)

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")

    ensure_public_guides_dir()

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = "Write a short and engaging news update for trttnews24bd."

    try:
        response = model.generate_content(prompt)
        print("Response generated successfully:")
        print(getattr(response, "text", "No response text returned."))
    except Exception as exc:
        print(f"Error generating content with gemini-2.0-flash: {exc}")

if __name__ == "__main__":
    main()
