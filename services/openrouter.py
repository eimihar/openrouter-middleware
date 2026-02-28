import requests
import config

def call_openrouter(body: dict) -> requests.Response:
    headers = {
        "Authorization": f"Bearer {config.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": config.APP_URL,
        "X-Title": config.APP_NAME
    }
    
    response = requests.post(config.OPENROUTER_URL, json=body, headers=headers)
    return response
