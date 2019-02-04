.. image:: https://travis-ci.org/CMeza99/trello-api-poc.svg?branch=master
    :target: https://travis-ci.org/CMeza99/trello-api-poc

==============
trello-api-poc
==============

Testing Trello API

Currently the ui exposes a fucntion to add a new card on board in nth list.

-----
Usage
-----

Set your credentials as environment variables: TRELLO_KEY, TRELLO_TOKEN.

.. code-block:: bash

   mytrello [options] <boardid> <column>

   Options:
     -n CARDNAME --name=CARDNAME       Give new card name (text)
     -c COMMENT --comment=COMMENT      Add a comment (text)
     -l LABELID --label=LABELID        Attach labels, csv (resource id)
     -v --version     Show version
     -h --help     Show this screen

Example
^^^^^^^

This command:
.. code-block:: bash

   mytrello -l 5c53e48991d0c2ddc5c4cabd -c "cli test" -n "CLI Test" 5c53e48984ab033e7e5477ed 2

created:
https://trello.com/c/bPMFJCvA

----
Todo
----

* fix type hints
* mock test
* proper docstrings
* add more authentication options, i.e. Oauth
