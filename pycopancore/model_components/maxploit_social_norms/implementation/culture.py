"""Culture process taxon mixing class exploit_social_learning."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from pycopancore.model_components.base import interface as B
from .. import interface as I
from .... import Step

import numpy as np
from scipy.special import expit
import networkx as nx


class Culture (I.Culture):
    """Culture process taxon mixin for exploit_social_learning."""

    # process-related methods:

    def individual_update(self, t):

        self.last_execution_time = t
        agent_i = self.get_update_agent()

        # book keeping
        opinion = agent_i.opinion
        behaviour = agent_i.behaviour
        group_j = list(agent_i.group_memberships)[0] # should be only one
        injunction = group_j.group_opinion

        # Step (1)
        assert (self.acquaintance_network.neighbors(agent_i)
                and self.group_membership_network.successors(agent_i)), "agent not in mandatory networks"
        # Step (2)
        # self.individual_behaviour_switch()
        # Step (3)
        # self.individual_opinion_switch()
        # Step (4)
        # self.set_new_update_time(agent_i)

    def individual_behaviour_switch(self, agent_i):
        """Apply a switch of individuals behaviour, informed by individuals own opinion (cognitive dissonance),
         neighbours behaviour (descriptive norm) and groups opinion (injunctive norm)."""
        # x = 1
        # probability = expit(x)
        # if np.random.random() < probability:
        #     agent_i.behaviour = mean_opinion_j

    def individual_opinion_switch(self, agent_i):
        """Apply a switch of individuals opinion, informed by individuals own behaviour (cognitive dissonance),
         neighbours behaviour (descriptive norm) and groups opinion (injunctive norm)."""

    # def group_opinion_switch(self, unused_t):
    #     """Apply a switch of groups opinion, informed by ?."""
    # for now situated in group.py

    def get_update_agent(self):
        """Return the agent with the closest waiting time.

        Choose from all agents the one with the smallest update_time.
        Returns
        -------

        """
        next_agent = list(self.acquaintance_network.nodes())[0]
        for agent in self.acquaintance_network:
            if agent.update_time < next_agent.update_time:
                next_agent = agent
        return next_agent

    def set_new_update_time(self, agent):
        """Set next time step when agent is to be called again.

        Set the attribute update_time of agent to
        old_update_time + new_update_time, where new_update_time is again
        drawn from an exponential distribution.

        Parameters
        ----------
        agent : Agent (Individual or SocialSystem)
            The agent whose new update_time should be drawn and set.

        Returns
        -------

        """
        # print('old_update_time: ',individual.update_time)
        new_update_time = np.random.exponential(agent.average_waiting_time)
        agent.update_time += new_update_time

    def step_timing(self, t):
        """Return the next time step is to be called.

        This function is used to get to know when the step function is
        to be called.
        Parameters
        ----------
        t : float
            time

        Returns
        -------

        """
        if isinstance(self.last_execution_time, type(None)):
            self.last_execution_time = 0
        if t < self.last_execution_time:
            print('last execution time after t!')

        next_time = list(self.acquaintance_network.nodes())[0].update_time
        for agent in self.acquaintance_network:
            if agent.update_time < next_time:
                next_time = agent.update_time
        if t > next_time:
            print('next update time before t!')
        return next_time

    processes = [Step('Social Update is a step function',
                      [I.Culture.acquaintance_network,
                       B.Culture.worlds.individuals.behaviour,
                       B.Culture.worlds.individuals.opinion,
                       B.Culture.worlds.individuals.update_time],
                      [step_timing, individual_update])]
