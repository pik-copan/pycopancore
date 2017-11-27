"""The exploit_social_learning.world class.

In this module the exploit_social_learning World mixing class inherits from
World_ in that basic variables and parameters are defined.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

import numpy as np
from pycopancore.model_components import abstract
from pycopancore.model_components.exploit_social_learning import interface as I


class World (I.World, abstract.World):
    """Define properties of exploit_social_learning.world.

    Inherits from I.World as the interface with all necessary variables
    and parameters.
    """

    def __init__(self,
                 *,
                 contact_network=None,
                 agent_list=[],
                 **kwargs
                 ):
        """Initialize an instance of World.

        Parameters
        ----------
        agent_list
        """
        super(World, self).__init__(**kwargs)

        self.contact_network = contact_network
        self.agent_list = agent_list
        # assert isinstance(self.contact_network, np.ndarray),\
        #     'Given network is not an numpy.ndarray.'
        # assert (len(self.agent_list) == len(self.contact_network[:, 0]) and
        #         len(self.agent_list) == len(self.contact_network[0, :])),\
        #     'agent_list and contact_network do not have suitable dimensions.'
        # # Make sure that all diagonal entries are zero.
        # np.fill_diagonal(self.contact_network, 0)

    processes = []

    def has_neighbor(self, agent):
        """Return True if agent has a neighbor and False if not.

        Parameters
        ----------
        agent Agent: Individual or SocialSystem

        Return
        ------
        boolean
        """
        assert agent in self.agent_list, 'agent is not in agent_list'
        index = self.agent_list.index(agent)
        isolated = True
        i = 0
        n = self.contact_network[0].size

        while isolated and i < n:
            if self.contact_network[index, i] != 0:
                isolated = False
            i += 1
        return not isolated

    def get_random_neighbor(self, agent):
        """Return a random neighbor of agent.

        Parameters
        ----------
        agent Agent: Individual or SocialSystem

        Return
        ------
        neighbor Agent
        """
        assert agent in self.agent_list, 'agent is not in agent_list'
        neighbors = self.get_neighbors(agent)
        neighbor = np.random.choice(neighbors)
        return neighbor

    def get_neighbors(self, agent):
        """Return a list of the neighbors of agent.

        Parameters
        ----------
        agent Agent: Individual or SocialSystem

        Returns
        -------
        neighbors: A list of all neighbors of agent
        """
        assert agent in self.agent_list, 'agent is not in agent_list'
        index = self.agent_list.index(agent)
        n = self.contact_network[0].size
        neighbors = []
        for i in range(n):
            if self.contact_network[index, i] != 0:
                neighbors.append(self.agent_list[i])
        return neighbors

    def get_non_neighbors(self, agent):
        """Return a list of all agents that are not connected to agent.

        Parameters
        ----------
        agent Agent: Individual or SocialSystem

        Returns
        -------
        non_neighbors: A list of all agents that are no neighbors of agent
        """
        assert agent in self.agent_list, 'agent is not in agent_list'
        index = self.agent_list.index(agent)
        n = self.contact_network[0].size
        non_neighbors = []
        for i in range(n):
            if index != i and self.contact_network[index, i] == 0:
                non_neighbors.append(self.agent_list[i])
        return non_neighbors
