"""model component Interface template.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>

# Use variables from the master data model wherever possible
from ... import master_data_model as D
from ...data_model.master_data_model import CUL

# TODO: uncomment and adjust to use variables from other pycopancore model
# components:
# from ..MODEL_COMPONENT import interface as MODEL_COMPONENT

# TODO: uncomment and adjust only if you really need other variables:
from ... import Variable


class Model (object):
    """Interface for Model mixin."""

    # metadata:
    name = "Granovetter social dynamics"
    """a unique name for the model component"""
    description = """Spreading and fading of one ore more attributes in a 
    network"""
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

    # exogenous variables / parameters:
    activation_threshold = \
        Variable("activation threshold",
                 """share of active nodes above which an individual can 
                 potentially turn active""",
                 unit=D.unity, lower_bound=0, upper_bound=1,
                 is_extensive=False,
                 default=0.6)
    deactivation_threshold = \
        Variable("deactivation threshold",
                 """share of active nodes below which an individual can 
                 potentially turn inactive""",
                 unit=D.unity, lower_bound=0, upper_bound=1,
                 is_extensive=False,
                 default=0.4)
    is_active = \
        Variable("is active",
                 """wether the individual is active or not""",
                 scale="ordinal", levels=[False, True], default=False)
    is_certainly_active = \
        Variable("is certainly active",
                 """wether the individual is certainly active or not""",
                 scale="ordinal", levels=[False, True], default=False)
    is_certainly_inactive = \
        Variable("is certainly inactive",
                 """wether the individual is certainly inactive or not""",
                 scale="ordinal", levels=[False, True], default=False)
    is_contingently_active = \
        Variable("is contingently active",
                 """wether the individual is active or not""",
                 scale="ordinal", levels=[False, True], default=False)
    is_influencable = \
        Variable("is influencable",
                 """wether the individual is influencable or not""",
                 scale="ordinal", levels=[False, True], default=True)
    # instead of all these definitions we could also just set the 
    # (de)activation thresholds accordingly
    activation_probability = \
        Variable("activation probability",
                 """probability an individual turns active once its 
                 activation threshold is reached""",
                 unit=D.unity, lower_bound=0, upper_bound=1,
                 is_extensive=False,
                 default=1)
    deactivation_probability = \
        Variable("deactivation probability",
                 """probability an individual turns inactive once its 
                 deactivation threshold is reached""",
                 unit=D.unity, lower_bound=0, upper_bound=1,
                 is_extensive=False,
                 default=1)
    share_of_active_neighbors = \
        Variable("share of active neighbors",
                 """fraction of neighbors that is active""",
                 unit=D.unity, lower_bound=0, upper_bound=1,
                 is_extensive=False,
                 default=0)
    
#
# Process taxa
#
class Culture (object):
    """Interface for Culture process taxon mixin."""

    # endogenous variables:
    acquaintance_network = CUL.acquaintance_network

    # TODO: uncomment and adjust if you need further variables from another
    # model component:
    # ANOTHERCULTUREVARIABLE= MODEL_COMPONENT.Culture.ANOTHERCULTUREVARIABLE

    # exogenous variables / parameters:
    
    number_of_active_individuals = \
        Variable("number of active individuals",
                 """number of individuals that are active""",
                 unit=D.unity, lower_bound=0,
                 is_extensive=True)
    activity_update_rate = \
        Variable("activity update rate",
                 """rate at which a fraction of individuals update their 
                 activity""",
                 unit=D.weeks**-1, lower_bound=0, default=1)
    
