"""
Run script template.

TODO: Go through the file and adjust all parts of the code marked with the 
TODO flag. Pay attention to those variables and objects written in capital 
letters. These are placeholders and must be adjusted as needed. For further 
details see also the model development tutorial.
"""
# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>

# set the path for importing modules (assuming this file resides directly 
# in the studies folder)
from os.path import dirname
import sys
sys.path.insert(0, dirname(dirname(__file__)))

import pycopancore.models.social_movement_growth as M

# standard runner for simulating any model:
from pycopancore.runners.runner import Runner

# to be able to specify variables with physical units
from pycopancore import master_data_model as D

import numpy as np  # which is usually needed
# to generate random initial conditions
from numpy.random import choice, uniform

#import pylab as plt  # to plot stuff
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx

from pickle import dump
import bisect


filename = "/tmp/smg_data.pickle"

# model parameters:
growth_strategy = 0.2
meeting_rate = 2 / D.months
organizing_success_probability = 0.2
mobilizing_success_probability = 0.2

ninds_core = 5
ninds_base = 10
ninds_support = 50
ninds_inactive = 150

ninds = ninds_core + ninds_base + ninds_support + ninds_inactive

# simulation parameters:
t_max = 5  # interval for which the model will be simulated
dt = 0.1  # desired temporal resolution of the resulting output.


# instantiate the model and have it analyse its own structure:
model = M.Model()

# instantiate process taxa:
env = M.Environment()
met = M.Metabolism()
cul = M.Culture(
    growth_strategy = growth_strategy,
    meeting_rate = meeting_rate,
    organizing_success_probability = organizing_success_probability,
    mobilizing_success_probability = mobilizing_success_probability,
    )

# generate entities:
world = M.World(
    environment = env,
    metabolism = met,
    culture = cul,
    )
soc = M.SocialSystem(
    world = world,
    )
cell = M.Cell(
    social_system = soc,
    )
inds = [M.Individual(
    cell = cell,
    engagement_level = 'core'
    ) for j in range(ninds_core)] \
        + [M.Individual(
    cell = cell,
    engagement_level = 'base'
    ) for j in range(ninds_base)] \
        + [M.Individual(
    cell = cell,
    engagement_level = 'support'
    ) for j in range(ninds_support)] \
        + [M.Individual(
    cell = cell,
    engagement_level = 'inactive'
    ) for j in range(ninds_inactive)]
    

# set some further variables:

# initialize Barabasi-Albert network:
N = ninds
m0 = 3 # size of the initial (fully connected) clique
m = 3 # number of connections for each new node
edges = []

'adds the edges of the initial clique connecting all the m nodes'
for i in range(m0):
    for j in range(i+1, m0):
        edges.append((inds[i], inds[j]))

'runs over all the reamining nodes'
for i in range(m0, N):
    # flatten the edges array so each node appears proportional to the number of links it has
    prob = [node for edge in edges for node in edge]
    'for each new node, creates m new links'
    for j in range(m):
        'picks up a random node, so nodes will be selected proportionally to their degree'
        node = choice(prob)
        edges.append((inds[i], node))

cul.acquaintance_network.add_edges_from(edges)

#
# Run the model
#

runner = Runner(model=model)
traj = runner.run(t_0=0, t_1=t_max, dt=dt,
                  add_to_output=[M.Individual.engagement_level])

#tosave = {
          #v.owning_class.__name__ + "."
          #+ v.codename: {str(e): traj[v][e]
                         #for e in traj[v].keys()
                         #} 
          #for v in traj.keys() if v is not "t"
          #}
#tosave["t"] = traj["t"]
#dump(tosave, open(filename,"wb"))


#print([i.engagement_level for i in inds])
color_dict = {'core': 'red',
              'base': 'orange',
              'support': 'yellow',
              'inactive': 'black'}
time = traj["t"]
times = np.arange(0, 5, 0.05)
frame_indices = [bisect.bisect(time, i) - 1 for i in times]

el_data = traj[M.Individual.engagement_level]
el = [[el_data[k][t] for k in el_data.keys()] for t in frame_indices]
color_list = [color_dict[i.engagement_level] for i in inds]

G = cul.acquaintance_network
fig = plt.figure()
pos = nx.spring_layout(cul.acquaintance_network)
nc = [color_dict[e] for e in el[0]]
nodes = nx.draw_networkx_nodes(G, pos, node_color=nc)
edges = nx.draw_networkx_edges(G, pos)

def update(i):
    nc = [color_dict[e] for e in el[i]]
    nodes.set_color(nc)
    return nodes,

ani = animation.FuncAnimation(fig, update, frames=len(frame_indices), interval=50, blit=True)
plt.show()
