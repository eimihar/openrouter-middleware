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
        
        self.requests[api_key] = [t for t in self.requests[api_key] if t > minute_ago]
        
        if len(self.requests[api_key]) >= self.requests_per_minute:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        self.requests[api_key].append(now)

rate_limiter = RateLimiter(requests_per_minute=30)
