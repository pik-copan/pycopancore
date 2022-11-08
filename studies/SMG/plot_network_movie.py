"""Plot script to show the evolution of the network for the SMG
model.
"""

from pickle import load
import numpy as np
import networkx as nx
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from bisect import bisect

res_dir = "./simulation_results/SMG/"
with open(res_dir+"all_runs.txt", "r") as f:
    for line in f:
        pass
date_time_str = line.strip()
filename = res_dir+date_time_str

# Load data:
with open(filename+".pickle", "rb") as f:
    traj = load(f)

# Extract network trajectory (at time 0, static anyways):
network_as_list = list(traj["Culture.acquaintance_network"].values())[0]
G = nx.from_edgelist(network_as_list)

# Extract engagement level trajectory:
engagement_level = traj["Individual.engagement_level"]

# Define color dictionary for plotting:
color_dict = {'core': 'red',
              'base': 'orange',
              'support': 'yellow',
              'indifferent': 'black'}

# Extract time:
time = traj["t"]

# Create an equidistant time array:
ideal_times = np.linspace(0, time[-1], 51)

# Choose most recent frame for each time:
frames = [bisect(time, t) - 1 for t in ideal_times]

def plot_frame(framenumber):
    # Plot frame:
    fig, ax = plt.subplots()
    pos = nx.spring_layout(G)
    #pos = nx.circular_layout(G)
    nc = [color_dict[engagement_level[ind][frames[framenumber]]] 
        for ind in G.nodes()]
    nodes = nx.draw_networkx_nodes(G, pos, ax=ax, alpha=0.75, node_size=50, node_color=nc)
    edges = nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.05)
    ax.axis('off')

    plt.show()
    

def plot_animation():
    # Plot animation:
    fig, ax = plt.subplots()
    pos = nx.spring_layout(G)
    #pos = nx.circular_layout(G)
    nodes = nx.draw_networkx_nodes(G, pos, ax=ax, alpha=0.75, node_size=50, node_color='k')
    edges = nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.05)
    title = ax.set_title(r"$t = 0.00\/\mathrm{{a}}$")
    ax.axis('off')

    # Update node color in each animation step:
    def update(i):
        nc = [color_dict[engagement_level[ind][frames[i]]] 
            for ind in G.nodes()]
        nodes.set_color(nc)
        title = ax.set_title(rf"$t = {ideal_times[i]:.2f}\/\mathrm{{a}}$")
        return nodes, title,

    ani = animation.FuncAnimation(fig, update, frames=len(frames),
                                  interval=50, blit=False)
    plt.show()

plot_animation()
#plot_frame(160)
