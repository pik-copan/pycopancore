"""Script to run example2 model."""

from time import time
from numpy import random, array
import numpy as np

import pycopancore.models.example2 as M
from pycopancore import master_data_model as D
from pycopancore.runners import Runner

from pylab import plot, gca, show, figure, subplot, gca, semilogy, legend

# first thing: set seed so that each execution must return same thing:
random.seed(10)

# parameters:

nworlds = 1  # no. worlds
nsocs = 2 # no. social_systems
ncells = 4  # no. cells
ninds = 400 # no. individuals

t_1 = 2120

# choose one of two scenarios:
filename = "/home/jobst/work/with.pickle"
#filename = "/home/jobst/work/without.pickle"
# (these files will be read by plot_example1.py)

if filename == "/home/jobst/work/with.pickle":
    with_awareness = 1
    with_learning = 1
    with_voting = 1
else:
    with_awareness = 0
    with_learning = 0
    with_voting = 0

model = M.Model()

# instantiate process taxa:

environment = M.Environment()

metabolism = M.Metabolism(
    renewable_energy_knowledge_spillover_fraction = 0
    )

culture = M.Culture(
    awareness_lower_carbon_density=1e-5,
    awareness_upper_carbon_density=4e-5,
    awareness_update_rate = 1 if with_awareness else 0,
    environmental_friendliness_learning_rate = 1 if with_learning else 0,
    )

# generate entities and plug them together:

(world, ) = worlds = [M.World(
    environment = environment, 
    metabolism = metabolism, 
    culture = culture,
    atmospheric_carbon = 830 * D.gigatonnes_carbon,
    upper_ocean_carbon = (5500 - 830 - 2480 - 1125) * D.GtC
    ) for w in range(nworlds)]

(north, south) = social_systems = [M.SocialSystem(
    world = world,
    has_renewable_subsidy = False,
    has_emissions_tax = False,
    has_fossil_ban = False,
    emissions_tax_intro_threshold = 0.5, # disabled
    renewable_subsidy_intro_threshold = 1, # disabled
    fossil_ban_intro_threshold = 1, # disabled
    emissions_tax_level = 30 * 200e9, # see Wikipedia social cost of carbon. 100e9*3.5,
    time_between_votes = 4 if with_voting else 1e100, 
    ) for s in range(nsocs)]

(boreal, temperate, subtropical, tropical) = cells = [M.Cell(
    social_system = social_systems[c//2],
    renewable_sector_productivity = [.7, .9, 1.1, 1.3][c]
        * 2000 * M.Cell.renewable_sector_productivity.default,
        # represents dependency of solar energy on solar insolation angle
    fossil_sector_productivity = M.Cell.fossil_sector_productivity.default * 7,
    biomass_sector_productivity = M.Cell.biomass_sector_productivity.default * 5
    # these values result in realistic total energy production for the year 2000, see below
    ) for c in range(ncells)]

individuals = [M.Individual(
                cell = cells[i%4],
                is_environmentally_friendly = 
                    random.choice([False, True], p=[.8, .2]), # represents the "20% suffice" assumption 
                ) 
               for i in range(ninds)]

# initialize block model acquaintance network:
target_degree = 10 # = 2.5% of all agents. Dunbar's number would be too large
target_degree_samecell = 0.5 * target_degree
target_degree_samesoc = 0.35 * target_degree
target_degree_other = 0.15 * target_degree
p_samecell = target_degree_samecell / (ninds/ncells - 1)
p_samesoc = target_degree_samesoc / (ninds/nsocs - ninds/ncells - 1)
p_other = target_degree_other / (ninds - ninds/nsocs - 1)
for index, i in enumerate(individuals):
    for j in individuals[:index]:
        if random.uniform() < (
                p_samecell if i.cell == j.cell 
                else p_samesoc if i.social_system == j.social_system \
                else p_other):
            culture.acquaintance_network.add_edge(i, j)

# distribute area and vegetation uniformly since it seems there are no real differences between the actual zones:
Sigma0 = 1.5e8 * D.square_kilometers * array([0.25, 0.25,  .25, .36])
M.Cell.land_area.set_values(cells, Sigma0)

L0 = 2480 * D.gigatonnes_carbon * array([0.25, 0.25,  .25, .25])  # 2480 is yr 2000
M.Cell.terrestrial_carbon.set_values(cells, L0)

# distribute fossils linearly from north to south:
G0 = 1125 * D.gigatonnes_carbon * array([.4, .3,  .2, .1])  # 1125 is yr 2000
M.Cell.fossil_carbon.set_values(cells, G0)

# distribute population 1:3 between north and south, and 2:3 within each:
r = random.uniform(size=nsocs)
P0 = 6e9 * D.people * array([0.1, 0.15,  0.3, 0.45])  # 6e9 is yr 2000
M.SocialSystem.population.set_values(social_systems, P0)

# distribute capital 2:1:
K0 = sum(P0) * 1e4 * D.dollars/D.people * array([2/3, 1/3])
M.SocialSystem.physical_capital.set_values(social_systems, K0)

S0 = 1e12 * D.gigajoules * array([1, 1])
M.SocialSystem.renewable_energy_knowledge.set_values(social_systems, S0)

w = worlds[0]
s = social_systems[0]
c = cells[0]
for v in environment.variables: print(v,v.get_value(environment))
for v in metabolism.variables: print(v,v.get_value(metabolism))
for v in w.variables: print(v,v.get_value(w))
for v in s.variables: print(v,v.get_value(s))
for v in c.variables: print(v,v.get_value(c))


# do simulation:
runner = Runner(model=model)
start = time()
traj = runner.run(t_0=2000, t_1=t_1, dt=1, 
                  add_to_output=[
                    M.Individual.represented_population, 
                    M.SocialSystem.population
                    ])


for v in environment.variables: print(v,v.get_value(environment))
for v in metabolism.variables: print(v,v.get_value(metabolism))
for v in w.variables: print(v,v.get_value(w))
for v in s.variables: print(v,v.get_value(s))
for v in c.variables: print(v,v.get_value(c))


from pickle import dump
tosave = {
          v.owning_class.__name__ + "."
          + v.codename: {str(e): traj[v][e]
                         for e in traj[v].keys()
                         } 
          for v in traj.keys() if v is not "t"
          }
tosave["t"] = traj["t"]
dump(tosave, open(filename,"wb"))
print(time()-start, " seconds")

t = np.array(traj['t'])
print("max. time step", (t[1:]-t[:-1]).max())

print("\nyr 2000 values (real):")
print("photo (123):",sum(traj[M.Cell.photosynthesis_carbon_flow][c][5] 
                         for c in cells))
print("resp (118):",sum(traj[M.Cell.terrestrial_respiration_carbon_flow][c][5] 
                        for c in cells))
print("GWP (4e13):",sum(traj[M.SocialSystem.economic_output_flow][s][5] 
                        for s in social_systems))
B0 = sum(traj[M.SocialSystem.biomass_input_flow][s][5] 
         for s in social_systems)
Bglobal = B0 * D.gigatonnes_carbon / D.years
Fglobal = sum(traj[M.SocialSystem.fossil_fuel_input_flow][s][5] 
              for s in social_systems) * D.gigatonnes_carbon / D.years
Rglobal = sum(traj[M.SocialSystem.renewable_energy_input_flow][s][5] 
              for s in social_systems) * D.gigajoules / D.years
Eglobal = sum(traj[M.SocialSystem.secondary_energy_flow][s][5] 
              for s in social_systems) * D.gigajoules / D.years
print("B (3), F (11), R(100):",
      Bglobal, Bglobal.tostr(unit=D.gigatonnes_carbon/D.years),
      Fglobal, Fglobal.tostr(unit=D.gigatonnes_carbon/D.years),
      Rglobal, Rglobal.tostr(unit=D.gigawatts),
      ) 
print("cap. deprec. at begin (0.1?):",
      np.mean([traj[M.SocialSystem.physical_capital_depreciation_rate][s][5] 
               for s in social_systems]))
print("cap. deprec. at end (0.1?):",
      np.mean([traj[M.SocialSystem.physical_capital_depreciation_rate][s][-1] 
               for s in social_systems]))
print("temp. at begin:", traj[M.World.surface_air_temperature][worlds[0]][5])
print("temp. at end:", traj[M.World.surface_air_temperature][worlds[0]][-1])
print("has emissions tax at begin", traj[M.SocialSystem.has_emissions_tax][north][5])
print("has emissions tax at end", traj[M.SocialSystem.has_emissions_tax][north][-1])
print("biomass prod. at begin", traj[M.Cell.biomass_relative_productivity][boreal][5] / traj[M.Cell.terrestrial_carbon][boreal][5]**2)
print("biomass prod. at end", traj[M.Cell.biomass_relative_productivity][boreal][-1] / traj[M.Cell.terrestrial_carbon][boreal][-1]**2)

