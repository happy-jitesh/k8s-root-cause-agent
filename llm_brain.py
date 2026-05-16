import requests
from config import MODEL

OLLAMA_URL = "http://localhost:11434/api/chat"

def analyze(context, prompt):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": context
                }
            ],
            "stream": False
        }
    )

    return response.json()["message"]["content"]