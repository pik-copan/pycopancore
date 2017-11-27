# @PydevCodeAnalysisIgnore

from time import time
from numpy import random, array, average, exp
from pylab import show, subplots

from pycopancore import master_data_model as D
from pycopancore.runners import Runner

import pycopancore.models.coccon.full as M

# first thing: set seed so that each execution must return same thing:

random.seed(1)

# parameters:

nworlds = 1  # no. worlds
nsocs = 5 #2    # no. social_systems
ncells = 50 #20  # no. cells
ninds = 500 #200  # no. individuals
years = 100  # time to simulate

# instantiate model and process taxa:

model = M.Model()
environment = M.Environment()
metabolism = M.Metabolism(
    renewable_energy_knowledge_spillover_fraction = 0,
#    renewable_energy_knowledge_spillover_fraction = .5,
    basic_emigration_probability_rate = 0,
#    basic_emigration_probability_rate = 1e-13,
    )
culture = M.Culture(
    awareness_lower_carbon_density=1e-4,
    awareness_upper_carbon_density=2e-4,
    awareness_update_rate=0,
#    awareness_update_rate=.5,
    environmental_friendliness_learning_rate=0,
#    environmental_friendliness_learning_rate=1,
    )

# generate entities and plug them together at random:

world = M.World(environment=environment, metabolism=metabolism, culture=culture,
                atmospheric_carbon = 830 * D.gigatonnes_carbon,
                upper_ocean_carbon = (5500 - 830 - 2480 - 1125) * D.gigatonnes_carbon
                )
social_systems = [M.SocialSystem(world=world,
                       has_renewable_subsidy = random.choice([False, True], p=[3/4, 1/4]),
                       has_emissions_tax = random.choice([False, True], p=[4/5, 1/5]),
                       has_fossil_ban = False,
                       time_between_votes = 1e100,
#                       time_between_votes = 4,
                       ) 
             for s in range(nsocs)]
cells = [M.Cell(social_system=random.choice(social_systems),
                renewable_sector_productivity = 2 * random.rand() * M.Cell.renewable_sector_productivity.default
                )
         for c in range(ncells)]
individuals = [M.Individual(cell=random.choice(cells),
                            is_environmentally_friendly = random.choice([False, True], p=[.7, .3]),
                            ) 
               for i in range(ninds)]

# initialize block model acquaintance network:

target_degree = 20
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

# distribute global aggregate quantities to cells and social_systems:

r = random.uniform(size=ncells)
Sigma0 = 1.5e8 * D.square_kilometers * r / sum(r)
M.Cell.land_area.set_values(cells, Sigma0)

r += random.uniform(size=ncells)
L0 = 2480 * D.gigatonnes_carbon * r / sum(r)  # 2480 is yr 2000
M.Cell.terrestrial_carbon.set_values(cells, L0)

r = exp(random.normal(size=ncells))
G0 = 1125 * D.gigatonnes_carbon * r / sum(r)  # 1125 is yr 2000
M.Cell.fossil_carbon.set_values(cells, G0)

r = random.uniform(size=nsocs)
P0 = 6e9 * D.people * r / sum(r)  # 500e9 is middle ages, 6e9 would be yr 2000
M.SocialSystem.population.set_values(social_systems, P0)
M.SocialSystem.migrant_population.set_values(social_systems, P0 * 250e6/6e9)
for s in social_systems:
    s.max_protected_terrestrial_carbon = 0.90 * sum(c.terrestrial_carbon for c in s.cells)

r = random.uniform(size=nsocs)
K0 = sum(P0) * 1e4 * D.dollars/D.people * r / sum(r)
M.SocialSystem.physical_capital.set_values(social_systems, K0)

r = random.uniform(size=nsocs)
S0 = 1e12 * D.gigajoules * r / r.mean()
M.SocialSystem.renewable_energy_knowledge.set_values(social_systems, S0)

# print initial global state:

for v in culture.variables: 
    if v.unit: print(v, v.get_quantity(culture))
for v in environment.variables:
    if v.unit: print(v, v.get_quantity(environment))
for v in metabolism.variables: 
    if v.unit: print(v, v.get_quantity(metabolism))
for v in world.variables: 
    if v.unit: print(v, v.get_quantity(world))

# run simulation:

runner = Runner(model=model)
starttime = time()
traj = runner.run(t_0=2000, t_1=2000+years, dt=1, 
                  add_to_output=[M.Individual.represented_population])

# plots:

t = array(traj['t'])

fig, (ax1,ax2,ax3) = subplots(3, sharex=True)

ax1.plot(t[3:], 100*average(array([traj[M.Individual.is_environmentally_friendly][i][3:] for i in individuals]), 
                            weights=[traj[M.Individual.represented_population][i][0] for i in individuals],
                            axis=0), 
                            "--", color="green", lw=1, label="env. friendly individuals")
ax1.plot(t[3:], 100*average(array([traj[M.SocialSystem.has_renewable_subsidy][s][3:] for s in social_systems]), axis=0),
         color="orange", lw=2, label="social_systems with renewable subsidy")
ax1.plot(t[3:], 100*average(array([traj[M.SocialSystem.has_emissions_tax][s][3:] for s in social_systems]), axis=0),
         color="blue", lw=2, label="social_systems with emissions tax")
ax1.plot(t[3:], 100*average(array([traj[M.SocialSystem.has_fossil_ban][s][3:] for s in social_systems]), axis=0),
         color="black", lw=2, label="social_systems with fossil ban")
ax1.set_ylabel('percent')
ax1.legend()

for i, s in enumerate(social_systems):
    ax2.semilogy(t[3:], traj[M.SocialSystem.population][s][3:], color="yellow", lw=2, label="population [humans]" if i==0 else None)
    ax2.semilogy(t[3:], traj[M.SocialSystem.physical_capital][s][3:], color="black", lw=2, label="physical capital [$]" if i==0 else None)
    ax2.semilogy(t[3:], traj[M.SocialSystem.renewable_energy_knowledge][s][3:], color="orange", lw=2, label="renewable energy knowledge [GJ]" if i==0 else None)
ax2.set_ylabel('(mixed units)')
ax2.legend()

ax3.plot(t[3:], traj[M.World.atmospheric_carbon][world][3:], color="cyan", lw=3, label="atmospheric carbon")
ax3.plot(t[3:], traj[M.World.upper_ocean_carbon][world][3:], color="blue", lw=3, label="upper ocean carbon")
ax3.plot(t[3:], traj[M.World.terrestrial_carbon][world][3:], color="green", lw=3, label="terrestrial carbon")
ax3.plot(t[3:], traj[M.World.fossil_carbon][world][3:], color="gray", lw=3, label="fossil carbon")
ax3.set_ylabel('global GtC')
ax3.legend()
ax3b = ax3.twinx()
for c in cells:
    ax3b.plot(t[3:], traj[M.Cell.terrestrial_carbon][c][3:], color="green", lw=1, alpha=0.2)
ax3b.set_ylabel("cells' GtC")

print(time()-starttime, " seconds")

show()


