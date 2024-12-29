import logging
from logging.handlers import TimedRotatingFileHandler
import os

def setup_logger():
    # Ensure the logs directory exists
    log_directory = "logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    logger = logging.getLogger("template_logger")
    logger.setLevel(logging.INFO)

    handler = TimedRotatingFileHandler(f"{log_directory}/template.log", when="midnight", interval=1)
    handler.suffix = "%Y-%m-%d"
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    logger.addHandler(handler)
    return logger

logger = setup_logger()