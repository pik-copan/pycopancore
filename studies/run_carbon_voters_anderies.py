"""Skript to run Carbon Voters model."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from time import time
import datetime as dt
# from numpy import random
import random
# import networkx as nx
import numpy as np
# import sys
import pycopancore.models.carbon_voters_anderies_model as M
# import pycopancore.models.only_copan_global_like_carbon_cycle as M
from pycopancore import master_data_model as D
from pycopancore.runners import Runner

# import plotly.plotly as py
import plotly.offline as py
import plotly.graph_objs as go

# first thing: set seed so that each execution must return same thing:
random.seed(1)
# TODO: figure out why it doesn't seem to work here ...

# parameters:
timeinterval = 60
timestep = 1
expected_degree = 10
nindividuals = 400
rewiring_probability = 0.1
possible_opinions = list(range(2))
impact_scaling_factor=20
no_impact_opinion_change=0.5
no_impact_atmospheric_carbon_level=0.2

# use fast method and with multple updates
M.avof.Culture.configure(
    update_mode=M.avof.Culture.update_modes.fast,
    synchronous_updates=100
)

# instantiate model
model = M.Model()


# instantiate process taxa:
culture = M.Culture(
    timestep=timestep,
    rewiring=rewiring_probability, impact_scaling_factor=impact_scaling_factor,
    no_impact_opinion_change=no_impact_opinion_change,
    no_impact_atmospheric_carbon_level=no_impact_atmospheric_carbon_level
)
environment = M.Environment()

# generate entities and distribute opinions uniformly randomly:
world = M.World(culture=culture, environment=environment,
                atmospheric_carbon=0.2 * D.gigatonnes_carbon,
                ocean_carbon=0.6 * D.gigatonnes_carbon
                )
social_system = M.SocialSystem(world=world)
cell = M.Cell(world=world, social_system=social_system)
individuals = [M.Individual(cell=cell,
                            initial_opinion=float(np.random.choice(possible_opinions, 1, p=[0.6,0.4])))
               for _ in range(nindividuals)] # individual opinion 0 with prob. p1, 1(aware) with prob. p2

# set initial values
Sigma0 = 1.5e8 * D.square_kilometers
cell.land_area = Sigma0
# print(M.Cell.land_area.get_values(cells))

L0 = 0.2 * D.gigatonnes_carbon # 2480 is yr 2000
cell.terrestrial_carbon = L0
# print(M.Cell.terrestrial_carbon.get_values(cells))

G0 = 0.5 * D.gigatonnes_carbon   # 1125 is yr 2000
cell.fossil_carbon = G0

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
# majority opinion
data_majority_opinion = go.Scatter(
    x=t,
    y=traj[M.SocialSystem.opinion][social_system],
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
# carbon
data_ca = go.Scatter(
    x=t,
    y=traj[M.World.atmospheric_carbon][world],
    mode="lines",
    name="atmospheric carbon",
    line=dict(
        color="lightblue",
        width=4
    )
)
data_ct = go.Scatter(
    x=t,
    y=traj[M.World.terrestrial_carbon][world],
    mode="lines",
    name="terrestrial carbon",
    line=dict(
        color="green",
        width=4
    )
)
data_cm = go.Scatter(
    x=t,
    y=traj[M.World.ocean_carbon][world],
    mode="lines",
    name="maritime carbon",
    line=dict(
        color="blue",
        width=4
    )
)
data_cf = go.Scatter(
    x=t,
    y=traj[M.World.fossil_carbon][world],
    mode="lines",
    name="fossil carbon",
    line=dict(
        color="gray",
        width=4
    )
)

layout = dict(title='Adaptive Voter Model and Anderies Carbon Cycle',
              xaxis=dict(title='time'),
              yaxis=dict(title='relative opinion and carbon amounts'),
              )

fig = dict(data=[data_opinion0, data_opinion1, data_majority_opinion,
                 data_ca, data_cf, data_cm, data_ct], layout=layout)
py.plot(fig, filename="adaptive-voter-model.html")
