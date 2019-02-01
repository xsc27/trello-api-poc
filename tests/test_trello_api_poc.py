#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=no-self-use, invalid-name

"""Tests for mytrello package."""

from pprint import pprint
import pytest

import requests.exceptions
import mytrello

"""
Board API-POC:
- 'id': '5c53e48984ab033e7e5477ed'
  'url': 'https://trello.com/b/zPYgUjVy/api-poc'
Lists:
- 'id': '5c53e48984ab033e7e5477ee'
  'name': 'To Do'
  'pos': 16384
- 'id': '5c53e48984ab033e7e5477ef'
  'name': 'Doing'
  'pos': 32768
- 'id': '5c53e48984ab033e7e5477f0'
  'name': 'Done'
  'pos': 49152
Labels:
- 'color': 'orange'
  'id': '5c53e48991d0c2ddc5c4cab8'
- 'color': 'green'
  'id': '5c53e48991d0c2ddc5c4cab9'
- 'color': 'yellow'
  'id': '5c53e48991d0c2ddc5c4caba'
- 'color': 'red'
  'id': '5c53e48991d0c2ddc5c4cabd'
- 'color': 'purple'
  'id': '5c53e48991d0c2ddc5c4cac0'
- 'color': 'blue'
  'id': '5c53e48991d0c2ddc5c4cac1'
"""

@pytest.fixture
def client():
    return mytrello.Client()

class TestClient:
    def test_bad(self):
        client = mytrello.Client("badkey", "badtoken")
        with pytest.raises(requests.exceptions.HTTPError):
            client.request("GET", "badresource")

    def test_search(self, client):
        response = client.request("GET", "search", query="API")
        assert isinstance(response, dict)
        assert all(k in response for k in ("boards", "cards", "members", "options", "organizations"))

class TestBoards:
    def test110_create(self, client):
        trello_obj1 = mytrello.api.Boards(client, properties={"name": "pytest"})
        assert isinstance(trello_obj1.properties, dict)
        assert all(k in trello_obj1.properties for k in ("closed", "desc", "id", "name", "labelNames", "url"))
        trello_obj2 = mytrello.api.Boards(client, objectid=trello_obj1.id)
        assert trello_obj1.id == trello_obj2.id
        assert trello_obj1.properties["url"] == trello_obj2.properties["url"]
        response = trello_obj1.delete()
        assert not trello_obj1.id
        assert response == {"_value": None}

    def test120_get_lists(self, client):
        trello_obj = mytrello.api.Boards(client, "5c53e48984ab033e7e5477ed")
        lists = trello_obj.get_lists()
        assert isinstance(lists, list)
        assert all(k in lists[0].properties for k in ("closed", "id", "idBoard", "name", "pos", "subscribed"))

    def test130_get_labels(self, client):
        trello_obj = mytrello.api.Boards(client, "5c53e48984ab033e7e5477ed")
        labels = trello_obj.get_labels()
        assert isinstance(labels, list)
        pprint(labels)
        assert all(l in labels[0].properties for l in ("color", "id", "idBoard", "name"))

    def test200_create_error(self, client):
        trello_obj = mytrello.api.Boards(client, "5c53e48984ab033e7e5477ed")
        trello_obj2 = trello_obj.create()
        # add log check
        assert trello_obj2 is None


class TestLists:
    def test_get(self, client):
        trello_obj = mytrello.api.Lists(client, "5c53e48984ab033e7e5477ee")
        assert isinstance(trello_obj.properties, dict)
        assert all(k in trello_obj.properties for k in ("closed", "id", "idBoard", "name", "pos"))

    def test_add_card_name(self, client):
        card_name: str = "pytest_add_card_name"
        trello_obj = mytrello.api.Lists(client, "5c53e48984ab033e7e5477ee")
        trello_card = trello_obj.add_card(name=card_name)
        assert trello_card.properties["name"] == card_name
        response = trello_card.delete()
        assert not trello_card.id
        assert response == {'limits': {}}
        with pytest.raises(requests.exceptions.HTTPError):
            trello_card.get()

    def test_add_card_labels(self, client):
        trello_obj = mytrello.api.Lists(client, "5c53e48984ab033e7e5477ee")
        trello_card1 = trello_obj.add_card(name="label", labelids=["5c53e48991d0c2ddc5c4cabd"])
        trello_card2 = mytrello.api.Cards(client, objectid=trello_card1.id)
        assert trello_card1.properties["url"] == trello_card2.properties["url"]
        response = trello_card1.delete()
        assert not trello_card1.id
        assert response == {'limits': {}}
        with pytest.raises(requests.exceptions.HTTPError):
            trello_card2.get()

    def test_add_card_noname_nolabel(self, client):
        trello_obj = mytrello.api.Lists(client, "5c53e48984ab033e7e5477ee")
        trello_card1 = trello_obj.add_card()
        trello_card2 = mytrello.api.Cards(client, objectid=trello_card1.id)
        assert trello_card1.properties["url"] == trello_card2.properties["url"]
        response = trello_card1.delete()
        assert not trello_card1.id
        assert response == {'limits': {}}
        with pytest.raises(requests.exceptions.HTTPError):
            trello_card2.get()


class TestLabels:
    def test_get(self, client):
        trello_obj = mytrello.api.Labels(client, "5c53e48991d0c2ddc5c4cabd")
        assert isinstance(trello_obj.properties, dict)
        assert all(l in trello_obj.properties for l in ("color", "id", "idBoard", "name"))


class TestCards:
    def test_add_comment(self, client):
        trello_obj = mytrello.api.Cards(client, objectid="5c540df68c034f03b7c51d5a")
        text = "Comment from pytest"
        trello_action = trello_obj.add_comment(text)
        assert trello_action.properties["type"] == "commentCard"
        trello_action_check = mytrello.api.Actions(client, trello_action.id)
        assert trello_action_check.properties["data"]["text"] == text
        trello_action.delete()
        with pytest.raises(requests.exceptions.HTTPError):
            trello_action_check.get()
