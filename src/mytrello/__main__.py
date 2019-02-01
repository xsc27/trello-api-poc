import logging
import sys

from mytrello.ui import add_a_card_with_comments
from mytrello.utils import config_logging

LOGGER: logging.Logger = logging.getLogger(__package__)
config_logging(LOGGER, log_file=f"{__package__}.log")


def main():

    module_args = sys.argv[1:]
    LOGGER.info("Arguments received: %s", module_args)
    add_a_card_with_comments(*module_args)


if __name__ == "__main__":
    main()
