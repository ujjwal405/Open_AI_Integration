import logging
import json
import os
from pythonjsonlogger import jsonlogger

# Get log level from environment variable or default to INFO
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Create logger
logger = logging.getLogger("json_logger")
logger.setLevel(LOG_LEVEL)

# Create a stream handler (console output)
log_handler = logging.StreamHandler()

# Define JSON log format
formatter = jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
    rename_fields={
        "asctime": "timestamp",
        "levelname": "level",
        "name": "logger",
        "message": "message"
    }
)

log_handler.setFormatter(formatter)
logger.addHandler(log_handler)

# Avoid duplicate log messages
logger.propagate = False

# Example function to log messages
def log_info(message: str, extra_data: dict = None):
    log_data = {"message": message}
    if extra_data:
        log_data.update(extra_data)
    logger.info(json.dumps(log_data))

def log_error(message: str, extra_data: dict = None):
    log_data = {"message": message}
    if extra_data:
        log_data.update(extra_data)
    logger.error(json.dumps(log_data))
