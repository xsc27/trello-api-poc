from typing import Optional

import mytrello

CLIENT = mytrello.Client()


def add_a_card_with_comments(
    column: Optional[str] = None,
    cardname: Optional[str] = None,
    labelids: Optional[str] = None,
    comment: Optional[str] = None,
):
    # column is being used as the nominclature from the implementation spec
    # for simplicity of the interface a card name is rquired.

    trello_list = mytrello.api.Lists(CLIENT, column)
    trello_card = trello_list.add_card(cardname, labelids)
    if comment:
        trello_card.add_comment(comment)

    return trello_card
