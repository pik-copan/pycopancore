import pandas as pd
import json
import itertools as it
import numpy as np
import matplotlib.pyplot as plt
# from plot_maxploit_functions import correct_timeline
from studies.plotting_tools.plot_maxploit_functions import phase_transition

parameter_name_list = ["ind_initialisation", "group_initialisation", "fix_group_attitude", "timeinterval", "timestep",
                       "k_value", "majority_threshold", "weight_descriptive", "weight_injunctive", "ni_sust",
                       "ni_nonsust", "nindividuals", "average_waiting_time", "update_probability", "nc", "ng_total",
                       "ng_sust", "ng_nonsust", "group_meeting_interval", "p"]
# parameter_name_list = ["k_value", "majority_threshold", "weight_descriptive", "weight_injunctive",
#                        "average_waiting_time", "update_probability", "ng_total", "group_meeting_interval"]
INDEX = {i: parameter_name_list[i] for i in range(len(parameter_name_list))}

# path to data
# PATH = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\results\\maxploit\\cluster_results\\majority_threshold_descriptive_only"

# path to test data
PATH = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\results\\maxploit\\" \
       f"test"

# path to save figures
SAVE_PATH = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\plots\\maxploit\\" \
       f"test"

# load config
CONFIG_LOAD_PATH = PATH + "\\config.json"
config = json.load(open(CONFIG_LOAD_PATH))

# parameter_dict = {str(key): value for key, value in config.items() if key in parameter_name_list}
parameter_dict = config

# create parameter list
ind_initialisation = parameter_dict["ind_initialisation"]
group_initialisation = parameter_dict["group_initialisation"]
if "fix_group_attitude" in parameter_dict.keys():
    fix_group_attitude = parameter_dict["fix_group_attitude"]
else:
    fix_group_attitude = parameter_dict["fix_group_opinion"]
timeinterval = parameter_dict["timeinterval"]
timestep = parameter_dict["timestep"]
k_value = parameter_dict["k_value"]
majority_threshold = parameter_dict["majority_threshold"]
weight_descriptive = parameter_dict["weight_descriptive"]
weight_injunctive = parameter_dict["weight_injunctive"]
ni_sust = parameter_dict["ni_sust"]
ni_nonsust = parameter_dict["ni_nonsust"]
nindividuals = parameter_dict["nindividuals"]
average_waiting_time = parameter_dict["average_waiting_time"]
update_probability = parameter_dict["update_probability"]
nc = parameter_dict["nc"]
ng_total = parameter_dict["ng_total"]
ng_sust = parameter_dict["ng_sust"]
ng_nonsust = parameter_dict["ng_nonsust"]
group_meeting_interval = parameter_dict["group_meeting_interval"]
p = parameter_dict["p"]

parameter_list = [ind_initialisation, group_initialisation, fix_group_attitude, timeinterval, timestep, k_value,
                  majority_threshold, weight_descriptive, weight_injunctive, ni_sust, ni_nonsust, nindividuals,
                  average_waiting_time, update_probability, nc, ng_total, ng_sust, ng_nonsust, group_meeting_interval,
                  p]

last_timestep = timeinterval[0] - timestep[0]

PARAM_COMBS\
    = list(it.product(ind_initialisation, group_initialisation, fix_group_attitude, timeinterval, timestep, k_value,
          majority_threshold, weight_descriptive, weight_injunctive, ni_sust, ni_nonsust, nindividuals,
          average_waiting_time, update_probability, nc, ng_total, ng_sust, ng_nonsust, group_meeting_interval,
          p))

# RAW_LOAD_PATH = PATH + "\\raw\\1-1-1-10-0o1-2-0o5-1-0-400-0-400-1-0o5-400-1-0-1-1-0o05_s0.pkl"
# raw = pickle.load(open(RAW_LOAD_PATH, "rb"))

RES_LOAD_PATH = PATH + "\\res\\stateval_results.pkl"
data = pd.read_pickle(RES_LOAD_PATH)

# how to deal with keys
data.head()
# for x in PARAM_COMBS:
#     data['mean'].unstack('observables').xs(key=tuple(x), level=parameter_name_list).plot()
#     plt.show()
# data['sem'].unstack('observables').xs(key=key_dict["0"], level=parameter_name_list).plot()
# plt.show()

# how to access single data
"""
data['EVA'].unstack('observables').xs(key=key_dict["X"], level=parameter_name_list).loc[TIMESTAMP, "VARIABLE"]
EVA: the functions you used in eva, e.g. "mean" or "sem"
X: which specific parameter set you want to plot
TIMESTAMP: which index (e.g. last timestep of run)
VARIABLE: which variable of interest you want to plot
"""

# ----- phase transition plot
# figure = phase_transition(data, parameter_name_list, parameter_dict, parameter_list, "majority_threshold", last_timestep, "cells")



# create key sets for single parameter sweeps for plotting
# change the ones that were sweeped and fix the other ones

# get names of all alternating params
alternating_params = []
for key, value in config.items():
    if len(value) > 1 and isinstance(value, list):
        alternating_params.append(key)

param_locs = {}
for index, key in enumerate(parameter_name_list):
    if key in alternating_params:
        param_locs[key] = index

pairs = list(it.combinations(alternating_params, 2))

for p in pairs:
    param1 = p[0]
    param2 = p[1]
    param_loc1 = param_locs[param1]
    param_loc2 = param_locs[param2]

    A = np.zeros((len(parameter_list[param_loc1]), len(parameter_list[param_loc2])), dtype=list)

    param_list1 = parameter_list[param_loc1]
    param_list2 = parameter_list[param_loc2]

    # sort lists in case
    if param_list1.sort() is not None:
        param_list1 = parameter_list[param_loc1].sort()
    if param_list2.sort() is not None:
        param_list2 = parameter_list[param_loc2].sort()

    for c in PARAM_COMBS:
        value = list(c)
        for index_i, i in enumerate(param_list1):
            for index_j, j in enumerate(param_list2):
                new_key = []
                for index, x in enumerate(value):
                    if index == param_loc1:
                        new_key.append(i)
                    elif index == param_loc2:
                        new_key.append(j)
                    else:
                        new_key.append(x)
                A[index_i][index_j] = new_key

    # create a data matrix
    cells_matrix = np.zeros((len(parameter_list[param_loc1]), len(parameter_list[param_loc2])), dtype=float)
    inds_matrix = np.zeros((len(parameter_list[param_loc1]), len(parameter_list[param_loc2])), dtype=float)
    sem_cells_matrix = np.zeros((len(parameter_list[param_loc1]), len(parameter_list[param_loc2])), dtype=float)
    sem_inds_matrix = np.zeros((len(parameter_list[param_loc1]), len(parameter_list[param_loc2])), dtype=float)
    for i in range(np.shape(cells_matrix)[0]):
        for j in range(np.shape(cells_matrix)[1]):
            cells_matrix[i][j] = float(data['mean'].unstack('observables').xs(key=tuple(A[i][j]),
                                                                             level=parameter_name_list).loc[
                                          last_timestep, "Cell.stock"])
            sem_cells_matrix[i][j] = float(data['sem'].unstack('observables').xs(key=tuple(A[i][j]),
                                                                             level=parameter_name_list).loc[
                                          last_timestep, "Cell.stock"])
            inds_matrix[i][j] = float(data['mean'].unstack('observables').xs(key=tuple(A[i][j]),
                                                                             level=parameter_name_list).loc[
                                          last_timestep, "Individual.behaviour"])
            sem_inds_matrix[i][j] = float(data['sem'].unstack('observables').xs(key=tuple(A[i][j]),
                                                                             level=parameter_name_list).loc[
                                          last_timestep, "Individual.behaviour"])
    matrices = [cells_matrix, sem_cells_matrix, inds_matrix, sem_inds_matrix]
    m_names = ["Cells", "Sem_Cells", "Inds", "Sem_Inds"]
    # ----- PIXEL PLOT -----
    # create a 2d data set

    for index, m in enumerate(matrices):
        pixel_plot = plt.figure()
        plt.suptitle(param1 + " vs. " + param2)
        plt.title(f"{m_names[index]}")
        plt.imshow(m, origin="lower")
        plt.colorbar()
        plt.xlabel(param1)
        plt.ylabel(param2)
        # save a plot
        plt.savefig(SAVE_PATH + "\\" + param1 + "_" + param2 + f"_{m_names[index]}" + ".png")
        # show plot
        #plt.show()
        # clear axes
        plt.close()

# ----- PLOT PHASE TRANSITION -----