# app/llm_client.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("LLM_API_KEY", "")
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def generate_text(prompt: str, system_prompt: str = "You are an expert recruiter.") -> str:
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}

    data = {
        "contents": [
            {"role": "user", "parts": [{"text": f"{system_prompt}\n\n{prompt}"}]}
        ]
    }

    response = requests.post(GEMINI_ENDPOINT, headers=headers, params=params, json=data, timeout=30)
    if response.status_code != 200:
        print("Gemini API Error:", response.text)
        response.raise_for_status()

    result = response.json()
    return result["candidates"][0]["content"]["parts"][0]["text"]
