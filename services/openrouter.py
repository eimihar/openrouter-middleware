import requests
import config

def call_openrouter(body: dict, api_key: str) -> requests.Response:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": config.APP_URL,
        "X-Title": config.APP_NAME
    }
    
    response = requests.post(config.OPENROUTER_URL, json=body, headers=headers)
    return response
