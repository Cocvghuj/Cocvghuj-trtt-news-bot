import os
import traceback

import google.generativeai as genai

MARKER = "787950"
MODEL_CANDIDATES = ["gemini-1.5-pro", "gemini-1.0-pro", "gemini-pro"]


def ensure_public_guides_dir():
    os.makedirs("public/guides", exist_ok=True)


def generate_prompt():
    return (
        "Write a short, engaging, and search-friendly travel update for a Europe-focused "
        "travel website. Keep it factual, useful, and conversion-friendly. Mention smart "
        "trip planning, budget travel, and affiliate-ready recommendations for Europe."
    )


def generate_content_with_fallback(prompt: str):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)
    last_error = None

    for model_name in MODEL_CANDIDATES:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            text = getattr(response, "text", None)
            if text:
                return {"model": model_name, "text": text}
            text = str(response)
            if text and text != "None":
                return {"model": model_name, "text": text}
        except Exception as exc:
            last_error = exc
            print(f"Model {model_name} failed: {exc}")
            continue

    raise RuntimeError(f"All Gemini models failed. Last error: {last_error}")


def main():
    ensure_public_guides_dir()
    try:
        output = generate_content_with_fallback(generate_prompt())
        print(f"Response generated successfully with model: {output['model']}")
        print(output["text"])
    except Exception as exc:
        print(f"Error generating content: {exc}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
