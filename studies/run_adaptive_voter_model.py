"""Skript to run Jobsts model."""

from time import time
# from numpy import random
import random
import networkx as nx
import numpy as np
import sys
import pycopancore.models.adaptive_voter_model as M
# import pycopancore.models.only_copan_global_like_carbon_cycle as M
from pycopancore import master_data_model as D
from pycopancore.runners import Runner

# import plotly.plotly as py
import plotly.offline as py
import plotly.graph_objs as go
# from pylab import plot, gca, show

# assert False, "to be changed"

# first thing: set seed so that each execution must return same thing:
random.seed(1)
# TODO: figure out why it doesn't seem to work here ...

# parameters:
nindividuals = 10
rewiring_probability = 0.1
possible_opinions = list(range(2))


# instantiate model
model = M.Model()


# instantiate process taxa:
culture = M.Culture(rewiring_probability=rewiring_probability)

# generate entities and distribute opinions uniformly randomly:
world = M.World(culture=culture)
cell = M.Cell(world=world)
individuals = [M.Individual(cell=cell, initial_opinion=random.choice(possible_opinions)) for _ in range(nindividuals)]

# TODO: ask Jobst, why are all individuals already in the network?

def erdosrenyify(graph, p = 0.5):
    """take a a networkx.Graph with nodes and distribute the edges following the erdos-renyi graph procedure"""
    assert not graph.edges(), "your graph has already edges"
    nodes = graph.nodes()
    for i, n1 in enumerate(nodes[:-1]):
        for n2 in nodes[i+1:]:
            if random.random() < p:
                graph.add_edge(n1, n2)

# set the initial graph structure to be an erdos-renyi graph
erdosrenyify(culture.acquaintance_network, p = 0.5)

runner = Runner(model=model)

start = time()
traj = runner.run(t_1=100, dt=.1)
print(time()-start, " seconds")


t = np.array(traj['t'])
print("max. time step", (t[1:]-t[:-1]).max())

individuals_opinions = np.array([traj[M.Individual.opinion][ind] for ind in individuals])

nopinion1_list = np.sum(individuals_opinions, axis=0) / nindividuals
nopinion0_list = 1 - nopinion1_list

# everything below is just plotting commands for plotly

data_opinion0 = go.Scatter(
    x=t,
    y=nopinion0_list,
    mode="lines+markers",
    name="relative amount opinion 0",
    line=dict(
        color="lightblue",
        width=2
    )
)
data_opinion1 = go.Scatter(
    x=t,
    y=nopinion1_list,
    mode="lines+markers",
    name="relative amount opinion 1",
    line=dict(
        color="orange",
        width=2
    )
)

layout = dict(title = 'Adaptive Voter Model',
              xaxis = dict(title = 'time'),
              yaxis = dict(title = 'relative opinion amounts'),
              )

fig = dict(data=[data_opinion0, data_opinion1], layout=layout)
py.plot(fig, filename="adaptive-voter-model.html")

