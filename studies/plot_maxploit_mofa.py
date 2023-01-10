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

# parameter_list_full = [ind_initialisation, group_initialisation, fix_group_opinion, timeinterval, timestep, k_value,
#                   majority_threshold, weight_descriptive, weight_injunctive, ni_sust, ni_nonsust, nindividuals,
#                   average_waiting_time, update_probability, nc, ng_total, ng_sust, ng_nonsust, group_meeting_interval,
#                   p]
# parameter_name_list_full = ["ind_initialisation", "group_initialisation", "fix_group_opinion", "timeinterval", "timestep",
#                        "k_value", "majority_threshold", "weight_descriptive", "weight_injunctive", "ni_sust",
#                        "ni_nonsust", "nindividuals", "average_waiting_time", "update_probability", "nc", "ng_total",
#                        "ng_sust", "ng_nonsust", "group_meeting_interval", "p"]
parameter_name_list = ["k_value", "majority_threshold", "weight_descriptive", "weight_injunctive",
                       "average_waiting_time", "update_probability", "ng_total", "group_meeting_interval"]
INDEX = {i: parameter_name_list[i] for i in range(len(parameter_name_list))}

# path to data
PATH = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\results\\maxploit\\test2"

# load config
CONFIG_LOAD_PATH = PATH + "\\config.json"
config = json.load(open(CONFIG_LOAD_PATH))

parameter_dict = {str(key): value for key, value in config.items() if key in parameter_name_list}

# create key list in dictionary
key_dict = {}
max_length = max([len(value) for key, value in parameter_dict])
for n in range(max_length):
    key_list = []
    for key, value in config.items():
        if key in parameter_name_list:
            if isinstance(value, list):
                key_list.append(value[n])
            else:
                key_list.append(value)
    key_dict[f"{n}"] = key_list


# RAW_LOAD_PATH = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\results\\pymofa_test2\\raw\\0-0-1-1-0o01-2-0o5-0o5-0o5-400-0-400-1-400-10-5-5-1-0o05_s1.pkl"
RES_LOAD_PATH = PATH + "\\res\\stateval_results.pkl"

# raw = pickle.load(open(RAW_LOAD_PATH, "rb"))
data = pd.read_pickle(RES_LOAD_PATH)

# how to deal with keys

data['mean'].unstack('observables').xs(key=(0.1, 0.1, 0.01, 1.0, 1000), level=parameter_name_list)