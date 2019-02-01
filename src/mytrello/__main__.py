import logging
import sys

from mytrello.utils import config_logging

LOGGER: logging.Logger = logging.getLogger(__package__)
config_logging(LOGGER, log_file=f"{__package__}.log")


def main():
    LOGGER.error("Not Implemented")
    LOGGER.info("Arguments received: %s", sys.argv[1:])


if __name__ == "__main__":
    main()
