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
# from ... import Variable


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


class Society (object):
    """Interface for Society entity type mixin."""

    # endogenous variables:

    # exogenous variables / parameters:


class Cell (object):
    """Interface for Cell entity type mixin."""

    # endogenous variables:

    # exogenous variables / parameters:


class Individual (object):
    """Interface for Individual entity type mixin."""

    # endogenous variables:

    # exogenous variables / parameters:


# process taxa:


class Nature (object):
    """Interface for Nature process taxon mixin."""

    # endogenous variables:

    # exogenous variables / parameters:


class Metabolism (object):
    """Interface for Metabolism process taxon mixin."""

    # endogenous variables:

    # exogenous variables / parameters:


class Culture (object):
    """Interface for Culture process taxon mixin."""

    # endogenous variables:

    # exogenous variables / parameters:
