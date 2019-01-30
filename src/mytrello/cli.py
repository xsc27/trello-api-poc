"""
Usage:
  trelloapi

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

import logging

from docopt import docopt

import mytrello.__version__ as version


def main():
    arguments = docopt(__doc__, version=version)
    logging.error("Not Implemented")


if __name__ == "__main__":
    main()
