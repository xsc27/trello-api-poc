import logging
from abc import ABC
from typing import Dict, List, Optional

from mytrello.client import Client


class Resource(ABC):
    _resource: str

    def __init__(self, client: Client, objectid: Optional[str] = None, **kwargs) -> None:
        """
        Base class to make calls to any resource.

        Parameters
        ----------
        client
            Client to make api calls.
        objectid
            Id of resource to manipulate. If none given, a new resource will be created.
        """
        self.client: Client = client
        self.id = objectid if objectid else ""

    def _path(self, resource: str, path: Optional[str] = None) -> str:
        if not path:
            path = ""
        url_path: str = "/".join([resource, self.id, path])
        return url_path

    def _request(
        self, method: str, path: Optional[str] = None, **kwargs
    ) -> Optional[Dict[str, str]]:
        url_path = self._path(self._resource, path)
        response = self.client.request(method, url_path, **kwargs)
        return response

    def delete(self, path: Optional[str] = None, **kwargs) -> Optional[Dict[str, str]]:
        return self._request("DELETE", path, **kwargs)

    def get(self, path: Optional[str] = None, **kwargs) -> Optional[Dict[str, str]]:
        return self._request("GET", path, **kwargs)

    def post(self, path: Optional[str] = None, **kwargs) -> Optional[Dict[str, str]]:
        return self._request("POST", path, **kwargs)

    def put(self, path: Optional[str] = None, **kwargs) -> Optional[Dict[str, str]]:
        return self._request("PUT", path, **kwargs)


class TrelloObject(Resource):

    def __init__(
        self,
        client: Client,
        objectid: Optional[str] = None,
        properties: Optional[Dict[str, str]] = None,
    ) -> None:
        """
        Instantiates an object of a Trello resource by either
        fetching an existing resource if an id is given or creates a new resource.

        Parameters
        ----------
        client
            Client to make api calls.
        objectid
            Id of resource to manipulate. If none given, a new resource will be created.
        properties
           Properties of resource to avoid making an API call or properties to apply if creating a resource.
        """
        super().__init__(client, objectid)
        if objectid:
            if properties:
                self.properties = properties
            else:
                self.get()
        else:
            self.create(**properties)

    def __repr__(self):
        return self.id

    def create(self, **kwargs: str) -> Optional[str]:
        """
        Parameters
        ----------
        kwargs : str
            Any key-values to be passed as parameters.

        Returns
        -------
        str, Optional
            ID of resource created.
        """

        if self.id:
            logging.error("Object contains resource %s", self.id)
            return None

        response = self.client.request("POST", self._resource, **kwargs)
        self.id = response["id"]
        self.properties = response
        logging.info("Created resource: %s %s", self._resource, self.id)
        return response["id"]

    def delete(self, **kwargs) -> Dict[str, str]:
        response = super().delete()
        logging.info("Resource deleted: %s", self.id)
        self.properties = response
        self.id = ""
        return response

    def get(self, path: Optional[str] = None, **kwargs) -> Dict[str, str]:
        properties = super().get(path, **kwargs)
        self.properties = properties
        return properties


class Actions(TrelloObject):
    _resource: str = "actions"


class Boards(TrelloObject):
    _resource: str = "boards"

    def get_lists(self, **kwargs) -> List[TrelloObject]:
        response = self.get("lists", **kwargs)
        lists: List[TrelloObject] = [
            Lists(self.client, l["id"], properties=l) for l in response
        ]
        return lists

    def get_labels(self, **kwargs) -> List[TrelloObject]:
        response = self.get("labels", **kwargs)
        lists: List[TrelloObject] = [
            Labels(self.client, l["id"], properties=l) for l in response
        ]
        return lists


class Cards(TrelloObject):
    _resource: str = "cards"

    def add_comment(self, text: str):
        response = self.post("actions/comments", text=text)
        self.get()
        trello_obj = Actions(self.client, objectid=response["id"])
        return trello_obj


class Labels(TrelloObject):
    _resource: str = "labels"


class Lists(TrelloObject):
    _resource: str = "lists"

    def add_card(
        self, name: Optional[str] = None, labelids: List[str] = None, **kwargs
    ):
        properties: Dict[str, str] = dict()
        properties.update(kwargs)
        if name:
            properties["name"] = name
        if labelids:
            properties["idLabels"] = ",".join(labelids)
        properties["idList"] = self.id

        card = Cards(self.client, properties=properties)
        self.get()

        return card
