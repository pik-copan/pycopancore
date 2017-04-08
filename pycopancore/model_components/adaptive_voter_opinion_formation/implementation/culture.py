"""Culture process taxon mixing class template.

TODO: adjust or fill in code and documentation wherever marked by "TODO:",
then remove these instructions
"""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from .. import interface as I
#from .... import master_data_model as D
from .... import Step

from blist import sorteddict, sortedlist # blist are more performant for modifying large lists
from enum import Enum
import profilehooks as ph
import random

# class DummyFunction(object):
#     def __init__(self, error_msg):
#         self.error_msg = error_msg
#     def __call__(self, *args, **kwargs):
#         raise RuntimeError(self.error_msg)



class Culture (I.Culture):
    """Culture process taxon mixin implementation class."""

    # standard methods:

    # __opinion_update = DummyFunction("choose the correct opinion_update function")

    __nodes_by_opinion = None
    __nodes = None
    __filter_by_opinion = lambda opinion, input_list: list(filter(lambda ind: ind.opinion == opinion, input_list))
    __remove_by_opinion = lambda opinion, input_list: list(filter(lambda ind: ind.opinion != opinion, input_list))

    def __init__(self,
                   *,
                 rewiring_probability,
                 timestep=0.1,
                 possible_opinions={0,1},
                 # update_method=UPDATE_METHOD.basic,
                 **kwargs):
        """Initialize the unique instance of Culture."""
        super().__init__(**kwargs)

        self.rewiring_probability = rewiring_probability
        self.possible_opinions = possible_opinions

        self.next_update_time = 0
        self.timestep = timestep

    # process-related methods:

    def analyze_graph(self):
        self.__nodes = sortedlist(self.acquaintance_network.nodes())
        self.__nodes_by_opinion = {opinion : sortedlist() for opinion in self.possible_opinions}
        for node in self.acquaintance_network:
            self.__nodes_by_opinion[node.opinion].add(node)

    # @ph.profile
    def opinion_update_basic(self, t):
        """update the aquaintance network following the adaptive voter model prescription by (Holme, Newman - 2006)"""
        # this code is currently only precisely following the model prescription
        # without any additional speed-ups

        nodes = self.acquaintance_network.nodes()
        nopinion0 = len(list(filter(lambda x: x.opinion == 0, nodes)))
        print("\tt = {t:>4.1f}; nopinion0 = {nopinion0:>3d}".format(**locals()))

        active_individual = random.choice(nodes)
        active_neighbor = random.choice(self.acquaintance_network.neighbors(active_individual))

        # check if link is active, i.e. the opinions differ
        if active_individual.opinion != active_neighbor.opinion:
            # link is active and something is to be done
            # decide randomly whether to rewire or to adopt the opinion
            if random.random() < self.rewiring_probability:
                # rewire
                # TODO: add check that this is possible, to be combined with the speed-ups
                #
                new_neighbor = random.choice(Culture.__filter_by_opinion(active_individual.opinion, nodes))
                # new_neighbor = random.choice(list(filter(lambda x: x.opinion == active_individual.opinion, self.acquaintance_network.nodes())))
                self.acquaintance_network.remove_edge(active_individual, active_neighbor)
                self.acquaintance_network.add_edge(active_individual, new_neighbor)
            else:
                # adopt opinion
                # TODO: ask Jobst, whether this is okai within his framework!
                active_individual.opinion = active_neighbor.opinion
        # else: do nothing

    # @ph.profile
    def opinion_update_fast(self, t):
        """update the aquaintance network following the adaptive voter model prescription by (Holme, Newman - 2006)"""
        # TODO: there are some intuitive speed-ups:
        #   1) (done) use a list with references to nodes of the differing opinions so the statement with filter can be avoided
        #   2) cluster the updates instead of making every update separately ... make sure that the rest of the model works on longer time scales if you do that

        nopinion0 = len(self.__nodes_by_opinion[0])
        print("\tt = {t:>4.1f}; nopinion0 = {nopinion0:>3d}".format(**locals()))

        # choose only between the active nodes, which are the keys of this sortedset
        active_individual = random.choice(self.__nodes)
        active_neighbors = Culture.__remove_by_opinion(active_individual.opinion, self.acquaintance_network.neighbors(active_individual))
        if not active_neighbors:
            return # nothing to be done
        active_neighbor = random.choice(active_neighbors)

        # link is active and something is to be done
        # decide randomly whether to rewire or to adopt the opinion
        if random.random() < self.rewiring_probability:
            # rewire
            # TODO: add check that this is possible, to be combined with the speed-ups

            # remove old link
            self.acquaintance_network.remove_edge(active_individual, active_neighbor)
            # find new neighbor with same opinion
            new_neighbor = random.choice(self.__nodes_by_opinion[active_individual.opinion])
            # add new link
            self.acquaintance_network.add_edge(active_individual, new_neighbor)
        else:
            # adopt opinion
            # TODO: ask Jobst, whether this is okai within his framework!

            # move the active individual to the new opinion list
            self.__nodes_by_opinion[active_individual.opinion].remove(active_individual)
            self.__nodes_by_opinion[active_neighbor.opinion].add(active_individual)
            # set the new opinion
            active_individual.opinion = active_neighbor.opinion


    def next_update_time(self, t):
        self.next_update_time += self.timestep
        return self.next_update_time


    # opinion_update = opinion_update_basic # workaround for now
    opinion_update = opinion_update_fast # workaround for now
    processes = [
        Step(
            'opinion update',
            [I.Culture.acquaintance_network, I.Individual.opinion],
            [next_update_time, opinion_update]
        )
    ]
