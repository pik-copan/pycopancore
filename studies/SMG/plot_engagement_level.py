"""Plot script for showing (the development of) engagement levels in
the SMG model.
"""

from pickle import load
import numpy as np
import networkx as nx
import sys
import matplotlib.pyplot as plt

res_dir = "./simulation_results/social_movement_growth/"
with open(res_dir+"all_runs.txt", "r") as f:
    for line in f:
        pass
date_time_str = line.strip()
filename = res_dir+date_time_str
print(filename)

# Load data:
with open(filename+".pickle", "rb") as f:
    traj = load(f)

# Extract network trajectory (at time 0, static anyways):
network_as_list = list(traj["Culture.acquaintance_network"].values())[0]
G = nx.from_edgelist(network_as_list)

# Extract engagement level trajectory:
engagement_level = traj["Individual.engagement_level"]
levels = ["core", "base", "support", "indifferent"]

# Define color dictionary for plotting:
color_dict = {'core': 'red',
            'base': 'orange',
            'support': 'yellow',
            'indifferent': 'black'}

def plot_degree_distribution(time):
    # Group individuals according to their level in a dict (at time):
    level_dict = {key: [] for key in levels}
    for ind in engagement_level.keys():
        level_dict[engagement_level[ind][time]].append(ind)

    # Plot degree distribution by level:
    fig = plt.figure()
    plt.title('\nDistribution Of Node Linkages (log-log scale)')
    plt.xlabel('Degree')
    plt.ylabel('Number of Nodes')
    plt.xscale('log') 
    plt.yscale('log')
    degree_sequence = {}
    degrees_n_counts = {}
    for l in levels:
        degree_sequence[l] = sorted((d for n, d in G.degree(level_dict[l])),
                                reverse=True)
        degrees_n_counts[l] = np.unique(degree_sequence[l], 
                                        return_counts=True)
        plt.plot(*degrees_n_counts[l], label=l, color=color_dict[l])
    plt.legend()
    plt.show()


# Extract time:
time = traj["t"]
def plot_time_series():
    level_count = {l: [0] * len(time) for l in levels}

    for ind in engagement_level:
        for t in range(len(time)):
            level_count[engagement_level[ind][t]][t] += 1
    
    plt.title('Engagement level evolution')
    plt.xlabel('Time (years)')
    plt.ylabel('Number of Individuals')
    for l in levels:
        plt.plot(time, level_count[l], color=color_dict[l], label=l)
    plt.legend()
    plt.show()

# plot_degree_distribution(0)
plot_time_series()
