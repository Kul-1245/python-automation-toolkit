# =============================================================================
# utils/logger.py
# Sets up a consistent logger used across the entire toolkit.
# Logs messages both to the console AND to a log file for record-keeping.
# =============================================================================

import logging
import os
import sys
from config.settings import LOG_DIR, LOG_FILE, LOG_FORMAT, LOG_DATE_FORMAT


def get_logger(name: str) -> logging.Logger:
    """
    Creates and returns a named logger with both console and file handlers.

    Args:
        name: A short identifier for the module (e.g. 'organizer').

    Returns:
        A configured logging.Logger instance.
    """
    # Create the logs directory if it doesn't exist yet
    os.makedirs(LOG_DIR, exist_ok=True)
    log_path = os.path.join(LOG_DIR, LOG_FILE)

    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers if the logger is requested more than once
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

    # --- Console handler: shows INFO and above in the terminal ---
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # --- File handler: saves DEBUG and above to the log file ---
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
