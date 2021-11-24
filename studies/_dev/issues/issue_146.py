"""Script to run example1 model."""

from time import time
from numpy import random, array
import numpy as np

import pycopancore.models._dev.issues.issue_146 as M
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

t_1 = 2120

# directory to store results:
dir = "/tmp/";

filename = dir + "with_social.pickle"

print("Using model as defined in file", M.__file__)
model = M.Model()
runner = Runner(model=model)

# instantiate process taxa:
environment = M.Environment()
metabolism = M.Metabolism()
culture = M.Culture()

# generate entities and plug them together at random:
worlds = [M.World(environment=environment, 
                  metabolism=metabolism, 
                  culture=culture,
                  ) for w in range(nworlds)]
social_systems = [M.SocialSystem(
                    world=random.choice(worlds),
                    has_renewable_subsidy = random.choice([False, True], 
                                                          p=[3/4, 1/4]),
                    has_emissions_tax = random.choice([False, True], 
                                                      p=[4/5, 1/5]),
                    has_fossil_ban = False, 
                    time_between_votes = 4, 
                    ) for s in range(nsocs)]
cells = [M.Cell(social_system=random.choice(social_systems))
         for c in range(ncells)]
individuals = [M.Individual(
                cell=random.choice(cells),
                is_environmentally_friendly = 
                    random.choice([False, True], p=[.7, .3]), 
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

# distribute area and vegetation randomly but correlatedly:
r = random.uniform(size=ncells)
Sigma0 = 1.5e8 * D.square_kilometers * r / sum(r)
M.Cell.land_area.set_values(cells, Sigma0)

r += random.uniform(size=ncells)
L0 = 2480 * D.gigatonnes_carbon * r / sum(r)  # 2480 is yr 2000
M.Cell.terrestrial_carbon.set_values(cells, L0)

for s in social_systems:
    s.max_protected_terrestrial_carbon = \
        0.90 * sum(c.terrestrial_carbon for c in s.cells)

# do simulation:
start = time()
traj = runner.run(t_0=2000, t_1=t_1, dt=1)

print(time()-start, " seconds")

t = np.array(traj['t'])
print("max. time step", (t[1:]-t[:-1]).max())

