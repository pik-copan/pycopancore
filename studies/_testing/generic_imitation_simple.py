"""Script to run example1 model."""

from pycopancore import config
config.profile = False

from time import time
from numpy import random
# first thing: set seed so that each execution must return same thing:
#random.seed(10)

import numpy as np
import pylab as plt

import pycopancore.models._testing.generic_imitation.simple as M
from pycopancore import master_data_model as D
from pycopancore.runners import Runner


from numba.errors import NumbaDeprecationWarning, NumbaPendingDeprecationWarning
import warnings
warnings.simplefilter('ignore', category=NumbaDeprecationWarning)
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)

# parameters:

nworlds = 1 # no. worlds
nsocs = 100 # no. social_systems
ncells = 100  # no. cells
ninds = 100 # no. individuals

ER_p = 0.5

t_1 = 1

dir = "/tmp/";

print("Using model as defined in file", M.__file__)
model = M.Model()
runner = Runner(model=model)

"""
'bool': Granovetter-style activation
'ord': 'meet two' complex contagion
'pair': 'take the best' learning 
"""
culture = M.Culture(
    imi_rate = {
        'bool': 10000,   # -> 10000 updates
        'ord': 1000,  # *10 in batch -> 10000 updates
        'pair': 200, # *~50 in batch -> 10000 updates
        '*': 0,
        },
    imi_type = 'complex',
    imi_batch_n = {'bool': 1, 'ord': 10},
    imi_p_in_batch = {'pair': 0.5},
    imi_network = M.Culture.acquaintance_network,
    imi_p_neighbor_drawn = {'bool': 1.0, 'pair': 1.0},
    imi_n_neighbors_drawn = {'ord': 20},
    imi_rel_threshold = {'bool': { 
            ((False,),(True,)): 0.4, 
            ((True,),(False,)): 0.8
        }},
    imi_abs_threshold = {'ord': 2, 'pair': 0},
    imi_include_own_trait = {'pair': True, '*': False},
    imi_delta = {'pair': 10.0},  # evaluation will be done by Individual.imi_evaluate_pair
    imi_p_imitate = {'pair': 1.0, 'bool': {
            ((False,),(True,)): 0.9, 
            ((True,),(False,)): 0.7
        }}  # for 'ord', the value is set by Cell.imi_p_imitate_ord
    )

worlds = [M.World(culture=culture) for w in range(nworlds)]

social_systems = [
    M.SocialSystem(
        world=random.choice(worlds),
        is_active=random.choice([False, True], p=[0.65,0.35]),
    ) for s in range(nsocs)]

cells = [
    M.Cell(
        social_system=random.choice(social_systems),
        an_ordinal_var=random.choice(M.Cell.an_ordinal_var.levels),
    ) for c in range(ncells)]

individuals = [
    M.Individual(
        cell=random.choice(cells),
        a_nominal_var=random.choice(M.Individual.a_nominal_var.levels),
        a_dimensional_var=random.normal(),
        a_criterion=random.normal(),
        ) for i in range(ninds)]

for list in [social_systems, cells, individuals]:
    for index, i in enumerate(list):
        for j in list[:index]:
            if random.uniform() < ER_p:
                culture.acquaintance_network.add_edge(i, j)

# now profile the whole thing:

from pycopancore import profile

#@profile
def doit():
    start = time()
    res = runner.run(t_0=0, t_1=t_1, dt=1)
    end = time()
    print(end-start, "seconds")
    return res
    
traj = doit()

print(culture.imi_event_counter, culture.imi_trigger_counter, culture.imi_update_counter, culture.imi_imitate_counter)

t = traj['t']

plt.plot(t, np.sum([l for e,l in traj[M.SocialSystem.is_active].items()], axis = 0),
         label="# SocialSystem.is_active")

for level in M.Cell.an_ordinal_var.levels:
    plt.plot(t, np.sum([[v==level for v in l] for e,l in traj[M.Cell.an_ordinal_var].items()], axis = 0), "-.",
    label="# Cell.an_ordinal_var="+str(level))

for level in M.Individual.a_nominal_var.levels:
    plt.plot(t, np.sum([[v==level for v in l] for e,l in traj[M.Individual.a_nominal_var].items()], axis = 0), ".", 
    label="# Individual.a_nominal_var="+str(level))

plt.plot(t, np.mean([l for e,l in traj[M.Individual.a_dimensional_var].items()], axis = 0), "-",
         label="mean Individual.a_dimensional_var")
    
plt.legend()
plt.show()

profile.print_stats()
