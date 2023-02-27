import os
import pickle
import glob
import pandas as pd
import json
import itertools as it
import numpy as np
import matplotlib.pyplot as plt
# from plot_maxploit_functions import correct_timeline
from studies.plotting_tools.plot_maxploit_functions import phase_transition
import studies.plotting_tools.plot_maxploit_functions as pmf

parameter_name_list = ["attitude_on", "ind_initialisation", "group_initialisation", "fix_group_attitude", "timeinterval", "timestep",
                       "k_value", "majority_threshold", "weight_descriptive", "weight_injunctive","nindividuals",
                       "ni_sust_frac", "average_waiting_time", "update_probability", "nc", "ng_total",
                       "ng_sust_frac", "group_update_probability", "group_meeting_interval", "p"]
# parameter_name_list = ["k_value", "majority_threshold", "weight_descriptive", "weight_injunctive",
#                        "average_waiting_time", "update_probability", "ng_total", "group_meeting_interval"]
INDEX = {i: parameter_name_list[i] for i in range(len(parameter_name_list))}

experiment_name = "sustainable_state_test3"

# path to data
PATH = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\results\\maxploit\\{experiment_name}"

# path to test data
# PATH = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\results\\maxploit\\test"

# path to save figures
SAVE_PATH = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\plots\\maxploit\\{experiment_name}"
if not os.path.exists(SAVE_PATH):
    os.mkdir(SAVE_PATH)
MEAN_PATHS = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\plots\\maxploit\\{experiment_name}\\mean_sem"
if not os.path.exists(MEAN_PATHS):
    os.mkdir(MEAN_PATHS)
TRAJ_PATHS = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\plots\\maxploit\\{experiment_name}\\trajs"
if not os.path.exists(TRAJ_PATHS):
    os.mkdir(TRAJ_PATHS)

# test
# SAVE_PATH = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\plots\\maxploit\\test"

# load config
CONFIG_LOAD_PATH = PATH + "\\config.json"
config = json.load(open(CONFIG_LOAD_PATH))

# parameter_dict = {str(key): value for key, value in config.items() if key in parameter_name_list}
parameter_dict = config

# create parameter list
attitude_on = parameter_dict["attitude_on"]
ind_initialisation = parameter_dict["ind_initialisation"]
group_initialisation = parameter_dict["group_initialisation"]
fix_group_attitude = parameter_dict["fix_group_attitude"]
timeinterval = parameter_dict["timeinterval"]
timestep = parameter_dict["timestep"]
k_value = parameter_dict["k_value"]
majority_threshold = parameter_dict["majority_threshold"]
weight_descriptive = parameter_dict["weight_descriptive"]
weight_injunctive = parameter_dict["weight_injunctive"]
nindividuals = parameter_dict["nindividuals"]
ni_sust_frac = parameter_dict["ni_sust_frac"]
average_waiting_time = parameter_dict["average_waiting_time"]
update_probability = parameter_dict["update_probability"]
nc = parameter_dict["nc"]
ng_total = parameter_dict["ng_total"]
ng_sust_frac = parameter_dict["ng_sust_frac"]
group_meeting_interval = parameter_dict["group_meeting_interval"]
group_update_probability = parameter_dict["group_update_probability"]
p = parameter_dict["p"]

parameter_list = [attitude_on, ind_initialisation, group_initialisation, fix_group_attitude, timeinterval, timestep, k_value,
             majority_threshold, weight_descriptive, weight_injunctive, nindividuals, ni_sust_frac,
             average_waiting_time, update_probability, nc, ng_total, ng_sust_frac, group_update_probability, group_meeting_interval,
             p]

last_timestep = timeinterval[0] - timestep[0]
timepoints = np.arange(0, timeinterval[0], timestep[0])

PARAM_COMBS\
    = list(it.product(attitude_on, ind_initialisation, group_initialisation, fix_group_attitude, timeinterval, timestep, k_value,
             majority_threshold, weight_descriptive, weight_injunctive, nindividuals, ni_sust_frac,
             average_waiting_time, update_probability, nc, ng_total, ng_sust_frac, group_update_probability, group_meeting_interval,
             p))

RAW_PATH = PATH + "\\raw"
# raw = pickle.load(open(RAW_LOAD_PATH, "rb"))

RES_LOAD_PATH = PATH + "\\res\\stateval_results.pkl"
print("Loading data...")
data = pd.read_pickle(RES_LOAD_PATH)
print("Done loading data!")

# how to deal with keys
# data.head()
# for x in PARAM_COMBS:
#     data['mean'].unstack('observables').xs(key=tuple(x), level=parameter_name_list).plot()
#     plt.show()
# data['sem'].unstack('observables').xs(key=key_dict["0"], level=parameter_name_list).plot()
# plt.show()

# how to access single data from aggregates
"""
data['EVA'].unstack('observables').xs(key=key_dict["X"], level=parameter_name_list).loc[TIMESTAMP, "VARIABLE"]
EVA: the functions you used in eva, e.g. "mean" or "std"
X: which specific parameter set you want to plot
TIMESTAMP: which index (e.g. last timestep of run)
VARIABLE: which variable of interest you want to plot
"""

# get names of variables that were saved
variables = [name for name, values in data['mean'].unstack('observables').iteritems()]
# or set them yourself
variables = ['Cell.stock', 'Individual.behaviour', 'Group.group_attitude', 'Group.mean_group_behaviour']

# ----- plot traj trajectories
import glob
ids = pmf.get_mofa_id(PARAM_COMBS[0])
for i in ids:
    if not os.path.exists(TRAJ_PATHS + "\\" + i):
        os.mkdir(TRAJ_PATHS + "\\" + i)
fnames = np.sort(glob.glob(RAW_PATH + "\\*"))
to_plot = []
for i in ids:
    for f in fnames:
        n = 0
        if i in f:
            raw = pickle.load(open(f, "rb"))
            fig, ax = plt.subplots()
            for name in variables:
                ax.plot(timepoints, raw[name], label=name)
            ax.set_xlabel("t")
            ax.set_ylabel("Value")
            ax.set_title(i + "_" + str(n))
            n += 1
            ax.legend(loc="best")
            save_path = TRAJ_PATHS + "\\" + i
            plt.show()
            # plt.savefig(save_path + "\\" + f"_{n}" + ".png")

# little function that recreates the id's of pymofa runs

# ----- plot mean and sem trajectories -----
for c in PARAM_COMBS:
    fig, ax = plt.subplots(len(variables))
    for index, name in enumerate(variables):
        y = data['mean'].unstack('observables').xs(key=c, level=parameter_name_list)[name]
        y_e = data['sem'].unstack('observables').xs(key=c, level=parameter_name_list)[name]
        ax[index].set_title(name)
        ax[index].set_xlabel("t")
        ax[index].set_ylabel("Value")
        ax[index].plot(timepoints, y, c="blue")
        ax[index].plot(timepoints, y_e, c="red")
        ax[index].fill_between(timepoints, list(np.subtract(np.array(y), np.array(y_e))),
                         list(np.add(np.array(y), np.array(y_e))), alpha=0.2)
    plt.suptitle(str(c))
    plt.tight_layout()
    plt.show()
    # plt.savefig(MEAN_PATHS + "\\" + f"_{c}" + ".png")
    plt.close()

# ----- phase transition plot
# pmf.phase_transition(data, parameter_name_list, parameter_dict, parameter_list, "majority_threshold",
#                      last_timestep, "cells", SAVE_PATH)
# pmf.phase_transition(data, parameter_name_list, parameter_dict, parameter_list, "majority_threshold",
#                      last_timestep, "inds", SAVE_PATH)

# ----- PIXEL PLOT -----
pmf.pixel_plot(data, config, parameter_name_list, parameter_list, PARAM_COMBS, last_timestep, SAVE_PATH)