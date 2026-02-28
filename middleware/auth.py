from fastapi import Request, HTTPException
from datetime import datetime, timedelta

API_KEYS = {
    "sk-your-key-1": {"credits": 1000, "user": "user1"},
    "sk-your-key-2": {"credits": 500, "user": "user2"},
}

def verify_api_key(api_key: str):
    if api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return API_KEYS[api_key]

def check_credits(api_key: str, estimated_tokens: int):
    key_data = API_KEYS[api_key]
    estimated_credits = estimated_tokens / 1000
    if key_data["credits"] < estimated_credits:
        raise HTTPException(status_code=402, detail="Insufficient credits")

def deduct_credits(api_key: str, tokens_used: int):
    if api_key in API_KEYS:
        credits_used = tokens_used / 1000
        API_KEYS[api_key]["credits"] -= credits_used
