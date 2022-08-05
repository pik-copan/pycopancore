"""Test Study for the exploit model.

A study to test the runner with the exploit model.
It includes the module components exploit_social_learning,
most_simple_vegetation and simple_extraction.
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

import plotly.offline as py
import plotly.graph_objs as go

import pycopancore.models.maxploit as M
from pycopancore.runners.runner import Runner

# parameters:
timeinterval = 100
timestep = 0.1
ni_sust = 50  # number of agents with sustainable behaviour 1
ni_nonsust = 50  # number of agents with unsustainable behaviour 0
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
ng = 10  # number of groups
groups = [M.Group(culture=culture, world=world) for i in range(ng)]

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

# initialize group_membership network
interlink_density = 0.5
for i in individuals:
    for g in groups:
        if np.random.uniform() < interlink_density:
            culture.group_membership_network.add_edge(i, g)

print("done ({})".format(dt.timedelta(seconds=(time() - start))))

print('\n runner starting')

r = Runner(model=model)
start = time()
traj = r.run(t_1=timeinterval, dt=timestep)
runtime = dt.timedelta(seconds=(time() - start))
print('runtime: {runtime}'.format(**locals()))

t = np.array(traj['t'])
print("max. time step", (t[1:] - t[:-1]).max())
# print('keys:', np.array(traj.keys()))
# print('completeDict: ', traj)

individuals_behaviours = np.array([traj[M.Individual.behaviour][ind]
                                   for ind in individuals])
individuals_opinions = np.array([traj[M.Individual.opinion][ind]
                                 for ind in individuals])

nbehav1_list = np.sum(individuals_behaviours, axis=0) / nindividuals
nbehav0_list = 1 - nbehav1_list

nopinion1_list = np.sum(individuals_opinionss, axis=0) / nindividuals
nopinion0_list = 1 - nopinion1_list

# everything below is just plotting commands for plotly

data_opinion0 = go.Scatter(
    x=t,
    y=nopinion0_list,
    mode="lines",
    name="relative amount behaviour 0",
    line=dict(
        color="lightblue",
        width=2
    )
)
data_opinion1 = go.Scatter(
    x=t,
    y=nopinion1_list,
    mode="lines",
    name="relative amount behaviour 1",
    line=dict(
        color="orange",
        width=2
    )
)

layout = dict(title='Maxploit Model',
              xaxis=dict(title='time'),
              yaxis=dict(title='relative behaviour amounts'),
              )

fig = dict(data=[data_opinion0, data_opinion1], layout=layout)
py.plot(fig, filename="exlpoit_model.html")
