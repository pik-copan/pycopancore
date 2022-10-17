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

# to be saved?
save = "n" #"y" or "n"


#---paths and dirs---

# data from which date?
date = "2022_10_16"
# data from which set?
runsets = ["2"]# ["0", "1"]
traj_paths = []
for r in runsets:
    traj_paths.append(f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\mc\\{date}\\{r}\\")
configuration_path = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\mc" \
                     f"\\{date}\\{runsets[0]}\\configuration.json" # must be same configs, no sense else to compare

print(traj_paths)
Ns = []
# run counter
for p in traj_paths:
    Ns.append(len(glob.glob1(p,"*.pickle")))
# N = 5 # run numbers
N = 0
for n in Ns:
    N += n

if save == "y":
    # will save plots with the SAME date as the data was produced as to prevent confusion
    save_dir = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\plots\\mc\\{date}"
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
        print(f"Directory {date} created @ {save_dir}")
    current_time = datetime.datetime.now()
    current = [current_time.month, current_time.day, current_time.hour, current_time.minute, current_time.second]
    time_string = f"{current_time.year}"
    for i in current:
        if i < 10:
            time_string += f"_0{i}"
        else:
            time_string += f"_{i}"
    # text file
    with open(save_dir +"\\" +'readme.txt', 'w') as f:
        f.write(f'Data from {date} and runsets no. {runsets} used.')
    save_path = os.path.join(save_dir, time_string)
    os.mkdir(save_path)
    print(f"Directory {time_string} created @ {save_path}")

#---load data---
configuration = json.load(open(configuration_path))
trajs = []
for count, p in enumerate(traj_paths):
    for i in range(Ns[count]):
        print(f"Loading {i}.pickle from {p}...")
        trajs.append(pickle.load(open(p+str(i)+".pickle","rb")))


t, cells, individuals, groups = ([] for i in range(4))
for traj in trajs:
    t.append(np.array(traj["t"]))
    cells.append(list(traj["Cell.stock"].keys()))
    individuals.append(list(traj["Individual.behaviour"].keys()))
    groups.append(list(traj["Group.group_opinion"].keys()))

#---get things from congfig---
nindividuals = configuration["nindividuals"]
ng_total = configuration["ng_total"]

print("Done loading things!")
########################################################################################################################

individuals_behaviours, groups_opinions, total_stock, nbehav1, nbehav0 = ([] for i in range(5))
for count, traj in enumerate(trajs):
    individuals_behaviours.append(np.array([traj["Individual.behaviour"][ind]
                                   for ind in individuals[count]]))
    groups_opinions.append(np.array([traj["Group.group_opinion"][g]
                                     for g in groups[count]]))
    stock = traj["Cell.stock"]
    total_stock.append(np.sum([stock[c] for c in cells[count]], axis=0))
    nbehav1.append(np.sum(individuals_behaviours[count], axis=0))
    nbehav0.append(nindividuals - nbehav1[count])

frac1 = np.divide(nbehav1, nindividuals)

values = range(N)
jet = cm = plt.get_cmap('jet')
cNorm  = colors.Normalize(vmin=0, vmax=values[-1])
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
fig = plt.figure()
for count in range(N):
    colorVal = scalarMap.to_rgba(values[count])
    plt.plot(t[count], nbehav1[count], color=colorVal,)# label=f"run {count}")
# plt.legend()
plt.title("$n=25, N_{inds}=400, N_{groups}=2, p=0.05, \Delta T=1$")
plt.xlabel("$t$")
plt.ylabel("$N_s$")
plt.show()
plt.close(fig)

fig = plt.figure()
for count in range(N):
    colorVal = scalarMap.to_rgba(values[count])
    plt.plot(t[count], frac1[count], color=colorVal,)# label=f"run {count}")
# plt.legend()
plt.title("$n=25, N_{inds}=400, N_{groups}=2,p=0.05, \Delta T=1$")
plt.xlabel("$t$")
plt.ylabel("$n_s$")
plt.show()
plt.close(fig)

fig = plt.figure()
for g in range(ng_total):
    for count in range(N):
        colorVal = scalarMap.to_rgba(values[count])
        plt.plot(t[count], groups_opinions[count][g], color=colorVal,)# label=f"run {count}")
# plt.legend()
plt.title("$n=25, N_{inds}=400, N_{groups}=2,p=0.05, \Delta T=1$")
plt.xlabel("$t$")
plt.ylabel("$N_g$")
plt.show()
plt.close(fig)

fig = plt.figure()
for count in range(N):
    colorVal = scalarMap.to_rgba(values[count])
    plt.plot(t[count], total_stock[count], color=colorVal)# , label=f"run {count}")
# plt.legend()
plt.title("$n=25, N_{inds}=400, N_{groups}=2,p=0.05, \Delta T=1$")
plt.xlabel("$t$")
plt.ylabel("$s$")
plt.show()
plt.close(fig)


# calculate means and std
from plot_maxploit_functions import correct_timeline
t_mean = np.arange(0, 50, 1)
corrected_nbehav1 = correct_timeline(nbehav1, t, "2d", t_mean)
corrected_total_stock = correct_timeline(total_stock, t, "2d", t_mean)
mean_nbehav1 = np.mean(corrected_nbehav1, axis=0)
mean_total_stock = np.mean(corrected_total_stock, axis=0)
std_nbehav1 = np.std(corrected_nbehav1, axis=0)
std_total_stock = np.std(corrected_total_stock, axis=0)

fig = plt.figure()
plt.plot(t_mean, mean_nbehav1, color="navy", label="mean behaviour")
plt.plot(t_mean, mean_total_stock, color="crimson", label="mean stock")
plt.fill_between(t_mean, mean_nbehav1-std_nbehav1, mean_nbehav1+std_nbehav1,
                 facecolor="royalblue", edgecolor="navy", alpha=0.25, label="std behaviour")
plt.fill_between(t_mean, mean_total_stock-std_total_stock, mean_total_stock+std_total_stock,
                 facecolor="lightcoral", edgecolor="crimson", alpha=0.25, label="std stock")
plt.legend()
plt.xlabel("$t$")
# plt.ylabel("Means")
plt.show()
plt.close(fig)