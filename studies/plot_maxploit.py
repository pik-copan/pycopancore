import pickle
import json
import os
import datetime as dt
import networkx as nx
from matplotlib import pyplot as plt
import numpy as np
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import plotly.offline as py
# from plot_maxploit_functions import plot_trajectory

#---paths and dirs---

# data from which date?
date = "2022_10_10"
# data from which run?
run = "Run_2022_10_10_17_54_57"

traj_path = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\maxploit\\{date}\\{run}\\traj.pickle"
network_path = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\maxploit\\{date}\\{run}\\networks"
configuration_path = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\maxploit\\{date}\\{run}\\configuration.json"
networks = ["culture.acquaintance_network", "culture.group_membership_network"]

# will save plots with the SAME date as the data was produced as to prevent confusion
date_dir = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\plots\\maxploit\\{date}"
if not os.path.exists(date_dir):
    os.mkdir(date_dir)
    print(f"Directory {date} created @ {date_dir}")

import datetime
current_time = datetime.datetime.now()
current = [current_time.month, current_time.day, current_time.hour, current_time.minute, current_time.second]
time_string = f"{current_time.year}"
for i in current:
    if i < 10:
        time_string += f"_0{i}"
    else:
        time_string += f"_{i}"

save_directory = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\plots\\maxploit\\{date}\\{run}"
if not os.path.exists(save_directory):
    os.mkdir(save_directory)
    print(f"Directory {run} created @ {save_directory}")

# text file
with open(save_directory +"\\" +'readme.txt', 'w') as f:
    f.write(f'Data from {run} used.')

save_path = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\plots\\maxploit\\{date}\\{run}\\{time_string}"
os.mkdir(save_path)
print(f"Directory {time_string} created @ {save_path}")

#---load data---
configuration = json.load(open(configuration_path))
traj = pickle.load(open(traj_path,"rb"))
t = np.array(traj['t'])
acquaintance_network = pickle.load(open(network_path+"\\"+networks[0]+".pickle","rb"))
group_membership_network = pickle.load(open(network_path+"\\"+networks[1]+".pickle","rb"))

#---assign entities---
cells = list(traj["Cell.stock"].keys())
individuals = list(traj["Individual.behaviour"].keys())
groups = list(traj["Group.group_attitude"].keys())

#---get things from congfig---
nindividuals = configuration["nindividuals"]
ng_total = configuration["ng_total"]

# for ind in individuals:
#     print([traj[M.Individual.behaviour][ind]])
individuals_behaviours = np.array([traj["Individual.behaviour"][ind]
                                   for ind in individuals])
individuals_behaviours_dict=traj["Individual.behaviour"]
groups_attitudes = np.array([traj["Group.group_attitude"][g]
                           for g in groups])
groups_attitudes_dict = traj["Group.group_attitude"]
mean_groups_behaviours = traj["Group.mean_group_behaviour"]
# groups_attitudes_fixed = traj[M.Group.group_attitude]

# print(mean_groups_behaviours)
# plt.plot(t, mean_groups_behaviours[groups[0]])
# plt.show()

# for ind in individuals:
#     print([traj[M.Individual.attitude][ind]])
# individuals_attitudes = np.array([traj[M.Individual.attitude][ind]
#                                  for ind in individuals])

nbehav1_list = np.sum(individuals_behaviours, axis=0) / nindividuals
nbehav0_list = 1 - nbehav1_list

# nattitude1_list = np.sum(individuals_attitudes, axis=0) / nindividuals
# nattitude0_list = 1 - nattitude1_list

nbehav1 = np.sum(individuals_behaviours, axis=0)
nbehav0 = nindividuals - nbehav1



#trajectory plot
# fig = plot_trajectory(nbehav0, nbehav1, t)
# plt.show()

# group plot
ngroup_1 = np.sum(groups_attitudes, axis=0, dtype=float)

fig = plt.figure()
plt.plot(t, nbehav1, 'navy', label="N Inds. Sustainable")
# plt.plot(t, ngroup_1, 'crimson', label="N Groups Sustainable")
plt.legend()
plt.xlabel("t")
plt.ylabel("N")
my_file = f'Sustainability_over_time.png'
plt.show()
# fig.savefig(save_path+"\\"+my_file)
plt.close(fig)

"""
fig = plt.figure()
plt.xcorr(nbehav1, ngroup_1)
plt.show()
"""

stock = traj["Cell.stock"]
total_stock = np.sum([stock[c] for c in cells], axis=0)
fig = plt.figure()
plt.plot(t, total_stock, 'g', label="stock")
plt.legend()
plt.show()

fig = plt.figure()
plt.plot(t, stock["Cell[UID=2]"], label="stock Cell 0")
plt.plot(t, individuals_behaviours[0], label="behaviour Individual 0")
plt.legend()
plt.show()

# fig = plt.figure()
# plot_trajectory(nbehav1, total_stock, t)
# plt.show()

# stock_cell_0 = stock[cells[0]]
# behaviour_ind_0 = individuals_behaviours[individuals[0]] #first unsus ind living in cell 0
# stock_cell_50 = stock[cells[50]]
# behaviour_ind_50 = individuals_behaviours[individuals[50]] #first sus ind living in cell 50
#
# plt.plot(t, stock_cell_0, 'darkgreen', label="stock cell 0")
# plt.plot(t, behaviour_ind_0, 'orange', label="corresponding behaviour ind 0 (starts unsustainable)")
# plt.legend()
# plt.show()
#
# plt.plot(t, stock_cell_50, 'darkgreen', label="stock cell 50")
# plt.plot(t, behaviour_ind_50, 'orange', label="corresponding behaviour ind 50 (starts sustainable)")
# plt.legend()
# plt.show()

# print(groups_attitudes)
# print(groups_attitudes[groups[0]])
# print(groups_attitudes[groups[0]][0])
# print(groups_attitudes_fixed)
# print(groups_attitudes_fixed[groups[0]])
# print(groups_attitudes_fixed[groups[0]][0])
# print(individuals_behaviours_dict)
# print(individuals_behaviours_dict[individuals[0]])
# print(individuals_behaviours_dict[individuals[0]][0])

#
# from plot_multilayer import LayeredNetworkGraph
#
# #get a preliminary intergroup network for plotting multilayer
# inter_group_network = nx.Graph()
# for g in groups:
#     inter_group_network.add_node(g)
# for index, g in enumerate(groups):
#     for j in groups[:index]:
#         inter_group_network.add_edge(g, j)
#
# v_array1 = []
# v_array2 = []
# for i in individuals:
#     v_array1.append(individuals_behaviours_dict[i][0])
# for index, g in enumerate(groups):
#     v_array2.append(groups_attitudes_dict[g][0])
# v_array = [v_array1, v_array2]
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.set_proj_type('ortho')
# LayeredNetworkGraph([acquaintance_network, inter_group_network], [group_membership_network], v_array, ax=ax)
# plt.show()
#
# multilayer = LayeredNetworkGraph([acquaintance_network, inter_group_network], [group_membership_network],
#                     v_array, ax=ax, layout=nx.spring_layout)
# node_positions = multilayer.save_node_positions() # to get node positions
#
# for t_index in range(len(t)):
#     fig = plt.figure()
#     v_array1 = []
#     v_array2 = []
#     for i in individuals:
#         v_array1.append(individuals_behaviours_dict[i][t_index])
#     for index, g in enumerate(groups):
#         v_array2.append(groups_attitudes_dict[g][t_index])
#     v_array = [v_array1, v_array2]
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')
#     ax.view_init(40+0.075*t_index, 40-0.075*t_index)
#     LayeredNetworkGraph([acquaintance_network, inter_group_network], [group_membership_network],
#                         v_array, ax=ax, layout=nx.spring_layout, node_positions=node_positions)
#     my_file = f'layered_network_{t_index}.png'
#     fig.savefig(os.path.join(save_path, my_file))
#     plt.close(fig)
#
#
# for i in range(len(t)):
#     color_map = []
#     unsust_nodes = {n for n, d in GM.nodes(data=True) if (d["type"] == "Group" and groups_attitudes[n][i])
#                     or (d["type"] == "Individual" and individuals_behaviours_dict[n][i])}
#     for node in list(GM.nodes):
#         if node in unsust_nodes:
#             color_map.append("red")
#         else:
#             color_map.append("blue")
#     fig = plt.figure()
#     nx.draw(GM, node_color=color_map, with_labels=False,
#             pos=nx.bipartite_layout(GM, bottom_nodes, align="horizontal", aspect_ratio=4 / 1))
#     my_file = f'network_{i}.png'
#     fig.savefig(os.path.join(my_path, my_file))
#     plt.close(fig)



# color_map = []
# for node in list(GM.nodes):
#     color_map.append(GM.nodes[node]["color"])
# top_nodes = {n for n, d in GM.nodes(data=True) if d["type"] == "Group"}
# bottom_nodes = set(GM) - top_nodes
# nx.draw(GM, node_color=color_map, with_labels=False,
#         pos=nx.bipartite_layout(GM, bottom_nodes, align="horizontal", aspect_ratio=4 / 1))
# plt.show()#

# everything below is just plotting commands for plotly

data_behav0 = go.Scatter(
    x=t,
    y=nbehav0_list,
    mode="lines",
    name="relative amount behaviour 0 (nonsus)",
    line=dict(
        color="lightblue",
        width=2
    )
)
data_behav1 = go.Scatter(
    x=t,
    y=nbehav1_list,
    mode="lines",
    name="relative amount behaviour 1 (sus)",
    line=dict(
        color="orange",
        width=2
    )
)

layout = dict(title='Maxploit Model',
              xaxis=dict(title='time'),
              yaxis=dict(title='relative behaviour amounts'),
              )

fig = dict(data=[data_behav0, data_behav1], layout=layout)
# py.plot(fig, filename="maxlpoit_model.html")


plt.close('all')

# TODO: grit entfernen

