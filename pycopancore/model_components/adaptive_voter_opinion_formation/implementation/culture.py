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
        # TODO: there are some intuitive speed-ups:
        #   1) use a list with references to nodes of the differing opinions so the statement with filter can be avoided
        #   2) use a list with references to nodes that can be active nodes (i.e. have a neighbor with a different opinion)
        #       2.1) choose neighbor such that the link is active, probably best to use filter there
        #       2.2) track number of active neighbors or always read len from the list generated in 2.1
        #   3) cluster the updates instead of making every update separately ... make sure that the rest of the model works on longer time scales if you do that
        print("\tt = {:>4.1f}; nopinion0 = {:>3d}".format(t, len(list(filter(lambda x: x.opinion == 0, self.acquaintance_network.nodes())))))
        active_individual = random.choice(self.acquaintance_network.nodes())
        active_neighbor = random.choice(self.acquaintance_network.neighbors(active_individual))

        # check if link is active, i.e. the opinions differe
        if active_individual.opinion != active_neighbor.opinion:
            # link is active and something is to be done
            # decide randomly whether to rewire or to adopt the opinion
            if random.random() < self.rewiring_probability:
                # rewire
                # TODO: add check that this is possible, to be combined with the speed-ups
                #
                new_neighbor = random.choice(filter(lambda x: x.opinion == active_individual.opinion, self.acquaintance_network.nodes()))
                self.acquaintance_network.remove_edge(active_individual, active_neighbor)
                self.acquaintance_network.add_edge(active_individual, new_neighbor)
            else:
                # adopt opinion
                # TODO: ask Jobst, whether this is okai within his framework!
                active_individual.opinion = active_neighbor.opinion
        # else: do nothing



    processes = [
        Event('opinion update',
              [I.Culture.acquaintance_network, I.Individual.opinion],
              ['rate', 0.1, opinion_update])
    ]
