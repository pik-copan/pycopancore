import numpy as np
from numpy import random

import pycopancore.models.jobsts_prototype_1 as M
from pycopancore import master_data_model as D
from pycopancore.runners import Runner

from pylab import plot, gca, show

# parameters:

nworlds = 1  # no. worlds
nsocs = 2  # no. societies
ncells = 4  # no. cells

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


# distribute area and vegetation randomly but correlatedly:
r = random.uniform(size=ncells)
Sigma0 = 1.5e8 * D.square_kilometers * r / sum(r)
M.Cell.land_area.set_values(cells, Sigma0)
#print(M.Cell.land_area.get_values(cells))

r += random.uniform(size=ncells)
L0 = 2480 * D.gigatonnes_carbon * r / sum(r) # 2480 is yr 2000
M.Cell.terrestrial_carbon.set_values(cells, L0)
#print(M.Cell.terrestrial_carbon.get_values(cells))

r = np.exp(random.normal(size=ncells))
G0 = 1125 * D.gigatonnes_carbon * r / sum(r) # 1125 is yr 2000
M.Cell.fossil_carbon.set_values(cells, G0)
#print(M.Cell.fossil_carbon.get_values(cells))

r = random.uniform(size=nsocs)
P0 = 6e9 * D.people * r / sum(r) # 500e9 is middle ages, 6e9 would be yr 2000
M.Society.population.set_values(societies, P0)
#print(M.Society.population.get_values(societies))

r = random.uniform(size=nsocs)
S0 = 1e13 * D.gigajoules * r / sum(r) # in AWS paper: 1e12 (alternatively: 1e13)
#M.Society.renewable_energy_knowledge.set_values(societies, S0)
#print(M.Society.renewable_energy_knowledge.get_values(societies))

r = random.uniform(size=nsocs)
K0 = sum(P0) * 1e4 * D.dollars/D.people * r / sum(r) # ?
#M.Society.physical_capital.set_values(societies, K0)
#print(M.Society.physical_capital.get_values(societies))

# TODO: add noise to parameters

runner = Runner(model=model)

from time import time
start = time()
traj = runner.run(t_1=1, dt=.01)
print(time()-start, " seconds")

print(traj)

t = traj['t'][:-1]
print(len(t), len(traj[M.World.atmospheric_carbon][worlds[0]][:-1]))
plot(t, traj[M.World.atmospheric_carbon][worlds[0]][:-1],"b",lw=3)
plot(t, traj[M.World.ocean_carbon][worlds[0]][:-1],"b--",lw=3)
plot(t, traj[M.World.terrestrial_carbon][worlds[0]][:-1],"g",lw=3)
plot(t, traj[M.World.fossil_carbon][worlds[0]][:-1],"gray",lw=3)
for s in societies:
    plot(t, traj[M.Society.population][s][:-1],"yellow",lw=2)
#    plot(t, traj[M.Society.physical_capital][s][:-1],"k",lw=2)
#    plot(t, traj[M.Society.renewable_energy_knowledge][s][:-1],color="darkorange",lw=2)
#    plot(t, traj[M.Society.biomass_input_flow][s][:-1],"g--",lw=2)
#    plot(t, traj[M.Society.fossil_fuel_input_flow][s][:-1],"--",color="gray",lw=2)
#    plot(t, traj[M.Society.renewable_energy_input_flow][s][:-1],"--",color="darkorange",lw=2)
for c in cells:
    plot(t, traj[M.Cell.terrestrial_carbon][c][:-1],"g")
    plot(t, traj[M.Cell.fossil_carbon][c][:-1],"gray")
gca().set_yscale('symlog')
show()
