"""movement growth component interface

TODO: adjust or fill in code and documentation wherever marked by "TODO:", then
remove these instructions.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2022 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>

from typing import List

# Use variables from the master data model wherever possible
from ... import master_data_model as D

# TODO: uncomment and adjust to use variables from other pycopancore model
# components:
# from ..MODEL_COMPONENT import interface as MODEL_COMPONENT

# TODO: uncomment and adjust only if you really need other variables:
from ... import Variable


class Model (object):
    """Interface for Model mixin."""

    # metadata:
    name = "social movement growth"
    """a unique name for the model component"""
    description = "component encompassing strategies for growth"
    """some longer description"""
    requires = []
    """list of other model components required for this model component to
    make sense"""

    # Notes:
    # - Model does NOT define variables or parameters, only entity types
    #   and process taxons do!
    # - implementation.Model lists these entity-types and process taxons


#
# Entity types
#
class Individual (object):
    """Interface for Individual entity type mixin."""

    # endogenous variables:
        
    # TODO: use variables from the master data model wherever possible
    # wherever possible!:
    # ONEINDIVIDUALVARIABLE = master_data_model.Individual.ONEINDIVIDUALVARIABLE

    # TODO: uncomment and adjust if you need further variables from another
    # model component:
    # ANOTHERINDIVIDUALVARIABLE= MODEL_COMPONENT.Individual.ANOTHERINDIVIDUALVARIABLE

    # TODO: uncomment and adjust only if you really need other variables:
    # PERSONALINDIVIDUALVARIABLE = Variable("name", "desc", unit=..., ...)
    engagement_level = Variable(
        "engagement level",
        "level of engagement of an individual",
        scale = 'nominal',
        datatype = str,
        levels = ['inactive', 'support', 'base', 'core']
        )
    
    is_mobilizing = Variable(
        "is mobilizing",
        "whether an individual is mobilizing or not",
        datatyp = bool,
        default = False
        )
    
    interaction_rate = Variable(
        "interaction rate",
        "rate at which people interact when mobilizing",
        unit = D.days**(-1),
        lower_bound = 0,
        is_intensive = True,
        default = 1 / D.days
        )

    # exogenous variables / parameters:

#
# Process taxa
#
class Culture (object):
    """Interface for Culture process taxon mixin."""

    # endogenous variables:
    acquaintance_network = D.Culture.acquaintance_network

    # TODO: use variables from the master data model wherever possible
    # wherever possible!:
    # ONECULTUREVARIABLE = master_data_model.Culture.ONECULTUREVARIABLE

    # TODO: uncomment and adjust if you need further variables from another
    # model component:
    # ANOTHERCULTUREVARIABLE= MODEL_COMPONENT.Culture.ANOTHERCULTUREVARIABLE

    # TODO: uncomment and adjust only if you really need other variables:
    # PERSONALCULTUREVARIABLE = Variable("name", "desc", unit=..., ...)
    growth_strategy = Variable(
        "growth strategy",
        "strategy ratio followed to grow, 1 is pure organizing, 0 is pure mobilizing",
        unit = D.unity,
        lower_bound = 0,
        upper_bound = 1
        )
    
    meeting_rate = Variable(
        "action rate",
        "rate at which the group meets to decide on their strategy",
        unit = D.months**(-1),
        lower_bound = 0,
        is_intensive = True,
        default = 1 / D.months
        )
    
    organizing_success_probability = Variable(
        "organizing success probability",
        "probability of organizing success",
        unit = D.unity,
        lower_bound = 0,
        upper_bound = 1
        )
    
    mobilizing_success_probability = Variable(
        "mobilizing success probability",
        "probability of mobilizing success",
        unit = D.unity,
        lower_bound = 0,
        upper_bound = 1
        )

    # exogenous variables / parameters:
