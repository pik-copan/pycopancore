"""model component Interface exploit_social_learning."""

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
# TODO: uncomment and adjust only if you really need other variables:
from ... import Variable


class Model(object):
    """Interface for Model mixin."""

    # metadata:
    name = "..."
    """Exploit Social Learning"""
    description = "..."
    """The Exploit social learning dynamics including reward based imitation
    behaviour"""
    requires = []
    """list of other model components required for this model component to
    make sense"""


# entity types:
class World(object):
    """Define Interface for World."""

    agent_list = Variable('list of all agents', 'all agents in network')


class Individual(object):
    """Interface for Individual."""

    strategy = Variable('harvesting behaviour', 'harvesting behaviour indiv.')
    imitation_tendency = Variable('imitation tendency', 'former rationality')
    rewiring_prob = Variable('rewiring probability', 'rew. prob.')
    imitation_prob = Variable("imitation probability",
                              """Probability to copy some behaviour or opinion.""")
    average_waiting_time = Variable('estimated waiting time tau', 'tau')
    update_time = Variable('next update time', 'next time for update')
    opinion = Variable("harvesting opinion",
                       """Opinion on how one should be harvesting.""")

class Cell(object):
    """Interface for Cell."""

    stock = Variable('current stock', 'current stock of resource')
    growth_rate = Variable('growth rate', 'growth rate of resource')


class Culture(object):
    """Define Interface for Culture."""

    acquaintance_network = D.CUL.acquaintance_network
    last_execution_time = Variable('last exec.time',
                                   'last time a step was executed',
                                   default=-1)
    consensus = Variable('consensus state', 'indicating if consensus is there',
                         default=False)
