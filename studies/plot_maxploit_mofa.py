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

LOAD_PATH = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\results\\pymofa_test26\\raw\\0-0-1-2-1-2-0o5-0o5-0o5-400-0-400-1-400-10-5-5-1-0o05_s0.pkl"
traj = pickle.load(open(LOAD_PATH, "rb"))

#print("Done loading things!")


########################################################################################################################
# Total_stock, Nbehav1, Groups_opinions = ([] for i in range(3))
# for count1, i in enumerate(Traj):
#     individuals_behaviours, total_stock, nbehav1, groups_opinions = ([] for i in range(4))
#     for count2, k in enumerate(i):
#         individuals_behaviours.append(np.array([k["Individual.behaviour"][ind]
#                                        for ind in Individuals[count1][count2]]))
#         groups_opinions.append(np.array(np.array([k["Group.group_opinion"][g]
#                                          for g in Groups[count1][count2]])))
#         stock = k["Cell.stock"]
#         total_stock.append(np.divide(np.sum([stock[c] for c in Cells[count1][count2]], axis=0), nindividuals))
#         nbehav1.append(np.divide(np.sum(individuals_behaviours[count2], axis=0), nindividuals))
#     Groups_opinions.append(groups_opinions)
#     Total_stock.append(total_stock)
#     Nbehav1.append(nbehav1)
#
#
#
# values = range(N)
# jet = cm = plt.get_cmap('jet')
# cNorm  = colors.Normalize(vmin=0, vmax=values[-1])
# scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
#
#
# fig = plt.figure()
# for count1, n in enumerate(Ns):
#     # colorVal = scalarMap.to_rgba(values[count1])
#     for count2 in range(n):
#         colorVal = scalarMap.to_rgba(values[count2])
#         plt.plot(T[count1][count2], Nbehav1[count1][count2], color=colorVal)# label=f"run {count}")
# # plt.legend()
# plt.title("")
# plt.xlabel("$t$")
# plt.ylabel("$n_s$")
# plt.show()
# plt.close(fig)
#
# fig = plt.figure()
# for count1, n in enumerate(Ns):
#     # colorVal = scalarMap.to_rgba(values[count1])
#     for count2 in range(n):
#         colorVal = scalarMap.to_rgba(values[count2])
#         plt.plot(T[count1][count2], Total_stock[count1][count2], color=colorVal)# , label=f"run {count}")
# # plt.legend()
# plt.title("")
# plt.xlabel("$t$")
# plt.ylabel("$s$")
# plt.show()
# plt.close(fig)
#
# Mean_nbehav1, Std_nbehav1, Mean_total_stock, Std_total_stock = ([] for i in range(4))
# t_mean = np.arange(0, timeinterval, timestep)
# for count, i in enumerate(Traj):
#     corrected_nbehav1 = correct_timeline(Nbehav1[count], T[count], "2d", t_mean)
#     mean_nbehav1 = np.mean(corrected_nbehav1, axis=0)
#     std_nbehav1 = np.std(corrected_nbehav1, axis=0)
#     Mean_nbehav1.append(mean_nbehav1)
#     Std_nbehav1.append(std_nbehav1)
#     corrected_total_stock = correct_timeline(Total_stock[count], T[count], "2d", t_mean)
#     Mean_total_stock.append(np.mean(corrected_total_stock, axis=0))
#     Std_total_stock.append(np.std(corrected_total_stock, axis=0))
#
# values = range(len(Ns))
# jet = cm = plt.get_cmap('jet')
# cNorm  = colors.Normalize(vmin=0, vmax=values[-1])
# scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
#
# fig = plt.figure()
# for count in range(len(Ns)):
#     colorVal = scalarMap.to_rgba(values[count])
#     plt.plot(t_mean, Mean_total_stock[count], color=colorVal) #, label=rf"$p = {ps[count]}$")
#     plt.fill_between(t_mean, Mean_total_stock[count]-Std_total_stock[count], Mean_total_stock[count]+Std_total_stock[count],
#                          facecolor=colorVal, edgecolor=colorVal, alpha=0.1)
# # plt.legend()
# plt.xlabel("$t$")
# plt.ylabel(r"$ \langle s \rangle$")
# plt.show()
# plt.close(fig)
#
# fig = plt.figure()
# for count in range(len(Ns)):
#     colorVal = scalarMap.to_rgba(values[count])
#     plt.plot(t_mean, Mean_nbehav1[count], color=colorVal)#, label=rf"$p = {ps[count]}$")
#     plt.fill_between(t_mean, Mean_nbehav1[count]-Std_nbehav1[count], Mean_nbehav1[count]+Std_nbehav1[count],
#                          facecolor=colorVal, edgecolor=colorVal, alpha=0.1)
# # plt.legend()
# plt.xlabel("$t$")
# plt.ylabel(r"$ \langle n_s \rangle$")
# plt.ylim(0, 1)
# plt.show()
# plt.close(fig)
#


# plot runs plus mean
# fig = plt.figure()
# for count1, n in enumerate(Ns):
#     colorVal = scalarMap.to_rgba(values[count1])
#     for count2 in range(n):
#         plt.plot(T[count1][count2], Nbehav1[count1][count2], color=colorVal,)
# for count in range(len(Ns)):
#     plt.plot(t_mean, Mean_nbehav1[count], color="black", label=r"$\langle s \rangle$")
#     plt.fill_between(t_mean, Mean_nbehav1[count]-Std_nbehav1[count], Mean_nbehav1[count]+Std_nbehav1[count],
#                           facecolor="black", edgecolor="black", alpha=0.1)
# plt.xlabel("$t$")
# plt.ylabel(r"$n$")
# plt.show()
# plt.close(fig)
#
# fig = plt.figure()
# for count1, n in enumerate(Ns):
#     colorVal = scalarMap.to_rgba(values[count1])
#     for count2 in range(n):
#         plt.plot(T[count1][count2], Total_stock[count1][count2], color=colorVal,)
# for count in range(len(Ns)):
#     plt.plot(t_mean, Mean_total_stock[count], color="black", label=r"$\langle s \rangle$")
#     plt.fill_between(t_mean, Mean_total_stock[count]-Std_total_stock[count], Mean_total_stock[count]+Std_total_stock[count],
#                           facecolor="black", edgecolor="black", alpha=0.1)
# plt.xlabel("$t$")
# plt.ylabel(r"$s$")
# plt.show()
# plt.close(fig)


# plot against DeltaT


# from pickle import dump
# f = open("Mean_total_stock.pickle", "wb")
# dump(Mean_total_stock, f)
# f = open("Mean_nbehav1.pickle", "wb")
# dump(Mean_nbehav1, f)
# f = open("Std_total_stock.pickle", "wb")
# dump(Std_total_stock, f)
# f = open("Std_nbehav1.pickle", "wb")
# dump(Std_nbehav1, f)
