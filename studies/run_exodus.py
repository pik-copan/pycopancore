"""This is the test script for the seven dwarfs step by step tutorial.

In this version only the Step-process 'aging' of entitytype 'Individual' is
implemented, such that the only relevant attributes of 'Individual' are 'age'
and 'cell'.
"""

import random
from scipy import stats
from time import time
import datetime as dt
import numpy as np

import plotly.offline as py
import plotly.graph_objs as go

import pycopancore.models.exodus as M
from pycopancore.runners.runner import Runner


# setting timeinterval for run method 'Runner.run()'
timeinterval = 1
# setting time step to hand to 'Runner.run()'
timestep = .1
nm = 1  # number of municipalities, also cities
nc = 1  # number of counties, also farmland_cells
nf = 10  # number of farmers
nt = 10  # number of townsmen

model = M.Model()

# instantiate process taxa culture:
# In this certain case we need 'M.Culture()' for the acquaintance network.
culture = M.Culture()
metabolism = M.Metabolism(water_price=1)

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
county_allocation = list(counties)
for fc in range(nc):
    # chose county:
    county = random.choice(county_allocation)
    county_allocation.remove(county)
    farmland_cells.append(M.Cell(world=world,
                                 society=county,
                                 characteristic='farmland',
                                 land_area=20,
                                 average_precipitation=0.75))
# Instantiate city cells:
city_cells = []
municipality_allocation = list(municipalities)

for cc in range(nm):
    # chose county:
    municipality = random.choice(municipality_allocation)
    municipality_allocation.remove(municipality)
    city_cells.append(M.Cell(world=world,
                             society=municipality,
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
                                outspokensess=1,
                                liquidity=liq))
# Instantiate townsmen:
townsmen = []
for t in range(nt):
    # Chose cell
    city = random.choice(city_cells)
    # determine liquidity before first market:
    liq = stats.lognorm.rvs(scale=700, s=0.34, loc=0)
    townsmen.append(M.Individual(cell=city,
                                 profession='townsman',
                                 outspokensess=1,
                                 liquidity=liq))

# Create Network:
expected_degree = 5

# from run_adaptive_voter_model:


def erdosrenyify(graph, p=0.5):
    """Create a ErdosRenzi graph from networkx graph.

    Take a a networkx.Graph with nodes and distribute the edges following the
    erdos-renyi graph procedure.
    """
    assert not graph.edges(), "your graph has already edges"
    nodes = graph.nodes()
    for i, n1 in enumerate(nodes[:-1]):
        for n2 in nodes[i+1:]:
            if random.random() < p:
                graph.add_edge(n1, n2)


# set the initial graph structure to be an erdos-renyi graph
print("erdosrenyifying the graph ... ", end="", flush=True)
start = time()
erdosrenyify(culture.acquaintance_network, p=expected_degree / (nf + nt))
print("done ({})".format(dt.timedelta(seconds=(time() - start))))

start = time()
# Run market clearing once:
metabolism.do_market_clearing(0)
print("done ({})".format(dt.timedelta(seconds=(time() - start))))

print('\n runner starting')
# Runner is instantiated
r = Runner(model=model)

start = time()
# run the Runner and saving the return dict in traj
traj = r.run(t_1=timeinterval, dt=timestep)
runtime = dt.timedelta(seconds=(time() - start))
print('runtime: {runtime}'.format(**locals()))

# Plotting:
t = np.array(traj['t'])
for key, val in traj.items():
    print('key', key,)

print(traj[M.Metabolism.water_price])
city_population = np.array([traj[M.Society.population][soc]
                      for soc in municipalities])
county_population = np.array([traj[M.Society.population][soc]
                      for soc in counties])

population_data = []
for i, s in enumerate(municipalities):
    population_data.append(go.Scatter(
        x=t,
        y=city_population[i],
        name='population of municipality {}'.format(i),
        mode='lines',
        line=dict(
            color="green",
            width=4)
    ))

for i, s in enumerate(counties):
    population_data.append(go.Scatter(
        x=t,
        y=county_population[i],
        name='population of county {}'.format(i),
        mode='lines',
        line=dict(
            color="red",
            width=4)
    ))


layout = dict(title='Exodus',
              xaxis=dict(title='time [yr]'),
              yaxis=dict(title='value'),
              )

fig = dict(data=[population_data[0], population_data[1]],
           layout=layout)
py.plot(fig, filename='Exodus first results.html')
