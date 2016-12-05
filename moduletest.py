from pycopancore.studies import test_base_and_dummy as tb
from pycopancore.runners.runner_prototype import RunnerPrototype


ns = 3
nc = 7
ni = 12


tb.Model.configure()

societies = [tb.Society(population=1) for s in range(ns)]
cells = [tb.Cell(society=societies[0]) for c in range(nc)]
individuals = [tb.Individual for i in range(ni)]

m = tb.Model()
