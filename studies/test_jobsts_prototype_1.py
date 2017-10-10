"""Skript to run Jobsts prototype model."""

from time import time
from numpy import random
import numpy as np
import pycopancore.models.jobsts_prototype_1 as M
# import pycopancore.models.only_copan_global_like_carbon_cycle as M
from pycopancore import master_data_model as D
from pycopancore.runners import Runner

from pylab import plot, gca, show

# first thing: set seed so that each execution must return same thing:
random.seed(10) # 10

# parameters:

nworlds = 1  # no. worlds
nsocs = 10 # no. societies #10
ncells = 100  # no. cells #100
ninds = 1000 # no. individuals

model = M.Model()

# instantiate process taxa:
nature = M.Nature()
metabolism = M.Metabolism(
    renewable_energy_knowledge_spillover_fraction = .1,
    basic_emigration_probability_rate = 3e-13) # 3e-13 leads to ca. 5mio. (real)
        # 1 w/o protection: success but desertification
        # .75 w protection: success (even w/o or w much migration)
        # .1 w protection: success but desertification
        # 0 w/o protection: very slow success but desertification
        # ?: oscillations
culture = M.Culture()

# generate entities and plug them together at random:
worlds = [M.World(nature=nature, metabolism=metabolism, culture=culture,
                  atmospheric_carbon = 830 * D.gigatonnes_carbon,
                  upper_ocean_carbon = (5500 - 830 - 2480 - 1125) * D.gigatonnes_carbon
                  ) for w in range(nworlds)]
societies = [M.Society(world=random.choice(worlds),
#                       protected_fossil_carbon_share=0.95, # (.95,.75) helps
#                       protected_terrestrial_carbon_share=0.75
                       ) for s in range(nsocs)]
cells = [M.Cell(society=random.choice(societies),
                renewable_sector_productivity=random.rand()*3e-16)
                    # random.rand()*3e-16 at S=1e12 leads to ca. 100 GW renewables initially 
         for c in range(ncells)]
individuals = [M.Individual(cell=random.choice(cells)) 
               for i in range(ninds)]


# distribute area and vegetation randomly but correlatedly:
r = random.uniform(size=ncells)
Sigma0 = 1.5e8 * D.square_kilometers * r / sum(r)
M.Cell.land_area.set_values(cells, Sigma0)
# print(M.Cell.land_area.get_values(cells))

r += random.uniform(size=ncells)
L0 = 2480 * D.gigatonnes_carbon * r / sum(r)  # 2480 is yr 2000
M.Cell.terrestrial_carbon.set_values(cells, L0)
# print(M.Cell.terrestrial_carbon.get_values(cells))

r = np.exp(random.normal(size=ncells))
G0 = 1125 * D.gigatonnes_carbon * r / sum(r)  # 1125 is yr 2000
M.Cell.fossil_carbon.set_values(cells, G0)
# print(M.Cell.fossil_carbon.get_values(cells))

try:
    r = random.uniform(size=nsocs)
    P0 = 6e9 * D.people * r / sum(r)  # 500e9 is middle ages, 6e9 would be yr 2000
    M.Society.population.set_values(societies, P0)
    M.Society.migrant_population.set_values(societies, P0 * 250e6/6e9)
    # print(M.Society.population.get_values(societies))
       
    r = random.uniform(size=nsocs)
    K0 = sum(P0) * 1e4 * D.dollars/D.people * r / sum(r)  # ?
    M.Society.physical_capital.set_values(societies, K0)
    # print(M.Society.physical_capital.get_values(societies))

    # for renewables, do NOT divide by number of socs:    
    r = random.uniform(size=nsocs)
    # in AWS paper: 1e12 (alternatively: 1e13):
    S0 = 1e12 * D.gigajoules * r / r.mean()
    M.Society.renewable_energy_knowledge.set_values(societies, S0)
    # print(M.Society.renewable_energy_knowledge.get_values(societies))

except:
    pass

# TODO: add noise to parameters

w = worlds[0]
s = societies[0]
c = cells[0]
for v in nature.variables: print(v,v.get_value(nature))
for v in metabolism.variables: print(v,v.get_value(metabolism))
for v in w.variables: print(v,v.get_value(w))
for v in s.variables: print(v,v.get_value(s))
for v in c.variables: print(v,v.get_value(c))

# from pycopancore.private._expressions import eval
# import pycopancore.model_components.base.interface as B
# import sympy as sp

runner = Runner(model=model)

start = time()
traj = runner.run(t_1=100, dt=1)


for v in nature.variables: print(v,v.get_value(nature))
for v in metabolism.variables: print(v,v.get_value(metabolism))
for v in w.variables: print(v,v.get_value(w))
for v in s.variables: print(v,v.get_value(s))
for v in c.variables: print(v,v.get_value(c))


from pickle import dump
dump(traj,open("/tmp/test.pickle","wb"))
print(time()-start, " seconds")

t = np.array(traj['t'])
print("max. time step", (t[1:]-t[:-1]).max())

plot(t, traj[M.World.atmospheric_carbon][worlds[0]], "b", lw=3)
plot(t, traj[M.World.upper_ocean_carbon][worlds[0]], "b--", lw=3)
plot(t, traj[M.World.terrestrial_carbon][worlds[0]], "g", lw=3)
plot(t, traj[M.World.fossil_carbon][worlds[0]], "gray", lw=3)
for s in societies:
    pass
    plot(t, traj[M.Society.population][s],"yellow",lw=2)
    plot(t, traj[M.Society.migrant_population][s],"-.",color="yellow",lw=2)
    plot(t, traj[M.Society.physical_capital][s], "k", lw=2)
    plot(t, traj[M.Society.renewable_energy_knowledge][s],
         color="darkorange", lw=2)
#    plot(t, traj[M.Society.carbon_emission_flow][s], "r--", lw=2)
#    plot(t, traj[M.Society.biomass_input_flow][s], "g--", lw=2)
#    plot(t, traj[M.Society.fossil_fuel_input_flow][s], "--", color="gray", lw=2)
#    plot(t, traj[M.Society.renewable_energy_input_flow][s], "--", color="darkorange", lw=2)
    plot(t[3:], traj[M.Society.wellbeing][s][3:],"magenta",lw=2)
#    plot(t, np.array(traj[M.Society.births][s]) - traj[M.Society.deaths][s],"--",color="yellow",lw=2)
#    plot(t, traj[M.Society.immigration][s],":",color="yellow",lw=2)
for c in cells:
    pass
#    plot(t, traj[M.Cell.terrestrial_carbon][c],"g")
#    plot(t, traj[M.Cell.fossil_carbon][c],"gray")
gca().set_yscale('symlog')

Bglobal = sum(traj[M.Society.biomass_input_flow][s][5] for s in societies) * D.gigatonnes_carbon / D.years
Fglobal = sum(traj[M.Society.fossil_fuel_input_flow][s][5] for s in societies) * D.gigatonnes_carbon / D.years
Rglobal = sum(traj[M.Society.renewable_energy_input_flow][s][5] for s in societies) * D.gigajoules / D.years
print((Bglobal * metabolism.biomass_energy_density * D.gigajoules/D.gigatonnes_carbon).tostr(unit=D.gigawatts),
      (Fglobal * metabolism.fossil_energy_density * D.gigajoules/D.gigatonnes_carbon).tostr(unit=D.gigawatts),
      Rglobal.tostr(unit=D.gigawatts)) # last should be ca. 100
print(Bglobal.tostr(unit=D.gigatonnes_carbon/D.years), # should be ca. 3
      Fglobal.tostr(unit=D.gigatonnes_carbon/D.years)) # should be ca. 11
print(sum(traj[M.Society.emigration][s][5] for s in societies)) # should be ca. 5e6
print(sum(traj[M.Individual.is_environmentally_friendly][i][-1] for i in individuals))

show()
