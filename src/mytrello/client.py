from typing import Dict

import requests

from mytrello import exceptions


class Client:
    __creds: Dict[str, str]

    def __init__(
        self,
        key: str,
        token: str,
        api_endpoint: str = "https://api.trello.com/",
        api_version: str = "1",
    ):
        self.__creds = {"key": key, "token": token}
        self.api_endpoint = api_endpoint
        self.api_version = api_version

    def _raise_for_status(self, response):
        """Raises stored :class:`HTTPError`, if one occurred."""

        http_error_msg: str = f"{response.status_code}"

        if 400 <= response.status_code < 600:
            http_error_msg = f"{http_error_msg} {response.text}"

        raise exceptions.HTTPError(http_error_msg, response=response)

    def request(self, method: str, resource: str, **kwargs):
        params: Dict = kwargs if kwargs else dict()
        url = f"{self.api_endpoint}{self.api_version}/{resource}/"
        headers: Dict[str, str] = dict(
            {"Content-Type": "application/json; charset=utf-8"}
        )
        params.update(self.__creds)
        response = requests.request(method, url, params=params, headers=headers)

        if not response.status_code == requests.codes.ok:
            self._raise_for_status(response)

        return response.json()
