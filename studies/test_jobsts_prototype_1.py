import numpy as np
from numpy import random

import pycopancore.models.jobsts_prototype_1 as M
from pycopancore import master_data_model as D
from pycopancore.runners import Runner

from pylab import plot, gca, show
from pycopancore.data_model.master_data_model.nature import ocean_carbon

# parameters:

nworlds = 1  # no. worlds
nsocs = 1  # no. societies
ncells = 1  # no. cells

model = M.Model()

# instantiate process taxa:
nature = M.Nature()
metabolism = M.Metabolism()

# generate entities and plug them together at random:
worlds = [M.World(nature=nature, metabolism=metabolism,
                  atmospheric_carbon = 830 * D.gigatonnes_carbon,
                  ocean_carbon = (5500 - 830 - 2480 - 1125) * D.gigatonnes_carbon
                  ) for w in range(nworlds)]
societies = [M.Society(world=random.choice(worlds)) for s in range(nsocs)]
cells = [M.Cell(society=random.choice(societies)) for c in range(ncells)]
# make references consistent:
for c in cells:
    c.world = c.society.world


# distribute area and vegetation randomly but correlatedly:
r = random.uniform(size=ncells)
Sigma0 = 1.5e8 * D.square_kilometers * r / sum(r)
M.Cell.land_area.set_values(cells, Sigma0)

r += random.uniform(size=ncells)
L0 = 2480 * D.gigatonnes_carbon * r / sum(r) # 2480 is yr 2000
M.Cell.terrestrial_carbon.set_values(cells, L0)

r = np.exp(random.normal(size=ncells))
G0 = 1125 * D.gigatonnes_carbon * r / sum(r) # 1125 is yr 2000
M.Cell.fossil_carbon.set_values(cells, G0)

r = random.uniform(size=nsocs)
P0 = 6e9 * D.people * r / sum(r) # 500e9 is middle ages, 6e9 would be yr 2000
M.Society.population.set_values(cells, P0)

r = random.uniform(size=nsocs)
S0 = 1e13 * D.gigajoules * r / sum(r) # in AWS paper: 1e12 (alternatively: 1e13)
#M.Society.renewable_energy_knowledge.set_values(cells, S0)

r = random.uniform(size=nsocs)
K0 = sum(P0) * 1e4 * D.dollars/D.people * r / sum(r) # ?
#M.Society.physical_capital.set_values(cells, K0)

print(M.Cell.terrestrial_carbon == M.World.terrestrial_carbon)
print(M.Cell.terrestrial_carbon.owning_classes)
print(M.World.terrestrial_carbon.owning_classes)

# TODO: add noise to parameters

runner = Runner(model=model)

traj = runner.run(t_1=1, dt=0.01)

t = traj['t']
print(traj[M.World.atmospheric_carbon][worlds[0]])
plot(t, traj[M.World.atmospheric_carbon][worlds[0]])
#plot(t, traj[M.Cell.photosynthesis_carbon_flow][cells[0]])
#plot(t, traj[M.Cell.biomass_harvest_flow][cells[0]])
#gca().set_yscale('symlog')
show()
