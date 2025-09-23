"""
Run script template.

TODO: Go through the file and adjust all parts of the code marked with the TODO
flag. Pay attention to those variables and objects written in capital letters.
These are placeholders and must be adjusted as needed. For further details see
also the model development tutorial.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>

import pycopancore.models.SOME_MODEL as M  # TODO: adjust

# standard runner for simulating any model:
from pycopancore.runners.runner import Runner

from pycopancore import (
    master_data_model as D,
)  # to be able to specify variables with physical units

import numpy as np  # which is usually needed

# to generate random initial conditions
from numpy.random import choice, uniform

import pylab as plt  # to plot stuff

# instantiate the model and have it analyse its own structure:
model = M.Model()

#
# TODO: All necessary model setup, such as setting initial conditions or
# instantiating taxa and entities, comes after this line and before the next
# commented block below. The following code is exemplary:
#


# model parameters:

nsocs = 2  # no. of social systems
ncellseach = 10  # no. of cells per social system
nindseach = 10  # no. of individuals per cell
link_density = 0.1  # random network link density

# simulation parameters:

t_max = 100  # interval for which the model will be simulated
dt = 0.1  # desired temporal resolution of the resulting output.


# instantiate process taxa:
env = M.Environment(
    # SOME_VARIABLE = SOME_INITIAL_VALUE, ...
)
met = M.Metabolism(
    # SOME_VARIABLE = SOME_INITIAL_VALUE, ...
)
cul = M.Culture(
    # SOME_VARIABLE = SOME_INITIAL_VALUE, ...
)

# generate entities:
world = M.World(
    environment=env,
    metabolism=met,
    culture=cul,
    # SOME_VARIABLE = SOME_INITIAL_VALUE, ...
)  # TODO: in case of many worlds, make a list
socs = [
    M.SocialSystem(
        world=world,
        # SOME_VARIABLE = SOME_INITIAL_VALUE, ...
    )
    for j in range(nsocs)
]
cells = [
    M.Cell(
        social_system=s,
        # SOME_VARIABLE = SOME_INITIAL_VALUE, ...
    )
    for s in socs
    for j in range(ncellseach)
]
inds = [
    M.Individual(
        cell=c,
        # SOME_VARIABLE = SOME_INITIAL_VALUE, ...
    )
    for c in cells
    for j in range(nindseach)
]

# set some further variables:
P0 = uniform(high=1e3, size=nsocs)
M.SocialSystem.population.set_values(socs, P0)

# initialize some network:
for index, i in enumerate(inds):
    for j in inds[:index]:
        if uniform() < link_density:
            cul.acquaintance_network.add_edge(i, j)

#
# Run the model
#

runner = Runner(model=model)
traj = runner.run(t_0=0, t_1=t_max, dt=dt)

# TODO: Add some further analysis such as plotting or saving
plt.plot(traj["t"], traj[M.SocialSystem.population][socs[0]])
plt.show()
