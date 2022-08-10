"""Test Study for the maxploit model.

A study to test the runner with the maxploit model.
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
from time import time
import datetime as dt
from numpy import random
import argparse

import networkx as nx
import matplotlib.pyplot as plt
import plotly.offline as py
import plotly.graph_objs as go

import pycopancore.models.maxploit as M
from pycopancore.runners.runner import Runner

# parameters:
timeinterval = 2
timestep = 0.1
ni_sust = 10  # number of agents with sustainable behaviour 1
ni_nonsust = 10  # number of agents with unsustainable behaviour 0
nindividuals = ni_sust + ni_nonsust
nc = nindividuals  # number of cells
p = 0.4  # link density

# New Order of instantiating things !!!!!
# instantiate model
model = M.Model()

# instantiate process taxa culture:
culture = M.Culture()

# generate entitites:
world = M.World(culture=culture)
social_system = M.SocialSystem(world=world)
cells = [M.Cell(stock=1, capacity=1, growth_rate=1, social_system=social_system)
         for c in range(nc)]
individuals = [M.Individual(behaviour=0, opinion=0, imitation_tendency=0,
                            rewiring_prob=0.5,
                            cell=cells[i]) for i in range(ni_nonsust)] \
              + [M.Individual(behaviour=1, opinion=0, imitation_tendency=0,
                              rewiring_prob=0.5,
                              cell=cells[i + ni_nonsust])
                 for i in range(ni_sust)]

# instantiate groups
ng_sust = 2  # number of groups
ng_nonsust = 2
groups = [M.Group(culture=culture, world=world, mean_group_opinion=1) for i in range(ng_sust)] + \
         [M.Group(culture=culture, world=world, mean_group_opinion=0) for i in range(ng_nonsust)]

for (i, c) in enumerate(cells):
    c.individual = individuals[i]


def erdosrenyify(graph, p=0.5):
    """Create a ErdosRenzi graph from networkx graph.

    Take a a networkx.Graph with nodes and distribute the edges following the
    erdos-renyi graph procedure.
    """
    assert not graph.edges(), "your graph has already edges"
    nodes = list(graph.nodes())
    for i, n1 in enumerate(nodes[:-1]):
        for n2 in nodes[i + 1:]:
            if random.random() < p:
                graph.add_edge(n1, n2)


# set the initial graph structure to be an erdos-renyi graph
print("erdosrenyifying the graph ... ", end="", flush=True)
start = time()
erdosrenyify(culture.acquaintance_network, p=p)

# nx.draw(culture.acquaintance_network)
# plt.show()


GM = culture.group_membership_network
# initialize group_membership network
interlink_density = 0.5
for i in individuals:
    for g in groups:
        if np.random.uniform() < interlink_density:
            GM.add_edge(i, g)
# make sure each individual is member of at least one group
    if not list(i.group_memberships): #i.e. list is empty
        GM.add_edge(i, np.random.choice(groups))

color_map = []
for node in list(GM.nodes):
    color_map.append(GM.nodes[node]["color"])
top_nodes = {n for n, d in GM.nodes(data=True) if d["type"] == "Group"}
bottom_nodes = set(GM) - top_nodes
nx.draw(GM, node_color=color_map, with_labels=False,
        pos=nx.bipartite_layout(GM, bottom_nodes, align="horizontal", aspect_ratio=4 / 1))
plt.show()

color_map = []
unsust_nodes = {n for n, d in GM.nodes(data=True) if (d["type"] == "Group" and n.mean_group_opinion)
                or (d["type"] == "Individual" and n.behaviour)}
# sust_nodes = {n for n, d in GM.nodes(data=True) if (d["type"] == "Group" and not n.mean_group_opinion)
#               or (d["type"] == "Individual" and not n.opinion)}
for node in list(GM.nodes):
    if node in unsust_nodes:
        color_map.append("red")
    else:
        color_map.append("blue")
nx.draw(GM, node_color=color_map, with_labels=False,
        pos=nx.bipartite_layout(GM, bottom_nodes, align="horizontal", aspect_ratio=4 / 1))
plt.show()


print("done ({})".format(dt.timedelta(seconds=(time() - start))))

print('\n runner starting')

r = Runner(model=model)
start = time()
traj = r.run(t_1=timeinterval, dt=timestep)
runtime = dt.timedelta(seconds=(time() - start))
print('runtime: {runtime}'.format(**locals()))

t = np.array(traj['t'])
print("max. time step", (t[1:] - t[:-1]).max())
print('keys:', np.array(traj.keys()))
# print('completeDict: ', traj)


# for ind in individuals:
#     print([traj[M.Individual.behaviour][ind]])
individuals_behaviours = np.array([traj[M.Individual.behaviour][ind]
                                   for ind in individuals])
individuals_behaviours_dict=traj[M.Individual.behaviour]
groups_opinions = traj[M.Group.mean_group_opinion]
# groups_opinions_fixed = traj[M.Group.group_opinion]

# for ind in individuals:
#     print([traj[M.Individual.opinion][ind]])
# individuals_opinions = np.array([traj[M.Individual.opinion][ind]
#                                  for ind in individuals])

nbehav1_list = np.sum(individuals_behaviours, axis=0) / nindividuals
nbehav0_list = 1 - nbehav1_list

# nopinion1_list = np.sum(individuals_opinions, axis=0) / nindividuals
# nopinion0_list = 1 - nopinion1_list

# everything below is just plotting commands for plotly

data_behav0 = go.Scatter(
    x=t,
    y=nbehav0_list,
    mode="lines",
    name="relative amount behaviour 0 (nonsus)",
    line=dict(
        color="lightblue",
        width=2
    )
)
data_behav1 = go.Scatter(
    x=t,
    y=nbehav1_list,
    mode="lines",
    name="relative amount behaviour 1 (sus)",
    line=dict(
        color="orange",
        width=2
    )
)

layout = dict(title='Maxploit Model',
              xaxis=dict(title='time'),
              yaxis=dict(title='relative behaviour amounts'),
              )

fig = dict(data=[data_behav0, data_behav1], layout=layout)
# py.plot(fig, filename="maxlpoit_model.html")

# print(groups_opinions)
# print(groups_opinions[groups[0]])
# print(groups_opinions[groups[0]][0])
# print(groups_opinions_fixed)
# print(groups_opinions_fixed[groups[0]])
# print(groups_opinions_fixed[groups[0]][0])
# print(individuals_behaviours_dict)
# print(individuals_behaviours_dict[individuals[0]])
# print(individuals_behaviours_dict[individuals[0]][0])

import os
my_path = "C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\plots\\maxploit\\volatile_group_opinion"

for i in range(len(t)):
    color_map = []
    unsust_nodes = {n for n, d in GM.nodes(data=True) if (d["type"] == "Group" and groups_opinions[n][i])
                    or (d["type"] == "Individual" and individuals_behaviours_dict[n][i])}
    # sust_nodes = {n for n, d in GM.nodes(data=True) if (d["type"] == "Group" and not n.mean_group_opinion)
    #               or (d["type"] == "Individual" and not n.opinion)}
    for node in list(GM.nodes):
        if node in unsust_nodes:
            color_map.append("red")
        else:
            color_map.append("blue")
    fig = plt.figure()
    nx.draw(GM, node_color=color_map, with_labels=False,
            pos=nx.bipartite_layout(GM, bottom_nodes, align="horizontal", aspect_ratio=4 / 1))
    my_file = f'network_{i}.png'
    fig.savefig(os.path.join(my_path, my_file))
    plt.close(fig)

# color_map = []
# for node in list(GM.nodes):
#     color_map.append(GM.nodes[node]["color"])
# top_nodes = {n for n, d in GM.nodes(data=True) if d["type"] == "Group"}
# bottom_nodes = set(GM) - top_nodes
# nx.draw(GM, node_color=color_map, with_labels=False,
#         pos=nx.bipartite_layout(GM, bottom_nodes, align="horizontal", aspect_ratio=4 / 1))
# plt.show()