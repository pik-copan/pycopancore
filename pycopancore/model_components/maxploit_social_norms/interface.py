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

    strategy = Variable("harvesting strategy",
                        """harvesting strategy of individual, if = 0 -> sustainable""")
    opinion = Variable("harvesting opinion",
                       """Opinion on how one should be harvesting.""")
    imitation_tendency = Variable('imitation tendency', 'former rationality')
    rewiring_prob = Variable('rewiring probability', 'rew. prob.')
    imitation_prob = Variable("imitation probability",
                              """Probability to copy some behaviour or opinion.""")
    average_waiting_time = Variable('estimated waiting time tau', 'tau')
    update_time = Variable('next update time', 'next time for update')

class Group(object):
    """Interface for Group."""

    mean_group_opinion = Variable(
        "mean opinion of group",
        "the mean of opinion, i.e. strategy of all of a groups members",
        default=True)

class Culture(object):
    """Define Interface for Culture."""

    group_membership_network = D.CUL.group_membership_network
    acquaintance_network = D.CUL.acquaintance_network
    last_execution_time = Variable('last exec.time',
                                   'last time a step was executed',
                                   default=-1)
    consensus = Variable('consensus state', 'indicating if consensus is there',
                         default=False)

