import logging
from datetime import datetime

logging.basicConfig(filename="requests.log", level=logging.INFO)
error_logger = logging.getLogger("error_logger")
error_handler = logging.FileHandler("error.log")
error_handler.setLevel(logging.ERROR)
error_logger.addHandler(error_handler)
error_logger.setLevel(logging.ERROR)

async def log_request(request_body: dict, response_data: dict):
    logging.info(f"""
        Timestamp: {datetime.now()}
        Model: {request_body.get('model')}
        Messages: {len(request_body.get('messages', []))}
        Response ID: {response_data.get('id')}
        Tokens Used: {response_data.get('usage', {}).get('total_tokens')}
    """)

async def log_error(error: Exception, context: dict = None):
    error_logger.error(f"""
        Timestamp: {datetime.now()}
        Error: {type(error).__name__}: {str(error)}
        Context: {context}
    """)
