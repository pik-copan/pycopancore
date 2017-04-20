"""Skript to run Jobsts model."""

from time import time
import datetime as dt
# from numpy import random
import random
# import networkx as nx
import numpy as np
# import sys
import pycopancore.models.adaptive_voter_model as M
# import pycopancore.models.only_copan_global_like_carbon_cycle as M
# from pycopancore import master_data_model as D
from pycopancore.runners import Runner

# import plotly.plotly as py
import plotly.offline as py
import plotly.graph_objs as go

# first thing: set seed so that each execution must return same thing:
random.seed(1)
# TODO: figure out why it doesn't seem to work here ...

# parameters:
timeinterval = 100
timestep = 0.1
expected_degree = 10
nindividuals = 4000
rewiring_probability = 0.1
possible_opinions = list(range(2))
p_initial = 0.7 # probability of initial opinion 0 (over opinion 1)

# instantiate model
model = M.Model()

# instantiate process taxa:
culture = M.Culture(rewiring=rewiring_probability)

# generate entities and distribute opinions uniformly randomly:
world = M.World(culture=culture)
society = M.Society(world=world, culture=culture)
cell = M.Cell(world=world, society=society)
individuals = [M.Individual(cell=cell,
                            initial_opinion=int(random.random() < p_initial))
               for _ in range(nindividuals)]

# TODO: ask Jobst, why are all individuals already in the network?


def erdosrenyify(graph, p=0.5):
    """Create a ErdosRenzi graph from networkx graph.

    Take a a networkx.Graph with nodes and distribute the edges following the
    erdos-renyi graph procedure.
    """
    assert not graph.edges(), "your graph has already edges"
    nodes = graph.nodes()
    for i, n1 in enumerate(nodes[:-1]):
        for n2 in nodes[i+1:]:
            if random.random() < p:
                graph.add_edge(n1, n2)


# set the initial graph structure to be an erdos-renyi graph
print("erdosrenyifying the graph ... ", end="", flush=True)
start = time()
erdosrenyify(culture.acquaintance_network, p=expected_degree / nindividuals)
print("done ({})".format(dt.timedelta(seconds=(time() - start))))

runner = Runner(model=model)

start = time()
traj = runner.run(t_1=timeinterval, dt=timestep)
runtime = dt.timedelta(seconds=(time() - start))
print("runtime: {runtime}".format(**locals()))


t = np.array(traj['t'])
print("max. time step", (t[1:]-t[:-1]).max())

individuals_opinions = np.array([traj[M.Individual.opinion][ind]
                                 for ind in individuals])

nopinion1_list = np.sum(individuals_opinions, axis=0) / nindividuals
nopinion0_list = 1 - nopinion1_list

# everything below is just plotting commands for plotly

data_opinion0 = go.Scatter(
    x=t,
    y=nopinion0_list,
    mode="lines",
    name="relative amount opinion 0",
    line=dict(
        color="lightblue",
        width=2
    )
)
data_opinion1 = go.Scatter(
    x=t,
    y=nopinion1_list,
    mode="lines",
    name="relative amount opinion 1",
    line=dict(
        color="orange",
        width=2
    )
)
data_majority_opinion = go.Scatter(
    x=t,
    y=traj[M.Society.opinion][society],
    mode="lines+markers",
    name="majority opinion",
    line=dict(
        color="red",
        width=2
    ),
    marker=dict(
        color="red",
        size=4
    )
)

layout = dict(title='Adaptive Voter Model',
              xaxis=dict(title='time'),
              )

fig = dict(data=[data_opinion0, data_opinion1, data_majority_opinion], layout=layout)
py.plot(fig, filename="adaptive-voter-model.html")
