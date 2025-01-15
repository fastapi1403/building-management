import logging
import sys
from pathlib import Path
from loguru import logger
from datetime import datetime


def setup_logging():
    # Remove default logger
    logger.remove()

    # Log format
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    # Create logs directory if it doesn't exist
    log_path = Path("logs")
    log_path.mkdir(exist_ok=True)

    # Add handlers
    logger.add(
        sys.stdout,
        format=log_format,
        level="INFO",
        colorize=True
    )

    logger.add(
        "logs/app_{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention="30 days",
        format=log_format,
        level="DEBUG",
        compression="zip"
    )

    return logger


# Create logger instance
log = setup_logging()