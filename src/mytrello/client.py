import logging
import os
import urllib.parse
from typing import Dict, Optional

import requests


class Client:
    __creds: Dict[str, str] = dict()

    def __init__(
        self,
        key: Optional[str] = None,
        token: Optional[str] = None,
        api_endpoint: str = "api.trello.com",
        api_version: str = "1",
    ):
        self.__creds["key"] = key if key else os.environ["TRELLO_KEY"]
        self.__creds["token"] = token if key else os.environ["TRELLO_TOKEN"]
        self.api_endpoint = api_endpoint
        self.api_version = api_version

    def _raise_for_status(self, response):  # pylint: disable=no-self-use
        """Raises stored :class:`HTTPError`, if one occurred."""

        http_error_msg: str = f"{response.status_code}"

        if 400 <= response.status_code < 600:
            http_error_msg = f"{http_error_msg} {response.text}"

        raise requests.exceptions.HTTPError(http_error_msg, response=response)

    def request(self, method: str, path: str, **kwargs):
        full_path: str = "/".join([self.api_version, path])
        url: str = urllib.parse.urlunparse(
            ("https", self.api_endpoint, full_path, None, None, None)
        )
        querystring: Dict = kwargs if kwargs else dict()
        headers: Dict[str, str] = dict(
            {"Content-Type": "application/json; charset=utf-8"}
        )

        logging.debug("url path = %s", full_path)
        logging.debug("url params = %s", querystring)
        querystring.update(self.__creds)
        response = requests.request(method, url, params=querystring, headers=headers)
        logging.debug("http status = %s", response.status_code)

        if not response.status_code == requests.codes.ok:
            self._raise_for_status(response)

        return response.json()
