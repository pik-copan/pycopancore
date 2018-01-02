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
from .. import majority_decision as md
from .. import anderies_carbon_cycle as cc
# TODO: uncomment and adjust only if you really need other variables:
from ... import Variable


class Model (object):
    """Interface for Model mixin."""

    # metadata:
    name = "carbon voters"
    """a unique name for the model component"""
    description = "sets the harvest rate by majority decision and " \
                  "the probability of awareness opinion adoption is dependent on atmospheric carbon"
    """some longer description"""
    requires = [avof, md, cc]
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
    atmospheric_carbon = cc.World.atmospheric_carbon
    # TODO: uncomment and adjust only if you really need other variables:
    # W = Variable("name", "desc", unit=..., ...)

    # exogenous variables / parameters:
    # surface_air_temperature = D.world.surface_air_temperature


class SocialSystem (object):
    """Interface for SocialSystem entity type mixin."""

    # endogenous variables:

    # exogenous variables / parameters:

    opinion = md.SocialSystem.opinion

    harvest_rate = cc.SocialSystem.harvest_rate


# class Cell (object):
#     """Interface for Cell entity type mixin."""
#
#     # endogenous variables:
#
#     # exogenous variables / parameters:


# class Individual (object):
#     """Interface for Individual entity type mixin."""
#
#     # endogenous variables:
#
#     # exogenous variables / parameters:


# process taxa:


# class Environment (object):
#     """Interface for Environment process taxon mixin."""
#
#     # endogenous variables:
#
#     # exogenous variables / parameters:


# class Metabolism (object):
#     """Interface for Metabolism process taxon mixin."""
#
#     # endogenous variables:
#
#     # exogenous variables / parameters:


class Culture (object):
    """Interface for Culture process taxon mixin."""

    # endogenous variables:

    # exogenous variables / parameters:
    #
    opinion_change = avof.Culture.opinion_change

    impact_scaling_factor = Variable("scaling factor", "")

    no_impact_atmospheric_carbon_level = Variable("", "level of atmospheric carbon that doesn't change peoples "
                                                      "probability of opinion change to awareness")

    no_impact_opinion_change = Variable("", "basic probability of opinion change to awareness in "
                                            "avof without climate impact effects")  # take adaptive voter model opinion_change?

    impact = Variable("impact of atmospheric carbon / temperature on social_system",
                      "based on atmospheric carbon level")
