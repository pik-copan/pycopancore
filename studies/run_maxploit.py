"""Test Study for the maxploit model.

A study to test the runner with the maxploit model.
"""

# expit() scipy

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

from plot_multilayer import LayeredNetworkGraph

import pycopancore.models.maxploit as M
from pycopancore.runners.runner import Runner

# first thing: set seed so that each execution must return same thing:
random.seed(1)

# parameters:
timeinterval = 1
timestep = 0.1
ni_sust = 50  # number of agents with sustainable behaviour 1
ni_nonsust = 50 # number of agents with unsustainable behaviour 0
nindividuals = ni_sust + ni_nonsust
nc = nindividuals  # number of cells
p = 0.5  # link density

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
              + [M.Individual(behaviour=1, opinion=1, imitation_tendency=0,
                              rewiring_prob=0.5,
                              cell=cells[i + ni_nonsust])
                 for i in range(ni_sust)]

# instantiate groups
ng_total = 10
ng_sust = 5 # number of groups
ng_nonsust = ng_total - ng_sust
group_meeting_interval = 1
groups = [M.Group(culture=culture, world=world, group_opinion=1,
                  group_meeting_interval=group_meeting_interval) for i in range(ng_sust)] + \
         [M.Group(culture=culture, world=world, group_opinion=0,
                  group_meeting_interval=group_meeting_interval) for i in range(ng_nonsust)]

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
# interlink_density = 0.5
# for i in individuals:
#     for g in groups:
#         if np.random.uniform() < interlink_density:
#             GM.add_edge(i, g)
# make sure each individual is member of at least one group
#     if not list(i.group_memberships): #i.e. list is empty
#         GM.add_edge(i, np.random.choice(groups))

# group_membership network with only one group membership for now
for i in individuals:
    GM.add_edge(i, np.random.choice(groups))


# color_map = []
# for node in list(GM.nodes):
#     color_map.append(GM.nodes[node]["color"])
# top_nodes = {n for n, d in GM.nodes(data=True) if d["type"] == "Group"}
# bottom_nodes = set(GM) - top_nodes
# nx.draw(GM, node_color=color_map, with_labels=False,
#         pos=nx.bipartite_layout(GM, bottom_nodes, align="horizontal", aspect_ratio=4 / 1))
# plt.show()

#get a preliminary intergroup network for plotting multilayer
inter_group_network = nx.Graph()
for g in groups:
    inter_group_network.add_node(g)
for index, g in enumerate(groups):
    for j in groups[:index]:
        inter_group_network.add_edge(g, j)


# try to plot a nice multilayer network
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# LayeredNetworkGraph([culture.acquaintance_network, inter_group_network], [culture.group_membership_network], ax=ax)
# ax.view_init(90, 0)
# plt.show()
#
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# LayeredNetworkGraph([culture.acquaintance_network, inter_group_network], [culture.group_membership_network], ax=ax)
# ax.view_init(40, 40)
# plt.show()

# color_map = []
# unsust_nodes = {n for n, d in GM.nodes(data=True) if (d["type"] == "Group" and n.group_opinion)
#                 or (d["type"] == "Individual" and n.behaviour)}
# sust_nodes = {n for n, d in GM.nodes(data=True) if (d["type"] == "Group" and not n.mean_group_opinion)
#               or (d["type"] == "Individual" and not n.opinion)}
# for node in list(GM.nodes):
#     if node in unsust_nodes:
#         color_map.append("red")
#     else:
#         color_map.append("blue")
# nx.draw(GM, node_color=color_map, with_labels=False,
#         pos=nx.bipartite_layout(GM, bottom_nodes, align="horizontal", aspect_ratio=4 / 1))
# plt.show()

print("done ({})".format(dt.timedelta(seconds=(time() - start))))

print('\n runner starting')

r = Runner(model=model)
start = time()
traj = r.run(t_1=timeinterval, dt=timestep)
runtime = dt.timedelta(seconds=(time() - start))
print('runtime: {runtime}'.format(**locals()))

import os
os_path = "C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\plots\\maxploit"

import datetime
current_time = datetime.datetime.now()
current = [current_time.month, current_time.day, current_time.hour, current_time.minute, current_time.second]
time_string = f"{current_time.year}"
for i in current:
    if i < 10:
        time_string += f"_0{i}"
    else:
        time_string += f"_{i}"

# save_time = f"{current_time.year}_" + f"{current_time.month}_" + f"{current_time.day}_" \
#             + f"{current_time.hour}_" + f"{current_time.minute}_" + f"{current_time.second}"

# Directory
directory = f"Run_{time_string}"

# Path
my_path = os.path.join(os_path, directory)

# Create the directory
# 'GeeksForGeeks' in
# '/home / User / Documents'
os.mkdir(my_path)
print(f"Directory {directory} created @ {my_path}")

# saving traj
# load pickle module
from pickle import dump
# create a binary pickle file
f = open(my_path + "traj_dic.pickle", "wb")

tosave = {
          f"{v.owning_class.__name__}" + "."
          + v.codename: {str(e): traj[v][e]
                         for e in traj[v].keys()
                         }
          for v in traj.keys() if v is not "t"
          }
tosave["t"] = traj["t"]
dump(tosave, f)
# close file
f.close()

t = np.array(traj['t'])
# print("max. time step", (t[1:] - t[:-1]).max())
# print('keys:', np.array(traj.keys()))
# print('completeDict: ', traj)


# for ind in individuals:
#     print([traj[M.Individual.behaviour][ind]])
individuals_behaviours = np.array([traj[M.Individual.behaviour][ind]
                                   for ind in individuals])
individuals_behaviours_dict=traj[M.Individual.behaviour]
groups_opinions = traj[M.Group.group_opinion]
mean_groups_behaviours = traj[M.Group.mean_group_behaviour]
# groups_opinions_fixed = traj[M.Group.group_opinion]

# print(mean_groups_behaviours)
# plt.plot(t, mean_groups_behaviours[groups[0]])
# plt.show()

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

v_array1 = []
v_array2 = []
for i in individuals:
    v_array1.append(individuals_behaviours_dict[i][0])
for index, g in enumerate(groups):
    v_array2.append(groups_opinions[g][0])
v_array = [v_array1, v_array2]
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_proj_type('ortho')
LayeredNetworkGraph([culture.acquaintance_network, inter_group_network], [culture.group_membership_network], v_array, ax=ax)
plt.show()

multilayer = LayeredNetworkGraph([culture.acquaintance_network, inter_group_network], [culture.group_membership_network],
                    v_array, ax=ax, layout=nx.spring_layout)
node_positions = multilayer.save_node_positions() # to get node positions

for t_index in range(len(t)):
    fig = plt.figure()
    v_array1 = []
    v_array2 = []
    for i in individuals:
        v_array1.append(individuals_behaviours_dict[i][t_index])
    for index, g in enumerate(groups):
        v_array2.append(groups_opinions[g][t_index])
    v_array = [v_array1, v_array2]
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.view_init(40+0.075*t_index, 40-0.075*t_index)
    LayeredNetworkGraph([culture.acquaintance_network, inter_group_network], [culture.group_membership_network],
                        v_array, ax=ax, layout=nx.spring_layout, node_positions=node_positions)
    my_file = f'layered_network_{t_index}.png'
    fig.savefig(os.path.join(my_path, my_file))
    plt.close(fig)
"""
for i in range(len(t)):
    color_map = []
    unsust_nodes = {n for n, d in GM.nodes(data=True) if (d["type"] == "Group" and groups_opinions[n][i])
                    or (d["type"] == "Individual" and individuals_behaviours_dict[n][i])}
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
"""
# color_map = []
# for node in list(GM.nodes):
#     color_map.append(GM.nodes[node]["color"])
# top_nodes = {n for n, d in GM.nodes(data=True) if d["type"] == "Group"}
# bottom_nodes = set(GM) - top_nodes
# nx.draw(GM, node_color=color_map, with_labels=False,
#         pos=nx.bipartite_layout(GM, bottom_nodes, align="horizontal", aspect_ratio=4 / 1))
# plt.show()#

plt.close('all')

# TODO: grit entfernen

