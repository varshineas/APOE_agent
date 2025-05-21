import openai
openai.api_key = os.getenv("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")

def generate(prompt):
    res = openai.ChatCompletion.create(
        model="gpt-4", messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content
