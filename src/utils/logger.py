import logging
import os
from datetime import datetime
from config.config import config

def setup_logger(name: str, log_file: str = None, level: int = logging.INFO) -> logging.Logger:
    """
    Function to setup as many loggers as you want
    """
    if not log_file:
        log_file = f"data/logs/{name}_{datetime.now().strftime('%Y%m%d')}.log"
    
    # Create logs directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.addHandler(console_handler)

    return logger

# Main logger instance
main_logger = setup_logger('abyssal_archive', 'data/logs/main.log')
youtube_logger = setup_logger('youtube_uploader', 'data/logs/youtube.log')
content_logger = setup_logger('content_generator', 'data/logs/content.log')
image_logger = setup_logger('image_generator', 'data/logs/image.log')
audio_logger = setup_logger('audio_generator', 'data/logs/audio.log')
