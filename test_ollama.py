from ollama import chat

response = chat(
    model="qwen3:8b",
    messages=[
        {
            "role": "user",
            "content": "Summarize: The website needs a redesign. Navigation is confusing."
        }
    ]
)

print(response["message"]["content"])