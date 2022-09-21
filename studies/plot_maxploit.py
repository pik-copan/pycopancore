import pickle
import json
import os
import networkx as nx
from matplotlib import pyplot as plt

# data from which date?
date = "2022_09_21"
# data from which run?
run = "Run_2022_09_21_14_57_43"

traj_path = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\maxploit\\{date}\\{run}\\traj.pickle"
network_path = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\maxploit\\{date}\\{run}\\networks"
configuration_path = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\maxploit\\{date}\\{run}\\configuration.json"


