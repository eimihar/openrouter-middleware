import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
APP_NAME = os.getenv("APP_NAME", "My API")
APP_URL = os.getenv("APP_URL", "https://your-site.com")
