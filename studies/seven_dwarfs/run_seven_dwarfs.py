"""This is the test script for the seven dwarfs step by step tutorial.

In this version only the Step-process 'aging' of entitytype 'Individual' is
implemented, such that the only relevant attributes of 'Individual' are 'age'
and 'cell'.
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

import networkx as nx
import matplotlib.pyplot as plt

import plotly.offline as py
import plotly.graph_objs as go

import pycopancore.models.seven_dwarfs as M
from pycopancore.runners.runner import Runner


# setting timeinterval for run method 'Runner.run()'
timeinterval = 10
# setting time step to hand to 'Runner.run()'
timestep = 0.1
nc = 1  # number of caves
dwarfs = 7  # number of dwarfs

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
cells = [
    M.Cell(social_system=social_system, eating_stock=100) for c in range(nc)
]

# instantiate dwarfs and assigning initial conditions
individuals = [
    M.Individual(
        cell=cells[0],
        age=0,
        beard_length=0,
        beard_growth_parameter=0.5,
        eating_parameter=0.1,
    )
    for i in range(dwarfs)
]

# assigning individuals to cell is not necessary since it is done by
# initializing the individuals in 'base.Individuals' with the 'cell' method


start = time()

print("done ({})".format(dt.timedelta(seconds=(time() - start))))

print("\n runner starting")

# Define termination signals as list [ signal_method, object_method_works_on ]
# the termination method 'check_for_extinction' must return a boolean
termination_signal = [M.Culture.check_for_extinction, culture]

# Define termination_callables as list of all signals
termination_callables = [termination_signal]

nx.draw(culture.acquaintance_network)
plt.show()

# Runner is instantiated
r = Runner(model=model, termination_calls=termination_callables)

start = time()
# run the Runner and saving the return dict in traj
traj = r.run(
    t_1=timeinterval,
    dt=timestep,
    add_to_output=[M.Culture.acquaintance_network],
)
runtime = dt.timedelta(seconds=(time() - start))
print("runtime: {runtime}".format(**locals()))

# saving time values to t
t = np.array(traj["t"])
print("max. time step", (t[1:] - t[:-1]).max())


# proceeding for plotting

# Create List of all dwarfes, not only the ones instantiated before the run,
# but also the one created during the run.

if M.Individual.idle_entities:
    all_dwarfs = M.Individual.instances + M.Individual.idle_entities
else:
    all_dwarfs = M.Individual.instances

individuals_age = np.array(
    [traj[M.Individual.age][dwarf] for dwarf in all_dwarfs]
)


individuals_beard_length = np.array(
    [traj[M.Individual.beard_length][dwarf] for dwarf in all_dwarfs]
)

cell_stock = np.array(traj[M.Cell.eating_stock][cells[0]])

t = np.array(traj["t"])

data_age = []
print("data age", data_age)
for i, dwarf in enumerate(all_dwarfs):
    data_age.append(
        go.Scatter(
            x=t,
            y=individuals_age[i],
            mode="lines",
            name="age of dwarf no. {}".format(i),
            line=dict(color="green", width=4),
        )
    )

data_beard_length = []
print("data beard", data_beard_length)
for i, dwarf in enumerate(all_dwarfs):
    data_beard_length.append(
        go.Scatter(
            x=t,
            y=individuals_beard_length[i],
            mode="lines",
            name="beard length of dwarf no. {}".format(i),
            line=dict(color="red", width=4),
        )
    )

data_stock = []
data_stock.append(
    go.Scatter(
        x=t,
        y=cell_stock,
        mode="lines",
        name="stock of cell",
        line=dict(color="blue", width=4),
    )
)


layout = dict(
    title="seven dwarfs",
    xaxis=dict(title="time [yr]"),
    yaxis=dict(title="value"),
)


# getting plots of two dwarfs:
fig = dict(
    data=[data_age[0], data_beard_length[0], data_stock[0]], layout=layout
)
py.plot(fig, filename="our-model-result{}.html".format(0))

fig = dict(
    data=[data_age[5], data_beard_length[5], data_stock[0]], layout=layout
)
py.plot(fig, filename="our-model-result{}.html".format(5))

# nx.draw(traj[M.Culture.acquaintance_network][culture][1])
# plt.show()
for i in range(len(traj["t"])):
    print(list(traj[M.Culture.acquaintance_network][culture][i].nodes()))
