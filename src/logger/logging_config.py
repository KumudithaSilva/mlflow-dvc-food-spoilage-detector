import atexit
import logging
import os
import sys

from utils.cloudwatch_logger import CloudWatchLogger

# -----------------------------
# Local logging
# -----------------------------
log_dir = "logs"
log_file_name = "running_logs.log"
os.makedirs(log_dir, exist_ok=True)
log_file = f"{log_dir}/{log_file_name}"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger("fsd_logger")


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


# -----------------------------
# CloudWatch logging
# -----------------------------
cw_handler = None
try:
    cw_logger = CloudWatchLogger()
    cw_handler = cw_logger.get_handler("fsd")  # you can change stream name here

    if cw_handler:
        root_logger = logging.getLogger()
        if cw_handler not in root_logger.handlers:
            root_logger.addHandler(cw_handler)

except Exception as e:
    logger.warning(f"CloudWatch logging disabled: {e}")

# -----------------------------
# Flush & close all handlers on exit
# -----------------------------


def flush_and_close_handlers():
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        try:
            if hasattr(handler, "flush"):
                handler.flush()
            if hasattr(handler, "close"):
                handler.close()
        except Exception as e:
            print(f"Error flushing/closing handler {handler}: {e}", file=sys.stderr)
    logging.shutdown()


atexit.register(flush_and_close_handlers)
