"""This is the test script for the seven dwarfs step by step tutorial.

In this version only the Step-process 'aging' of entitytype 'Individual' is
implemented, such that the only relevant attributes of 'Individual' are 'age'
and 'cell'.
"""

import random
import numpy as np
from time import time
import datetime as dt

import plotly.offline as py
import plotly.graph_objs as go

import pycopancore.models.exodus as M
from pycopancore.runners.runner import Runner


# setting timeinterval for run method 'Runner.run()'
timeinterval = 100
# setting time step to hand to 'Runner.run()'
timestep = .1
nm = 1  # number of municipalities, also cities
nc = 1  # number of counties, also farmland_cells
nf = 100  # number of farmers
nt = 100  # number of townsmen

model = M.Model()

# instantiate process taxa culture:
# In this certain case we need 'M.Culture()' for the acquaintance network.
culture = M.Culture()
metabolism = M.Metabolism()

# instantiate world:
world = M.World(culture=culture, metabolism=metabolism)
# Instantiate Societies:
municipalities = [M.Society(world=world,
                            municipality_like=True,
                            base_mean_income=1000)
                  for m in range(nm)
                  ]
counties = [M.Society(world=world,
                      municipality_like=False)
            for c in range(nc)
            ]
# Instantiate farmland cells:
farmland_cells = []
for fc in range(nc):
    # chose county:
    county = random.choice(counties)
    counties.remove(county)
    farmland_cells.append(M.Cell(world=world,
                                 society=county,
                                 characteristic='farmland',
                                 land_area=20,
                                 average_precipitation=0.75))
# Instantiate city cells:
city_cells = []
for cc in range(nm):
    # chose county:
    municipality = random.choice(municipalities)
    municipalities.remove(municipality)
    city_cells.append(M.Cell(world=world,
                             society=municipality,
                             characteristic='city'))

# Instantiate farmers:
farmers = []
for f in range(nf):
    # Chose cell
    farmland = random.choice(farmland_cells)
    # determine liquidity before first market:
    liq = np.random.lognomal(mean=500, sigma=0.34)
    farmers.append(M.Individual(cell=farmland,
                                profession='farmer',
                                outspokensess=1,
                                liquidity=liq,
                                nutrition=1000))
# Instantiate townsmen:
townsmen = []
for t in range(nt):
    # Chose cell
    city = random.choice(city_cells)
    # determine liquidity before first market:
    liq = np.random.lognomal(mean=500, sigma=0.34)
    townsmen.append(M.Individual(cell=city,
                                 profession='townsman',
                                 outspokensess=1,
                                 liquidity=liq,
                                 nutrition=1000))

start = time()

print("done ({})".format(dt.timedelta(seconds=(time() - start))))

print('\n runner starting')

# Runner is instantiated
r = Runner(model=model)

start = time()
# run the Runner and saving the return dict in traj
traj = r.run(t_1=timeinterval, dt=timestep)
runtime = dt.timedelta(seconds=(time() - start))
print('runtime: {runtime}'.format(**locals()))
