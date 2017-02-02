"""Moduletest, a study to test the runner with dummy dynamics."""

import numpy as np

from pycopancore.models import base_and_dummy as tb
from pycopancore.runners.runner import Runner


ns = 3
nc = 7
ni = 8


tb.Model.configure()

societies = [tb.Society(population=1) for s in range(ns)]
cells = [tb.Cell(society=societies[0]) for c in range(nc)]
individuals = [tb.Individual(cell=cells[0]) for i in range(ni)]

tb.Cell.location.set_values(dict={c: (0, 0) for c in cells})
tb.Cell.area.set_values(entities=cells, values=np.random.rand(nc))
tb.Cell.capacity.set_values(entities=cells, values=[1 for c in cells])
tb.Cell.resource.set_values(entities=cells, values=np.random.rand(nc))
tb.Cell.event_value.set_values(entities=cells, values=np.random.rand(nc))
tb.Cell.step_resource.set_values(entities=cells, values=np.random.rand(nc))
tb.Cell.explicit_value.set_values(entities=cells, values=np.random.rand(nc))

print('\n instantiating model')
m = tb.Model()

print('\n runner starting')
r = Runner(model=m)

traj = r.run(t_1=10, dt=.1)

print(traj)
