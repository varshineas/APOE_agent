import requests

LLAMA_API_URL = "http://llama:8001/generate"

def generate(prompt: str) -> str:
    try:
        response = requests.post(LLAMA_API_URL, json={"prompt": prompt}, timeout=60)
        result = response.json().get("response", "[No response]")
        print("🔁 Raw model output:", result[:500])
        return result
    except Exception as e:
        return f"[TinyLLaMA Container ERROR] {str(e)}"

