# Building a Completion API Middleware with FastAPI

Here's a suggested architecture for building your own completion API middleware:

## Basic Setup

```python
# main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import requests
import os

app = FastAPI()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    # Get the raw body
    body = await request.json()
    
    # Add your custom logic here (see below)
    
    # Forward to OpenRouter
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-site.com",  # Required by OpenRouter
        "X-Title": "Your App Name"
    }
    
    response = requests.post(OPENROUTER_URL, json=body, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    return response.json()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## Adding Middleware Features

### 1. Rate Limiting

```python
# middleware/rate_limit.py
from fastapi import Request, HTTPException
from datetime import datetime, timedelta
from collections import defaultdict

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)
    
    def check(self, api_key: str):
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)
        
        # Clean old requests
        self.requests[api_key] = [t for t in self.requests[api_key] if t > minute_ago]
        
        if len(self.requests[api_key]) >= self.requests_per_minute:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        self.requests[api_key].append(now)

rate_limiter = RateLimiter(requests_per_minute=30)

# Usage in main.py
@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    api_key = request.headers.get("Authorization", "").replace("Bearer ", "")
    rate_limiter.check(api_key)  # Add this line
    # ... rest of code
```

### 2. Logging & Monitoring

```python
# middleware/logging.py
import logging
from datetime import datetime

logging.basicConfig(filename="requests.log", level=logging.INFO)

async def log_request(request: Request, response_data: dict):
    logging.info(f"""
        Timestamp: {datetime.now()}
        Model: {request.json().get('model')}
        Messages: {len(request.json().get('messages', []))}
        Response ID: {response_data.get('id')}
        Tokens Used: {response_data.get('usage', {}).get('total_tokens')}
    """)
```

### 3. API Key Management

```python
# middleware/auth.py
from fastapi import Request, HTTPException
from datetime import datetime, timedelta
import sqlite3

# Simple API key database
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
    # Rough estimate: 1 token ≈ 4 characters, 1 credit ≈ 1000 tokens
    estimated_credits = estimated_tokens / 1000
    if key_data["credits"] < estimated_credits:
        raise HTTPException(status_code=402, detail="Insufficient credits")
```

### 4. Response Caching

```python
# middleware/cache.py
from functools import lru_cache
import hashlib
import json
from datetime import datetime, timedelta

cache = {}

def get_cache_key(messages: list, model: str) -> str:
    content = json.dumps({"messages": messages, "model": model})
    return hashlib.md5(content.encode()).hexdigest()

def get_cached_response(key: str):
    cached = cache.get(key)
    if cached and cached.get("expires", datetime.min) > datetime.now():
        return cached.get("data")
    return None

def set_cached_response(key: str, value: dict, ttl_seconds: int = 3600):
    cache[key] = {"data": value, "expires": datetime.now() + timedelta(seconds=ttl_seconds)}
```

---

## Complete Project Structure

```
my-api/
├── main.py                 # FastAPI app
├── config.py               # Configuration
├── middleware/
│   ├── __init__.py
│   ├── auth.py             # API key verification
│   ├── rate_limit.py       # Rate limiting
│   ├── logging.py          # Request logging
│   └── cache.py            # Response caching
├── routers/
│   ├── __init__.py
│   └── completions.py      # Completion endpoint
├── services/
│   ├── __init__.py
│   └── openrouter.py       # OpenRouter client
└── requirements.txt
```

---

## requirements.txt

```
fastapi
uvicorn
requests
python-dotenv
```

---

## Features Summary

| Feature | Description |
|---------|-------------|
| Rate Limiting | Limit requests per API key per minute |
| Logging | Log all requests and responses |
| API Key Management | Verify keys and track credits |
| Response Caching | Cache responses to reduce costs |
| Error Handling | Proper error responses |
| Health Check | Endpoint for monitoring |