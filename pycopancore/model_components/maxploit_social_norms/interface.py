"""model component Interface maxploit_social_norms."""

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
from ..maxploit_individual_layer import interface as I
# import ..BBB.interface as BBB
# TODO: uncomment and adjust only if you really need other variables:
from ... import Variable


class Model(object):
    """Interface for Model mixin."""

    # metadata:
    name = "..."
    """Maxploit group rewiring"""
    description = "..."
    """Additional social rewiring in context of group membership as added to exploit in the maxploit model"""
    requires = []
    """list of other model components required for this model component to
    make sense"""


class Individual(object):
    """Interface for Individual."""

    behaviour = Variable("harvesting behaviour",
                        """harvesting behaviour of individual, if = 0 -> sustainable""")
    opinion = Variable("harvesting opinion",
                       """Opinion on how one should be harvesting.""")
    descriptive_norm = Variable("descriptive norm",
                                """mean behaviour in acquaintance network of individual""",
                                default=0)
    descriptive_norm_binary = Variable("descriptive norm binary",
                                """mean behaviour in acquaintance network of individual coded as binary""")
    average_waiting_time = Variable('estimated waiting time tau', 'tau', default=1)
    update_time = Variable('next update time', 'next time for update')

class Group(object):
    """Interface for Group."""

    group_opinion = Variable(
        "fixed opinion",
        "the group opinion on how to harvest"
    )

    mean_group_opinion = Variable(
        "mean opinion of group",
        "the mean of opinion on how to harvest of all of a groups members",
        default=0
    )

    mean_group_behaviour = Variable(
        "mean behaviour of group",
        "the mean of behaviour of all of a groups members",
        default=0
    )

    group_meeting_interval = Variable(
        "timestep for meeting",
        """gives the time interval for group meetings in which opinions can change""",
        default=1
    )

    group_update_probability = Variable(
        "probability for an update",
        """the probability that a group will consider updating their opinion""",
        default=1
    )


class Culture(object):
    """Define Interface for Culture."""

    #parameters for the logit
    weight_injunctive = Variable('Weight for Injunction',
                                 """Weight for the injuctive Norm influence""",
                                 default=0.5)
    weight_descriptive = Variable('Weight for Descriptive Norm',
                                 """Weight for the descriptive Norm influence""",
                                 default=0.5)
    weight_dissonance =  Variable('Weight for Cognitive Dissonance',
                                 """Weight for the Cognitive Dissonance influence""",
                                 default=0.5)
    k_value = Variable('k value',
                       """Value for trimming the possibilites form the logit distribution. 
                       The default of k = 2.94445 produces probabilites of 0.05, 0.5 and 0.95 for
                       2 x_values element [0,1] and their combinations.""",
                       default=2.94445
                       )


    majority_threshold = Variable('Treshold for majority',
                                 """Trehshold for a majority of individual opinions in a group being considered group opinion""",
                                 default=0.5)

    fix_group_opinion = Variable("Fixed group opinion",
                                 """Fixes the group opinion so it does not change, i.e. group becomes a fixed norm.""",
                                 default=False,
                                 datatype=bool)

    group_membership_network = D.CUL.group_membership_network
    acquaintance_network = D.CUL.acquaintance_network
    average_waiting_time = Individual.average_waiting_time.copy()
    individual_updating_probability = Variable("prob",
                                               "blalbla no time",
                                               default=0.1)
    ast_execution_time = Variable('last exec.time',
                                   'last time a step was executed',
                                   default=-1)
    consensus = Variable('consensus state', 'indicating if consensus is there',
                         default=False)

