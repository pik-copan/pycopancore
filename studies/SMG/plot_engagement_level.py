"""Plot script for showing (the development of) engagement levels in
the SMG model.
"""

import pickle
import yaml
import numpy as np
import networkx as nx
import sys
import matplotlib.pyplot as plt

res_dir = "./simulation_results/SMG/"
with open(res_dir+"all_runs.txt", "r") as f:
    for line in f:
        pass
date_time_str = line.strip()
filename = res_dir+date_time_str

# Load data:
with open(filename+".pickle", "rb") as f:
    traj = pickle.load(f)

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

def load_traj_and_conf(filenames):
    trajectories_list = []
    configs_list = []
    for filename in filenames:
        with open(res_dir+filename+".pickle", "rb") as f:
            traj = pickle.load(f)
        trajectories_list.append(traj)
        with open(res_dir+filename+"_conf.yaml", "rb") as f:
            next(f)
            conf = yaml.safe_load(f)
        configs_list.append(conf)
    return trajectories_list, configs_list

def load_n_traj_and_conf_for_date(date, n, n0):
    with open(res_dir+"all_runs.txt", "r") as f:
        filenames = []
        for line in f:
            if date in line:
                filenames.append(line.strip())
    filenames = filenames[n0:n0+n]
    trajectories_list, configs_list = load_traj_and_conf(filenames)
    return trajectories_list, configs_list

def plot_degree_distribution(time):
    # Group individuals according to their level in a dict (at time):
    level_dict = {key: [] for key in levels}
    for ind in engagement_level.keys():
        level_dict[engagement_level[ind][time]].append(ind)

    # Plot degree distribution by level:
    fig, ax = plt.subplots()
    ax.set_title('\nDistribution Of Node Linkages (log-log scale)')
    ax.set_xlabel('Degree')
    ax.set_ylabel('Number of Nodes')
    ax.set_xscale('log')
    ax.set_yscale('log')
    degree_sequence = {}
    degrees_n_counts = {}
    for l in levels:
        degree_sequence[l] = sorted((d for n, d in G.degree(level_dict[l])),
                                reverse=True)
        degrees_n_counts[l] = np.unique(degree_sequence[l], 
                                        return_counts=True)
        ax.scatter(*degrees_n_counts[l], label=l, color=color_dict[l])
    ax.legend()
    plt.show()


# Extract time:
def plot_time_series(trajectories, configs):
    level_count = [] * len(trajectories)
    
    for tr in trajectories:
        time = tr["t"]
        tr["level_count"] = {l: [0] * len(time) for l in levels}
        engagement_level = tr["Individual.engagement_level"]
        for ind in engagement_level:
            for t in range(len(time)):
                tr["level_count"][engagement_level[ind][t]][t] += 1
    
    fig, ax = plt.subplots()
    labels = True
    for tr in trajectories:
        if labels:
            for l in levels:
                ax.plot(tr["t"], tr["level_count"][l], color=color_dict[l], label=l)
        else:
            for l in levels:
                ax.plot(tr["t"], tr["level_count"][l], color=color_dict[l])
        labels = False
    phi = configs[0]["growth_strategy"]
    ax.set_xlabel('Time (years)')
    ax.set_ylabel('Number of Individuals')
    ax.set_title(rf'Engagement Level: Time Evolution for $\phi = {phi}$')
    ax.legend()
    fig.savefig(res_dir+date+f'/time_series_{phi}.png')

#plot_degree_distribution(0)
#plot_time_series()

date = "2022-10-31"
for i in range(10):
    trajectories, configs = load_n_traj_and_conf_for_date(date, 20, 20*i)
    plot_time_series(trajectories, configs)
