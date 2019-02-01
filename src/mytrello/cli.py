"""Naval Fate.

Usage:
  naval_fate.py ship new <name>...
  naval_fate.py ship <name> move <x> <y> [--speed=<kn>]
  naval_fate.py ship shoot <x> <y>
  naval_fate.py mine (set|remove) <x> <y> [--moored | --drifting]
  naval_fate.py (-h | --help)
  naval_fate.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --speed=<kn>  Speed in knots [default: 10].
  --moored      Moored (anchored) mine.
  --drifting    Drifting mine.
"""

import sys
import logging

from docopt import docopt

from mytrello.utils import config_logging
from typing import Optional
import pkg_resources

LOGGER: logging.Logger = logging.getLogger(__package__)


version: Optional[str] = None

try:
    version = pkg_resources.get_distribution(__package__).version
except pkg_resources.DistributionNotFound:
    version = None


def main():
    config_logging(LOGGER, log_file=f"{__package__}.log")
    arguments = docopt(__doc__, version=version, options_first=True)
    LOGGER.error("Not Implemented")
    LOGGER.info("Arguments received: %s", arguments)


if __name__ == "__main__":
    main()
