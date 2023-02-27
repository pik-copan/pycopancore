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
import pymofa.experiment_handling
from numpy import random
import json
import networkx as nx
import pickle
from pymofa.experiment_handling import experiment_handling as eh
import itertools as it
import importlib
import os
import pycopancore.models.maxploit as M
from pycopancore.runners.runner import Runner

start = time()

experiment_name = "plot_chessboard_test"

#local
SAVE_FOLDER = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\results\\maxploit\\{experiment_name}"
os.mkdir(SAVE_FOLDER)
print(f"Directory created @ {SAVE_FOLDER}")
SAVE_PATH_RAW = SAVE_FOLDER + "\\" + "raw"
os.mkdir(SAVE_PATH_RAW)
SAVE_PATH_RES = SAVE_FOLDER + "\\" + "res"
os.mkdir(SAVE_PATH_RES)

#cluster
# SAVE_FOLDER = f"/p/projects/copan/users/maxbecht/results/maxploit/{experiment_name}"
# os.mkdir(SAVE_FOLDER)
# print(f"Directory created @ {SAVE_FOLDER}")
# SAVE_PATH_RAW = SAVE_FOLDER + "\\" + "raw"
# os.mkdir(SAVE_PATH_RAW)
# SAVE_PATH_RES = SAVE_FOLDER + "\\" + "res"
# os.mkdir(SAVE_PATH_RES)

SAMPLE_SIZE = 1

########################################################################################################################
# MODEL CONFIGURATION

# ---configuration---

# facts - just for memory
which_norm = "Descriptive" # "Both", "Descriptive", "Injunctive"
group_meeting_type = "Step"  # "Step" or "Event"
"""Step means a regular meeting interval. 
Event means a similar way to the individuals way of drawing a next agent. 
Note that this variable is meant only for documentation purposes, the code needs to be changed by hand."""
group_attitude_formation = "Majority"  # "Majority" or "Random" or "Leader"
"""Majority means that the group attitude is calculated from the mean.
Random means that the group attitude is picked from one of the member individuals attitudes.
Leader means that the group attitude follows the lead of a leader (somehow to be implemented).
Note that this variable is meant only for documentation purposes, the code needs to be changed by hand."""
descriptive_norm_formation = "Majority"  # "Majority" or "Random"
"""Majority means that the descriptive norm is calculated from the mean of acquaintances.
Random means that the descriptive norm is calculated from one random one of the acquaintances attitudes.
Note that this variable is meant only for documentation purposes, the code needs to be changed by hand."""
adaptivity = "No"  # "Yes" or "No"
"""If adaptive or not, selfexplainatory. Is not a Toggle."""
switching_back = "No"  # can individuals switch even if norm does not say so?
acquaintance_network_type = "Erdos-Renyi"
group_membership_network_type = "1-random-Edge"

###### actual parameters

# toggles
ind_initialisation = [1]  # 0 or 1
"""1 means that inds are initialised randomly.
0 means that a certain percentage of individuals starts a way.
Note that this variable is a toggle."""
group_initialisation = [1]  # 0 or 1
"""1 means that groups are initialised randomly.
0 means that a certain percentage of groups starts a way.
Note that this variable is a toggle."""
fix_group_attitude = [1]  # into boolean, i.e. 1 = True
"""Does not allow the initial group attitude to change,
i.e. group becomes a norm entitiy."""

# seed
# seed = 1

# runner
timeinterval = [10]
timestep = [0.1]

# culture
majority_threshold = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
weight_descriptive = [1]
weight_injunctive = [0]

# logit
# k_value = 2.94445 #produces probabilities of roughly 0.05, 0.5, 0.95
k_value = [2]  # reproduces probs of exploit for gamma = 1

# updating
average_waiting_time = [1]
update_probability = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

# groups:
group_meeting_interval = [1]
ng_total = [1]  # number of total groups
ng_sust_frac = 0.5
ng_sust = []
for x in ng_total:
    ng_sust.append(int(x * ng_sust_frac))  # number of sustainable groups
ng_nonsust = []
for i in range(len(ng_sust)):
    ng_nonsust.append(ng_total[i] - ng_sust[i])

# networks
p = [0.05] # link density for random networks; wiedermann: 0.05



### parameters that usually will not be changed ###
# individuals
nindividuals = [400] # this does not change
ni_sust_frac = 1
ni_sust = []
for x in nindividuals:
    ni_sust.append(int(x * ni_sust_frac))  # number of agents with sustainable behaviour 1
ni_nonsust = []
for i in range(len(ni_sust)):
    ni_nonsust.append(nindividuals[i] - ni_sust[i])  # number of agents with unsustainable behaviour 0
# cells:
cell_stock = [1] # does not change
cell_capacity = [1] # does not change
cell_growth_rate = [1] # does not change
nc = nindividuals  # number of cells



# ---write into dic---
configuration = {
    "which_norm": which_norm,
    "group_meeting_type": group_meeting_type,
    "group_attitude_formation": group_attitude_formation,
    "descriptive_norm_formation": descriptive_norm_formation,
    "adaptivity": adaptivity,
    "switching_back": switching_back,
    "ind_initialisation": ind_initialisation,
    "group_initialisation": group_initialisation,
    "fix_group_attitude": fix_group_attitude,
    "timeinterval": timeinterval,
    "timestep": timestep,
    "k_value": k_value,
    "majority_threshold": majority_threshold,
    "weight_descriptive": weight_descriptive,
    "weight_injunctive": weight_injunctive,
    "ni_sust": ni_sust,
    "ni_nonsust": ni_nonsust,
    "nindividuals": nindividuals,
    "average_waiting_time": average_waiting_time,
    "update_probability": update_probability,
    "cell_stock": cell_stock,
    "cell_capacity": cell_capacity,
    "cell_growth_rate": cell_growth_rate,
    "nc": nc,
    "ng_total": ng_total,
    "ng_sust": ng_sust,
    "ng_nonsust": ng_nonsust,
    "group_meeting_interval": group_meeting_interval,
    "acquaintance_network_type": acquaintance_network_type,
    "group_membership_network_type": group_membership_network_type,
    "p": p
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
    f.write('Groups do not change their attitude')
print("Done saving readme.txt.")

########################################################################################################################


# Defining an experiment execution function according pymofa
def RUN_FUNC(ind_initialisation, group_initialisation, fix_group_attitude, timeinterval, timestep, k_value,
             majority_threshold, weight_descriptive, weight_injunctive, ni_sust, ni_nonsust, nindividuals,
             average_waiting_time, update_probability, nc, ng_total, ng_sust, ng_nonsust, group_meeting_interval,
             p, filename):

    # instantiate model
    model = M.Model()

    # instantiate process taxa culture:
    culture = M.Culture(majority_threshold=majority_threshold,
                        weight_descriptive=weight_descriptive,
                        weight_injunctive=weight_injunctive,
                        fix_group_attitude=fix_group_attitude,
                        k_value=k_value)
    print(f"Culture process taxon created: {culture}")

    # generate entitites:
    world = M.World(culture=culture)
    social_system = M.SocialSystem(world=world)
    cells = [M.Cell(stock=1, capacity=1, growth_rate=1, social_system=social_system)
             for c in range(nc)]

    # random initialisation or not?
    if ind_initialisation:
        behaviour = [0, 1]
        attitude = [0, 1]
        individuals = [M.Individual(average_waiting_time=average_waiting_time,
                                    update_probability=update_probability,
                                    behaviour=np.random.choice(behaviour),
                                    cell=cells[i]) for i in range(nindividuals)]
    else:
        individuals = [M.Individual(behaviour=0, attitude=0,
                                    cell=cells[i]) for i in range(ni_nonsust)] \
                      + [M.Individual(behaviour=1, attitude=1,
                                      cell=cells[i + ni_nonsust])
                         for i in range(ni_sust)]

        # instantiate groups
    if group_initialisation:
        group_attitude = [0, 1]
        groups = [M.Group(culture=culture, world=world, group_attitude=np.random.choice(group_attitude),
                          group_meeting_interval=group_meeting_interval) for i in range(ng_total)]
    else:
        groups = [M.Group(culture=culture, world=world, group_attitude=1,
                          group_meeting_interval=group_meeting_interval) for i in range(ng_sust)] + \
                 [M.Group(culture=culture, world=world, group_attitude=0,
                          group_meeting_interval=group_meeting_interval) for i in range(ng_nonsust)]

    for (i, c) in enumerate(cells):
        c.individual = individuals[i]

    def erdosrenyify(graph, p=0.5):
        """Create a ErdosRenzi graph from networkx graph.

        Take a a networkx.Graph with nodes and distribute the edges following the
        erdos-renyi graph procedure.
        """
        assert not graph.edges(), "your graph has already edges"
        nodes = list(graph.nodes())
        for i, n1 in enumerate(nodes[:-1]):
            for n2 in nodes[i + 1:]:
                if random.random() < p:
                    graph.add_edge(n1, n2)

    # set the initial graph structure to be an erdos-renyi graph
    print("erdosrenyifying the graph ... ", end="", flush=True)
    start = time()
    erdosrenyify(culture.acquaintance_network, p=p)

    # assert that each ind has at least one edge
    # for i in individuals:
    #     if not list(i.acquaintances):
    #         culture.acquaintance_network.add_edge(i, np.random.choice(individuals))

    GM = culture.group_membership_network
    # group_membership network with only one group membership for now
    for i in individuals:
        GM.add_edge(i, np.random.choice(groups))

    # get a preliminary intergroup network for plotting multilayer
    inter_group_network = nx.Graph()
    for g in groups:
        inter_group_network.add_node(g)  # groups have no interaction so far


    # Runner
    # print("done ({})".format(dt.timedelta(seconds=(time() - start))))
    # print('\n runner starting')
    r = Runner(model=model)
    start = time()
    traj = r.run(t_1=timeinterval, dt=timestep)
    # runtime = dt.timedelta(seconds=(time() - start))
    # print('runtime: {runtime}'.format(**locals()))

    # saving trajs in another folder
    # create a binary pickle file



    #SAVE_PATH_TRAJ = SAVE_PATH_RAW.replace("raw", "traj")
    #os.mkdir(SAVE_PATH_TRAJ)

    #f = open(SAVE_PATH_TRAJ + filename, "wb")

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

    ### SAVE AS PANDAS
    # # optionally the whole traj can be safed in a pd frame
    # # preparing the data
    # save_traj = pd.DataFrame({
    #     v.owning_class.__name__ + "."
    #     + v.codename: {str(e): traj[v][e]
    #                    for e in traj[v].keys()
    #                    }
    #     for v in traj.keys() if v is not "t"
    # })
    # ts = {}
    # for v in traj.keys():
    #     if v is not "t":
    #         for e in traj[v].keys():
    #             ts[str(e)] = t
    # save_traj["t"] = ts
    # save_traj.to_pickle(TRAJ_PATH) #save the full traj


    # prepare data from copan core output to be further analysed with pymofa
    # for that sum up all data over the entities that own them so it can be put into a pd.series
    # i.e. all single individual behaviours will be given as total individuals with behaviour something

    prep = {}
    for v in traj.keys():
        if traj[v] and v is not "t":
            placeholder_list = []
            for e in traj[v].keys():
                placeholder_list.append([traj[v][e]])
            prep[v.owning_class.__name__ + "." + v.codename] = np.sum(placeholder_list, axis=0).flatten()

    del prep["World.terrestrial_carbon"]
    del prep["World.fossil_carbon"]
    # res = pd.DataFrame(prep)

    # correct the timelines
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
    # need to drop timestamps
    # res.reset_index(drop=True)
    res.to_pickle(filename)

    # save networks
    # network_list = [culture.acquaintance_network, culture.group_membership_network, inter_group_network]
    # network_names = ["culture.acquaintance_network", "culture.group_membership_network", "inter_group_network"]
    # for counter, n in enumerate(network_list):
    #     f = open(filename, "wb")
    #     save_nx = nx.relabel_nodes(n, lambda x: str(x))
    #     pickle.dump(save_nx, f)
    # print("Done saving networks.")

    # with open(filename, 'w') as f:
    #     f.write('Groups do not change their attitude')

    # delete old taxa to avoid instantiation errors
    world.delete()
    culture.delete()
    social_system.delete()
    for c in cells:
        c.delete()
    for i in individuals:
        i.delete()
    for g in groups:
        g.delete()

    exit_status = 1

    return exit_status

parameter_list = [ind_initialisation, group_initialisation, fix_group_attitude, timeinterval, timestep, k_value,
                  majority_threshold, weight_descriptive, weight_injunctive, ni_sust, ni_nonsust, nindividuals,
                  average_waiting_time, update_probability, nc, ng_total, ng_sust, ng_nonsust, group_meeting_interval,
                  p]
parameter_name_list = ["ind_initialisation", "group_initialisation", "fix_group_attitude", "timeinterval", "timestep",
                       "k_value", "majority_threshold", "weight_descriptive", "weight_injunctive", "ni_sust",
                       "ni_nonsust", "nindividuals", "average_waiting_time", "update_probability", "nc", "ng_total",
                       "ng_sust", "ng_nonsust", "group_meeting_interval", "p"]
# parameter_list = [k_value, majority_threshold, weight_descriptive, weight_injunctive, average_waiting_time,
#                   update_probability, ng_total,group_meeting_interval]
# parameter_name_list = ["k_value", "majority_threshold", "weight_descriptive", "weight_injunctive",
#                        "average_waiting_time", "update_probability", "ng_total", "group_meeting_interval"]
INDEX = {i: parameter_name_list[i] for i in range(len(parameter_name_list))}
PARAM_COMBS = list(it.product(ind_initialisation, group_initialisation, fix_group_attitude, timeinterval, timestep, k_value,
                  majority_threshold, weight_descriptive, weight_injunctive, ni_sust, ni_nonsust, nindividuals,
                  average_waiting_time, update_probability, nc, ng_total, ng_sust, ng_nonsust, group_meeting_interval,
                  p))
handle = eh(sample_size=SAMPLE_SIZE, parameter_combinations=PARAM_COMBS, index=INDEX, path_raw=SAVE_PATH_RAW, path_res=SAVE_PATH_RES)
handle.compute(RUN_FUNC)

##### POSTPROCESSING #####

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
    import scipy.stats as st
    import numpy as np
    import pandas as pd

    return pd.concat([np.load(f, allow_pickle=True) for f in fnames if "traj" not in f]).groupby(level=0).mean()

EVA = {
    "mean": lambda fnames: pd.concat([np.load(f, allow_pickle=True)
                                      for f in fnames if "traj" not in f]).groupby(level=0).mean(),
    "std": lambda fnames: pd.concat([np.load(f, allow_pickle=True)
                                     for f in fnames if "traj" not in f]).groupby(level=0).std()
}

handle.resave(EVA, filename)

runtime = dt.timedelta(seconds=(time() - start))
print('runtime: {runtime}'.format(**locals()))