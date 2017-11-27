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
from .. import adaptive_voter_opinion_formation as avof
# TODO: uncomment and adjust only if you really need other variables:
from ... import Variable


class Model (object):
    """Interface for Model mixin."""

    # metadata:
    name = "majority decision"
    """a unique name for the model component"""
    description = "find the opinion the most represented in a social_system"
    """some longer description"""
    requires = [avof]
    """list of other model components required for this model component to
    make sense"""

    # Notes:
    # - Model does NOT define variables or parameters, only entity types
    #   and process taxons do!
    # - implementation.Model lists these entity-types and process taxons


# entity types:


class SocialSystem (object):
    """Interface for SocialSystem entity type mixin."""

    # endogenous variables:

    opinion = avof.Individual.opinion.copy()

    # exogenous variables / parameters:


class Individual (object):
    """Interface for Individual entity type mixin."""

    # endogenous variables:

    opinion = avof.Individual.opinion

    # exogenous variables / parameters:


class Culture (object):
    """Interface for Culture process taxon mixin."""

    # endogenous variables:
    acquaintance_network = D.CUL.acquaintance_network

    # exogenous variables / parameters:
