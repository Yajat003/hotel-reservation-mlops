import logging
import os
from datetime import datetime

LOGS_DIR = "logs"

# This will create the logs folder if it doesn't already exist; exist_ok=True prevents an error if the folder is already there
os.makedirs(LOGS_DIR, exist_ok= True)

# The name of the log file will include today's date so that each day gets its own log file; strftime('%Y-%m-%d') formats the date like 2026-03-03
LOG_FILE = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")

# basicConfig sets up the root logger configuration
# filename -> tells logging to write logs to this file instead of console; format -> defines how each log message will look; level=logging.INFO -> means it will log INFO, WARNING, ERROR and CRITICAL
logging.basicConfig(filename = LOG_FILE,
                    format = "%(asctime)s - %(levelname)s - %(message)s",
                    level = logging.INFO)

def get_logger(name):
    # This creates or retrieves if already created a logger with a specific name; usually __name__ is passed from each file so that we know where logs are coming from
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger