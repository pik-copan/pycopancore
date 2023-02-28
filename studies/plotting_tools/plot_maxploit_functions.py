import numpy as np
import matplotlib.pyplot as plt
import glob
import matplotlib.colors as colors
import matplotlib.cm as cmx
import os
import glob
import pickle

def plot_trajectory(list_1, list_2, t):
    for index in range(len(t)):
        plt.scatter(list_1[index], list_2[index], c="navy", )
        plt.xlabel(str(list_1))
        plt.xlabel(str(list_2))
        plt.title(f"Trajectory {str(list_1)} vs. {str(list_2)}")

def get_mofa_id(parameter_combinations):
    """
    Recreates the fnames used by pymofa without the _s1 indicating number of runs.
    With this all trajectories from a single run can then be plotted.

    parameter_combinations: single tuple or list of tuples as created by it.product(param1, param2)

    returns: list of ids
    """

    ids = []

    if isinstance(parameter_combinations, list):
        for comb in parameter_combinations:
            res = str(comb)  # convert to sting
            res = res[1:-1]  # delete brackets
            res = res.replace(", ", "-")  # remove ", " with "-"
            res = res.replace(",", "-")  # remove "," with "-"
            res = res.replace(".", "o")  # replace dots with an "o"
            res = res.replace("'", "")  # remove 's from values of string variables
            # Remove all the other left over mean
            # charakters that might fuck with you
            # bash scripting or wild card usage.
            for mean_character in "[]()^ #%&!@:+={}'~":
                res = res.replace(mean_character, "")
            ids.append(res)

    elif isinstance(parameter_combinations, tuple):
        id = str(parameter_combinations)  # convert to sting
        id = id[1:-1]  # delete brackets
        id = id.replace(", ", "-")  # remove ", " with "-"
        id = id.replace(",", "-")  # remove "," with "-"
        id = id.replace(".", "o")  # replace dots with an "o"
        id = id.replace("'", "")  # remove 's from values of string variables
        # Remove all the other left over mean
        # charakters that might fuck with you
        # bash scripting or wild card usage.
        for mean_character in "[]()^ #%&!@:+={}'~":
            id = id.replace(mean_character, "")
        ids.append(id)

    else:
        pass

    return ids


def correct_timeline(lists, t_lists, shape, t_new):
    """Correct the timeline of one list to have same time points.
    Careful, depending on the resolution of t_new some data might be lost!

    lists: list or list of list containing data
    t_lists: list or list of list containing time points and are of different length
    shape: "1d" if single list, "2d" if list of lists
    t_new: time shape lists should be cast into
    """
    print(f"Correcting time line of lists...")

    if shape == "2d":
        new_list = []
        n_lists = len(lists)
        for i in range(n_lists):
            new_sub_list = []
            for index, t in enumerate(t_new[1:]):
                list_index = 0
                for count, k in enumerate(t_lists[i]):
                    if k >= t_new[index - 1] and k < t_new[index]:
                        list_index = count
                new_sub_list.append(lists[i][list_index])
            new_sub_list.append(lists[i][len(lists[i])-1])
            new_list.append(new_sub_list)

    else: # 1d
        new_list = []
        list_index = 0
        for index, t in enumerate(t_new[1:]):
            for count, k in enumerate(t_lists):
                if k >= t_new[index-1] and k < t_new[index]:
                    list_index = count
            new_list.append(lists[list_index])
        new_list.append(lists[len(lists)-1])

    print(f"Done correcting timelines!")
    return new_list


def plot_single_trajs(variables, parameter_combinations, timepoints, RAW_PATH, SAVE_PATH):
    ids = get_mofa_id(parameter_combinations)
    for i in ids:
        if not os.path.exists(SAVE_PATH + "\\" + i):
            os.mkdir(SAVE_PATH + "\\" + i)
    fnames = np.sort(glob.glob(RAW_PATH + "\\*"))
    for i in ids:
        n = 0
        for f in fnames:
            if i in f:
                raw = pickle.load(open(f, "rb"))
                fig, ax = plt.subplots()
                for name in variables:
                    ax.plot(timepoints, raw[name], label=name)
                ax.set_xlabel("t")
                ax.set_ylabel("Value")
                ax.set_title(i + "_" + str(n))
                ax.legend(loc="best")
                save_path = SAVE_PATH + "\\" + i
                # plt.show()
                plt.savefig(save_path + "\\" + str(i) + f"_{n}" + ".png")
                plt.close()
                n += 1


def plot_all_trajs_in_one(variables, parameter_combinations, timepoints, RAW_PATH, SAVE_PATH):
    ids = get_mofa_id(parameter_combinations)
    for i in ids:
        if not os.path.exists(SAVE_PATH + "\\" + i):
            os.mkdir(SAVE_PATH + "\\" + i)
    fnames = np.sort(glob.glob(RAW_PATH + "\\*"))
    for i in ids:
        # get number of trajectories to plot cmap well
        n = 0
        for f in fnames:
            if i in f:
                n += 1
        cvalues = range(n)
        jet = cm = plt.get_cmap('jet')
        cNorm = colors.Normalize(vmin=0, vmax=cvalues[-1])
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
        fig, ax = plt.subplots(len(variables))
        count = 0
        for f in fnames:
            if i in f:
                raw = pickle.load(open(f, "rb"))
                colorVal = scalarMap.to_rgba(cvalues[count])
                for index, name in enumerate(variables):
                    ax[index].plot(timepoints, raw[name], color=colorVal)
                    ax[index].set_xlabel("t")
                    ax[index].set_ylabel("Value")
                    ax[index].set_title(name)
                    # ax[index].legend(loc="best")
                count += 1
        fig.set_figheight(16)
        plt.suptitle(i)
        save_path = SAVE_PATH + "\\" + i
        fig.tight_layout()
        # plt.show()
        plt.savefig(save_path + "\\" + f"00allruns" + ".png")
        plt.close()


def plot_mean_and_std_traj(data, parameter_combinations, parameter_name_list, variables, timepoints, SAVE_FOLDER):
    for c in parameter_combinations:
        fig, ax = plt.subplots(len(variables))
        for index, name in enumerate(variables):
            y = data['mean'].unstack('observables').xs(key=c, level=parameter_name_list)[name]
            y_e = data['std'].unstack('observables').xs(key=c, level=parameter_name_list)[name]
            ax[index].set_title(name)
            ax[index].set_xlabel("t")
            ax[index].set_ylabel("Value")
            ax[index].plot(timepoints, y, c="blue")
            ax[index].plot(timepoints, y_e, c="red")
            ax[index].fill_between(timepoints, list(np.subtract(np.array(y), np.array(y_e))),
                                   list(np.add(np.array(y), np.array(y_e))), alpha=0.1)
        plt.suptitle(str(c))
        fig.tight_layout()
        fig.set_figheight(16)
        plt.tight_layout()
        plt.savefig(SAVE_FOLDER + "\\" + f"_{c}" + ".png")
        plt.close()


def phase_transition(data, parameter_name_list, parameter_dict, parameter_list, param_1, timestep, value, SAVE_PATH):
    """Create phase transition plots for 1 parameter.
    data: the data
    parameter_name_list: list of parameter names
    parameter_dict: dictionary of parameters and their valuess
    param_combinations: all possible combinations
    param_1: name (str) of parameter of interest
    timestep: evaluation timestep
    value: what to plot, can be "cells" or "inds" """

    print("Start creating phase transition plot....")

    parameter_values = parameter_dict[param_1]

    A = []

    for index, key in enumerate(parameter_name_list):
        if key == param_1:
            param_loc = index

    for count in range(len(parameter_values)):
        new_key = []
        for index, i in enumerate(parameter_list):
            if index == param_loc:
                new_key.append(parameter_values[count])
            else:
                new_key.append(i[0])
        A.append(new_key)

    mean = np.zeros(len(parameter_values))
    sem = np.zeros(len(parameter_values))

    if value == "cells":
        for i in range(len(mean)):
            mean[i] = float(data['mean'].unstack('observables').xs(key=tuple(A[i]),
                                                                   level=parameter_name_list).loc[
                                timestep, "Cell.stock"])
            sem[i] = float(data['std'].unstack('observables').xs(key=tuple(A[i]),
                                                                 level=parameter_name_list).loc[
                               timestep, "Cell.stock"])

    elif value == "inds":
        for i in range(len(mean)):
            mean[i] = float(data['mean'].unstack('observables').xs(key=tuple(A[i]),
                                                                   level=parameter_name_list).loc[
                                timestep, "Individual.behaviour"])
            sem[i] = float(data['std'].unstack('observables').xs(key=tuple(A[i]),
                                                                 level=parameter_name_list).loc[
                               timestep, "Individual.behaviour"])

    plt.figure()

    plt.scatter(parameter_values, mean)
    plt.fill_between(parameter_values, list(np.subtract(np.array(mean), np.array(sem))),
                     list(np.add(np.array(mean), np.array(sem))), alpha=0.1)
    plt.savefig(SAVE_PATH + "\\" + f"{param_1}_{value}_" + ".png")

def pixel_plot(data, config, parameter_name_list, parameter_list, PARAM_COMBS, timestep, SAVE_PATH):
    import itertools as it
    # create key sets for single parameter sweeps for plotting
    # change the ones that were sweeped and fix the other ones

    # get names of all alternating params
    alternating_params = []
    for key, value in config.items():
        if len(value) > 1 and isinstance(value, list):
            alternating_params.append(key)

    param_locs = {}
    for index, key in enumerate(parameter_name_list):
        if key in alternating_params:
            param_locs[key] = index

    pairs = list(it.combinations(alternating_params, 2))

    for p in pairs:
        param1 = p[0]
        param2 = p[1]
        param_loc1 = param_locs[param1]
        param_loc2 = param_locs[param2]

        A = np.zeros((len(parameter_list[param_loc1]), len(parameter_list[param_loc2])), dtype=list)

        param_list1 = parameter_list[param_loc1]
        param_list2 = parameter_list[param_loc2]

        # sort lists in case
        if param_list1.sort() is not None:
            param_list1 = parameter_list[param_loc1].sort()
        if param_list2.sort() is not None:
            param_list2 = parameter_list[param_loc2].sort()

        for c in PARAM_COMBS:
            value = list(c)
            for index_i, i in enumerate(param_list1):
                for index_j, j in enumerate(param_list2):
                    new_key = []
                    for index, x in enumerate(value):
                        if index == param_loc1:
                            new_key.append(i)
                        elif index == param_loc2:
                            new_key.append(j)
                        else:
                            new_key.append(x)
                    A[index_i][index_j] = new_key

        # create a data matrix
        cells_matrix = np.zeros((len(parameter_list[param_loc1]), len(parameter_list[param_loc2])), dtype=float)
        inds_matrix = np.zeros((len(parameter_list[param_loc1]), len(parameter_list[param_loc2])), dtype=float)
        sem_cells_matrix = np.zeros((len(parameter_list[param_loc1]), len(parameter_list[param_loc2])), dtype=float)
        sem_inds_matrix = np.zeros((len(parameter_list[param_loc1]), len(parameter_list[param_loc2])), dtype=float)
        for i in range(np.shape(cells_matrix)[0]):
            for j in range(np.shape(cells_matrix)[1]):
                cells_matrix[i][j] = float(data['mean'].unstack('observables').xs(key=tuple(A[i][j]),
                                                                                  level=parameter_name_list).loc[
                                               timestep, "Cell.stock"])
                sem_cells_matrix[i][j] = float(data['std'].unstack('observables').xs(key=tuple(A[i][j]),
                                                                                     level=parameter_name_list).loc[
                                                   timestep, "Cell.stock"])
                inds_matrix[i][j] = float(data['mean'].unstack('observables').xs(key=tuple(A[i][j]),
                                                                                 level=parameter_name_list).loc[
                                              timestep, "Individual.behaviour"])
                sem_inds_matrix[i][j] = float(data['std'].unstack('observables').xs(key=tuple(A[i][j]),
                                                                                    level=parameter_name_list).loc[
                                                  timestep, "Individual.behaviour"])
        matrices = [cells_matrix, sem_cells_matrix, inds_matrix, sem_inds_matrix]
        m_names = ["Cells", "Std_Cells", "Inds", "Std_Inds"]
        # ----- PIXEL PLOT -----
        # create a 2d data set

        print("Plotting figures...")
        for index, m in enumerate(matrices):
            pixel_plot, ax = plt.subplots()
            plt.suptitle(param1 + " vs. " + param2)
            plt.title(f"{m_names[index]}")
            extent = [min(param_list2), max(param_list2), min(param_list1), max(param_list1)]
            plt.imshow(m, origin="lower")
            plt.colorbar()
            # ax.set_xscale('log', base=2)
            plt.xlabel(param2)
            plt.ylabel(param1)
            xticks = list(np.arange(0, np.shape(m)[1], 1))
            yticks = list(np.arange(0, np.shape(m)[0], 1))
            ax.set_xticks(xticks)
            ax.set_yticks(yticks)
            xtickslabels = param_list2
            ytickslabels = param_list1
            ax.set_xticklabels(xtickslabels)
            ax.set_yticklabels(ytickslabels)
            # plt.xticks(xticks)
            # plt.yticks(yticks)
            # save a plot
            plt.savefig(SAVE_PATH + "\\" + param1 + "_" + param2 + f"_{m_names[index]}" + ".png")
            # show plot
            # plt.show()
            # clear axes
            plt.close()
        print("Done plotting figures!")

