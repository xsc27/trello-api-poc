"""Utils Module"""
import logging
import logging.handlers
import os
import sys
from typing import Optional


def config_logging(
    logger: logging.Logger,
    console_loglevel: Optional[str] = None,
    file_loglevel: Optional[str] = None,
    log_file: Optional[str] = None,
) -> None:
    """
    Configure logging
    Parameters
    ----------
    logger: logging.Logger
        logger
    console_loglevel: str, optional
        Set console log level (Default: warning)
    file_loglevel: str, optional
        Set file log level (Default: debug)
    log_file: str, optional
        Name of log file. By default there is not fileHandler for logging
    """

    # root Logger lvl must be the lowest for child handlers to use
    # an lvl equal to or greater than that of the parent
    # see https://docs.python.org/3/library/logging.html#logging.Logger.setLevel
    logger.setLevel(logging.DEBUG)

    if console_loglevel is None:
        console_loglevel = logging.INFO

    log_formatter: logging.Formatter = logging.Formatter("%(levelname)s: %(message)s")
    console_handler: logging.StreamHandler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(console_loglevel)
    logger.addHandler(console_handler)

    if log_file:
        if not file_loglevel:
            file_loglevel = logging.DEBUG
        log_formatter = logging.Formatter(
            "[%(asctime)s:%(levelname)-7s:%(name)s.%(module)s:%(lineno)d] %(message)s"
        )

        if os.name == "posix":
            file_handler: logging.handlers.WatchedFileHandler = logging.handlers.WatchedFileHandler(
                log_file
            )
        else:
            file_handler: logging.FileHandler = logging.FileHandler(log_file)

        file_handler.setFormatter(log_formatter)
        file_handler.setLevel(file_loglevel)
        logger.addHandler(file_handler)
