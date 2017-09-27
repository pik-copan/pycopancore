"""
A descriptive test is missing here.
"""

from __future__ import print_function
import pickle
import getpass
import itertools as it
import numpy as np
import sys
import pandas as pd
import random
from scipy import stats

from pymofa.experiment_handling import experiment_handling as eh
import pycopancore.models.exodus as M
from pycopancore.runners.runner import Runner

# Save path
SAVE_PATH = "p/tmp/koster/exodus_data"

def run_function(timeinterval=100,
                 timestep=.1,
                 number_of_municipalities=5,
                 number_of_counties=5,
                 number_of_farmers=100,
                 number_of_townsmen=100,
                 market_frequency=1,
                 start_water_price=1,
                 base_mean_income=1000,
                 average_precipitation=0.75,
                 outspokensess=1,
                 network_degree=5,
                 filename='./'):
    """
    Set up the Model for different Parameters and determine
    which parts of the output are saved where.
    Output is saved in pickled dictionaries including the
    initial values and Parameters, as well as the time
    development of aggregated variables for each run.

    Parameters:
    -----------
    filename: string
        path to save the results to.
    """

    # Abbreviations:
    total_pop = number_of_farmers + number_of_townsmen

    model = M.Model()

    # instantiate process taxa culture:
    # In this certain case we need 'M.Culture()' for the acquaintance network.
    culture = M.Culture()
    metabolism = M.Metabolism(market_frequency=1)

    # instantiate world:
    world = M.World(culture=culture, metabolism=metabolism,
                    water_price=1, max_utility=1)
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
                                     land_area=0.01 * (nf + nt),
                                     # in square kilometers
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
                                     outspokensess=1,
                                     liquidity=liq,
                                     nutrition=100))

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
            for n2 in nodes[i + 1:]:
                if random.random() < p:
                    graph.add_edge(n1, n2)

    # set the initial graph structure to be an erdos-renyi graph
    print("erdosrenyifying the graph ... ", end="", flush=True)
    erdosrenyify(culture.acquaintance_network, p=expected_degree / (total_pop))

    # Before running the model, calculate necessary start stuff:
    # Calculate societies variables before run:
    for soc in M.Society.instances:
        soc.calculate_mean_income_or_farmsize(0)
        soc.calc_population(0)
        soc.calculate_average_liquidity(0)
    # Calculate other stuff:
    for ind in M.Individual.instances:
        ind.calculate_harvest(0)
        ind.calculate_utility(0)
    # Run market clearing once:
    metabolism.do_market_clearing(0)
    culture.calculate_modularity(0)

    termination_conditions = [[M.Culture.check_for_split, culture]]

    # run Model
    print('\n runner starting')
    # Runner is instantiated
    r = Runner(model=model, termination_calls=termination_conditions)
    # run the Runner and saving the return dict in traj
    traj = r.run(t_1=timeinterval, dt=timestep)
    print('runner is done')

    # Retrieve results.
    # and save them to the path indicated by 'filename'
    traj.save(filename=filename)

# Parameter Combinations:

number_of_municipalities = list(range(1, 5, 1))
number_of_counties = list(range(1, 5, 1))
number_of_farmers = [100, 500, 1000]
number_of_townsmen = [100, 500, 1000]
network_degree = list(range(3, 9, 2))


# Order of the parameters in the resulting tuples have to match the one indicated in the
# index dictionary.
param_combs = list(it.product(number_of_municipalities,
                              number_of_counties,
                              number_of_farmers,
                              number_of_townsmen,
                              network_degree))
print('computing results for {} parameter combinations'.format(len(param_combs)))

sample_size = 1

handle = eh(sample_size=sample_size,
            parameter_combinations=param_combs,
            use_kwargs=True,
            path_res=SAVE_PATH)

handle.compute(run_func=run_function)
