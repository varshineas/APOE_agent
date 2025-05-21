import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate(prompt):
    res = openai.ChatCompletion.create(
        model="gpt-4", messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content
