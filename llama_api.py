from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto"
)
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

app = FastAPI()

class Prompt(BaseModel):
    prompt: str

@app.post("/generate")
def generate_text(data: Prompt):
    try:
        result = generator(data.prompt, max_new_tokens=512, do_sample=True, temperature=0.7)
        return {"response": result[0]["generated_text"].replace(data.prompt, "").strip()}
    except Exception as e:
        return {"error": str(e)}
