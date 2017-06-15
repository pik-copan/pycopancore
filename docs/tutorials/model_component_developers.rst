Model component developers
==========================

A model component developer is a person who develops new components in copan:CORE in order to provide novel features
for a model. A model component developer does not change the framework of copan:CORE.

This tutorial guides the reader through the implementation of a new model component using the adaptive voter model as
an example.


Developing a new model component
--------------------------------

At first, bla bla bla

Entities and process taxonomy
-----------------------------

Determine necessary :doc:`entity types<../framework_documentation/entity_types/index>` and
:doc:`process taxa <../framework_documentation/process_taxonomy/index>`

Create model component files from template
------------------------------------------

Use :doc:`Jobst's doku<framework_documentation/python_implementation/model_components>`


Create attributes and methods of entites and taxa
-------------------------------------------------

This is a listing:

- One
- Two

Code snippet 1 from ``culture.py``:

::

from .. import interface as I


from ....runners import Hooks

from blist import sortedlist # more performant for large list modifications
import datetime as dt
from enum import Enum, unique
import random
from time import time


class Culture (I.Culture):
    """Culture process taxon mixin implementation class."""

    # standard methods:

    __nodes_by_opinion = None
    __nodes = None
    __filter_by_opinion = lambda opinion, input_list: list(filter(lambda ind: ind.opinion == opinion, input_list))
    __remove_by_opinion = lambda opinion, input_list: list(filter(lambda ind: ind.opinion != opinion, input_list))

    __update_function = None

    __configuration = dict( # keeps the configuration status, whether the updates are done basic or fast, and clusteredd or non-clustered
        configured=False,



Define processes
----------------


Module testing
--------------

