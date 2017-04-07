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
from .... import Event

import random

class Culture (I.Culture):
    """Culture process taxon mixin implementation class."""

    # standard methods:

    def __init__(self,
                   *,
                rewiring_probability,
                 **kwargs):
        """Initialize the unique instance of Culture."""
        super().__init__(**kwargs)

        self.rewiring_probability = rewiring_probability

    # process-related methods:

    def opinion_update(self, t):
        """update the aquaintance network following the adaptive voter model prescription by (Holme, Newman - 2006)"""
        # this code is currently only precisely following the model prescription
        # without any additional speed-ups
        # there are two intuitive speed-ups:
        #   1) use a list with references to nodes of the differing opinions so the statement with filter can be avoided
        #   2) use a list with references to nodes that can be active nodes (i.e. have a neighbor with a different opinion)
        #   3) cluster the updates instead of making every update separately ... make sure that the rest of the model works on longer time scales if you do that
        print("t = {t:>4.1d}", end="\r")
        active_individual = random.choice(self.acquaintance_network.nodes())
        active_neighbor = random.choice(self.acquaintance_network.neighbors(active_individual))
        if active_individual.opinion != active_neighbor.opinion:
            if random.random < self.rewiring_probability:
                # rewire
                new_neighbor = random.choice(filter(lambda x: x.opinion == active_individual.opinion, self.acquaintance_network.nodes()))
                # really slow probably, just a first implementation
                self.acquaintance_network.remove_edge(active_individual, active_neighbor)
                self.acquaintance_network.add_edge(active_individual, new_neighbor)
            else:
                # TODO: ask Jobst, whether this is okai within his framework!
                active_individual.opinion = active_neighbor.opinion
        # else: do nothing



    processes = [
        Event('opinion update',
              [I.Culture.acquaintance_network],
              ['rate', 0.1, opinion_update])
    ]
