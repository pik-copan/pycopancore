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

from ....runners import Hooks

from blist import sortedlist # more performant for large list modifications
import datetime as dt
from enum import Enum, unique
import random
from time import time


class Culture (I.Culture):
    """Culture process taxon mixin implementation class."""

    # standard methods:

    __nodes_by_opinion = None
    __nodes = None
    __filter_by_opinion = lambda opinion, input_list: list(filter(lambda ind: ind.opinion == opinion, input_list))
    __remove_by_opinion = lambda opinion, input_list: list(filter(lambda ind: ind.opinion != opinion, input_list))

    __configuration = dict(configured=False) # keeps the configuration status, whether the updates are done basic or fast, and clusteredd or non-clustered
    """configuration status"""
    @unique
    class update_modes(Enum):
        """update modes for the adaptive voter model: basic or fast"""
        basic = 0
        fast = 1

    def __init__(self,
                 *,
                 rewiring,
                 opinion_change = 1.0,
                 timestep=0.1,
                 possible_opinions={0,1},
                 active_neighbor_only = True,
                 **kwargs):
        """Initialize the unique instance of Culture.
        
        Parameters
        ----------
        rewiring : float or function
            if float: probability of rewiring
            if function: decide whether the link between the two individuals is separated and a link to a new individual is created
                takes: active_individual, active_individuals_neighbor
                
        opinion_change: float or function, optional, default:  1
            if float: probability of opinion adaption if there was no rewiring
            if function:  decide whether the opinion of the neighbor should be adopted
                takes: active_individual, active_individuals_neighbor
                
        timestep : float, optional, default: 0.1
            interval between opinion updates
              
        possible_opinions : set-like, optional, default: {0, 1}
            set of possible options the individuals can take
            
        active_neighbor_only : bool, optional, default: True
            if False: any neighbor of the active individual is chosen randomly
            if True: only neighbors with different opinions are chosen randomly (if there is at least one, else nothing is done)
        """
        super().__init__(**kwargs)

        # TODO: ask Jobst, whether this should get the network as input so it could be applied to different networks... seems sensible too me but might contradict the frameworks idea

        _rewiring = rewiring
        if not callable(rewiring):
            if rewiring == 1:
                _rewiring = lambda x, y: True
            else:
                assert 0 < rewiring < 1, "rewiring_probability should be a float between 0 and 1 or a function"
                _rewiring = lambda x, y: random.random() < rewiring
        self.rewiring = _rewiring

        if not callable(opinion_change):
            if opinion_change == 1:
                opinion_change = lambda x, y: True
            else:
                opinion_change = lambda x, y: random.random < opinion_change
        self.opinion_change = opinion_change

        self.possible_opinions = possible_opinions
        self.active_neighbor_only = active_neighbor_only

        self.next_update_time = 0
        self.timestep = timestep

    # process-related methods:

    def analyze_graph(self, t):
        """analyze the graph so speed-ups can be used later"""
        # TODO: test whether sortedlist or sets are faster for large numbers of entries
        assert t == 0, "This function should be run as a pre-hook of the runner!"
        print("    analyzing the graph ... ", end="", flush=True)
        start = time()

        self.__nodes = sortedlist(self.acquaintance_network.nodes())
        self.__nodes_by_opinion = {opinion : sortedlist() for opinion in self.possible_opinions}
        for node in self.acquaintance_network:
            self.__nodes_by_opinion[node.opinion].add(node)

        print("done ({})".format(dt.timedelta(seconds=(time() - start))))

    def clear_graph_analysis(self, t):
        """clear everything that was created during analyze_graph"""
        print("    deleting lists from graph analysis")
        del self.__nodes
        del self.__nodes_by_opinion

    def opinion_update_basic(self, t):
        """update the aquaintance network following the adaptive voter model prescription by (Holme, Newman - 2006)"""
        # this code is currently only precisely following the model prescription
        # without any additional speed-ups

        nodes = self.acquaintance_network.nodes()

        active_individual = random.choice(nodes)
        neighbors = self.acquaintance_network.neighbors(active_individual)
        if self.active_neighbor_only:
            active_neighbors = Culture.__remove_by_opinion(active_individual.opinion, neighbors)
            if not active_neighbors:
                return  # nothing to be done
            active_neighbor = random.choice(active_neighbors)
        else:
            active_neighbor = random.choice(neighbors)

        # decide whether to rewire or to adopt the opinion
        if self.rewiring(active_individual, active_neighbor):
            # rewire
            possible_new_neighbors = Culture.__filter_by_opinion(active_individual.opinion, nodes)
            if not possible_new_neighbors:
                return # can't find a new one, active_individual is the last one
            new_neighbor = random.choice(possible_new_neighbors)
            # new_neighbor = random.choice(list(filter(lambda x: x.opinion == active_individual.opinion, self.acquaintance_network.nodes())))
            self.acquaintance_network.remove_edge(active_individual, active_neighbor)
            self.acquaintance_network.add_edge(active_individual, new_neighbor)
        elif self.opinion_change(active_individual, active_neighbor):
            # adopt opinion
            active_individual.opinion = active_neighbor.opinion

    def opinion_update_fast(self, t):
        """update the aquaintance network following the adaptive voter model prescription by (Holme, Newman - 2006)"""
        # TODO: there are some intuitive speed-ups:
        #   1) (done) use a list with references to nodes of the differing opinions so the statement with filter can be avoided
        #   2) cluster the updates instead of making every update separately
        #       ... this should probably be done as a separate function calling one of the opinion_update_basic/fast functions
        #       ... make sure that the rest of the model works on longer time scales if you do that
        #       ... introduce a time scale for that

        # choose only between the active nodes, which are the keys of this sortedset
        active_individual = random.choice(self.__nodes)
        neighbors = self.acquaintance_network.neighbors(active_individual)
        if self.active_neighbor_only:
            active_neighbors = Culture.__remove_by_opinion(active_individual.opinion, neighbors)
            if not active_neighbors:
                return  # nothing to be done
            active_neighbor = random.choice(active_neighbors)
        else:
            active_neighbor = random.choice(neighbors)

        # decide whether to rewire or to adopt the opinion
        if self.rewiring(active_individual, active_neighbor):
            # rewire

            # find new neighbor with same opinion
            if not self.__nodes_by_opinion[active_individual.opinion]:
                return # active_individual is the last one with this opinion and cannot connect to a new one
            new_neighbor = random.choice(self.__nodes_by_opinion[active_individual.opinion])
            # remove old link
            self.acquaintance_network.remove_edge(active_individual, active_neighbor)
            # add new link
            self.acquaintance_network.add_edge(active_individual, new_neighbor)
        elif self.opinion_change(active_individual, active_neighbor):
            # adopt opinion

            # move the active individual to the new opinion list
            self.__nodes_by_opinion[active_individual.opinion].remove(active_individual)
            self.__nodes_by_opinion[active_neighbor.opinion].add(active_individual)
            # set the new opinion
            # TODO: ask Jobst, whether this is okai within his framework!
            active_individual.opinion = active_neighbor.opinion


    def next_update_time(self, t):
        self.next_update_time += self.timestep
        return self.next_update_time

    @classmethod
    def configure(cls, *, update_mode, synchronous_updates=1):
        """configure the adaptive voter opinion formation model component
        
        Parameters
        ----------
        
        update_mode : element of Enum Cultur.update_modes
            chooses between the basic and the fast update mode. The fast update mode is preferred but needs the nodes of the acquaintance_network to stay the same
        
        synchronous_updates : (optional) positive int
            how many opinion updates should be done at once
        """

        synchronous_updates = int(synchronous_updates)
        assert synchronous_updates >= 1, "can't do a non-positive number of synchronous updates"

        assert update_mode in Culture.update_modes, "choose an update mode from Culture.update_modes Enum"

        if synchronous_updates > 1:
            raise NotImplementedError("synchronous updates are not yet implemented")

        process_type = Step
        process_name = "opinion update"
        process_variables = [I.Culture.acquaintance_network, I.Individual.opinion]
        process_time = cls.next_update_time

        if update_mode is Culture.update_modes.basic:
            process_func = cls.opinion_update_basic
        elif update_mode is Culture.update_modes.fast:
            process_func = cls.opinion_update_fast
            Hooks.register_hook(Hooks.Types.pre, cls.analyze_graph, I.Culture)
            Hooks.register_hook(Hooks.Types.post, cls.clear_graph_analysis, I.Culture)
        else:
            raise ValueError("unknown update_mode '{}'".format(update_mode))

        cls.__configuration = dict(
            configured=True,
            process_type=process_type,
            update_mode=update_mode,
            synchronous_updates=synchronous_updates
        )

        cls.processes = [
            process_type(
                process_name,
                process_variables,
                [process_time, process_func]
            )
        ]

# set the default configuration of the model component
Culture.configure(update_mode=Culture.update_modes.fast)