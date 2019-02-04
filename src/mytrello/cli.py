"""mytrello
Add a new card on board in nth list.

Usage: mytrello [options] <boardid> <column>

Options:
  -n CARDNAME --name=CARDNAME       Give new card name (text)
  -c COMMENT --comment=COMMENT      Add a comment (text)
  -l LABELID --label=LABELID        Attach labels, csv (resource id)
  -v --version     Show version
  -h --help     Show this screen
"""

import logging
from typing import Optional

import pkg_resources
from docopt import docopt

from mytrello.utils import config_logging
import mytrello.ui

LOGGER: logging.Logger = logging.getLogger(__package__)
config_logging(LOGGER, log_file=f"{__package__}.log")


VERSION: Optional[str] = None

try:
    VERSION = pkg_resources.get_distribution(__package__).version
except pkg_resources.DistributionNotFound:
    VERSION = None


def main():
    arguments = docopt(__doc__, version=VERSION, options_first=False)
    LOGGER.info("Arguments received: %s", arguments)
    new_card_params = dict(
        {"boardid": arguments["<boardid>"], "column": arguments["<column>"]}
    )
    if arguments["--name"]:
        new_card_params["cardname"] = arguments["--name"]
    if arguments["--label"]:
        new_card_params["labelids"] = arguments["--label"]
    if arguments["--comment"]:
        new_card_params["comment"] = arguments["--comment"]

    mytrello.ui.add_card(**new_card_params)


if __name__ == "__main__":
    main()
