import requests

LLAMA_API_URL = "http://llama:8001/generate"

def generate(prompt: str) -> str:
    try:
        response = requests.post(LLAMA_API_URL, json={"prompt": prompt}, timeout=30)
        return response.json().get("response", "[No response]")
    except Exception as e:
        return f"[TinyLLaMA Container ERROR] {str(e)}"
