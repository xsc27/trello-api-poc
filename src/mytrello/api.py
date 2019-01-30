from abc import ABC
from typing import Dict, Optional

from mytrello.client import Client


class Resource(ABC):
    resource: str

    def __init__(self, client: Client, objectid: str):
        self.client = client
        self.id = objectid

    def _path(self, resource: str, path: Optional[str] = None):
        if not path:
            path = ""
        url_path: str = "/".join([resource, self.id, path])
        return url_path

    def get(self, path: Optional[str] = None, **kwargs):
        url_path = self._path(self.resource, path)
        params: Dict[str, str] = dict()
        params.update(kwargs)
        response = self.client.request("GET", url_path, **params)
        return response


class TrelloObject(Resource):
    def __init__(self, client: Client, objectid: str):
        super().__init__(client, objectid)
        self.properties = self.get()


class Boards(TrelloObject):
    resource: str = "boards"

    def get_lists(self, **kwargs):
        response = self.get("lists", **kwargs)
        return response


class Lists(Resource):
    resource: str = "lists"

    def add_card(self, **kwargs):
        params: Dict[str, str] = dict({"idList": self.id})
        params.update(kwargs)
        self.client.request("POST", "cards", **params)
