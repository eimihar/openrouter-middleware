import requests
import config

def call_openrouter(body: dict, api_key: str, stream: bool = False) -> requests.Response:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": config.APP_URL,
        "X-Title": config.APP_NAME
    }
    
    response = requests.post(config.OPENROUTER_URL, json=body, headers=headers, stream=stream)
    return response

def get_balance(api_key: str) -> float:
    key_label = api_key[:12] + "..." + api_key[-3:]
    
    if config.MANAGEMENT_KEY:
        try:
            headers = {
                "Authorization": f"Bearer {config.MANAGEMENT_KEY}",
                "HTTP-Referer": config.APP_URL,
                "X-Title": config.APP_NAME
            }
            
            response = requests.get("https://openrouter.ai/api/v1/keys", headers=headers, timeout=5)
            if response.status_code == 200:
                keys_data = response.json().get("data", [])
                for key in keys_data:
                    if key.get("label") == key_label:
                        limit_remaining = key.get("limit_remaining")
                        if limit_remaining is not None:
                            return limit_remaining
                        return -key.get("usage", 0)
        except Exception as e:
            print(f"Balance fetch error: {e}")
    
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": config.APP_URL,
            "X-Title": config.APP_NAME
        }
        
        response = requests.get("https://openrouter.ai/api/v1/credits", headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            total_credits = data.get("data", {}).get("total_credits", 0)
            total_usage = data.get("data", {}).get("total_usage", 0)
            return total_credits - total_usage
    except Exception as e:
        print(f"Balance fetch error: {e}")
    return 0
