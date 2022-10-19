"""movement growth component interface"""

# This file is part of pycopancore.
#
# Copyright (C) 2022 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from typing import List

# Use variables from the master data model wherever possible
from ... import master_data_model as D

from ... import Variable


class Model (object):
    """Interface for Model mixin."""

    # metadata:
    name = "social movement growth"
    """a unique name for the model component"""
    description = """component encompassing strategies for growth"""
    """some longer description"""
    requires = []
    """list of other model components required for this model component
    to make sense
    """

#
# Entity types
#
class Individual (object):
    """Interface for Individual entity type mixin."""

    # endogenous variables:
    engagement_level = Variable(
        "engagement level",
        """level of engagement of an individual""",
        scale = 'nominal',
        datatype = str,
        levels = ['indifferent', 'support', 'base', 'core']
        )
    
    is_mobilizing = Variable(
        "is mobilizing",
        """whether an individual is mobilizing or not""",
        datatype = bool,
        default = False
        )

    # exogenous variables / parameters:

#
# Process taxa
#
class Culture (object):
    """Interface for Culture process taxon mixin."""

    # endogenous variables:
    acquaintance_network = D.Culture.acquaintance_network
    
    growth_strategy = Variable(
        "growth strategy",
        """strategy ratio followed to grow, 1 is pure organizing,
        0 is pure mobilizing""",
        unit = D.unity,
        lower_bound = 0,
        upper_bound = 1
        )
    
    meeting_rate = Variable(
        "meeting rate",
        """rate at which the group meets to decide on their
        strategy""",
        unit = D.years**(-1),
        lower_bound = 0,
        is_intensive = True,
        default = 1 / D.months
        )
    
    interaction_rate = Variable(
        "interaction rate",
        """rate at which people interact when mobilizing""",
        unit = D.years**(-1),
        lower_bound = 0,
        is_intensive = True,
        default = 1 / D.weeks
        )
    
    mobilizing_success_probability = Variable(
        "mobilizing success probability",
        """probability to actually mobilize an individual""",
        unit = D.unity,
        lower_bound = 0,
        upper_bound = 1
        )
    
    organizing_success_probability = Variable(
        "organizing success probability",
        """probability to actually organize an individual""",
        unit = D.unity,
        lower_bound = 0,
        upper_bound = 1
        )

    # exogenous variables / parameters:
