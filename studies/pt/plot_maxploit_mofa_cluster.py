import os
import pickle
import glob
import pandas as pd
import json
import itertools as it
import numpy as np
import matplotlib.pyplot as plt
# from plot_maxploit_functions import correct_timeline
from plot_functions import plot_maxploit_functions_cluster as pmf
import networkx as nx
from studies.pt.plot_functions.plot_multilayer import LayeredNetworkGraph

old_run = 0

parameter_name_list = ["attitude_on", "ind_initialisation", "group_initialisation", "fix_group_attitude", "timeinterval", "timestep",
                       "k_value", "descriptive_majority_threshold", "injunctive_majority_threshold", "weight_descriptive", "weight_injunctive", "weight_harvest",
                       "nindividuals",
                       "ni_sust_frac", "average_waiting_time", "update_probability", "nc", "ng_total",
                       "ng_sust_frac", "n_group_memberships", "group_update_probability", "group_meeting_interval", "p"]
# parameter_name_list = ["k_value", "majority_threshold", "weight_descriptive", "weight_injunctive",
#                        "average_waiting_time", "update_probability", "ng_total", "group_meeting_interval"]


INDEX = {i: parameter_name_list[i] for i in range(len(parameter_name_list))}

experiment_name = "full_model_thresholds_2_1"

# path to cluster data
# PATH = f"/p/projects/copan/users/maxbecht/results/maxploit2/{experiment_name}"
# PATH = f"/p/projects/copan/users/maxbecht/results/maxploit3/{experiment_name}"
PATH = f"/p/tmp/maxbecht/paper/{experiment_name}"

# path to test data
# PATH = f"C:/Users/bigma/Documents/Uni/Master/MA_Masterarbeit/results/maxploit/00_old/{experiment_name}"
# PATH = f"C:/Users/bigma/Documents/Uni/Master/MA_Masterarbeit/results/maxploit/{experiment_name}"

if old_run:
    parameter_name_list.remove("weight_harvest")
    weight_harvest = 0
    PATH = f"/p/projects/copan/users/maxbecht/paper/{experiment_name}"

# path to save figures
# SAVE_PATH = f"/p/projects/copan/users/maxbecht/plots/{experiment_name}"
SAVE_PATH = f"/p/tmp/maxbecht/paper_plots/{experiment_name}"
if not os.path.exists(SAVE_PATH):
    os.mkdir(SAVE_PATH)
# SINGLE_TRAJ_PLOT_PATHS = f"/p/projects/copan/users/maxbecht/plots/{experiment_name}/single_trajs"
SINGLE_TRAJ_PLOT_PATHS = f"/p/tmp/maxbecht/paper_plots/{experiment_name}/single_trajs"
if not os.path.exists(SINGLE_TRAJ_PLOT_PATHS):
    os.mkdir(SINGLE_TRAJ_PLOT_PATHS)
# MEAN_PATHS = f"/p/projects/copan/users/maxbecht/plots/{experiment_name}/mean_std"
MEAN_PATHS = f"/p/tmp/maxbecht/paper_plots/{experiment_name}/mean_std"
if not os.path.exists(MEAN_PATHS):
    os.mkdir(MEAN_PATHS)
# TRAJ_PLOT_PATHS = f"/p/projects/copan/users/maxbecht/plots/{experiment_name}/trajs"
TRAJ_PLOT_PATHS = f"/p/tmp/maxbecht/paper_plots/{experiment_name}/trajs"
if not os.path.exists(TRAJ_PLOT_PATHS):
    os.mkdir(TRAJ_PLOT_PATHS)
# DIST_PATHS = f"/p/projects/copan/users/maxbecht/plots/{experiment_name}/dist"
DIST_PATHS = f"/p/tmp/maxbecht/paper_plots/{experiment_name}/dist"
if not os.path.exists(DIST_PATHS):
    os.mkdir(DIST_PATHS)

# test
# SAVE_PATH = f"C:/Users/bigma/Documents/Uni/Master/MA_Masterarbeit/plots/maxploit/test"

# load config
CONFIG_LOAD_PATH = PATH + "/config.json"
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
weight_harvest = [0]
if not old_run:
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

if old_run:
    parameter_list.remove(weight_harvest)

timepoints = np.arange(0, timeinterval[0], timestep[0])
last_timestep = timepoints[-1]
# in case of weird error:
# np.delete(timepoints, [-1])

if not old_run:
    PARAM_COMBS\
        = list(it.product(attitude_on, ind_initialisation, group_initialisation, fix_group_attitude, timeinterval, timestep, k_value,
                 descriptive_majority_threshold, injunctive_majority_threshold, weight_descriptive, weight_injunctive, weight_harvest, nindividuals, ni_sust_frac,
                 average_waiting_time, update_probability, nc, ng_total, ng_sust_frac, n_group_memberships, group_update_probability, group_meeting_interval,
                 p))

else:
    PARAM_COMBS = list(it.product(attitude_on, ind_initialisation, group_initialisation, fix_group_attitude, timeinterval, timestep, k_value,
             descriptive_majority_threshold, injunctive_majority_threshold, weight_descriptive, weight_injunctive, nindividuals, ni_sust_frac,
             average_waiting_time, update_probability, nc, ng_total, ng_sust_frac, n_group_memberships, group_update_probability, group_meeting_interval,
             p))

RAW_PATH = PATH + "/raw"
# raw = pickle.load(open(RAW_LOAD_PATH, "rb"))

TRAJ_PATH = PATH + "/traj"

RES_LOAD_PATH = PATH + "/res/stateval_results.pkl"
print("Loading data...")
data = pd.read_pickle(RES_LOAD_PATH)
print("Done loading data!")

# NETWORK_PATHS = f"/p/projects/copan/users/maxbecht/plots/{experiment_name}/networks"
# if not os.path.exists(NETWORK_PATHS):
#     os.mkdir(NETWORK_PATHS)
# NETWORK_LOAD_PATH = PATH + "/networks"

# NETWORK_PATH = PATH + "/networks"
# if os.path.exists(NETWORK_PATH):
#     print("Loading networks...")
#     acquaintance_network = pickle.load(open(NETWORK_PATH+"/culture.acquaintance_network.pkl","rb"))
#     group_membership_network = pickle.load(open(NETWORK_PATH+"/culture.group_membership_network.pkl","rb"))
#     inter_group_network = pickle.load(open(NETWORK_PATH+"/inter_group_network.pkl","rb"))
#     node_states = pickle.load(open(NETWORK_PATH+"/node_states.pkl", "rb"))
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
# variables = [name for name, values in data['mean'].unstack('observables').items()]
# or set them yourself
variables = ['Cell.stock', 'Individual.behaviour', 'Group.group_attitude', 'Individual.alignment']
variables_2 = ['Cell.stock', 'Individual.behaviour']
ranges = [(0, 400), (0, 400)]

# ----- plot trajs -----
# if os.path.exists(TRAJ_PATH):
#     print("Trajectories are plotted.")
#     ids = pmf.get_mofa_id(PARAM_COMBS)
#     for i in ids:
#         if not os.path.exists(SINGLE_TRAJ_PLOT_PATHS + "/" + i):
#             os.mkdir(SINGLE_TRAJ_PLOT_PATHS + "/" + i)
#     fnames = np.sort(glob.glob(TRAJ_PATH + "/*"))
#     for i in ids:
#         for index, f in enumerate(fnames):
#             if i in f:
#                 traj = pickle.load(open(f, "rb"))
#                 t = np.array(traj["t"])
#                 cells = list(traj["Cell.stock"].keys())
#                 individuals = list(traj["Individual.behaviour"].keys())
#                 groups = list(traj["Group.group_attitude"].keys())
#                 fig, ax = plt.subplots()
#                 for c in cells:
#                     ax.plot(t, traj["Cell.stock"][c])
#                 ax.set_xlabel("t")
#                 ax.set_ylabel("Cell.stock")
#                 ax.set_title(f)
#                 # ax.legend(loc="best")
#                 # plt.show()
#                 plt.savefig(SINGLE_TRAJ_PLOT_PATHS + "/" + i + f"/{i}_stock_{index}.png")
#                 plt.close()
#                 for index in range(100):
#                     fig, ax = plt.subplots()
#                     ax.plot(t, traj["Cell.stock"][cells[index]], label="cell")
#                     ax.plot(t, traj["Individual.behaviour"][individuals[index]], label="ind")
#                     ax.set_xlabel("t")
#                     ax.set_ylabel("Value")
#                     ax.set_title(f)
#                     ax.legend(loc="best")
#                     plt.savefig(SINGLE_TRAJ_PLOT_PATHS + "/" + i + f"/{i}_all_{index}.png")
#                     # plt.show()
#                     plt.close()

# ----- plot raw data -----
if os.path.exists(RAW_PATH):
    print("Raw data is plotted...:")
    # ----- plot traj trajectories -----
    # can only be done if raw data available
    # pmf.plot_single_trajs(variables, PARAM_COMBS, timepoints, RAW_PATH, TRAJ_PLOT_PATHS, 400, 2)
    # pmf.plot_all_trajs_in_one(variables, PARAM_COMBS, timepoints, 400, RAW_PATH, TRAJ_PLOT_PATHS)
    # pmf.plot_all_trajs_in_one(variables_2, PARAM_COMBS, timepoints, 400, RAW_PATH, TRAJ_PLOT_PATHS)
    # pmf.plot_distributions(PARAM_COMBS, variables_2, ranges, last_timestep, RAW_PATH, DIST_PATHS)
    print("Plotting raw data done!")

# ----- analyse stationarity -----
# pmf.stationarity_analysis(PARAM_COMBS, RAW_PATH, SAVE_PATH)

# ----- plot mean and std trajectories -----
# can only be done if raw data available
#pmf.plot_mean_and_std_traj(data, PARAM_COMBS, parameter_name_list, variables_2, timepoints, 400, MEAN_PATHS)

# ----- phase transition plot -----
# pmf.phase_transition(data, PARAM_COMBS, parameter_dict, parameter_name_list, "descriptive_majority_threshold", last_timestep, variables_2, 400, SAVE_PATH)
# pmf.phase_transition(data, PARAM_COMBS, parameter_dict, parameter_name_list, "injunctive_majority_threshold", last_timestep, variables_2, 400, SAVE_PATH)
# pmf.phase_transition(data, PARAM_COMBS, parameter_dict, parameter_name_list, "average_waiting_time", last_timestep, variables_2, 400, SAVE_PATH, scale="log")
# pmf.phase_transition(data, PARAM_COMBS, parameter_dict, parameter_name_list, "p", last_timestep, variables_2, 400, SAVE_PATH, scale="log")
# pmf.phase_transition(data, PARAM_COMBS, parameter_dict, parameter_name_list, "k_value", last_timestep, variables_2, 400, SAVE_PATH, scale="log")
# pmf.phase_transition(data, PARAM_COMBS, parameter_dict, parameter_name_list, "ng_total", last_timestep, variables_2, 400, SAVE_PATH)
# pmf.phase_transition(data, PARAM_COMBS, parameter_dict, parameter_name_list, "group_update_probability", last_timestep, variables_2, 400, SAVE_PATH)

# ----- 2d phase space plot -----
# pmf.plot_phase_plot(data, PARAM_COMBS, parameter_name_list, ["Cell.stock", "Individual.behaviour"], timepoints, 400, SAVE_PATH)
# pmf.plot_phase_plot_with_analytical_h(data, False, PARAM_COMBS, parameter_name_list, parameter_list, ["Cell.stock", "Individual.behaviour"], timepoints, 400, SAVE_PATH)

# ----- pixel plot -----
# differemt cmaps: classic gradient: "viridis", "plasma"; diverging: "coolwarm", "seismic";
cmaps = ["RdYlGn", "RdBu", "inferno_r"]
pmf.pixel_plot(data, config, cmaps, parameter_name_list, parameter_list, PARAM_COMBS, last_timestep, variables_2, 400, SAVE_PATH)
# groups:
# pmf.pixel_plot(data, config, cmaps, parameter_name_list, parameter_list, PARAM_COMBS, last_timestep, variables_2, 400, SAVE_PATH, groups=True)

# ----- plot networks -----

plot_networks = False
if plot_networks:
    if os.path.exists(NETWORK_LOAD_PATH):
        print("Networks are plotted.")
        ids = pmf.get_mofa_id(PARAM_COMBS)
        for i in ids:
            if not os.path.exists(NETWORK_PATHS + "/" + i):
                os.mkdir(NETWORK_PATHS + "/" + i)
        fnames = np.sort(glob.glob(NETWORK_LOAD_PATH + "/*"))
        for i in ids:
            for index, f in enumerate(fnames):
                if i in f:
                    acquaintance_network = pickle.load(open(f + "/culture.acquaintance_network.pkl", "rb"))
                    group_membership_network = pickle.load(
                        open(f + "/culture.group_membership_network.pkl", "rb"))
                    inter_group_network = pickle.load(open(f + "/inter_group_network.pkl", "rb"))
                    node_states = pickle.load(open(f + "/node_states.pkl", "rb"))
                    # node states are saved at same length
                    n_t = len(node_states["Individual.behaviour"][list(node_states["Individual.behaviour"].keys())[0]])
                    t = np.arange(0, n_t, 1)
                    v_array1 = []
                    v_array2 = []
                    for key, value in node_states["Individual.behaviour"].items():
                        v_array1.append(value)
                    for key, value in node_states["Group.group_attitude"].items():
                        v_array2.append(value)
                    v_array1_0 = [item[0] for item in v_array1]
                    v_array2_0 = [item[0] for item in v_array2]
                    v_array = [v_array1_0, v_array2_0]
                    fig = plt.figure()
                    ax = fig.add_subplot(111, projection='3d')
                    # ax.set_proj_type('ortho')
                    # multilayer = LayeredNetworkGraph([acquaintance_network, inter_group_network],
                    #                                  [group_membership_network],
                    #                                  v_array, ax=ax, layout=nx.random_layout, highlight_cluster="Unsus")
                    multilayer = LayeredNetworkGraph([acquaintance_network, inter_group_network],
                                                     [group_membership_network],
                                                     v_array, ax=ax, layout=nx.random_layout)
                    node_positions = multilayer.save_node_positions()  # to get node positions
                    plt.close()
                    for t_index in range(len(t)):
                        fig = plt.figure()
                        v_array1 = []
                        v_array2 = []
                        for key, value in node_states["Individual.behaviour"].items():
                            v_array1.append(value)
                        for key, value in node_states["Group.group_attitude"].items():
                            v_array2.append(value)
                        v_array1_t = [item[t_index] for item in v_array1]
                        v_array2_t = [item[t_index] for item in v_array2]
                        v_array = [v_array1_t, v_array2_t]
                        fig = plt.figure(figsize=(10, 10), dpi=200)
                        ax = fig.add_subplot(111, projection='3d')
                        # ax.view_init(40 + 0.075 * t_index, 40 - 0.075 * t_index)
                        LayeredNetworkGraph([acquaintance_network, inter_group_network], [group_membership_network],
                                            v_array, ax=ax, layout=nx.spring_layout, node_positions=node_positions)
                        plt.axis('off')
                        my_file = f'layered_network_{t_index}.png'
                        save_path = NETWORK_PATHS + "/" + i + "/" + str(index)
                        if not os.path.exists(save_path):
                            os.mkdir(save_path)
                        fig.savefig(os.path.join(save_path, my_file))

                    plt.close()
                    plt.close('all')
                    plt.close(fig)
                plt.close('all')
            plt.close('all')
        plt.close('all')
    plt.close('all')
plt.close('all')
print("End plotting.")