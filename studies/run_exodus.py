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
import networkx as nx
import pickle, json

import plotly.offline as py
import plotly.graph_objs as go
from matplotlib.pyplot import plot, gca, show, savefig

import pycopancore.models.exodus as M
from pycopancore.runners.runner import Runner


# setting timeinterval for run method 'Runner.run()'
timeinterval = 50
# setting time step to hand to 'Runner.run()'
timestep = .1

nm = 5  # number of municipalities, also cities
nc = 5  # number of counties, also farmland_cells
na = 200  # number of agents
pf = .9  # percentage of farmers
nf = int(na * pf)  # number of farmers
nt = int(na - nf)  # number of townsmen


model = M.Model()

# instantiate process taxa culture:
# In this certain case we need 'M.Culture()' for the acquaintance network.
culture = M.Culture(fully_connected_network=True)
metabolism = M.Metabolism(market_frequency=1)

# instantiate world:
world = M.World(culture=culture, metabolism=metabolism,
                water_price=1)
# Instantiate Societies:
municipalities = [M.Society(world=world,
                            municipality_like=True,
                            base_mean_income=1000,
                            scaling_parameter=1.12,
                            migration_cost=0)
                  for m in range(nm)
                  ]

counties = [M.Society(world=world,
                      municipality_like=False,
                      migration_cost=0)
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
                                 land_area=0.01 * (nf + nt),  # in square kilometers
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
                                outspokenness=.1,
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
                                 outspokenness=.1,
                                 liquidity=liq,
                                 nutrition=100))

# # Create Network:
# expected_degree = 5
#
# # from run_adaptive_voter_model:
#
#
# def erdosrenyify(graph, p=0.5):
#     """Create a ErdosRenyi graph from networkx graph.
#
#     Take a a networkx.Graph with nodes and distribute the edges following the
#     erdos-renyi graph procedure.
#     """
#     assert not graph.edges(), "your graph has already edges"
#     nodes = graph.nodes()
#     for i, n1 in enumerate(nodes[:-1]):
#         for n2 in nodes[i+1:]:
#             if random.random() < p:
#                 graph.add_edge(n1, n2)
#
#
# # set the initial graph structure to be an erdos-renyi graph
# print("erdosrenyifying the graph ... ", end="", flush=True)
# start = time()
# erdosrenyify(culture.acquaintance_network, p=expected_degree / (nf + nt))
# print("done ({})".format(dt.timedelta(seconds=(time() - start))))

start = time()
# Calculate societies variables before run:
print('calculating society attributes before run:')
for soc in M.Society.instances:
    soc.calc_population(0)
    soc.calculate_mean_income_or_farmsize(0)
    soc.calculate_average_liquidity(0)
# Calculate other stuff:
for ind in M.Individual.instances:
    ind.calc_farm_size()
    ind.calc_gross_income()
    ind.calculate_harvest(0)
    ind.calculate_utility(0)
for soc in M.Society.instances:
    soc.calculate_average_utility(0)
    soc.calculate_gini(0)
# Run market clearing once:
metabolism.do_market_clearing(0)
# In case of a erdos renyi network:
# culture.calculate_modularity(0)
# culture.calculate_transitivity(0)
print("done ({})".format(dt.timedelta(seconds=(time() - start))))

termination_conditions = [[M.Culture.check_for_split, culture],
                          [M.Metabolism.check_for_market_equilibrium, metabolism]]

print('\n runner starting')
# Runner is instantiated
r = Runner(model=model  # , termination_calls=termination_conditions
           )

start = time()
# run the Runner and saving the return dict in traj
traj = r.run(t_1=timeinterval, dt=timestep, max_resolution=True)
runtime = dt.timedelta(seconds=(time() - start))
print('runtime: {runtime}'.format(**locals()))


# Saving:
print('saving:')
traj.save(filename='data')
print('...is done')

# Plotting:
t = np.array(traj['t'])
# for key, val in traj.items():
#     print('key', key,)
plot(t, traj[M.World.water_price][world], "b", lw=3)
plot(t, traj[M.World.total_gross_income][world], "m:", lw=3)
plot(t, traj[M.World.total_harvest][world], "m--", lw=3)
# plot(t, traj[M.Culture.network_clustering][culture], "r--", lw=3)
# plot(t, traj[M.Culture.modularity][culture], "r:", lw=3)

for soc in municipalities:
    plot(t, traj[M.Society.population][soc], "r", lw=3)
    plot(t, traj[M.Society.average_utility][soc], "r:", lw=3)
    plot(t, traj[M.Society.gini_coefficient][soc], "r--", lw=3)
for soc in counties:
    plot(t, traj[M.Society.population][soc], "k", lw=3)
    plot(t, traj[M.Society.average_utility][soc], "k:", lw=3)
    plot(t, traj[M.Society.gini_coefficient][soc], "k--", lw=3)
#for ind in M.Individual.instances:
#    plot(t, traj[M.Individual.utility][ind], "y", lw=0.5)
gca().set_yscale('symlog')

# savefig('20_ag_4_soc.png', dpi=150)
show()

# network_data = traj[M.Culture.acquaintance_network][culture]
# G = network_data[-1]

# Make list to have colors according to profession:
# professions = {}
# for ind in M.Individual.instances:
#     if ind.profession == 'farmer':
#         professions[ind] = 'yellow'
#     else:
#         professions[ind] = 'red'
# colors = [professions.get(node) for node in G.nodes()]
# # Make second list to have labels according to society:
# societies = {}
# for ind in M.Individual.instances:
#     societies[ind] = str(ind.society._uid)
# nx.draw(G, node_color=colors,
#         labels=societies,
#         pos=nx.spring_layout(G))
# show()
