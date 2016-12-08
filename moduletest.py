import numpy as np

from pycopancore.studies import test_base_and_dummy as tb
from pycopancore.runners.runner_prototype import RunnerPrototype


ns = 3
nc = 7
ni = 12


tb.Model.configure()

societies = [tb.Society(population=1) for s in range(ns)]
cells = [tb.Cell(society=societies[0]) for c in range(nc)]
individuals = [tb.Individual for i in range(ni)]

tb.Cell.location.set_values(dict={c: (0, 0) for c in cells})
tb.Cell.area.set_values(entities=cells, values=np.random.rand(nc))
tb.Cell.capacity.set_values(entities=cells, values=[1 for c in cells])
print(tb.Cell.capacity.get_value_list(entities=cells))
tb.Cell.resource.set_values(entities=cells, values=np.random.rand(nc))
tb.Cell.event_value.set_values(entities=cells, values=np.random.rand(nc))
tb.Cell.step_resource.set_values(entities=cells, values=np.random.rand(nc))
tb.Cell.explicit_value.set_values(entities=cells, values=np.random.rand(nc))


m = tb.Model(societies=societies, cells=cells, individuals=individuals)

print(tb.Cell.explicit_value.get_value_list(entities=cells))
print(tb.Cell.capacity.get_value_list(entities=cells))
print('Model Processes in Moduletest', m.processes)

r = RunnerPrototype(model=m)

traj = r.run(t_1=10, dt=.1)
