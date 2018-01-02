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


class SocialSystem (object):
    """Interface for SocialSystem entity type mixin."""

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
    
    renewable_subsidy_intro_threshold = \
        Variable("renewable subsidy introduction threshold",
                 "share of environmentally friendly voters needed to introduce"
                 "a subsidy for renewables",
                 unit=D.unity, lower_bound=0, upper_bound=1, default=1/2)
        
    emissions_tax_intro_threshold = \
        Variable("emissions tax introduction threshold",
                 "share of environmentally friendly voters needed to introduce"
                 "an emissions tax",
                 unit=D.unity, lower_bound=0, upper_bound=1, default=2/3)

    fossil_ban_intro_threshold = \
        Variable("fossil ban introduction threshold",
                 "share of environmentally friendly voters needed to ban"
                 "fossil fuels",
                 unit=D.unity, lower_bound=0, upper_bound=1, default=3/4)

    renewable_subsidy_keeping_threshold = \
        Variable("renewable subsidy keeping threshold",
                 "share of environmentally friendly voters needed to keep "
                 "a subsidy for renewables",
                 unit=D.unity, lower_bound=0, upper_bound=1, default=1/3)
        
    emissions_tax_keeping_threshold = \
        Variable("emissions tax keeping threshold",
                 "share of environmentally friendly voters needed to keep "
                 "an emissions tax",
                 unit=D.unity, lower_bound=0, upper_bound=1, default=1/2)

    fossil_ban_keeping_threshold = \
        Variable("fossil ban keeping threshold",
                 "share of environmentally friendly voters needed to keep "
                 "a ban on fossil fuels",
                 unit=D.unity, lower_bound=0, upper_bound=1, default=2/3)
