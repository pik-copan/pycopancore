import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import datetime
import glob
from studies.plotting_tools.plot_maxploit_functions import correct_timeline

# to be saved?
save = "n" #"y" or "n"


#---paths and dirs---

# data from which date?
date = "2022_10_20"
# data from which set?
# runsets = [ "62", "63", "64", "70", "72", "73", "65", "77", "76", "71", "66", "67", "68"]
runsets = ["2"]
# ps = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
# Dt = [0.1]
# theta= [ 0.2, 0.3, 0.4, 0.45, 0.49, 0.495, 0.5, 0.505, 0.51, 0.55, 0.6, 0.7, 0.8]
# theta= [ 0.2, 0.3, 0.4, 0.45, 0.49, 0.495, 0.5, 0.51, 0.55, 0.6, 0.7, 0.8]
traj_paths = []
# for general paths
# for r in runsets:
#     traj_paths.append(f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\mc\\{date}\\{r}\\")
# configuration_path = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\mc" \
#                      f"\\{date}\\{runsets[0]}\\configuration.json" # must be same configs, no sense else to compare

# for specified paths
folder_name = "des_inj_norms"
for r in runsets:
    traj_paths.append(f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\mc\\{folder_name}\\{r}\\")
configuration_path = f"C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\mc" \
                     f"\\{folder_name}\\{runsets[0]}\\configuration.json"


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
# configuration = json.load(open(configuration_path))
# Ns= [1, 1, 1] #just first runs
Traj = []
for count, p in enumerate(traj_paths):
    traj = []
    for i in range(Ns[count]):
        print(f"Loading {i}.pickle from {p}...")
        traj.append(pickle.load(open(p+str(i)+".pickle","rb")))
    Traj.append(traj)

T, Cells, Individuals, Groups = ([] for i in range(4))
for i in Traj:
    t, cells, individuals, groups = ([] for i in range(4))
    for k in i:
        t.append(np.array(k["t"]))
        cells.append(list(k["Cell.stock"].keys()))
        individuals.append(list(k["Individual.behaviour"].keys()))
        groups.append(list(k["Group.group_opinion"].keys()))
    T.append(t)
    Cells.append(cells)
    Individuals.append(individuals)
    Groups.append(groups)

#---get things from congfig---
# nindividuals = configuration["nindividuals"]
# ng_total = configuration["ng_total"]

nindividuals = 400
ng_total = 1
timeinterval = 100
timestep = 1

print("Done loading things!")
########################################################################################################################
Total_stock, Nbehav1, Groups_opinions = ([] for i in range(3))
for count1, i in enumerate(Traj):
    individuals_behaviours, total_stock, nbehav1, groups_opinions = ([] for i in range(4))
    for count2, k in enumerate(i):
        individuals_behaviours.append(np.array([k["Individual.behaviour"][ind]
                                       for ind in Individuals[count1][count2]]))
        groups_opinions.append(np.array(np.array([k["Group.group_opinion"][g]
                                         for g in Groups[count1][count2]])))
        stock = k["Cell.stock"]
        total_stock.append(np.divide(np.sum([stock[c] for c in Cells[count1][count2]], axis=0), nindividuals))
        nbehav1.append(np.divide(np.sum(individuals_behaviours[count2], axis=0), nindividuals))
    Groups_opinions.append(groups_opinions)
    Total_stock.append(total_stock)
    Nbehav1.append(nbehav1)



values = range(N)
jet = cm = plt.get_cmap('jet')
cNorm  = colors.Normalize(vmin=0, vmax=values[-1])
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)


fig = plt.figure()
for count1, n in enumerate(Ns):
    # colorVal = scalarMap.to_rgba(values[count1])
    for count2 in range(n):
        colorVal = scalarMap.to_rgba(values[count2])
        plt.plot(T[count1][count2], Nbehav1[count1][count2], color=colorVal)# label=f"run {count}")
# plt.legend()
plt.title("")
plt.xlabel("$t$")
plt.ylabel("$n_s$")
plt.show()
plt.close(fig)

fig = plt.figure()
for count1, n in enumerate(Ns):
    # colorVal = scalarMap.to_rgba(values[count1])
    for count2 in range(n):
        colorVal = scalarMap.to_rgba(values[count2])
        plt.plot(T[count1][count2], Total_stock[count1][count2], color=colorVal)# , label=f"run {count}")
# plt.legend()
plt.title("")
plt.xlabel("$t$")
plt.ylabel("$s$")
plt.show()
plt.close(fig)

Mean_nbehav1, Std_nbehav1, Mean_total_stock, Std_total_stock = ([] for i in range(4))
t_mean = np.arange(0, timeinterval, timestep)
for count, i in enumerate(Traj):
    corrected_nbehav1 = correct_timeline(Nbehav1[count], T[count], "2d", t_mean)
    mean_nbehav1 = np.mean(corrected_nbehav1, axis=0)
    std_nbehav1 = np.std(corrected_nbehav1, axis=0)
    Mean_nbehav1.append(mean_nbehav1)
    Std_nbehav1.append(std_nbehav1)
    corrected_total_stock = correct_timeline(Total_stock[count], T[count], "2d", t_mean)
    Mean_total_stock.append(np.mean(corrected_total_stock, axis=0))
    Std_total_stock.append(np.std(corrected_total_stock, axis=0))

values = range(len(Ns))
jet = cm = plt.get_cmap('jet')
cNorm  = colors.Normalize(vmin=0, vmax=values[-1])
scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)

fig = plt.figure()
for count in range(len(Ns)):
    colorVal = scalarMap.to_rgba(values[count])
    plt.plot(t_mean, Mean_total_stock[count], color=colorVal) #, label=rf"$p = {ps[count]}$")
    plt.fill_between(t_mean, Mean_total_stock[count]-Std_total_stock[count], Mean_total_stock[count]+Std_total_stock[count],
                         facecolor=colorVal, edgecolor=colorVal, alpha=0.1)
# plt.legend()
plt.xlabel("$t$")
plt.ylabel(r"$ \langle s \rangle$")
plt.show()
plt.close(fig)

fig = plt.figure()
for count in range(len(Ns)):
    colorVal = scalarMap.to_rgba(values[count])
    plt.plot(t_mean, Mean_nbehav1[count], color=colorVal)#, label=rf"$p = {ps[count]}$")
    plt.fill_between(t_mean, Mean_nbehav1[count]-Std_nbehav1[count], Mean_nbehav1[count]+Std_nbehav1[count],
                         facecolor=colorVal, edgecolor=colorVal, alpha=0.1)
# plt.legend()
plt.xlabel("$t$")
plt.ylabel(r"$ \langle n_s \rangle$")
plt.ylim(0, 1)
plt.show()
plt.close(fig)



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
