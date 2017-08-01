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
from ... import Variable


class Model (object):
    """Interface for Model mixin."""

    # metadata:
    name = "..."
    """a unique name for the model component"""
    description = "..."
    """some longer description"""
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

    # endogenous variables:
    # TODO: use variables from the master data model wherever possible
    # wherever possible!:
    # X = D.X
    # TODO: uncomment and adjust of you need further variables from another
    # model component:
    # Z = BBB.Z
    # TODO: uncomment and adjust only if you really need other variables:
    # W = Variable("name", "desc", unit=..., ...)

    # exogenous variables / parameters:
    # TODO: similarly



class Individual (object):
    """Interface for Individual entity type mixin."""

    # endogenous variables:
    behavior = Variable("behavior", "Publicly observable behavior of this individual")

    # exogenous variables / parameters:
    degree_preference = Variable("degree preference", "Maximal number of links for this individual")
    disposition = Variable("disposition", "Disposition for a certain behavior")

# process taxa:

class Culture (object):
    """Interface for Culture process taxon mixin."""

    # endogenous variables:
    friendship_network = D.CUL.friendship_network

    eigenvector_centrality = Variable("eigenvector centrality", "eigenvector centrality for all individuals in the network")

    conditional_probability = Variable("conditional probability", "conditional probability of individual dependent on contacts")

    # exogenous variables / parameters:
    n_individual = Variable("number of individuals", "static number of individuals in the network")

