import logging
import os
import sys

"""

Logging Setup Module

This script configures Python's built-in logging system and import this module or run it to initialize logging. 
Then use the configured logger to add log messages throughout the application.

"""

log_dir = "logs"
log_file_name = "running_logs.log"

# Create logs directory if not exists
os.makedirs(f"{log_dir}", exist_ok=True)
log_file = f"{log_dir}/{log_file_name}"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s",
    handlers=[
        # Write log messages to the specified file
        logging.FileHandler(log_file),
        # Write log messages to the specified file
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger("fsd_logger")
