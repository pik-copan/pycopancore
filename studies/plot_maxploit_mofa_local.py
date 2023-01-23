import numpy as np
from time import time
import datetime as dt

import pandas as pd
from numpy import random
import json
import itertools as it
import networkx as nx
import os
import pickle
from matplotlib import pyplot as plt
import numpy as np
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import plotly.offline as py
import matplotlib.colors as colors
import matplotlib.cm as cmx
import datetime
import glob
# from plot_maxploit_functions import correct_timeline

parameter_name_list = ["ind_initialisation", "group_initialisation", "fix_group_opinion", "timeinterval", "timestep",
                       "k_value", "majority_threshold", "weight_descriptive", "weight_injunctive", "ni_sust",
                       "ni_nonsust", "nindividuals", "average_waiting_time", "update_probability", "nc", "ng_total",
                       "ng_sust", "ng_nonsust", "group_meeting_interval", "p"]
# parameter_name_list = ["k_value", "majority_threshold", "weight_descriptive", "weight_injunctive",
#                        "average_waiting_time", "update_probability", "ng_total", "group_meeting_interval"]
INDEX = {i: parameter_name_list[i] for i in range(len(parameter_name_list))}

# path to data
PATH = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\results\\maxploit\\handle_test"

# load config
CONFIG_LOAD_PATH = PATH + "\\config.json"
config = json.load(open(CONFIG_LOAD_PATH))

parameter_dict = {str(key): value for key, value in config.items() if key in parameter_name_list}

# create parameter list
ind_initialisation = parameter_dict["ind_initialisation"]
group_initialisation = parameter_dict["group_initialisation"]
fix_group_opinion = parameter_dict["fix_group_opinion"]
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

parameter_list = [ind_initialisation, group_initialisation, fix_group_opinion, timeinterval, timestep, k_value,
                  majority_threshold, weight_descriptive, weight_injunctive, ni_sust, ni_nonsust, nindividuals,
                  average_waiting_time, update_probability, nc, ng_total, ng_sust, ng_nonsust, group_meeting_interval,
                  p]

last_timestep = timeinterval[0] - timestep[0]

PARAM_COMBS\
    = list(it.product(ind_initialisation, group_initialisation, fix_group_opinion, timeinterval, timestep, k_value,
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

# create key sets for single parameter sweeps for plotting
# change the ones that were sweeped and fix the other ones

# get names of alternating params
alternating_params = []
for key, value in config.items():
    if len(value) > 1 and isinstance(value, list):
        alternating_params.append(key)

# get param location
param_name_1 = "average_waiting_time"
param_name_2 = "update_probability"

# 2 params in which place?
for index, key in enumerate(parameter_name_list):
    if key == param_name_1:
        param_loc_1 = index
for index, key in enumerate(parameter_name_list):
    if key == param_name_2:
        param_loc_2 = index
# param_loc_1 = 6
# param_loc_2 = 13
param_sweep_1 = []
# which parameters have to be fixed? (2 need to remain free)

param_fix_names = []
for x in alternating_params:
    if x is not param_name_1 or param_name_2:
        param_fix_names.append(x)

param_fix_name = "majority_threshold"
for index, key in enumerate(parameter_name_list):
    if key == param_fix_name:
        param_fix_loc_1 = index

param_fix_value_1 = config[param_fix_name][0]

#create the a key matrix
A = np.zeros((len(parameter_list[param_loc_1]), len(parameter_list[param_loc_2])), dtype=list)
for p in PARAM_COMBS:
    value = list(p)
    if value[param_fix_loc_1] == param_fix_value_1: #and fix 2 = ... and so on
        for index_i, i in enumerate(parameter_list[param_loc_1]):
            for index_j, j in enumerate(parameter_list[param_loc_2]):
                new_key = []
                for index, x in enumerate(value):
                    if index == param_loc_1:
                        new_key.append(i)
                    elif index == param_loc_2:
                        new_key.append(j)
                    else:
                        new_key.append(x)
                A[index_i][index_j] = new_key

# create a data matrix
data_matrix = np.zeros((len(parameter_list[param_loc_1]), len(parameter_list[param_loc_2])), dtype=float)
for i in range(np.shape(data_matrix)[0]):
    for j in range(np.shape(data_matrix)[1]):
        data_matrix[i][j] = float(data['mean'].unstack('observables').xs(key=tuple(A[i][j]),
                           level=parameter_name_list).loc[last_timestep, "Cell.stock"])

# ----- PIXEL PLOT -----
# create a 2d data set
pixel_plot = plt.figure()
# plotting a plot
# pixel_plot.add_axes()
# customizing plot
plt.title("Chessboard")
pixel_plot = plt.imshow(data_matrix, cmap='jet', interpolation='nearest')
plt.colorbar(pixel_plot)
# save a plot
# plt.savefig('pixel_plot.png')
# show plot
plt.show()
