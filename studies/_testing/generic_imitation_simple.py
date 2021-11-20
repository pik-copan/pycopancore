"""Script to run example1 model."""

from pycopancore import config
config.profile = True

from numpy import random
# first thing: set seed so that each execution must return same thing:
random.seed(10)

import numpy as np

import pycopancore.models._testing.generic_imitation.simple as M
from pycopancore import master_data_model as D
from pycopancore.runners import Runner


from numba.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning
import warnings
warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)

# parameters:

nworlds = 1  # no. worlds
nsocs = 10 # no. social_systems
ncells = 100  # no. cells
ninds = 1000 # no. individuals

ER_p = 0.5

t_1 = 1

dir = "/tmp/";

print("Using model as defined in file", M.__file__)
model = M.Model()
runner = Runner(model=model)

"""
'bool': Granovetter-style activation
'ord': 'take the best' learning
'pair' 'meet two' complex contagion
"""
culture = M.Culture(
    imi_rate = 1.0,
    imi_type = 'complex',
    imi_batch_n = {'bool': 1, 'ord': 2},
    imi_p_in_batch = {'pair': 0.5},
    imi_network = M.Culture.acquaintance_network,
    imi_p_neighbor_drawn = {'bool': 1.0, 'ord': 1.0},
    imi_n_neighbors_drawn = {'pair': 2},
    imi_rel_threshold = {'bool': { 
            ((False,),(True,)): 0.4, 
            ((True,),(False,)): 0.8
        }},
    imi_abs_threshold = {'pair': 2, 'ord': 0},
    imi_include_own_trait = {'ord': True, '*': False},
    imi_delta = {'ord': 0.0},  # evaluation will be done by Cell.imi_evaluate_ord
    imi_p_imitate = {'ord': 1.0, 'bool': {
            ((False,),(True,)): 0.9, 
            ((True,),(False,)): 0.7
        }}  # for 'pair', the value is set by Individual.imi_p_imitate_pair
    )

worlds = [M.World(culture=culture) for w in range(nworlds)]

social_systems = [
    M.SocialSystem(
        world=random.choice(worlds),
        is_active=random.choice([False, True], p=[0.9,0.1]),
    ) for s in range(nsocs)]

cells = [
    M.Cell(
        social_system=random.choice(social_systems),
        an_ordinal_var=random.choice(M.Cell.an_ordinal_var.levels),
        a_criterion=random.normal(),
    ) for c in range(ncells)]

individuals = [
    M.Individual(
        cell=random.choice(cells),
        a_nominal_var=random.choice(M.Individual.a_nominal_var.levels),
        a_dimensional_var=random.normal(),
        ) for i in range(ninds)]

for list in [social_systems, cells, individuals]:
    for index, i in enumerate(list):
        for j in list[:index]:
            if random.uniform() < ER_p:
                culture.acquaintance_network.add_edge(i, j)

# now profile the whole thing:

from pycopancore import profile

@profile
def doit():
    return runner.run(t_0=0, t_1=t_1, dt=1)

traj = doit()

print(traj[M.SocialSystem.is_active][social_systems[0]])
print(traj[M.Cell.an_ordinal_var][cells[0]])
print(traj[M.Individual.a_dimensional_var][individuals[0]])

profile.print_stats()
