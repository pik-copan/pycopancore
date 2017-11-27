"""Moduletest, a study to test the runner with dummy dynamics."""

import numpy as np

from pycopancore.models import base_and_dummy as tb
from pycopancore.runners.runner import Runner

nworlds = 1
nsocs = 3
ncells = 7
ni = 8

print('\n instantiating model')
m = tb.Model()

nature = tb.Nature()
metabolism = tb.Metabolism()
culture = tb.Culture()

worlds = [tb.World(nature=nature, metabolism=metabolism, culture=culture) for w in range(nworlds)]
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
