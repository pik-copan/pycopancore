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

import random

class Culture (I.Culture):
    """Culture process taxon mixin implementation class."""

    # standard methods:

    def __init__(self,
                   *,
                rewiring_probability,
                 **kwargs):
        """Initialize the unique instance of Culture."""
        super().__init__(**kwargs)  # must be the first line

        self.phi = rewiring_probability

    # process-related methods:

    def opinion_update(self, t):
        active_individual = random.choice(self.aquaintance_network.nodes())
        active_neighbor = random.choice(self.aquaintance_network.neighbors(active_individual))
        if active_individual.opinion != active_neighbor.opinion:
            if random.random < self.phi:
                # rewire
                new_neighbor = random.choice(filter(lambda x: x.opinion == active_individual.opinion, self.aquaintance_network.nodes()))
                # really slow probably, just a first implementation
                self.aquaintance_network.remove_edge(active_individual, active_neighbor)
                self.aquaintance_network.add_edge(active_individual, new_neighbor)
            else:
                active_individual.opinion = active_neighbor.opinion


    # TODO: add some if needed...

    processes = [
        Event('opinion update',
              [opinion_update],
              ['rate', 0.1, a_event_function])
    ]  # TODO: instantiate and list process objects here
