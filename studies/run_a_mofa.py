"""Test Study for the maxploit model.

A study to test the runner with the maxploit model.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

import numpy as np
from time import time
import datetime as dt
import pandas as pd
import json
import pickle
from pymofa.experiment_handling import experiment_handling as eh
import itertools as it
import os

# TODO: import your model here
import pycopancore.models.PLACEHOLDER as M
from pycopancore.runners.runner import Runner

# to keep track of runtimes
start = time()

# how your experiment will be named
experiment_name = "test"

# local paths
"""I chose to create a new folder each time, so that I will get an error if a folder 
already exists. Like this I wont overwrite any data."""
SAVE_FOLDER = f"..\\{experiment_name}"
os.mkdir(SAVE_FOLDER)
print(f"Directory created @ {SAVE_FOLDER}")
SAVE_PATH_RAW = SAVE_FOLDER + "\\" + "raw"
os.mkdir(SAVE_PATH_RAW)
SAVE_PATH_RES = SAVE_FOLDER + "\\" + "res"
os.mkdir(SAVE_PATH_RES)

# how many times you want to run your model with the SAME parameter set
SAMPLE_SIZE = 10

########################################################################################################################
# MODEL CONFIGURATION
"""Note: for pymofa to work your parameters must be lists. For ones you do not want to alternate
throughout an experiment you just give it a list of length 1. For others you give all the parameters
you want to sweep through."""


# ---configuration---
# runner
timeinterval = [10]
timestep = [0.1]

# culture
parameter1 = [1, 2, 3]  # the first parameter we will sweep
parameter2 = [1, 2, 3]  # second parameter sweep

# individuals
nindividuals = [100]

# cells:
nc = nindividuals

# ---write into dic---
# this configuration dictionary will be saved one level, so you remember what you did
configuration = {
    "parameter1": parameter1,
    "parameter2": parameter2,
    "nindividuals": nindividuals,
    "nc": nc,
}

# saving config
# ---save json file---
print("Saving config.json")
f = open(SAVE_FOLDER + "\\" + "config.json", "w+")
json.dump(configuration, f, indent=4)
print("Done saving config.json.")

# text file
print("Saving readme.txt.")
with open(SAVE_FOLDER + "\\" + 'readme.txt', 'w') as f:
    f.write('Something particular about this experiment you want to remember.')
print("Done saving readme.txt.")

########################################################################################################################


# Defining an experiment execution function according pymofa
def RUN_FUNC(timeinterval, timestep, parameter1, parameter2, nindividuals, nc, filename):
    # filename must be last kwarg
    # instantiate model
    model = M.Model()

    # instantiate process taxa culture:
    culture = M.Culture(parameter1=parameter1,
                        parameter2=parameter2)
    print(f"Culture process taxon created: {culture}")

    # generate entities:
    world = M.World(culture=culture)
    social_system = M.SocialSystem(world=world)
    cells = [M.Cell(social_system=social_system)
             for c in range(nc)]
    inds = [M.Individual() for i in range(nindividuals)]

    for (i, c) in enumerate(cells):
        c.individual = inds[i]

    # Runner
    r = Runner(model=model)
    traj = r.run(t_1=timeinterval, dt=timestep)

    # we will also save the traj, disable this to save data
    tosave = {
              v.owning_class.__name__ + "."
              + v.codename: {str(e): traj[v][e]
                             for e in traj[v].keys()
                             }
              for v in traj.keys() if v is not "t"
              }

    del tosave["Culture.group_membership_network"]
    del tosave["Culture.acquaintance_network"]
    tosave["t"] = traj["t"]
    t = np.array(traj["t"]).flatten()
    TRAJ_PATH = filename.replace(".pkl", "_traj.pkl")
    with open(TRAJ_PATH, "wb") as f:
        pickle.dump(tosave, f)

    # prepare data from copan core output to be further analysed with pymofa
    # pymofa needs pandas data objects
    # for that sum up all data over the entities that own them, so it can be put into a pd.series
    # i.e. all single individual behaviours will be given as total individuals with behaviour something

    prep = {}
    for v in traj.keys():
        if traj[v] and v is not "t":  # this will only save the variables that actually change during a run
            placeholder_list = []
            for e in traj[v].keys():
                placeholder_list.append([traj[v][e]])
            prep[v.owning_class.__name__ + "." + v.codename] = np.sum(placeholder_list, axis=0).flatten()

    del prep["World.terrestrial_carbon"]
    del prep["World.fossil_carbon"]

    # correct the timelines
    """Do this only if you have random events. We have to do this, since each run will have different
    timestamps otherwise (due to stochasticity). Be careful: how you choose t_grid defines the resolution
    of your data but also runtime, so you have to think about tradeoffs well."""
    t_grid = np.arange(0, timeinterval, timestep)
    for key in prep.keys():
        correcting_list = prep[key]
        new_list = []
        list_index = 0
        for index, t_index in enumerate(t_grid[1:]):
            for count, k in enumerate(t):
                if k >= t_grid[index - 1] and k < t_grid[index]:
                    list_index = count
            new_list.append(correcting_list[list_index])
        new_list.append(correcting_list[len(correcting_list) - 1])
        prep[key] = new_list

    res = pd.DataFrame(prep, index=t_grid)
    res.to_pickle(filename)

    # save networks
    # network_list = [culture.acquaintance_network, culture.group_membership_network, inter_group_network]
    # network_names = ["culture.acquaintance_network", "culture.group_membership_network", "inter_group_network"]
    # for counter, n in enumerate(network_list):
    #     f = open(filename, "wb")
    #     save_nx = nx.relabel_nodes(n, lambda x: str(x))
    #     pickle.dump(save_nx, f)
    # print("Done saving networks.")

    # delete old taxa to avoid instantiation errors
    # this is very important!
    world.delete()
    culture.delete()
    social_system.delete()
    for c in cells:
        c.delete()
    for i in inds:
        i.delete()
    # for g in groups:
    #     g.delete()

    # to check if everything went well
    exit_status = 1

    return exit_status


# -----PYMOFA-----
parameter_list = [timeinterval, timestep, parameter1, parameter2, nindividuals, nc]
parameter_name_list = ["timeinterval", "timestep", "parameter1", "parameter2", "nindividuals", "nc"]

INDEX = {i: parameter_name_list[i] for i in range(len(parameter_name_list))}
# it.product creates a list of all combinations of params
PARAM_COMBS = list(it.product(timeinterval, timestep, parameter1, parameter2, nindividuals, nc))
# create experiment handle
handle = eh(sample_size=SAMPLE_SIZE, parameter_combinations=PARAM_COMBS, index=INDEX,
            path_raw=SAVE_PATH_RAW, path_res=SAVE_PATH_RES)
# actually run the whole thing
handle.compute(RUN_FUNC)

# ----- POSTPROCESSING -----

# how to call these results
filename = "stateval_results.pkl"


def sem(fnames):
    """calculate the standard error of the mean for the data in the files
    that are in the list of fnames

    Parameter:
    ----------
    fnames: string
        list of strings of filenames containing simulation results
    Returns:
    sem: float
        Standard error of the mean of the data in the files specified
        by the list of fnames
    """
    import numpy as np
    import pandas as pd

    return pd.concat([np.load(f, allow_pickle=True) for f in fnames if "traj" not in f]).groupby(level=0).sem()


# this will calculate all means and std. errors of your data
EVA = {
    "mean": lambda fnames: pd.concat([np.load(f, allow_pickle=True)
                                      for f in fnames if "traj" not in f]).groupby(level=0).mean(),
    "sem": lambda fnames: pd.concat([np.load(f, allow_pickle=True)
                                     for f in fnames if "traj" not in f]).groupby(level=0).sem()
}


# this actually does the magic
handle.resave(EVA, filename)

# how long did this take?
runtime = dt.timedelta(seconds=(time() - start))
print('runtime: {runtime}'.format(**locals()))
