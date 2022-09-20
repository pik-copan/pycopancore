"""Plot script to show the evolution of the network for the SMG
model.
"""
filename = "/tmp/smg_data.p"

from pickle import load
import numpy as np
import networkx as nx
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import bisect

# Load data:
traj = load(open(filename,"rb"))

# Extract network trajectory (at time 0, static anyways):
network_as_list = list(traj["Culture.acquaintance_network"].values())[0]
G = nx.from_edgelist(network_as_list[0])

# Extract engagement level trajectory:
engagement_level = traj["Individual.engagement_level"]

# Define color dictionary for plotting:
color_dict = {'core': 'red',
              'base': 'orange',
              'support': 'yellow',
              'inactive': 'black'}

# Extract time:
time = traj["t"]

# Create equidistant frame iterator:
ideal_frames = np.arange(0, 5, 0.05)
frames = [bisect.bisect(time, frame) - 1 for frame in ideal_frames]

# Plot animation:
fig = plt.figure()
pos = nx.spring_layout(G)
nodes = nx.draw_networkx_nodes(G, pos)
edges = nx.draw_networkx_edges(G, pos)

# Update node color in each animation step:
def update(frame):
    nc = [color_dict[engagement_level[ind][frame]] 
          for ind in engagement_level]
    nodes.set_color(nc)
    return nodes,

ani = animation.FuncAnimation(fig, update, frames=frames, interval=50, 
                              blit=True)
plt.show()
