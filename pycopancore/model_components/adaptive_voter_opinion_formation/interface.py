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
from ... import master_data_model as D
# TODO: uncomment and adjust of you need further variables from another
# model component:
# import ..BBB.interface as BBB
# TODO: uncomment and adjust only if you really need other variables:
from ... import Variable # used for opinion here, maybe that should be included in the master data model? But I wouldn't know how? something like discrete opinion


class Model (object):
    """Interface for Model mixin."""

    # metadata:
    name = "adaptive voter model"
    """a unique name for the model component"""
    description = "..."
    """see Holme, Newman - 2006"""
    requires = []
    """list of other model components required for this model component to
    make sense"""

    # Notes:
    # - Model does NOT define variables or parameters, only entity types
    #   and process taxons do!
    # - implementation.Model lists these entity-types and process taxons


# entity types:


class World (object):
    """Interface for World mixin."""


class Individual (object):
    """Interface for Individual entity type mixin."""

    # endogenous variables:
    opinion = Variable(
        "opinion",
        "opinion of an individual in the sense of the adaptive voter model, can be 1"
    )
    # TODO: maybe this should be replaced by a variable discrete_opinion in the master data model where an input is the set of possible opinions

    # exogenous variables / parameters:


class Culture (object):
    """Interface for Culture process taxon mixin."""

    # endogenous variables:
    aquaintance_network = D.CUL.acquaintance_network

    # exogenous variables / parameters:
