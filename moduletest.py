"""Moduletest, a study to test the runner with dummy dynamics."""

import numpy as np

from pycopancore.models import base_and_dummy as tb
from pycopancore.runners.runner import Runner

nw = 1
ns = 3
nc = 7
ni = 8


worlds = [tb.World() for w in range(nw)]
societies = [tb.Society(population=1) for s in range(ns)]
cells = [tb.Cell(society=societies[0], world=worlds[0]) for c in range(nc)]
individuals = [tb.Individual(cell=cells[0]) for i in range(ni)]

for cell in cells:
    cell.location = (0, 0)
    cell.area = np.random.rand(1)
    cell.capacity = 1
    cell.resource = np.random.rand(1)
    cell.event_value = np.random.rand(1)
    cell.step_resource = np.random.rand(1)
    cell.explicit_value = np.random.rand(1)

print('\n instantiating model')
m = tb.Model()

print('\n runner starting')
r = Runner(model=m)

traj = r.run(t_1=10, dt=.1)

# print(traj)
