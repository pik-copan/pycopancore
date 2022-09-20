"""Plot script for showing (the development of) engagement levels in
the SMG model.
"""
filename = "/tmp/smg_data.p"

from pickle import load
import numpy as np
import networkx as nx
import sys
import matplotlib.pyplot as plt

# Load data:
traj = load(open(filename,"rb"))

# Extract network trajectory (at time 0, static anyways):
network_as_list = list(traj["Culture.acquaintance_network"].values())[0]
G = nx.from_edgelist(network_as_list[0])

# Extract engagement level trajectory:
engagement_level = traj["Individual.engagement_level"]
levels = ["core", "base", "support", "inactive"]

# Group individuals according to their level in a dict (at time 0):
level_dict = {key: [] for key in levels}
for ind in engagement_level.keys():
    level_dict[engagement_level[ind][0]].append(ind)

# Plot degree distribution by level:
plt.title('\nDistribution Of Node Linkages (log-log scale)')
plt.xlabel('Degree')
plt.ylabel('Number of Nodes')
plt.xscale('log')
plt.yscale('log')
for level in levels:
    degree_sequence = sorted((d for n, d in G.degree(level_dict[level])),
                             reverse=True)
    degrees_n_counts = np.unique(degree_sequence, return_counts=True)
    plt.plot(*degrees_n_counts, label=level)
plt.legend()
plt.show()
