"""This is an illustration script for some of the features that come with the group entity based on the seven dwarfs model.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

import numpy as np
from numpy.random import uniform
from time import time
import datetime as dt

import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt

import plotly.offline as py
import plotly.graph_objs as go

import pycopancore.models.groups_seven_dwarfs as M
from pycopancore.runners.runner import Runner

# from studies import plot_multilayer as pm
# from mpl_toolkits.mplot3d import Axes3D
# from mpl_toolkits.mplot3d.art3d import Line3DCollection


# setting timeinterval for run method 'Runner.run()'
timeinterval = 10
# setting time step to hand to 'Runner.run()'
timestep = .1
nc = 1  # number of caves
dwarfs = 10  # number of dwarfs

# instantiate model M (needs to be done in the beginning of each script).
# This configures the model M through 'ModelLogics' in module
# 'base.model_logics' such that initialisation of attributes and entities gets
# possible
model = M.Model()

# instantiate process taxa culture:
# In this certain case we need 'M.Culture()' for the acquaintance network.
culture = M.Culture()

# instantiate world:
world = M.World(culture=culture)

# instantiate one social system:
social_system = M.SocialSystem(world=world)

# instantiate cells (the caves):
cells = [M.Cell(social_system=social_system,
                eating_stock=100
                )
        for c in range(nc)
        ]

# instantiate dwarfs and assigning initial conditions
individuals = [M.Individual(cell=cells[0],
                            age=0,
                            beard_length=0,
                            beard_growth_parameter=0.5,
                            eating_parameter=.1
                            ) for i in range(dwarfs)
               ]

print("\n The individuals:")
print(individuals)
print("\n \n")

# assigning individuals to cell is not necessary since it is done by
# initializing the individuals in 'base.Individuals' with the 'cell' method

#instantiate groups
ng = 10 #number of groups
groups = [M.Group(culture=culture, world=world) for i in range (ng)]

print("\n The groups:")
print(groups)
print("\n \n")

start = time()

print("done ({})".format(dt.timedelta(seconds=(time() - start))))

print('\n runner starting')

# first test for group network
#nx.draw(culture.group_membership_network)
#plt.show()


# initialize the network:
for i in individuals:
    for g in groups:
        culture.group_membership_network.add_edge(i, g)

print("\n Individual 1 Group Memberships:")
print(list(individuals[0].group_memberships))
print("\n")

print("\n Group Members:")
print(list(groups[0].group_members))
print("\n")

#draw network of one group
# nx.draw(individuals[0].culture.group_membership_network)
# plt.show()

GM = culture.group_membership_network

print("\n The data structure in gm network:")
print(GM.nodes.data())
print("\n")

# How networkx would classicaly plot the network
nx.draw(culture.group_membership_network)
plt.show()

# How to plot more intuitively using the type and color information
color_map = []
shape_map = []
for node in list(GM.nodes):
    print(node)
    print(GM.nodes[node])
    color_map.append(GM.nodes[node]["color"])

    if GM.nodes[node]["type"] == "Group":
        shape_map.append("o")
    else:
        shape_map.append("^")
top_nodes = {n for n, d in GM.nodes(data=True) if d["type"] == "Group"}
bottom_nodes = set(GM) - top_nodes
nx.draw(GM, node_color=color_map, with_labels=False,
        pos=nx.bipartite_layout(GM, bottom_nodes, align="horizontal", aspect_ratio=4/1))
plt.show()

# Define termination signals as list [ signal_method, object_method_works_on ]
# the termination method 'check_for_extinction' must return a boolean
termination_signal = [M.Culture.check_for_extinction,
                      culture]

# Define termination_callables as list of all signals
termination_callables = [termination_signal]

# nx.draw(culture.acquaintance_network)
# plt.show()

# Runner is instantiated
r = Runner(model=model,
           termination_calls=termination_callables
           )

start = time()
# run the Runner and saving the return dict in traj
traj = r.run(t_1=timeinterval, dt=timestep, add_to_output=[M.Culture.acquaintance_network])
runtime = dt.timedelta(seconds=(time() - start))
print('runtime: {runtime}'.format(**locals()))

# saving time values to t
t = np.array(traj['t'])
print("max. time step", (t[1:]-t[:-1]).max())

# save and print membership

membercheck = traj[M.Group.having_members]
plt.plot(t, membercheck[groups[0]]) # plot if dwarf 0 was member of group 0
plt.show()
