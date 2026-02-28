from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
from middleware.logging import log_request
from services.openrouter import call_openrouter, get_balance

router = APIRouter()

def inject_balance_to_messages(messages: list, balance: float) -> list:
    balance_message = {
        "role": "system",
        "content": f"You have ${balance:.4f} USD of OpenRouter credits remaining."
    }
    
    new_messages = [balance_message]
    for msg in messages:
        if msg.get("role") == "system":
            msg["content"] = msg.get("content", "") + f"\n\nYou have ${balance:.4f} USD of OpenRouter credits remaining."
        else:
            new_messages.append(msg)
    
    return new_messages

@router.post("/v1/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()
    
    api_key = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not api_key:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    
    is_streaming = body.get("stream", False)
    
    balance = get_balance(api_key)
    messages = body.get("messages", [])
    body["messages"] = inject_balance_to_messages(messages, balance)
    
    response = call_openrouter(body, api_key, stream=is_streaming)
    
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
    
    return response_data
