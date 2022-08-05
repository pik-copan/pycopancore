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
import networkx as nx


class Culture (I.Culture):
    """Culture process taxon mixin for exploit_social_learning."""

    # process-related methods:

    def social_update(self, t):
        """Execute the social update.

        Parameters
        ----------
        t : float
            time

        Returns
        -------

        """
        self.last_execution_time = t
        agent_i = self.get_update_agent()

        # Step (1)
        if self.acquaintance_network.neighbors(agent_i):
            agent_j = np.random.choice(
                list(self.acquaintance_network.neighbors(agent_i)))
            # Step (2): Compare strategies of i and j:
            # If they are the same, do nothing. Else change i's behaviour.
            if agent_i.behaviour != agent_j.behaviour:
                # Step (2.1)
                if np.random.random() < agent_i.rewiring_prob:
                    self.reconnect(agent_i, agent_j)
                # Step (2.2)
                else:
                    self.change_strategy(agent_i, agent_j)
        # Step (3)
        self.set_new_update_time(agent_i)

        if self.check_for_consensus():
            print('Consensus! time ', t)

    def reconnect(self, agent_i, agent_j):
        """Reconnect agent_i from agent_j and connect it to k.

        Disconnect agent_i from agent_j and connect agent_i
        to a randomly chosen agent_k with the same behaviour,
        agent_i.behaviour == agent_k.behaviour.

        Parameters
        ----------
        agent_i : Agent (Individual or SocialSystem)
        agent_j : Agent (Individual or SocialSystem)

        Returns
        -------

        """
        # Find a random stranger agent_k with same behaviour as agent_i
        all_non_neighbors = \
            list(set(self.acquaintance_network.nodes())
                 - set(self.acquaintance_network.neighbors(agent_i)))
        strategy_i = agent_i.behaviour
        for stranger in all_non_neighbors:
            if stranger.behaviour != strategy_i:
                all_non_neighbors.remove(stranger)
        if not all_non_neighbors:
            print('No possible neighbors with different behaviour.')
        else:
            # Disconnect agent_i and agent_j
            self.acquaintance_network.remove_edge(agent_i, agent_j)
            # Connect agent_i and agent_k
            agent_k = np.random.choice(all_non_neighbors)
            self.acquaintance_network.add_edge(agent_i, agent_k)

    def change_strategy(self, agent_i, agent_j):
        """Change behaviour of agent_i to agent_j's.

        Change the behaviour of agent_i to the behaviour of agent_j
        depending on their respective harvest rates and the imitation tendency
        according to a sigmoidal function.

        Parameters
        ----------
        agent_i : Agent (Individual or SocialSystem)
            Agent i whose behaviour is to be changed to agent j's behaviour
        agent_j : Agent (Individual or SocialSystem)
            Agent j whose behaviour is imitated
        Returns
        -------

        """
        probability = 0.5 * np.tanh(agent_i.imitation_tendency *
                                    (agent_j.get_harvest_rate() -
                                     agent_i.get_harvest_rate()) + 1)
        if np.random.random() < probability:
            agent_i.behaviour = agent_j.behaviour

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

    def check_for_consensus(self):
        """Check if the model has run into a consensus state.

        The model is in a consensus state if in each connected component
        all agents use the same behaviour. In this case, there will be no more
        change of strategies since the agents are only connected to agents
        with the same behaviour.

        Returns
        -------
        consensus : bool
            True if model is into consensus state, otherwise False
        """
        cc = nx.connected_components(self.acquaintance_network)
        # iterate through all connected components
        for component in cc:
            # iterate through all agents in this component
            stratlist = []
            for j in component:
                # check if all agents of component have the same behaviour
                stratlist.append(j.behaviour)
            if stratlist.count(stratlist[0]) != len(stratlist):
                self.consensus = False
                return self.consensus

        # If in each component, all agents have the same behaviour, then a
        # consensus state is reached
        self.consensus = True
        return self.consensus

    def step_timing(self,
                    t):
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
                       B.Culture.worlds.individuals.behaviour, B.Culture.worlds.individuals.update_time,
                       I.Culture.consensus],
                      [step_timing, social_update])]
