from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Print available models
def list_models():
    print("Available OpenAI models for this API key:")
    try:
        models = client.models.list()
        for model in models.data:
            print("-", model.id)
    except Exception as e:
        print(f"[ERROR] Failed to list models: {str(e)}")

# Run once on import
list_models()

# Core generation function
def generate(prompt: str):
    model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[ERROR] Could not generate response from OpenAI: {str(e)}"
