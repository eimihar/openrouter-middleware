import logging
from datetime import datetime

logging.basicConfig(filename="requests.log", level=logging.INFO)

async def log_request(request_body: dict, response_data: dict):
    logging.info(f"""
        Timestamp: {datetime.now()}
        Model: {request_body.get('model')}
        Messages: {len(request_body.get('messages', []))}
        Response ID: {response_data.get('id')}
        Tokens Used: {response_data.get('usage', {}).get('total_tokens')}
    """)
