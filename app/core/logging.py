import logging
import sys
from typing import Any
from loguru import logger as loguru_logger


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging():
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]

    # Configure loguru
    logger.configure(
        handlers=[
            {
                "sink": sys.stdout,
                "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                          "<level>{level: <8}</level> | "
                          "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                          "<level>{message}</level>",
                "level": "INFO",
            },
            {
                "sink": "logs/app.log",
                "rotation": "500 MB",
                "retention": "2 months",
                "compression": "zip",
                "format": "{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | "
                          "{name}:{function}:{line} | {message}",
                "level": "DEBUG",
            }
        ]
    )


logger = loguru_logger