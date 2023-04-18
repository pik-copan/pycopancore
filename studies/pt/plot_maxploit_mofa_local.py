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
                       "k_value", "descriptive_majority_threshold", "injunctive_majority_threshold", "weight_descriptive", "weight_injunctive", "weight_harvest",
                       "nindividuals",
                       "ni_sust_frac", "average_waiting_time", "update_probability", "nc", "ng_total",
                       "ng_sust_frac", "n_group_memberships", "group_update_probability", "group_meeting_interval", "p"]
# parameter_name_list = ["k_value", "majority_threshold", "weight_descriptive", "weight_injunctive",
#                        "average_waiting_time", "update_probability", "ng_total", "group_meeting_interval"]
INDEX = {i: parameter_name_list[i] for i in range(len(parameter_name_list))}

experiment_name = "new_measures_test4"

# path to cluster data
# PATH = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\results\\maxploit\\cluster_results\\{experiment_name}"

# path to test data
# PATH = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\results\\maxploit\\00_old\\{experiment_name}"
PATH = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\results\\maxploit\\{experiment_name}"

# path to save figures
SAVE_PATH = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\plots\\maxploit\\{experiment_name}"
if not os.path.exists(SAVE_PATH):
    os.mkdir(SAVE_PATH)
SINGLE_TRAJ_PLOT_PATHS = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\plots\\maxploit\\{experiment_name}\\single_trajs"
if not os.path.exists(SINGLE_TRAJ_PLOT_PATHS):
    os.mkdir(SINGLE_TRAJ_PLOT_PATHS)
MEAN_PATHS = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\plots\\maxploit\\{experiment_name}\\mean_std"
if not os.path.exists(MEAN_PATHS):
    os.mkdir(MEAN_PATHS)
TRAJ_PLOT_PATHS = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\plots\\maxploit\\{experiment_name}\\trajs"
if not os.path.exists(TRAJ_PLOT_PATHS):
    os.mkdir(TRAJ_PLOT_PATHS)
DIST_PATHS =f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\plots\\maxploit\\{experiment_name}\\dist"
if not os.path.exists(DIST_PATHS):
    os.mkdir(DIST_PATHS)

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
descriptive_majority_threshold = parameter_dict["descriptive_majority_threshold"]
injunctive_majority_threshold = parameter_dict["injunctive_majority_threshold"]
weight_descriptive = parameter_dict["weight_descriptive"]
weight_injunctive = parameter_dict["weight_injunctive"]
weight_harvest = parameter_dict["weight_harvest"]
nindividuals = parameter_dict["nindividuals"]
ni_sust_frac = parameter_dict["ni_sust_frac"]
average_waiting_time = parameter_dict["average_waiting_time"]
update_probability = parameter_dict["update_probability"]
nc = parameter_dict["nc"]
ng_total = parameter_dict["ng_total"]
ng_sust_frac = parameter_dict["ng_sust_frac"]
n_group_memberships = parameter_dict["n_group_memberships"]
group_meeting_interval = parameter_dict["group_meeting_interval"]
group_update_probability = parameter_dict["group_update_probability"]
p = parameter_dict["p"]

parameter_list = [attitude_on, ind_initialisation, group_initialisation, fix_group_attitude, timeinterval, timestep, k_value,
             descriptive_majority_threshold, injunctive_majority_threshold, weight_descriptive, weight_injunctive, weight_harvest, nindividuals, ni_sust_frac,
             average_waiting_time, update_probability, nc, ng_total, ng_sust_frac, n_group_memberships, group_update_probability, group_meeting_interval,
             p]


timepoints = np.arange(0, timeinterval[0], timestep[0])
last_timestep = timepoints[-1]
# in case of weird error:
# np.delete(timepoints, [-1])

PARAM_COMBS\
    = list(it.product(attitude_on, ind_initialisation, group_initialisation, fix_group_attitude, timeinterval, timestep, k_value,
             descriptive_majority_threshold, injunctive_majority_threshold, weight_descriptive, weight_injunctive, weight_harvest, nindividuals, ni_sust_frac,
             average_waiting_time, update_probability, nc, ng_total, ng_sust_frac, n_group_memberships, group_update_probability, group_meeting_interval,
             p))

RAW_PATH = PATH + "\\raw"
# raw = pickle.load(open(RAW_LOAD_PATH, "rb"))

TRAJ_PATH = PATH + "\\traj"

RES_LOAD_PATH = PATH + "\\res\\stateval_results.pkl"
print("Loading data...")
data = pd.read_pickle(RES_LOAD_PATH)
print("Done loading data!")

# NETWORK_PATH = PATH + "\\networks"
# if os.path.exists(NETWORK_PATH):
#     print("Loading networks...")
#     acquaintance_network = pickle.load(open(NETWORK_PATH+"\\culture.acquaintance_network.pkl","rb"))
#     group_membership_network = pickle.load(open(NETWORK_PATH+"\\culture.group_membership_network.pkl","rb"))
#     inter_group_network = pickle.load(open(NETWORK_PATH+"\\inter_group_network.pkl","rb"))
#     node_states = pickle.load(open(NETWORK_PATH+"\\node_states.pkl", "rb"))
#     print("Done loading networks!")

# how to deal with keys
# data.head()
# for x in PARAM_COMBS:
#     data['mean'].unstack('observables').xs(key=tuple(x), level=parameter_name_list).plot()
#     plt.show()
# data['std'].unstack('observables').xs(key=key_dict["0"], level=parameter_name_list).plot()
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
# variables = ['Cell.stock', 'Individual.behaviour', 'Group.group_attitude', 'Group.mean_group_behaviour']
variables_2 = ['Cell.stock', 'Individual.behaviour']
ranges = [(0, 400), (0, 400)]

# ----- plot trajs -----
if os.path.exists(TRAJ_PATH):
    print("Trajectories are plotted.")
    ids = pmf.get_mofa_id(PARAM_COMBS)
    for i in ids:
        if not os.path.exists(SINGLE_TRAJ_PLOT_PATHS + "\\" + i):
            os.mkdir(SINGLE_TRAJ_PLOT_PATHS + "\\" + i)
    fnames = np.sort(glob.glob(TRAJ_PATH + "\\*"))
    for i in ids:
        for index, f in enumerate(fnames):
            if i in f:
                traj = pickle.load(open(f, "rb"))
                t = np.array(traj["t"])
                cells = list(traj["Cell.stock"].keys())
                individuals = list(traj["Individual.behaviour"].keys())
                groups = list(traj["Group.group_attitude"].keys())
                fig, ax = plt.subplots()
                for c in cells:
                    ax.plot(t, traj["Cell.stock"][c])
                ax.set_xlabel("t")
                ax.set_ylabel("Cell.stock")
                ax.set_title(f)
                # ax.legend(loc="best")
                # plt.show()
                plt.savefig(SINGLE_TRAJ_PLOT_PATHS + "\\" + i + f"\\{i}_stock_{index}.png")
                plt.close()
                for index in range(100):
                    fig, ax = plt.subplots()
                    ax.plot(t, traj["Cell.stock"][cells[index]], label="cell")
                    ax.plot(t, traj["Individual.behaviour"][individuals[index]], label="ind")
                    ax.set_xlabel("t")
                    ax.set_ylabel("Value")
                    ax.set_title(f)
                    ax.legend(loc="best")
                    plt.savefig(SINGLE_TRAJ_PLOT_PATHS + "\\" + i + f"\\{i}_all_{index}.png")
                    # plt.show()
                    plt.close()

# ----- plot raw data -----
if os.path.exists(RAW_PATH):
    print("Raw data is plotted...:")
    # ----- plot traj trajectories -----
    # can only be done if raw data available
    # pmf.plot_single_trajs(variables, PARAM_COMBS, timepoints, RAW_PATH, TRAJ_PLOT_PATHS)
    pmf.plot_all_trajs_in_one(variables, PARAM_COMBS, timepoints, RAW_PATH, TRAJ_PLOT_PATHS)
    # pmf.plot_distributions(PARAM_COMBS, variables_2, ranges, last_timestep, RAW_PATH, DIST_PATHS)
    print("Plotting raw data done!")

# ----- plot mean and std trajectories -----
# can only be done if raw data available
# pmf.plot_mean_and_std_traj(data, PARAM_COMBS, parameter_name_list, variables, timepoints, MEAN_PATHS)

# ----- phase transition plot -----
# pmf.phase_transition(data, parameter_name_list, parameter_dict, parameter_list, "majority_threshold", last_timestep, variables_2, SAVE_PATH)

# ----- pixel plot -----
# pmf.pixel_plot(data, config, parameter_name_list, parameter_list, PARAM_COMBS, last_timestep, variables, SAVE_PATH)