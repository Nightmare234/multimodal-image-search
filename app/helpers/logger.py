import logging
import os
from logging.handlers import RotatingFileHandler

ENV = os.getenv("ENV", "dev")

LOG_FORMAT = "%(asctime)s [%(levelname)s] [%(name)s] - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logger = logging.getLogger("backend")
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)

if ENV == "dev":
    if not os.path.exists("logs"):
        os.makedirs("logs")
    file_handler = RotatingFileHandler("logs/app.log", maxBytes=5*1024*1024, backupCount=3)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT))
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

def get_logger(name="backend"):
    return logger.getChild(name)
