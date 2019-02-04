from typing import Optional, Union

import mytrello

CLIENT = mytrello.Client()


def add_card(
    boardid: str,
    column: Union[int, str],
    cardname: Optional[str] = None,
    labelids: Optional[str] = None,
    comment: Optional[str] = None,
):
    column = int(column)
    trello_board = mytrello.api.Boards(CLIENT, boardid)
    trello_lists = trello_board.get_lists()
    trello_lists.sort(key=lambda l: l.properties["pos"])
    trello_card = trello_lists[column - 1].add_card(cardname, labelids)
    if comment:
        trello_card.add_comment(comment)

    return trello_card
