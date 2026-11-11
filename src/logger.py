from __future__ import annotations

import logging
from typing import Optional


def get_logger(name: str = "crypto_ai_desk", level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(level)
    try:
        from rich.logging import RichHandler

        handler: logging.Handler = RichHandler(rich_tracebacks=True, show_path=False)
        formatter = logging.Formatter("%(message)s")
    except Exception:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def set_log_level(logger: logging.Logger, verbose: bool = False, quiet: bool = False) -> None:
    if quiet:
        logger.setLevel(logging.WARNING)
    elif verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
