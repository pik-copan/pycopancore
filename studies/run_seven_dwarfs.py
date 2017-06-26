"""Test Study for the exploit model.

A study to test the runner with the exploit model.
It includes the module components exploit_social_learning,
most_simple_vegetation and simple_extraction.
"""

import numpy as np
from time import time
import datetime as dt
from numpy import random

import plotly.offline as py
import plotly.graph_objs as go

import pycopancore.models.seven_dwarfs as M
from pycopancore.runners.runner import Runner

#parameters:
timeinterval = 100
timestep = 1
nc = 1  # number of caves
dwarfs = 7  # number of dwarfs

# instantiate model
model = M.Model()

# instantiate process taxa culture:
culture = M.Culture()

# generate entitites:
world = M.World(culture=culture)
cells = [M.Cell(stock=100, world=world)
         for c in range(nc)]
individuals = [M.Individual(age=0,
                 beard_length=0,
                 beard_growth_parameter=0.1,
                 eating_parameter=1) for i in range(dwarfs)]

for (i, c) in enumerate(cells):
    c.individual = individuals[i]


start = time()

print("done ({})".format(dt.timedelta(seconds=(time() - start))))

print('\n runner starting')

# Define termination signals as list [ signal_method, object_method_works_on ]
termination_signal = [M.Culture.acquaintance_network.nodes()==[],
                    culture]
# Define termination_callables as list of all signals
termination_callables = [termination_signal]
print('termination_callables: ', termination_callables)

r = Runner(model=model, termination_calls=termination_callables)
start = time()
traj = r.run(t_1=timeinterval, dt=timestep)
runtime = dt.timedelta(seconds=(time() - start))
print('runtime: {runtime}'.format(**locals()))

t = np.array(traj['t'])
print("max. time step", (t[1:]-t[:-1]).max())
# print('keys:', np.array(traj.keys()))
# print('completeDict: ', traj)

individuals_beard_length = np.array([traj[M.Individual.beard_length][dwarf]
                                 for dwarf in individuals])
individuals_age = np.array([traj[M.Individual.age][dwarf]
                                 for dwarf in individuals])
stock = np.array([traj[M.Cell.stock][cave]
                                 for cave in cells])


