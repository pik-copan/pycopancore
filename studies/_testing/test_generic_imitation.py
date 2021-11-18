"""Script to run example1 model."""

from time import time
from numpy import random, array
import numpy as np

import pycopancore.models._testing.test_generic_imitation as M
from pycopancore import master_data_model as D
from pycopancore.runners import Runner

from pylab import plot, gca, show, figure, subplot, gca, semilogy, legend

from numba.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning
import warnings
warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)

# first thing: set seed so that each execution must return same thing:
random.seed(10)

# parameters:

nworlds = 1  # no. worlds
nsocs = 5 # no. social_systems
ncells = 100  # no. cells
ninds = 1000 # no. individuals

t_1 = 2010

# choose one of two scenarios:
with_social = 0  # 0 or 1

# directory to store results:
dir = "/tmp/";

if with_social:
    filename = dir + "with_social.pickle"
    with_migration = 1
    with_awareness = 1
    with_learning = 1
    with_voting = 1
else:
    filename = dir + "without_social.pickle"
    with_migration = 0
    with_awareness = 0
    with_learning = 0
    with_voting = 0
with_spillovers = 1

print("Using model as defined in file", M.__file__)
model = M.Model()
runner = Runner(model=model)

# instantiate process taxa:
environment = M.Environment()
metabolism = M.Metabolism(
    renewable_energy_knowledge_spillover_fraction = 
        .1 if with_spillovers else 0,
    basic_emigration_probability_rate = 
        16e-13 if with_migration else 0, # leads to ca. 5mio. at 5 socs, (real)
    )
culture = M.Culture(
    awareness_lower_carbon_density=1e-4,
    awareness_upper_carbon_density=2e-4,
    awareness_update_rate = 10 if with_awareness else 0,
#    environmental_friendliness_learning_rate = 1 if with_learning else 0,
    max_protected_terrestrial_carbon_share=0,
    terrestrial_carbon_averaging_time=10,
    imi_traits = {'env': (M.Individual.is_environmentally_friendly,),
                  'tax': (M.SocialSystem.has_emissions_tax, M.SocialSystem.emissions_tax_level)},
    imi_rates = {'env': 5.0, 'tax': 5.0 },
    imi_types = {'tax': 'simple', 'env': 'threshold'},
    imi_p_in_batch = {'env': 0.2},  # 20% of individuals imitate at once 
    imi_batch_n = {'tax': 1},  # each social system imitates independently
    imi_networks = M.Culture.acquaintance_network,
    imi_n_neighbors_drawn = 2,
#    imi_abs_threshold = 2,
    imi_rel_threshold = 1e-9,
    imi_p_imitate = {'env': {((True,),(False,)): 0.5, ((False,),(False,)): 1.0 }, 
                     'tax': 1.0},
    
    )

# generate entities and plug them together at random:
worlds = [M.World(environment=environment, 
                  metabolism=metabolism, 
                  culture=culture,
                  atmospheric_carbon = 830 * D.gigatonnes_carbon,
                  upper_ocean_carbon = (5500 - 830 - 2480 - 1125) * D.GtC
                  ) for w in range(nworlds)]
social_systems = [M.SocialSystem(
                    world=random.choice(worlds),
                    has_renewable_subsidy = random.choice([False, True], 
                                                          p=[3/4, 1/4]),
                    has_emissions_tax = random.choice([False, True], 
                                                      p=[4/5, 1/5]),
                    has_fossil_ban = False, 
                    time_between_votes = 4 if with_voting else 1e100, 
                    ) for s in range(nsocs)]
cells = [M.Cell(social_system=random.choice(social_systems))
         for c in range(ncells)]
individuals = [M.Individual(
                cell=random.choice(cells),
                is_environmentally_friendly = 
                    random.choice([False, True], p=[.7, .3]), 
                relative_weight=random.geometric(0.1)
                ) 
               for i in range(ninds)]

# initialize block model acquaintance network:
target_degree = 150
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
for s1 in social_systems:
    for s2 in social_systems:
        culture.acquaintance_network.add_edge(s1, s2)

# set renewable sector productivities randomly:
rel_prod = 2 * random.uniform(size=ncells)
M.Cell.renewable_sector_productivity.set_values(cells, rel_prod * M.Cell.renewable_sector_productivity.default)

# distribute area and vegetation randomly but correlatedly:
r = random.uniform(size=ncells)
Sigma0 = 1.5e8 * D.square_kilometers * r / sum(r)
M.Cell.land_area.set_values(cells, Sigma0)

r += random.uniform(size=ncells)
L0 = 2480 * D.gigatonnes_carbon * r / sum(r)  # 2480 is yr 2000
M.Cell.terrestrial_carbon.set_values(cells, L0)
M.Cell.mean_past_terrestrial_carbon.set_values(cells, L0)

r = np.exp(random.normal(size=ncells))
G0 = 1125 * D.gigatonnes_carbon * r / sum(r)  # 1125 is yr 2000
M.Cell.fossil_carbon.set_values(cells, G0)

r = random.uniform(size=nsocs)
P0 = 6e9 * D.people * r / sum(r)  # 6e9 is yr 2000
M.SocialSystem.population.set_values(social_systems, P0)
M.SocialSystem.migrant_population.set_values(social_systems, P0 * 250e6 / 6e9)
for s in social_systems:
    s.max_protected_terrestrial_carbon = \
        0.90 * sum(c.terrestrial_carbon for c in s.cells)
 
r = random.uniform(size=nsocs)
K0 = sum(P0) * 1e4 * D.dollars/D.people * r / sum(r)  # ?
M.SocialSystem.physical_capital.set_values(social_systems, K0)

# for renewables, do NOT divide by number of socs:    
r = random.uniform(size=nsocs)
S0 = 1e12 * D.gigajoules * r / r.mean()
M.SocialSystem.renewable_energy_knowledge.set_values(social_systems, S0)

# do simulation:
start = time()
traj = runner.run(t_0=2000, t_1=t_1, dt=1, 
                  add_to_output=[M.Individual.represented_population,
                                 M.Cell.mean_past_terrestrial_carbon])

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
