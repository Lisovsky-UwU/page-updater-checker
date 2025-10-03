import logging
import os
import sys
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("main")

LEVELS_MAP = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
    "NOTSET": logging.NOTSET,
}


def setup_log(level_str: str, log_to_console: bool) -> None:
    if not os.path.exists("logs"):
        os.makedirs("logs")

    level_up = level_str.upper()
    if level_up not in LEVELS_MAP:
        raise Exception(
            "Уровернь логирования {level_up} не является доступным. "
            f"Доступны следующие уровни: {', '.join(LEVELS_MAP.keys())}",
        )

    level = LEVELS_MAP[level_up]

    logger.setLevel(level)

    log_format = logging.Formatter(
        "%(asctime)s [%(levelname)-8s] %(module)s:%(lineno)d - %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        os.path.join("logs", "main.log"),
        maxBytes=5*1024*1024,
        backupCount=7,
        encoding="utf-8",
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(log_format)
        logger.addHandler(console_handler)

