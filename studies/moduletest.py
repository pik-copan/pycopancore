"""Moduletest, a study to test the runner with dummy dynamics."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

import numpy as np

from pycopancore.models import base_and_dummy as tb
from pycopancore.runners.runner import Runner

nworlds = 1
nsocs = 3
ncells = 7
ni = 8

print('\n instantiating model')
m = tb.Model()

environment = tb.Environment()
metabolism = tb.Metabolism()
culture = tb.Culture()

worlds = [tb.World(environment=environment, metabolism=metabolism, culture=culture) for w in range(nworlds)]
social_systems = [tb.SocialSystem(world=worlds[0], population=1) for s in range(nsocs)]
cells = [tb.Cell(social_system=social_systems[0]) for c in range(ncells)]
individuals = [tb.Individual(cell=cells[0],social_system=social_systems[0]) for i in range(ni)]

for cell in cells:
    cell.location = (0, 0)
    cell.land_area = np.random.rand(1)
    cell.capacity = 1
    cell.resource = np.random.rand(1)
    cell.event_value = np.random.rand(1)
    cell.step_resource = np.random.rand(1)
    cell.explicit_value = np.random.rand(1)

print('\n runner starting')
r = Runner(model=m)

traj = r.run(t_1=10, dt=.1)

# print(traj)
