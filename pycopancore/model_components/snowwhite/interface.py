"""model component Interface template.

TODO: adjust or fill in code and documentation wherever marked by "TODO:", then
remove these instructions.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

# TODO: use variables from the master data model wherever possible:
# from ... import master_data_model as D
# TODO: uncomment and adjust of you need further variables from another
# model component:
# import ..BBB.interface as BBB
# TODO: uncomment and adjust only if you really need other variables:
from ... import Variable
from ... import master_data_model as D
from ..seven_dwarfs.interface import Cell as C


class Model (object):
    """Interface for Model mixin."""

    # metadata:
    name = "Snwow White Component"
    description = "Snow White arrives at the Dwarf's cave."
    requires = []
    """list of other model components required for this model component to
    make sense"""

    # Notes:
    # - Model does NOT define variables or parameters, only entity types
    #   and process taxons do!
    # - implementation.Model lists these entity-types and process taxons


# entity types:

class Cell (object):
    """Interface for Cell entity type mixin."""

    # endogenous variables:
    eating_stock = C.eating_stock    # exogenous variables / parameters:
