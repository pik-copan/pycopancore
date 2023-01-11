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
PATH = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\results\\maxploit\\test10"

# load config
CONFIG_LOAD_PATH = PATH + "\\config.json"
config = json.load(open(CONFIG_LOAD_PATH))

parameter_dict = {str(key): value for key, value in config.items() if key in parameter_name_list}

# create key list in dictionary
key_dict = {}
# find max lengt
max_length = max([len(value) for key, value in parameter_dict.items()])
for n in range(max_length):
    key_list = []
    for key, value in parameter_dict.items():
        if n < len(value):
            key_list.append(value[n])
        else:
            key_list.append(value[0])
    key_dict[f"{n}"] = key_list


RAW_LOAD_PATH = PATH + "\\raw\\1-1-1-10-0o1-2-0o5-1-0-400-0-400-1-0o5-400-1-0-1-1-0o05_s0.pkl"
raw = pickle.load(open(RAW_LOAD_PATH, "rb"))

RES_LOAD_PATH = PATH + "\\res\\stateval_results.pkl"
data = pd.read_pickle(RES_LOAD_PATH)

# how to deal with keys
data.head()
data['mean'].unstack('observables').xs(key=key_dict["0"], level=parameter_name_list).plot()
data['sem'].unstack('observables').xs(key=key_dict["0"], level=parameter_name_list).plot()
plt.show()