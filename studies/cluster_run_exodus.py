"""
Experiment to test the influence of drought events.
Drought events start once the civilisation has reached
a 'complex society' state (after 200 years) and vary
in length and severity from 0 to 100 years and 0 to 100%
less precipitation.

Therefore, starting point is at t = 200 where the model has
reached a complex society state in all previous studies.
We also use parameters for income from trade, agriculture and
ecosystem services, that have previously proven to lead to
some influence of precipitation variability on the state of the
system.

Also, we vary the parameter for income from trade so see, if
there is a certain parameter value, that results in
stable complex society for some drought events and collapse for others.
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

from mayasim.model.ModelCore import ModelCore as Model
from mayasim.model.ModelParameters import ModelParameters as Parameters

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

    # initialize the Model
    model = M.Model()

    # instantiate taxa:
    culture = M.Culture()
    metabolism = M.Metabolism(market_frequency=market_frequency)

    # instantiate world:
    world = M.World(culture=culture, metabolism=metabolism,
                    water_price=start_water_price)
    # Instantiate Societies:
    municipalities = [M.Society(world=world,
                                municipality_like=True,
                                base_mean_income=base_mean_income)
                      for m in range(number_of_municipalities)
                      ]
    counties = [M.Society(world=world,
                          municipality_like=False)
                for c in range(number_of_counties)
                ]
    # Instantiate farmland cells:
    farmland_cells = []
    county_allocation = list(counties)
    for fc in range(number_of_counties):
        # chose county:
        county = random.choice(county_allocation)
        county_allocation.remove(county)
        farmland_cells.append(M.Cell(world=world,
                                     society=county,
                                     characteristic='farmland',
                                     land_area=0.01 * (total_pop),
                                     # in square kilometers
                                     average_precipitation=average_precipitation))
    # Instantiate city cells:
    city_cells = []
    municipality_allocation = list(municipalities)
    for cc in range(number_of_municipalities):
        # chose county:
        municipality = random.choice(municipality_allocation)
        municipality_allocation.remove(municipality)
        city_cells.append(M.Cell(world=world,
                                 society=municipality,
                                 characteristic='city',
                                 average_precipitation=0))

    # Instantiate farmers:
    farmers = []
    for f in range(number_of_farmers):
        # Chose cell
        farmland = random.choice(farmland_cells)
        # determine liquidity before first market:
        liq = stats.lognorm.rvs(scale=300, s=0.34, loc=0)
        farmers.append(M.Individual(cell=farmland,
                                    profession='farmer',
                                    outspokensess=outspokensess,
                                    liquidity=liq,
                                    nutrition=1000))
    # Instantiate townsmen:
    townsmen = []
    for t in range(number_of_townsmen):
        # Chose cell
        city = random.choice(city_cells)
        # determine liquidity before first market:
        liq = stats.lognorm.rvs(scale=700, s=0.34, loc=0)
        townsmen.append(M.Individual(cell=city,
                                     profession='townsman',
                                     outspokensess=outspokensess,
                                     liquidity=liq,
                                     nutrition=100))

    # Create Network
    expected_degree = network_degree

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

    # run Model
    print('\n runner starting')
    # Runner is instantiated
    r = Runner(model=model)
    # run the Runner and saving the return dict in traj
    traj = r.run(t_1=timeinterval, dt=timestep)
    print('runner is done')

    # Retrieve results.
    # and save them to the path indicated by 'filename'
    try:
        with open(filename, 'wb') as dumpfile:
            pickle.dump(traj, dumpfile, pickle.HIGHEST_PROTOCOL)
            return 1
    except IOError:
        return -1


def run_experiment(argv):
    """
    Take arv input variables and run sub_experiment accordingly.
    This happens in five steps:
    1)  parse input arguments to set switches
        for [test],
    2)  set output folders according to switches,
    3)  generate parameter combinations,
    4)  define names and dictionaries of callables to apply to sub_experiment
        data for post processing,
    5)  run computation and/or post processing and/or plotting
        depending on execution on cluster or locally or depending on
        experimentation mode.

    Parameters
    ----------
    argv: list[N]
        List of parameters from terminal input

    Returns
    -------
    rt: int
        some return value to show whether sub_experiment succeeded
        return 1 if sucessfull.
    """
    # Generate paths according to switches and user name

    raw = 'raw_data/'
    res = 'results/'

    save_path_res = './{}'.format(res)
    save_path_raw = './{}'.format(raw)

    # Generate parameter combinations and set up 'index' dictionary,
    # indicating their possition in the Index of the postprocessed results.

    index = {0: "d_length", 1: "d_severity", 2: "r_trade"}

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

    # In this experiment, I use the job_id variable from an array job to split the
    # parameter combinations into equally sized junks.
    # This makes it easier for the queing algorithm to allocate its resources (which means,
    # it will give you more of it ;)
    # this also means, that the total number of jobs you run, must be a divider of the
    # number of parameter combinations that you run.
    if len(param_combs) % max_id != 0:
        print('number of jobs ({}) has to be multiple of max_id ({})!!'.format(len(param_combs), max_id))
        exit(-1)

    sample_size = 1

    # Define names and callables for post processing

    name1 = "trajectory"
    estimators1 = {"<mean_trajectories>":
                   lambda fnames:
                   pd.concat([np.load(f)["trajectory"] for f in fnames]).groupby(level=0).mean(),
                   "<sigma_trajectories>":
                   lambda fnames:
                   pd.concat([np.load(f)["trajectory"] for f in fnames]).groupby(level=0).std()
                   }
    name2 = "all_trajectories"
    estimators2 = {"trajectory_list":
                   lambda fnames: [np.load(f)["trajectory"] for f in fnames]}

    def foo(fnames, keys):
        key = keys[0]
        data = [np.load(f)[key] for f in fnames]
        df = pd.DataFrame(data=data, columns=[keys[0]])
        for key in keys[1:]:
            data = [np.load(f)[key] for f in fnames]
            df[key] = data
        return df

    name3 = "all_final_states"
    estimators3 = {"final states":
                   lambda fnames:
                   foo(fnames, ["final population",
                                "final trade links",
                                "final max cluster size"])
                   }

    # Run computation and post processing.

    # devide parameter combination into equally sized chunks.
    cl = int(len(param_combs)/max_id)
    i = (job_id-1)*cl
    j = job_id*cl

    handle = eh(sample_size=sample_size,
                parameter_combinations=param_combs[i:j],
                index=index,
                path_raw=save_path_raw,
                path_res=save_path_res,
                use_kwargs=True)
    if mode == 1:
        handle.compute(run_func=run_function)
        return 0
    elif mode == 2:
        handle.resave(eva=estimators1, name=name1)
        handle.resave(eva=estimators2, name=name2)
        handle.resave(eva=estimators3, name=name3)
        return 0

    return 1

# The definition of the run_function makes it easier to test the experiment with pytest.
if __name__ == '__main__':

    run_experiment(sys.argv)