"""model component Interface template.

TODO: adjust or fill in code and documentation wherever marked by "TODO:", then
remove these instructions.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

# TODO: use variables from the master data model wherever possible:
from ... import master_data_model as D
# TODO: uncomment and adjust of you need further variables from another
# model component:
# import ..BBB.interface as BBB
# TODO: uncomment and adjust only if you really need other variables:
from ... import Variable  # used for opinion here, maybe that should be included in the master data model? But I wouldn't know how? something like discrete opinion
from ..base import interface as baseI


class Model (object):
    """Interface for Model mixin."""

    # metadata:
    name = "adaptive voter model"
    """a unique name for the model component"""
    description = "..."
    """see (Holme, Newman - 2006)"""
    requires = []
    """list of other model components required for this model component to
    make sense"""

    # Notes:
    # - Model does NOT define variables or parameters, only entity types
    #   and process taxons do!
    # - implementation.Model lists these entity-types and process taxons


# entity types:

class Culture (object):
    """Interface for Culture process taxon mixin."""

    # endogenous variables:
    acquaintance_network = D.CUL.acquaintance_network
    # TODO: give possible_opinions a type, wait for Wolf's choice stuff in the
    # master data model
    possible_opinions = Variable(
        "possible opinions",
        "possible opinions of an individual in the sense of the adaptive voter model"
    )

    opinion_change = Variable("probability to adopt another opinion", "")

    multiple_updates = Variable(
        "number of updates", "number of updates that are done at the same time")

    # exogenous variables / parameters:


class Individual (object):
    """Interface for Individual entity type mixin."""

    # endogenous variables:
    opinion = Variable(
        "opinion",
        "opinion of an individual in the sense of the adaptive voter model"
    )
    """Interface for Culture process taxon mixin."""

    # endogenous variables:
    rewiring_probability = Variable(
        "rewiring probability",
        "rewiring probability phi in the sense of the adaptive voter model by (Holme, Newman - 2006)"
    )

    # exogenous variables / parameters:
