# OpenRouter Middleware

A FastAPI-based middleware for OpenRouter API with rate limiting, response caching, API key authentication, and request logging.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and add your OpenRouter API key:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | Application name for OpenRouter | My Openrouter middleware |
| `APP_URL` | Application URL for OpenRouter referer | https://your-site.com |

> **Note**: The OpenRouter API key is passed via the `Authorization` header in requests.

### 3. Run the Server

```bash
uvicorn main:app --reload
```

Or:

```bash
python main.py
```

The server will start on `http://localhost:8000`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v1/chat/completions` | Chat completions endpoint |
| GET | `/health` | Health check |

### Chat Completions

```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Authorization: Bearer YOUR_OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## Features

- **Client API Key Pass-through** - Forward client's OpenRouter API key directly
- **Request Logging** - Log all requests and responses to `requests.log`
- **Streaming Support** - Full support for streaming responses
- **Health Check** - Endpoint for monitoring

## Project Structure

```
openrouter-middleware/
├── main.py                 # FastAPI application entry point
├── config.py               # Configuration management
├── .env.example            # Example environment variables
├── requirements.txt        # Python dependencies
├── middleware/
│   ├── __init__.py
│   └── logging.py          # Request logging
├── routers/
│   ├── __init__.py
│   └── completions.py      # Chat completions endpoint
└── services/
    ├── __init__.py
    └── openrouter.py       # OpenRouter API client
```