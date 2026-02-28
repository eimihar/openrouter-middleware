from fastapi import FastAPI
from routers.completions import router as completions_router

app = FastAPI()

app.include_router(completions_router)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
