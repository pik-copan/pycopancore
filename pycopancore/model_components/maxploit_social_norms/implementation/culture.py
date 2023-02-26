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
from .... import Step, Event

import numpy as np
from scipy.special import expit
import networkx as nx


class Culture (I.Culture):
    """Culture process taxon mixin for exploit_social_learning."""

    # process-related methods:

    def individual_update(self, t):

        w = list(self.worlds)[0]
        agents = list(w.individuals)
        # agent_i = np.random.choice(agents)

        for agent_i in agents:
            agent_i.update_time = np.random.exponential()

        ordered_list = agents
        n = len(ordered_list)
        for i in range(n):
            already_sorted = True
            for j in range(n-i-1):
                if ordered_list[j].update_time > ordered_list[j+1].update_time:
                    ordered_list[j], ordered_list[j+1] = ordered_list[j+1], ordered_list[j]
                    already_sorted = False
            if already_sorted:
                break


        for agent_i in ordered_list:
            # print("Update prob.:", agent_i.update_probability)
            if np.random.uniform() < agent_i.update_probability:
                # attitude = agent_i.attitude
                # behaviour = agent_i.behaviour
                group_j = np.random.choice(list(agent_i.group_memberships))

                # Step (1)
                assert (self.acquaintance_network.neighbors(agent_i)
                        and self.group_membership_network.successors(agent_i)), "agent not in mandatory networks"
                # Step (2)
                self.individual_behaviour_switch(agent_i, group_j)
                # self.descriptive_only(agent_i)
                # self.injunctive_only(agent_i, group_j)
                # Step (3)
                # self.individual_attitude_switch(agent_i)
                # Step (4)

    def individual_behaviour_switch(self, agent_i, group_j):
        """Apply a switch of individuals behaviour, informed by individuals own attitude (cognitive dissonance),
         neighbours behaviour (descriptive norm) and groups attitude (injunctive norm)."""

        injunctive_norm = group_j.group_attitude
        if injunctive_norm == 0: # for symmetric probabilities in the logit
            injunctive_norm = -1

        descriptive_norm = self.get_descriptive_norm(agent_i)
        if descriptive_norm is not None:
            if descriptive_norm > self.descriptive_majority_threshold:
                descriptive_norm = 1
            else:
                descriptive_norm = 0

            # descriptive_norm = agent_i.descriptive_norm_binary
            if descriptive_norm == 0:
                descriptive_norm = -1
            x = self.weight_descriptive * descriptive_norm + self.weight_injunctive * injunctive_norm
            probability_distribution = expit(self.k_value*x)
            if agent_i.behaviour == 0:
                probability = probability_distribution
            else:
                probability = 1 - probability_distribution
            # print(injunctive_norm, descriptive_norm, probability)
            if np.random.random() < probability:
                agent_i.behaviour = int(not agent_i.behaviour)

    def descriptive_only(self, agent_i):
        descriptive_norm = self.get_descriptive_norm(agent_i)
        if descriptive_norm is not None:
            if descriptive_norm > self.majority_threshold:
                descriptive_norm = 1
            else:
                descriptive_norm = 0

            if agent_i.behaviour != descriptive_norm:
                if descriptive_norm == 0:
                    descriptive_norm = -1
                x = self.weight_descriptive * descriptive_norm
                probability_distribution = expit(self.k_value*x)
                if agent_i.behaviour == 0:
                    probability = probability_distribution
                else:
                    probability = 1 - probability_distribution
                # print(injunctive_norm, descriptive_norm, probability)
                if np.random.random() < probability:
                    agent_i.behaviour = int(not agent_i.behaviour)

    def injunctive_only(self, agent_i, group_j):
        # print("New agent.")
        injunctive_norm = group_j.group_attitude
        # print(group_j, "Group attitude of this agent...", injunctive_norm)
        if injunctive_norm == 0: # for symmetric probabilities in the logit
            injunctive_norm = -1
        x = self.weight_injunctive * injunctive_norm
        probability_distribution = expit(self.k_value*x)
        if agent_i.behaviour == 0:
            probability = probability_distribution
        else:
            probability = 1 - probability_distribution
        # print(injunctive_norm, descriptive_norm, probability)
        # print(probability)
        if np.random.random() < probability:
            # print(agent_i.behaviour, "Behaviour before...")
            agent_i.behaviour = int(not agent_i.behaviour)
            # print(agent_i.behaviour, "Behaviour after...")

    # def individual_attitude_switch(self, agent_i):
    #     """Apply a switch of individuals attitude, informed by individuals own behaviour,
    #      neighbours behaviour (descriptive norm) and groups attitude (injunctive norm)."""


    def get_descriptive_norm(self, agent_i):
        """Calculate the descriptive norm in a less time expensive fashion than
        via an explicit method in individual. Also tries to use as little networkx stuff as possible"""
        if not list(agent_i.acquaintances):
            descriptive_norm = None
        else:
            n = 0
            N = 0
            for i in list(agent_i.acquaintances):
                N += 1
                if i.behaviour:
                    n += 1
            # N = len(list(agent_i.acquaintances))
            assert N > 0
            descriptive_norm = n/N
        return descriptive_norm

    def next_update_time(self, t):
        return t + np.random.exponential(self.average_waiting_time)



    processes = [Event("Social Update",
                      [B.Culture.worlds.individuals.behaviour],
                      ["time", next_update_time, individual_update])]
