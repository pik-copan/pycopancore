"""This is the test exodus model.

In this version only the Step-process 'aging' of entitytype 'Individual' is
implemented, such that the only relevant attributes of 'Individual' are 'age'
and 'cell'.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

import random
from scipy import stats
from time import time
import datetime as dt
import numpy as np
import networkx as nx
import pickle, json

#import plotly.offline as py
#import plotly.graph_objs as go
from matplotlib.pyplot import plot, gca, show, savefig

import pycopancore.models.exodus as M
from pycopancore.runners.runner import Runner


# setting timeinterval for run method 'Runner.run()'
timeinterval = 200
# setting time step to hand to 'Runner.run()'
timestep = .1

nm = 1  # number of municipalities, also cities
nc = 1  # number of counties, also farmland_cells
na = 200  # number of agents
pf = .5  # percentage of farmers
nf = int(na * pf)  # number of farmers
nt = int(na - nf)  # number of townsmen


model = M.Model()

# instantiate process taxa culture:
# In this certain case we need 'M.Culture()' for the acquaintance network.
culture = M.Culture(fully_connected_network=True)  # fully connected -> static network
metabolism = M.Metabolism(market_frequency=1)

# instantiate world:
world = M.World(culture=culture, metabolism=metabolism,
                water_price=.1)
# Instantiate Social Systems:
municipalities = [M.SocialSystem(world=world,
                            municipality_like=True,
                            base_mean_income=6130,
                            scaling_parameter=1.12,
                            migration_cost=0,
                            last_one_standing=False,
                            continuous_exploration=False)
                  for m in range(nm)
                  ]

counties = [M.SocialSystem(world=world,
                      municipality_like=False,
                      migration_cost=0,
                      last_one_standing=False,
                      continuous_exploration=False)
            for c in range(nc)
            ]
# Instantiate farmland cells:
farmland_cells = []
county_allocation = list(counties)
for fc in range(nc):
    # chose county:
    county = random.choice(county_allocation)
    county_allocation.remove(county)
    farmland_cells.append(M.Cell(world=world,
                                 social_system=county,
                                 characteristic='farmland',
                                 land_area=0.0025 * (nf + nt) / nc,  # in square kilometers
                                 average_precipitation=0.75))
# Instantiate city cells:
city_cells = []
municipality_allocation = list(municipalities)

for cc in range(nm):
    # chose county:
    municipality = random.choice(municipality_allocation)
    municipality_allocation.remove(municipality)
    city_cells.append(M.Cell(world=world,
                             social_system=municipality,
                             characteristic='city',
                             average_precipitation=0))

# Instantiate farmers:
farmers = []
for f in range(nf):
    # Chose cell
    farmland = random.choice(farmland_cells)
    # determine liquidity before first market:
    liq = stats.lognorm.rvs(scale=300, s=0.34, loc=0)
    farmers.append(M.Individual(cell=farmland,
                                profession='farmer',
                                outspokenness=3,
                                liquidity=liq,
                                nutrition=1000))
# Instantiate townsmen:
townsmen = []
for t in range(nt):
    # Chose cell
    city = random.choice(city_cells)
    # determine liquidity before first market:
    liq = stats.lognorm.rvs(scale=700, s=0.34, loc=0)
    townsmen.append(M.Individual(cell=city,
                                 profession='townsman',
                                 outspokenness=3,
                                 liquidity=liq,
                                 nutrition=100))

start = time()
# Calculate social_systems variables before run:
print('calculating social_system attributes before run:')
for soc in M.SocialSystem.instances:
    soc.calc_population(0)
    soc.calculate_mean_income_or_farmsize(0)
    soc.calculate_average_liquidity(0)
# Calculate other stuff:
for ind in M.Individual.instances:
    ind.calc_farm_size()
    ind.calc_gross_income()
    ind.calculate_harvest(0)
    ind.calculate_utility(0)
for soc in M.SocialSystem.instances:
    soc.calculate_average_utility(0)
    soc.calculate_gini(0)
    soc.calculate_migration_rate(0)

world.calc_total_gross_income(0)
world.calc_total_harvest(0)
world.calc_total_nutrition(0)
world.calc_total_liquidity(0)

# Run market clearing once:
metabolism.do_market_clearing(0)

print("done ({})".format(dt.timedelta(seconds=(time() - start))))

termination_conditions = [[M.Metabolism.check_for_market_equilibrium, metabolism],
                          [M.World.check_for_exceptions, world]]

print('\n runner starting')
# Runner is instantiated
r = Runner(model=model, termination_calls=termination_conditions
           )

start = time()
# run the Runner and saving the return dict in traj
traj = r.run(t_1=timeinterval,
             dt=timestep,
             max_resolution=True
             )
runtime = dt.timedelta(seconds=(time() - start))
print('runtime: {runtime}'.format(**locals()))


# Saving:
print('saving:')
#traj.save(filename='data')
print('...is done')

# Plotting:
t = np.array(traj['t'])
# for key, val in traj.items():
#     print('key', key,)
plot(t, traj[M.World.water_price][world], "b", lw=3)
#plot(t, traj[M.World.total_gross_income][world], "m:", lw=3)
#plot(t, traj[M.World.total_harvest][world], "m--", lw=3)
# plot(t, traj[M.Culture.network_clustering][culture], "r--", lw=3)
# plot(t, traj[M.Culture.modularity][culture], "r:", lw=3)

for soc in municipalities:
    plot(t, traj[M.SocialSystem.population][soc], "r", lw=3)
    #plot(t, traj[M.SocialSystem.average_utility][soc], "r:", lw=3)
    #plot(t, traj[M.SocialSystem.gini_coefficient][soc], "r--", lw=3)
for soc in counties:
    plot(t, traj[M.SocialSystem.population][soc], "k", lw=3)
    #plot(t, traj[M.SocialSystem.average_utility][soc], "k:", lw=3)
    #plot(t, traj[M.SocialSystem.gini_coefficient][soc], "k--", lw=3)

# for ind in M.Individual.instances:
#    plot(t, traj[M.Individual.utility][ind], "y", lw=0.5)
gca().set_yscale('symlog')

# savefig('20_ag_4_soc.png', dpi=150)
show()

