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

import logging
import sys
from typing import Optional

import pkg_resources
from docopt import docopt

from mytrello.utils import config_logging

LOGGER: logging.Logger = logging.getLogger(__package__)
config_logging(LOGGER, log_file=f"{__package__}.log")


version: Optional[str] = None

try:
    version = pkg_resources.get_distribution(__package__).version
except pkg_resources.DistributionNotFound:
    version = None


def main():
    arguments = docopt(__doc__, version=version, options_first=True)
    LOGGER.info("Arguments received: %s", arguments)


if __name__ == "__main__":
    main()
