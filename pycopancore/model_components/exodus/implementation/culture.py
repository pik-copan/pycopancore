"""Culture process taxon mixing class template.

TODO: adjust or fill in code and documentation wherever marked by "TODO:",
then remove these instructions
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from .. import interface as I
from pycopancore.model_components.base import interface as B
# from .... import master_data_model as D
from pycopancore import Explicit, Step
import networkx as nx
import community


class Culture (I.Culture):
    """Culture process taxon mixin implementation class."""

    def __init__(self,
                 *,
                 network_clustering=0,  # this is stupid but necessary, plotting failes otherwise
                 fully_connected_network=True,  # static network
                 **kwargs):
        """Initialize the unique instance of Metabolism."""
        super().__init__(**kwargs)  # must be the first line

        self.network_clustering = network_clustering
        self.fully_connected_network = fully_connected_network

    def calculate_av_clustering(self, unused_t):
        """Calculate clustering wih networkx."""
        # only if not fully connected:
        if not self.fully_connected_network:
            self.network_clustering = nx.average_clustering(
                self.acquaintance_network)

    def calculate_partition(self, graph):
        """Calculate the partition of the Graph using Louvain algo."""
        partition = community.best_partition(graph)
        return partition

    def calculate_modularity(self, unused_t):
        """Calculate modularity from partition."""
        # only if not fully connected:
        if not self.fully_connected_network:
            shallow_network = nx.from_scipy_sparse_matrix(
                nx.adjacency_matrix(self.acquaintance_network))
            partition = self.calculate_partition(shallow_network)
            self.modularity = community.modularity(
                partition,
                shallow_network)
            # print('modularity: ', self.modularity)

    def modularity_timing(self, t):
        """Timing for step process to calculate modularity."""
        # only if not fully connected:
        if not self.fully_connected_network:
            return t + 1
        else:
            return t + 1000  # just a high number, so it doesnt happen...

    def calculate_transitivity(self, unused_t):
        """Calculate the transitivity of the network"""
        # only if not fully connected:
        if not self.fully_connected_network:
            self.transitivity = nx.transitivity(self.acquaintance_network)

    def check_for_split(self):
        """Check if network has split into to groups."""
        # Iterate through all individuals and see if they know someone from
        # another profession:
        connection = False
        for ind in self.acquaintance_network:
            for acq in ind.acquaintances:
                if ind.profession != acq.profession:
                    # if one has another profession, the split has not
                    # taken place:
                    connection = True
                    break
        self.split = False
        if connection is False:
            self.split = True
        return self.split

    processes = [
                 Explicit("calculate average clustering",
                           [I.Culture.network_clustering],
                           calculate_av_clustering),
                 Step("Calculate Modularity",
                      [I.Culture.modularity],
                      [modularity_timing, calculate_modularity]),
                 Step("Calculate Transitivity",
                      [I.Culture.transitivity],
                      [modularity_timing, calculate_transitivity])
                 ]  # TODO: instantiate and list process objects here
