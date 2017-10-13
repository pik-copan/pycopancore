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
from ...data_model.master_data_model import S
# TODO: uncomment and adjust of you need further variables from another
# model component:
# import ..BBB.interface as BBB
# TODO: uncomment and adjust only if you really need other variables:
from ... import Variable


class Model (object):
    """Interface for Model mixin."""

    # metadata:
    name = "voting on climate policy"
    """a unique name for the model component"""
    description = "individuals vote on different climate policy measures" \
        "based on their environmental friendliness"
    """some longer description"""
    requires = []
    """list of other model components required for this model component to
    make sense"""


# entity types:


class Society (object):
    """Interface for Society entity type mixin."""

    # endogenous variables:
    
    has_renewable_subsidy = S.has_renewable_subsidy
    has_emissions_tax = S.has_emissions_tax
    has_fossil_ban = S.has_fossil_ban

    # exogenous variables / parameters:

    emissions_tax_level = S.emissions_tax_level
    renewable_subsidy_level = S.renewable_subsidy_level

    time_between_votes = \
        Variable("time between votes",
                 "every how many years votes are taken",
                 unit=D.years, strict_lower_bound=0, default=4)
    
    renewable_subsidy_threshold = \
        Variable("renewable subsidy threshold",
                 "share of environmentally friendly voters needed to introduce"
                 "a subsidy for renewables",
                 unit=D.unity, lower_bound=0, upper_bound=1, default=1/2)
        
    emissions_tax_threshold = \
        Variable("emissions tax threshold",
                 "share of environmentally friendly voters needed to introduce"
                 "an emissions tax",
                 unit=D.unity, lower_bound=0, upper_bound=1, default=2/3)

    fossil_ban_threshold = \
        Variable("fossil ban threshold",
                 "share of environmentally friendly voters needed to ban"
                 "fossil fuels",
                 unit=D.unity, lower_bound=0, upper_bound=1, default=3/4)
