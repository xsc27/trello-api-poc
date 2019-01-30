#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=no-self-use, invalid-name

"""Tests for mytrello package."""

import pytest

# dict({
#     "key": <KEY>,
#     "token": <TOKEN>
# })
from .creds import CREDS
import mytrello

@pytest.fixture
def client():
    return mytrello.Client(**CREDS)

class TestClient:
    def test_bad(self):
        client = mytrello.Client("badkey", "badtoken")
        with pytest.raises(mytrello.exceptions.HTTPError):
            client.request("GET", "badresource")

    def test_search(self, client):
        response = client.request("GET", "search", query="API")
        assert isinstance(response, dict)
        assert all(k in response for k in ("boards", "cards", "members", "options", "organizations"))

class TestBoards:
    def test_get(self, client):
        trello_obj = mytrello.api.Boards(client, "5c4fd7acc3d4fa598156482a")
        response= trello_obj.get()
        assert isinstance(response, dict)
        assert all(k in response for k in ("closed", "desc", "id", "name", "labelNames", "url"))

    def test_get_lists(self, client):
        trello_obj = mytrello.api.Boards(client, "5c4fd7acc3d4fa598156482a")
        response = trello_obj.get_lists()
        assert isinstance(response, list)
        assert all(k in response[0] for k in ("closed", "id", "idBoard", "name", "pos", "subscribed"))

class TestLists:
    # 5c4fd7ac14195824f4bc49e0
    # 5c4fd7ac23c1a06368c00c10
    # 5c4fd7ac822d570cf40e5951
    def test_get(self, client):
        trello_obj = mytrello.api.Lists(client, "5c4fd7ac14195824f4bc49e0")
        response = trello_obj.get()
        assert isinstance(response, dict)
        assert all(k in response for k in ("closed", "id", "idBoard", "name", "pos"))

    def test_add_card(self, client):
        trello_obj = mytrello.api.Lists(client, "5c4fd7ac14195824f4bc49e0")
        response = trello_obj.add_card()
        assert response is None


