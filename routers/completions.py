from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from middleware.auth import verify_api_key, check_credits, deduct_credits
from middleware.rate_limit import rate_limiter
from middleware.logging import log_request
from middleware.cache import get_cache_key, get_cached_response, set_cached_response
from services.openrouter import call_openrouter
import config

router = APIRouter()

@router.post("/v1/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()
    
    api_key = request.headers.get("Authorization", "").replace("Bearer ", "")
    
    verify_api_key(api_key)
    
    rate_limiter.check(api_key)
    
    is_streaming = body.get("stream", False)
    
    if not is_streaming:
        cache_key = get_cache_key(body.get("messages", []), body.get("model", ""))
        cached_response = get_cached_response(cache_key)
        if cached_response:
            return cached_response
    
    estimated_tokens = sum(len(msg.get("content", "")) for msg in body.get("messages", [])) // 4
    check_credits(api_key, estimated_tokens)
    
    response = call_openrouter(body)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    
    if is_streaming:
        return StreamingResponse(
            response.iter_content(chunk_size=None),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
    
    response_data = response.json()
    
    await log_request(body, response_data)
    
    tokens_used = response_data.get("usage", {}).get("total_tokens", 0)
    deduct_credits(api_key, tokens_used)
    
    cache_key = get_cache_key(body.get("messages", []), body.get("model", ""))
    set_cached_response(cache_key, response_data, config.CACHE_TTL_SECONDS)
    
    return response_data
    
    return response_data
