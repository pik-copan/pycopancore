import numpy as np
from time import time
import datetime as dt
from numpy import random
import json
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
from plot_maxploit_functions import correct_timeline

parameter_name_list = ["ind_initialisation", "group_initialisation", "fix_group_opinion", "timeinterval", "timestep",
                       "k_value", "majority_threshold", "weight_descriptive", "weight_injunctive", "ni_sust",
                       "ni_nonsust", "nindividuals", "average_waiting_time", "nc", "ng_total", "ng_sust", "ng_nonsust",
                       "group_meeting_interval", "p"]
INDEX = {i: parameter_name_list[i] for i in range(len(parameter_name_list))}

RAW_LOAD_PATH = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\results\\pymofa_test2\\raw\\0-0-1-1-0o01-2-0o5-0o5-0o5-400-0-400-1-400-10-5-5-1-0o05_s1.pkl"
RES_LOAD_PATH = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\results\\pymofa_test2\\res\\stateval_results.pkl"

raw = pickle.load(open(RAW_LOAD_PATH, "rb"))
res = pickle.load(open(RES_LOAD_PATH, "rb"))

