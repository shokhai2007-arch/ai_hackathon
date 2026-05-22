import os
import httpx

GEMINI_MODEL = "gemini-1.5-flash"
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{GEMINI_MODEL}:generateContent"
)


def ask_gemini(context: str, message: str) -> str:
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("API key not configured on server")

    full_prompt = f"{context}\n\nFoydalanuvchi savoli: {message}\n\nJavob:"

    with httpx.Client(timeout=60) as client:
        resp = client.post(
            f"{GEMINI_URL}?key={api_key}",
            json={'contents': [{'parts': [{'text': full_prompt}]}]}
        )
        result = resp.json()

    if 'candidates' in result and len(result['candidates']) > 0:
        return result['candidates'][0]['content']['parts'][0]['text']

    raise Exception(f"AI response failed: {result}")
