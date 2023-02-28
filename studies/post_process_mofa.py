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

# path to data
experiment_name = "group_size2"
SAVE_FOLDER = f"/p/projects/copan/users/maxbecht/results/maxploit/{experiment_name}"
# SAVE_FOLDER = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\results\\maxploit\\{experiment_name}"
SAVE_PATH_RAW = SAVE_FOLDER + "/" + "raw"
SAVE_PATH_RES = SAVE_FOLDER + "/" + "res"

# load config
CONFIG_LOAD_PATH = SAVE_FOLDER + "/config.json"
config = json.load(open(CONFIG_LOAD_PATH))

parameter_name_list = ["attitude_on", "ind_initialisation", "group_initialisation", "fix_group_attitude", "timeinterval", "timestep",
                       "k_value", "majority_threshold", "weight_descriptive", "weight_injunctive", "ni_sust",
                       "ni_nonsust", "nindividuals", "average_waiting_time", "update_probability", "nc", "ng_total",
                       "group_update_probability", "ng_sust", "ng_nonsust", "group_meeting_interval", "p"]

parameter_dict = {str(key): value for key, value in config.items() if key in parameter_name_list}

# create parameter list
attitude_on = parameter_dict["ind_initialisation"]
ind_initialisation = parameter_dict["ind_initialisation"]
group_initialisation = parameter_dict["group_initialisation"]
fix_group_attitude = parameter_dict["fix_group_attitude"]
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
group_update_probability = parameter_dict["group_update_probability"]
ng_sust = parameter_dict["ng_sust"]
ng_nonsust = parameter_dict["ng_nonsust"]
group_meeting_interval = parameter_dict["group_meeting_interval"]
p = parameter_dict["p"]

parameter_list = [attitude_on, ind_initialisation, group_initialisation, fix_group_attitude, timeinterval, timestep, k_value,
                  majority_threshold, weight_descriptive, weight_injunctive, ni_sust, ni_nonsust, nindividuals,
                  average_waiting_time, update_probability, nc, ng_total, group_update_probability, ng_sust, ng_nonsust, group_meeting_interval,
                  p]

INDEX = {i: parameter_name_list[i] for i in range(len(parameter_name_list))}
PARAM_COMBS = list(it.product(attitude_on, ind_initialisation, group_initialisation, fix_group_attitude, timeinterval, timestep, k_value,
                  majority_threshold, weight_descriptive, weight_injunctive, ni_sust, ni_nonsust, nindividuals,
                  average_waiting_time, update_probability, nc, ng_total, group_update_probability, ng_sust, ng_nonsust, group_meeting_interval,
                  p))
SAMPLE_SIZE = 100

handle = eh(sample_size=SAMPLE_SIZE, parameter_combinations=PARAM_COMBS, index=INDEX, path_raw=SAVE_PATH_RAW, path_res=SAVE_PATH_RES)

# ----- postprocess -----

# how to call these results
filename = "stateval_results.pkl"

EVA = {
    "mean": lambda fnames: pd.concat([np.load(f, allow_pickle=True)
                                      for f in fnames if "traj" not in f]).groupby(level=0).mean(),
    "std": lambda fnames: pd.concat([np.load(f, allow_pickle=True)
                                     for f in fnames if "traj" not in f]).groupby(level=0).std()
}

handle.resave(EVA, filename)