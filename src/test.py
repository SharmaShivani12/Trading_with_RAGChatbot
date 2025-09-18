import ollama

response = ollama.chat(
    model="gemma:2b",   # or "phi:2.7b"
    messages=[{"role": "user", "content": "Explain Bitcoin simply"}]
)

print(response['message']['content'])