""" Package mytrello-api-poc top level """
import logging
from typing import List, Optional

import pkg_resources

from mytrello import api
from mytrello.client import Client
from mytrello import exceptions

__all__: List[str] = ["api"]

__version__: Optional[str]

try:
    __version__ = pkg_resources.get_distribution(__name__).version
except pkg_resources.DistributionNotFound:
    __version__ = None

logging.getLogger(__name__).addHandler(logging.NullHandler())
