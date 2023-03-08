"""Study for the maxploit model.

A study to run the maxploit model.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

# argparse for mc runs
# import argparse
# parser = argparse.ArgumentParser()
# parser.parse_args()
# parser.add_argument("runset_no",
#                     help="Integer that gives the number of the runset for MC-runs. \
#                                        Should be the same in the batch script.")
# args = parser.parse_args()  # returns data from the options specified
# print(type(args.runset_no))

import numpy as np
from time import time
import datetime as dt
from numpy import random
import json
import networkx as nx
from pickle import dump

import pycopancore.models.maxploit as M
from pycopancore.runners.runner import Runner

# ---configuration---

# facts
group_meeting_type = "Step"  # "Step" or "Event"
"""Step means a regular meeting interval. 
Event means a similar way to the individuals way of drawing a next agent. 
Note that this variable is meant only for documentation purposes, the code needs to be changed by hand."""
group_attitude_formation = "Majority"  # "Majority" or "Random" or "Leader"
"""Majority means that the group attitude is calculated from the mean.
Random means that the group attitude is picked from one of the member individuals attitudes.
Leader means that the group attitude follows the lead of a leader (somehow to be implemented).
Note that this variable is meant only for documentation purposes, the code needs to be changed by hand."""
descriptive_norm_formation = "Majority"  # "Majority" or "Random"
"""Majority means that the descriptive norm is calculated from the mean of acquaintances.
Random means that the descriptive norm is calculated from one random one of the acquaintances attitudes.
Note that this variable is meant only for documentation purposes, the code needs to be changed by hand."""
adaptivity = "No"  # "Yes" or "No"
"""If adaptive or not, selfexplainatory. Is not a Toggle."""
switching_back = "No"  # can individuals switch even if norm does not say so?

# toggles
ind_initialisation = "Random"  #"Random" or "Given"
"""Random means that inds are initialised randomly.
Given means that a certain percentage of individuals starts a way.
Note that this variable is a toggle."""
group_initialisation = "Random"  #"Random" or "Given"
"""Random means that groups are initialised randomly.
Given means that a certain percentage of groups starts a way.
Note that this variable is a toggle."""
fix_group_attitude = False # boolean
"""Does not allow the initial group attitude to change,
i.e. group becomes a norm entitiy."""

# seed
# seed = 1

# runner
timeinterval = 100
timestep = 1

# culture
majority_threshold = 0.5
weight_descriptive = 0.5
weight_injunctive = 0.5

# logit
# k_value = 2.94445 #produces probabilities of roughly 0.05, 0.5, 0.95
k_value = 2 # reproduces probs of exploit for gamma = 1

# individuals
nindividuals = 400
ni_sust_frac = 0.5
ni_sust = int(nindividuals * ni_sust_frac)  # number of agents with sustainable behaviour 1
ni_nonsust = nindividuals - ni_sust # number of agents with unsustainable behaviour 0
average_waiting_time = 1
update_probability = 0.75


# cells:
cell_stock=1
cell_capacity=1
cell_growth_rate=1
nc = nindividuals  # number of cells

#groups:
ng_total = 10 # number of total groups
ng_sust_frac = 0.5
ng_sust = int(ng_total * ng_sust_frac) # number of sustainable groups
ng_nonsust = ng_total - ng_sust
group_meeting_interval = 1

#networks
acquaintance_network_type = "Erdos-Renyi"
group_membership_network_type = "1-random-Edge"
p = 0.05  # link density for random networks; wiedermann: 0.05

# decide if results should be saved:
save = "n" # "y" or "n"

# decide if multiple results should be saved:
# mc_save = "y" # "y" or "n"
# run_set_no = "2" # give explicit number of runset

# for saving numbers (range(start_end))
# name_start = 0  # default
# name_end = 500

#---write into dic---
configuration = {
    "Group Meeting Type": group_meeting_type,
    "Group attitude Formation": group_attitude_formation,
    "Descriptive Norm Formation": descriptive_norm_formation,
    "Adaptivity": adaptivity,
    "Switching in opposite direction": switching_back,
    "Initialisation of Individuals": ind_initialisation,
    "Initialisation of Groups": group_initialisation,
    "Fixed group attitudes": fix_group_attitude,
    "timeinterval": timeinterval,
    "timestep": timestep,
    "k_value": k_value,
    "majority_treshold":  majority_threshold,
    "weight_descriptive": weight_descriptive,
    "weight_injunctive": weight_injunctive,
    "ni_sust" : ni_sust,
    "ni_nonsust" : ni_nonsust,
    "nindividuals" : nindividuals,
    "average_waiting_time": average_waiting_time,
    "cell_stock": cell_stock,
    "cell_capacity": cell_capacity,
    "cell_growth_rate": cell_growth_rate,
    "nc" : nc,
    "ng_total" : ng_total,
    "ng_sust" : ng_sust,
    "ng_nonsust" : ng_nonsust,
    "group_meeting_interval" : group_meeting_interval,
    "acquaintance_network_type" : acquaintance_network_type,
    "group_membership_network_type" : group_membership_network_type,
    "link density for random networks" : p
}


########################################################################################################################
# set seed so that each execution must return same thing:
# if "seed" in locals():
#     configuration["seed"]: seed
#     np.random.seed(seed)

attitude_on = 0
descriptive_majority_threshold = 0.5
injunctive_majority_threshold = 0.5

# instantiate model
model = M.Model()

# instantiate process taxa culture:
culture = M.Culture(attitude_on=attitude_on,
                    descriptive_majority_threshold=descriptive_majority_threshold,
                    injunctive_majority_threshold=injunctive_majority_threshold,
                    weight_injunctive=weight_injunctive,
                    fix_group_attitude=fix_group_attitude,
                    k_value=k_value)
print(f"Culture process taxon created: {culture}")

# generate entitites:
world = M.World(culture=culture)
social_system = M.SocialSystem(world=world)
cells = [M.Cell(stock=1, capacity=1, growth_rate=1, social_system=social_system)
         for c in range(nc)]

ni_sust = nindividuals * ni_sust_frac  # number of agents with sustainable behaviour 1
ni_nonsust = nindividuals - ni_sust  # number of agents with unsustainable behaviour 0

# random initialisation or not?
if ind_initialisation:
    behaviour = [0, 1]
    attitude = [0, 1]
    individuals = [M.Individual(average_waiting_time=average_waiting_time,
                                update_probability=update_probability,
                                behaviour=np.random.choice(behaviour),
                                cell=cells[i]) for i in range(nindividuals)]
else:
    individuals = [M.Individual(behaviour=0, attitude=0,
                                cell=cells[i]) for i in range(ni_nonsust)] \
                  + [M.Individual(behaviour=1, attitude=1,
                                  cell=cells[i + ni_nonsust])
                     for i in range(ni_sust)]

ng_sust = ng_total * ng_sust_frac  # number of sustainable groups
ng_nonsust = ng_total - ng_sust

    # instantiate groups
if group_initialisation:
    group_attitude = [0, 1]
    groups = [M.Group(culture=culture, world=world, group_attitude=np.random.choice(group_attitude),
                      group_meeting_interval=group_meeting_interval) for i in range(ng_total)]
else:
    groups = [M.Group(culture=culture, world=world, group_attitude=1,
                      group_meeting_interval=group_meeting_interval) for i in range(ng_sust)] + \
             [M.Group(culture=culture, world=world, group_attitude=0,
                      group_meeting_interval=group_meeting_interval) for i in range(ng_nonsust)]

for (i, c) in enumerate(cells):
    c.individual = individuals[i]

def erdosrenyify(graph, p=0.5):
    """Create a ErdosRenzi graph from networkx graph.

    Take a a networkx.Graph with nodes and distribute the edges following the
    erdos-renyi graph procedure.
    """
    assert not graph.edges(), "your graph has already edges"
    nodes = list(graph.nodes())
    for i, n1 in enumerate(nodes[:-1]):
        for n2 in nodes[i + 1:]:
            if random.random() < p:
                graph.add_edge(n1, n2)

# set the initial graph structure to be an erdos-renyi graph
print("erdosrenyifying the graph ... ", end="", flush=True)
start = time()
erdosrenyify(culture.acquaintance_network, p=p)

# nx.draw(culture.acquaintance_network)
# plt.show()

# degrees = [culture.acquaintance_network.degree(n) for n in culture.acquaintance_network.nodes()]
# plt.hist(degrees)
# plt.show()

# assert that each ind has at least one edge
# for i in individuals:
#     if not list(i.acquaintances):
#         culture.acquaintance_network.add_edge(i, np.random.choice(individuals))

n_group_memberships = 1

# for plausibility reasons
if n_group_memberships > ng_total:
    n_group_memberships = ng_total

# group_membership network with more than one group membership
for i in individuals:
    while len(list(i.group_memberships)) < n_group_memberships:
        g = np.random.choice(groups)
        culture.group_membership_network.add_edge(i, g)

# degrees = [culture.group_membership_network.degree(n) for n in culture.group_membership_network.nodes()]
# plt.hist(degrees)
# plt.show()

# GM = culture.group_membership_network
# color_map = []
# shape_map = []
# for node in list(GM.nodes):
#     color_map.append(GM.nodes[node]["color"])
#     if GM.nodes[node]["type"] == "Group":
#         shape_map.append("o")
#     else:
#         shape_map.append("^")
# top_nodes = {n for n, d in GM.nodes(data=True) if d["type"] == "Group"}
# bottom_nodes = set(GM) - top_nodes
# nx.draw(GM, node_color=color_map, with_labels=False,
#         pos=nx.bipartite_layout(GM, bottom_nodes, align="horizontal", aspect_ratio=4 / 1))
# plt.show()

# get a preliminary intergroup network for plotting multilayer
inter_group_network = nx.Graph()
for g in groups:
    inter_group_network.add_node(g)  # groups have no interaction so far

# Runner
# print("done ({})".format(dt.timedelta(seconds=(time() - start))))
# print('\n runner starting')
r = Runner(model=model)
start = time()
traj = r.run(t_1=timeinterval, dt=timestep)
# runtime = dt.timedelta(seconds=(time() - start))
# print('runtime: {runtime}'.format(**locals()))

# saving trajs in another folder
# create a binary pickle file



#SAVE_PATH_TRAJ = SAVE_PATH_RAW.replace("raw", "traj")
#os.mkdir(SAVE_PATH_TRAJ)

#f = open(SAVE_PATH_TRAJ + filename, "wb")

tosave = {
    v.owning_class.__name__ + "."
    + v.codename: {str(e): traj[v][e]
                   for e in traj[v].keys()
                   }
    for v in traj.keys() if v is not "t"
}

# import pickle
# import os
# SAVE_FOLDER = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\results\\maxploit\\network_test2"
# os.mkdir(SAVE_FOLDER)
#
# print("Saving networks.")
# network_list = [tosave["Culture.acquaintance_network"], tosave["Culture.group_membership_network"]]
# # network_names = ["culture.acquaintance_network", "culture.group_membership_network", "inter_group_network"]
# for counter, n in enumerate(network_list):
#     f = open(SAVE_FOLDER + "networks.pkl", "wb")
#     save_nx = nx.relabel_nodes(n, lambda x: str(x))
#     pickle.dump(save_nx, f)
# print("Done saving networks.")

# import os
# os_path = "/p/projects/copan/maxbecht"
#
# import datetime
# current_time = datetime.datetime.now()
# current = [current_time.month, current_time.day, current_time.hour, current_time.minute, current_time.second]
# time_string = f"{current_time.year}"
# parent_directory_name = f"{current_time.year}"
# for i in current:
#     if i < 10:
#         time_string += f"_0{i}"
#     else:
#         time_string += f"_{i}"
#
# for i in current[:2]:
#     if i < 10:
#         parent_directory_name += f"_0{i}"
#     else:
#         parent_directory_name += f"_{i}"
# # save_time = f"{current_time.year}_" + f"{current_time.month}_" + f"{current_time.day}_" \
# #             + f"{current_time.hour}_" + f"{current_time.minute}_" + f"{current_time.second}"
#
# # Directory
# directory = f"Run_{time_string}"
#
# # Path
# my_path = os.path.join(os_path, parent_directory_name)
#
# # import json
# # f = open(my_path + "_traj_dic.json", "wb")
# # json.dump(traj, f)
#
# if save == "y":
#
#     # Create the directory
#     if not os.path.exists(my_path):
#         os.mkdir(my_path)
#         print(f"Directory {parent_directory_name} created @ {my_path}")
#
#     my_path = os.path.join(my_path, directory)
#     os.mkdir(my_path)
#     print(f"Directory {directory} created @ {my_path}")
#
#     # saving things after succesfull run
#     # saving config
#     #---save json file---
#     print("Saving configuration.json.")
#     f = open(my_path+"/"+"configuration.json", "w+")
#     json.dump(configuration, f, indent=4)
#     print("Done saving configuration.json.")
#
#     # saving traj
#     # create a binary pickle file
#     f = open(my_path + "/" + "traj.pickle", "wb")
#
#     tosave = {
#               v.owning_class.__name__ + "."
#               + v.codename: {str(e): traj[v][e]
#                              for e in traj[v].keys()
#                              }
#               for v in traj.keys() if v is not "t"
#               }
#
#     del tosave["Culture.group_membership_network"]
#     del tosave["Culture.acquaintance_network"]
#     tosave["t"] = traj["t"]
#
#     print("Saving traj.pickle.")
#     dump(tosave, f)
#     # close file
#     f.close()
#     print("Done saving traj.pickle.")
#     # save networks
#     os.mkdir(my_path + "/networks")
#     print(f"Directory networks created @ {my_path}")
#     network_list = [culture.acquaintance_network, culture.group_membership_network, inter_group_network]
#     network_names = ["culture.acquaintance_network", "culture.group_membership_network", "inter_group_network"]
#     print("Saving networks.")
#     for counter, n in enumerate(network_list):
#         f = open(my_path +f"/networks/{network_names[counter]}.pickle", "wb")
#         save_nx = nx.relabel_nodes(n, lambda x: str(x))
#         dump(save_nx, f)
#     print("Done saving networks.")
#
#     # text file
#     print("Saving readme.txt.")
#     with open(my_path +"/" +'readme.txt', 'w') as f:
#         f.write('Groups do not change their attitude')
#     print("Done saving readme.txt.")
#
# mc_path = "/p/projects/copan/maxbecht/results/mc"
# # Path
# my_mc_path = os.path.join(mc_path, parent_directory_name)
#
# if mc_save == "y":
#     # Create the directory
#     if not os.path.exists(my_mc_path):
#         os.mkdir(my_mc_path)
#         print(f"Directory {parent_directory_name} created @ {my_mc_path}")
#     run_no = []
#
#     for i in range(name_start, name_end):
#         run_no.append(str(i))
#     # if args.runset_no:
#     #     run_set_no = args.runset_no
#     # else:
#     #     run_set_no = directory
#     run_set_no_path = os.path.join(my_mc_path, run_set_no)
#     if not os.path.exists(run_set_no_path):
#         os.mkdir(run_set_no_path)
#         print(f"Directory {run_set_no} created @ {run_set_no_path}")
#
#     config_path = f"{run_set_no_path}/configuration.json"
#     if not os.path.exists(config_path):
#         print("Saving configuration.json.")
#         f = open(config_path, "w+")
#         json.dump(configuration, f, indent=4)
#         print("Done saving configuration.json.")
#
#     # save networks
#     network_path = f"{run_set_no_path}/networks"
#     network_list = [culture.acquaintance_network, culture.group_membership_network, inter_group_network]
#     network_names = ["culture.acquaintance_network", "culture.group_membership_network", "inter_group_network"]
#     if not os.path.exists(network_path):
#         os.mkdir(network_path)
#         print("Saving networks.")
#         for counter, n in enumerate(network_list):
#             f = open(network_path +"/"+f"{network_names[counter]}.pickle", "wb")
#             save_nx = nx.relabel_nodes(n, lambda x: str(x))
#             dump(save_nx, f)
#         print("Done saving networks.")
#
#     # saving traj
#     # create a binary pickle file
#     for n in run_no:
#         run_no_path = os.path.join(run_set_no_path, n)
#         output_name = run_no_path + ".pickle"
#         if not os.path.exists(output_name):
#             f = open(output_name, "wb")
#             tosave = {
#                 v.owning_class.__name__ + "."
#                 + v.codename: {str(e): traj[v][e]
#                                for e in traj[v].keys()
#                                }
#                 for v in traj.keys() if v is not "t"
#             }
#             del tosave["Culture.group_membership_network"]
#             del tosave["Culture.acquaintance_network"]
#             tosave["t"] = traj["t"]
#             t = tosave["t"]
#             print("Saving output.")
#             dump(tosave, f)
#             print("Done saving output.")
#             break
