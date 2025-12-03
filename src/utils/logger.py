
import logging
import os
import requests

def setup_logging():
    """Configures the root logger for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - [%(levelname)s] - %(message)s',
        handlers=[
            logging.FileHandler("engine.log"),
            logging.StreamHandler()
        ]
    )

def log_telegram(message):
    """Sends a message to the configured Telegram chat."""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')

    if not token or not chat_id:
        logging.warning("Telegram token or chat_id not set. Skipping notification.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            logging.error(f"Failed to send Telegram message: {response.text}")
    except Exception as e:
        logging.error(f"Exception while sending Telegram message: {e}")
