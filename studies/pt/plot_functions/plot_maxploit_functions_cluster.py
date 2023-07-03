import os
import glob
import pickle
import numpy as np
import itertools as it
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
from mpl_toolkits.axes_grid1 import make_axes_locatable
import csv
from statsmodels.tsa.stattools import adfuller
from matplotlib.ticker import FormatStrFormatter


def plot_trajectory(list_1, list_2, t):
    for index in range(len(t)):
        plt.scatter(list_1[index], list_2[index], c="navy", )
        plt.xlabel(str(list_1))
        plt.ylabel(str(list_2))
        plt.title(f"Trajectory {str(list_1)} vs. {str(list_2)}")


def translate_into_thesis_naming(param):
    string = str()
    if param == "k_value":
        string = r"$k$"
    elif param == "descriptive_majority_threshold":
        string = r"$\theta_{DN}$"
    elif param == "injunctive_majority_threshold":
        string = r"$\theta_{IN}$"
    elif param == "weight_descriptive":
        string = r"$w_{DN}$"
    elif param == "weight_injunctive":
        string = r"$w_{IN}$"
    elif param == "weight_harvest":
        string = r"$w_{h}$"
    elif param == "average_waiting_time":
        string = r"$\Delta T_a$"
    elif param == "update_probability":
        string = r"$\Phi_a$"
    elif param == "ng_total":
        string = r"$N_g$"
    elif param == "n_group_memberships":
        string = r"$N_m$"
    elif param == "group_update_probability":
        string = r"$\Phi_g$"
    elif param == "group_meeting_interval":
        string = r"$\Delta T_g$"
    elif param == "p":
        string = r"$\rho$"
    else:
        string = param
        print("Error translating.")
    return string


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
            new_sub_list.append(lists[i][len(lists[i]) - 1])
            new_list.append(new_sub_list)

    else:  # 1d
        new_list = []
        list_index = 0
        for index, t in enumerate(t_new[1:]):
            for count, k in enumerate(t_lists):
                if k >= t_new[index - 1] and k < t_new[index]:
                    list_index = count
            new_list.append(lists[list_index])
        new_list.append(lists[len(lists) - 1])

    print(f"Done correcting timelines!")
    return new_list


def plot_single_trajs(variables, parameter_combinations, timepoints, RAW_PATH, SAVE_PATH, nc, ng):
    ids = get_mofa_id(parameter_combinations)
    for i in ids:
        if not os.path.exists(SAVE_PATH + "/" + i):
            os.mkdir(SAVE_PATH + "/" + i)
    fnames = np.sort(glob.glob(RAW_PATH + "/*"))
    for i in ids:
        n = 0
        for f in fnames:
            if i in f:
                raw = pickle.load(open(f, "rb"))
                fig, ax = plt.subplots()
                for name in variables:
                    if name == "Cell.stock":
                        ax.plot(timepoints, raw[name] / nc, label="Stock")
                    elif name == "Individual.behaviour":
                        ax.plot(timepoints, raw[name] / nc, label="$n_s$")
                    elif name == "Group.group_attitude":
                        ax.plot(timepoints, raw[name] / ng, label="Group attitude")
                    elif name == "Individual.alignment":
                        ax.plot(timepoints, raw[name] / nc, label="Concordance")
                ax.set_xlabel("t")
                ax.set_ylabel("Value")
                ax.set_title(i + "_" + str(n))
                ax.legend(loc="best")
                save_path = SAVE_PATH + "/" + i
                # plt.show()
                plt.savefig(save_path + "/" + str(i) + f"_{n}" + ".png")
                plt.close()
                n += 1


def plot_all_trajs_in_one(variables, parameter_combinations, timepoints, nc, RAW_PATH, SAVE_PATH):
    ids = get_mofa_id(parameter_combinations)
    # for i in ids:
    #     if not os.path.exists(SAVE_PATH + "/" + i):
    #         os.mkdir(SAVE_PATH + "/" + i)
    fnames = np.sort(glob.glob(RAW_PATH + "/*"))
    # print(ids)
    for z, i in enumerate(ids):
        # get number of trajectories to plot cmap well
        n = 0
        for f in fnames:
            if i in f:
                n += 1
        cvalues = range(n)
        jet = cm = plt.get_cmap('jet')
        cNorm = colors.Normalize(vmin=0, vmax=cvalues[-1])
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
        if len(variables) == 2:
            fig, ax = plt.subplots(1, 2)
        elif len(variables) == 4:
            fig, ax = plt.subplots(2, 2)
        else:
            fig, ax = plt.subplots(len(variables), 1)
        count = 0
        ng = parameter_combinations[z][17]
        for f in fnames:
            if i in f:
                raw = pickle.load(open(f, "rb"))
                colorVal = scalarMap.to_rgba(cvalues[count])
                for index, name in enumerate(variables):
                    ax.flatten()[index].set_xlabel("$t$")
                    if name == "Cell.stock":
                        ax.flatten()[index].set_ylabel(r"$S$")
                        ax.flatten()[index].plot(timepoints, raw[name] / nc, color=colorVal)
                        ax.flatten()[index].set_ylim(0, 1)
                        ax.flatten()[index].set_xlim(-0.1, timepoints[-1] + 0.1)
                        ax.flatten()[index].set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
                    elif name == "Individual.behaviour":
                        ax.flatten()[index].set_ylabel(r"$n_s$")
                        ax.flatten()[index].plot(timepoints, raw[name] / nc, color=colorVal)
                        ax.flatten()[index].set_ylim(0, 1)
                        ax.flatten()[index].set_xlim(-0.1, timepoints[-1] + 0.1)
                        ax.flatten()[index].set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
                    elif name == "Group.group_attitude":
                        ax.flatten()[index].set_ylabel(r"$A$")
                        ax.flatten()[index].plot(timepoints, raw[name] / ng, color=colorVal)
                        # print(raw[name])
                        # print(ng)
                        # print(raw[name] / ng)
                        ax.flatten()[index].set_ylim(-0.01, 1.01)
                        ax.flatten()[index].set_xlim(-0.1, timepoints[-1] + 0.1)
                        ax.flatten()[index].set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
                    elif name == "Individual.alignment":
                        ax.flatten()[index].set_ylabel(r"$C$")
                        ax.flatten()[index].plot(timepoints, raw[name] / nc, color=colorVal)
                        ax.flatten()[index].set_ylim(0, 1)
                        ax.flatten()[index].set_xlim(-0.1, timepoints[-1] + 0.1)
                        ax.flatten()[index].set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
                    else:
                        ax.flatten()[index].set_ylabel("Value")
                        ax.flatten()[index].plot(timepoints, raw[name], color=colorVal)
                    # ax[index].set_title(name)
                    # ax[index].legend(loc="best")
                count += 1
        fig.set_figwidth(8)
        # plt.suptitle(i)
        fig.tight_layout()
        # plt.show()
        plt.savefig(SAVE_PATH + "/" + i + ".png")
        plt.close("all")


def plot_distributions(parameter_combinations, variables, ranges, timestep, RAW_PATH, SAVE_PATH):
    """ranges must be a list of tuples with ranges same length as variables"""

    print("Plotting distributions...")
    ids = get_mofa_id(parameter_combinations)
    # for i in ids:
    #     if not os.path.exists(SAVE_PATH + "/" + i):
    #         os.mkdir(SAVE_PATH + "/" + i)
    fnames = np.sort(glob.glob(RAW_PATH + "/*"))
    for i in ids:
        dist_dict = {}
        for name in variables:
            dist_dict[name] = []
        for f in fnames:
            if i in f:
                raw = pickle.load(open(f, "rb"))
                for index, name in enumerate(variables):
                    dist_dict[name].append(raw[name][timestep])
        fig, ax = plt.subplots(len(variables))
        for index, name in enumerate(variables):
            n_bins = int(ranges[index][1] - ranges[index][0])
            if n_bins > 50:
                n_bins = int(n_bins / 10)
            ax[index].hist(dist_dict[name], bins=n_bins, range=ranges[index])
            # ax[index].set_xlabel("")
            ax[index].set_ylabel(name)
            # ax[index].set_title(name)
        # ax[index].legend(loc="best")
        fig.set_figheight(16)
        plt.suptitle(i)
        fig.tight_layout()
        # plt.show()
        plt.savefig(SAVE_PATH + "/" + i + ".png")
        plt.close()
    print("Done plotting distributions!")


def plot_mean_and_std_traj(data, parameter_combinations, parameter_name_list, variables, timepoints, nc, SAVE_FOLDER):
    for c in parameter_combinations:
        fig, ax = plt.subplots(1, len(variables))
        for index, name in enumerate(variables):
            y = data['mean'].unstack('observables').xs(key=c, level=parameter_name_list)[name]
            y_e = data['std'].unstack('observables').xs(key=c, level=parameter_name_list)[name]
            # ax[index].set_title(name)
            ax[index].set_xlabel("t")
            if name == "Cell.stock":
                ax[index].set_ylabel(r"$\langle S \rangle$")
                ax[index].plot(timepoints, y / nc, color="forestgreen")
                ax[index].fill_between(timepoints, list(np.subtract(np.array(y), np.array(y_e)) / nc),
                                       list(np.add(np.array(y), np.array(y_e)) / nc), alpha=0.1, color="forestgreen")
                ax[index].set_ylim(0, 1)
                ax[index].set_xlim(-0.1, timepoints[-1] + 0.1)
                ax[index].set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
            elif name == "Individual.behaviour":
                ax[index].set_ylabel(r"$\langle n_s \rangle$")
                ax[index].plot(timepoints, y / nc, color="firebrick")
                ax[index].fill_between(timepoints, list(np.subtract(np.array(y), np.array(y_e)) / nc),
                                       list(np.add(np.array(y), np.array(y_e)) / nc), alpha=0.1, color="firebrick")
                ax[index].set_ylim(0, 1)
                ax[index].set_xlim(-0.1, timepoints[-1] + 0.1)
                ax[index].set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
            else:
                ax[index].set_ylabel("Value")
                ax[index].plot(timepoints, y, color="blue")
                ax[index].fill_between(timepoints, list(np.subtract(np.array(y), np.array(y_e))),
                                       list(np.add(np.array(y), np.array(y_e))), alpha=0.1)
        # plt.suptitle(str(c))
        fig.tight_layout()
        fig.set_figwidth(len(variables) * 4)
        plt.tight_layout()
        plt.savefig(SAVE_FOLDER + "/" + f"{c}" + ".png")
        plt.close("all")


def phase_transition(data, parameter_combinations, parameter_dict, parameter_name_list, param_1, timestep, variables,
                     nc, SAVE_PATH, scale=None):
    """Create phase transition plots for 1 parameter. Only works for sweeps of single params!!!
    data: the data
    parameter_name_list: list of parameter names
    parameter_dict: dictionary of parameters and their valuess
    param_combinations: all possible combinations
    param_1: name (str) of parameter of interest
    timestep: evaluation timestep
    variables: list of variables to plot"""
    from scipy.stats import binom
    print("Start creating phase transition plots....")

    if not os.path.exists(SAVE_PATH + "/phase_transitions"):
        os.mkdir(SAVE_PATH + "/phase_transitions")

    parameter_values = parameter_dict[param_1]
    for index, key in enumerate(parameter_name_list):
        if key == param_1:
            param_loc = index

    key_list = []
    for c in parameter_combinations:
        c = list(c)
        keys = []
        for value in parameter_values:
            c[param_loc] = value
            keys.append(tuple(c))
        key_list.append(keys)

    # print(key_list)
    # print(len(key_list))
    deduplicated_list = list()
    [deduplicated_list.append(item) for item in key_list if item not in deduplicated_list]

    key_list = deduplicated_list
    # print(len(key_list))
    # print(key_list)
    n = 0
    for k in key_list:

        # data['mean'].unstack('observables').xs(key=c, level=param_1)[name]
        # y_e = data['std'].unstack('observables').xs(key=c, level=param_1)[name]

        A = k

        mean = np.zeros(len(parameter_values))
        std = np.zeros(len(parameter_values))

        fig, ax = plt.subplots(1, len(variables))
        for index, name in enumerate(variables):
            for i in range(len(mean)):
                mean[i] = float(data['mean'].unstack('observables').xs(key=tuple(A[i]),
                                                                       level=parameter_name_list).loc[
                                    timestep, name] / nc)
                std[i] = float(data['std'].unstack('observables').xs(key=tuple(A[i]),
                                                                     level=parameter_name_list).loc[
                                   timestep, name] / nc)
            if name == "Cell.stock":
                # ax[index].set_major_formatter(FormatStrFormatter('%.2f'))
                # ax[index].set_major_formatter(FormatStrFormatter('%.2f'))
                ax[index].set_ylabel(r"$\langle S \rangle$")
                ax[index].set_ylim(0, 1)
                ax[index].set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
                # ax[index].set_xticks(parameter_values)
                # ax[index].set_xticks(parameter_values[::5])
                if scale == "log":
                    ax[index].set_xscale('log')
                if scale == "log2":
                    ax[index].set_xscale('log', base=2)
                # ax[index].set_xticks([1, 2, 4, 8, 16, 32, 64, 128])
                ax[index].scatter(parameter_values, mean, color="forestgreen")
                ax[index].fill_between(parameter_values, list(np.subtract(np.array(mean), np.array(std))),
                                       list(np.add(np.array(mean), np.array(std))), alpha=0.1, color="forestgreen")
                # ax[index].set_title(name)
                ax[index].set_xlabel(translate_into_thesis_naming(param_1))
                # ax[index].set_ylabel("Value")

            elif name == "Individual.behaviour":
                # ax[index].set_major_formatter(FormatStrFormatter('%.2f'))
                # ax[index].set_major_formatter(FormatStrFormatter('%.2f'))
                ax[index].set_ylabel(r"$\langle n_s \rangle$")
                ax[index].set_ylim(0, 1)
                ax[index].set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
                # ax[index].set_xticks(parameter_values)
                # ax[index].set_xticks(parameter_values[::5])
                if scale == "log":
                    ax[index].set_xscale('log')
                if scale == "log2":
                    ax[index].set_xscale('log', base=2)
                # ax[index].set_xticks([1, 2, 4, 8, 16, 32, 64, 128])
                ax[index].scatter(parameter_values, mean, color="firebrick")
                # print(parameter_values, mean)
                ax[index].fill_between(parameter_values, list(np.subtract(np.array(mean), np.array(std))),
                                       list(np.add(np.array(mean), np.array(std))), alpha=0.1, color="firebrick")
                # ax[index].set_title(name)
                ax[index].set_xlabel(translate_into_thesis_naming(param_1))
                # plot cdf
                # x = np.arange(0, 1, 0.01)
                # cdf = binom.cdf(x * 400, 400, 0.5)
                # cdf_2 = 1 - cdf
                # ax[index].plot(x, cdf_2, color="orange", alpha = 1, label="CDF")
            else:
                ax[index].set_ylabel("Value")
                ax[index].scatter(parameter_values, mean, color="red")
                ax[index].fill_between(parameter_values, list(np.subtract(np.array(mean), np.array(std))),
                                       list(np.add(np.array(mean), np.array(std))), alpha=0.1, color="red")
                ax[index].set_title(name)
                ax[index].set_xlabel(param_1)
        # plt.legend()

        fig.set_figwidth(len(variables) * 4)

        plt.tight_layout()

        naming = list(A[0])
        naming[param_loc] = "x"
        print(naming)
        id = str(naming)  # convert to sting
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

        plt.savefig(SAVE_PATH + "/phase_transitions/" + f"{param_1}_{id}" + ".png")
        plt.close("all")
        n += 1


def pixel_plot(data, config, cmaps, parameter_name_list, parameter_list, PARAM_COMBS, timestep, variables, nc,
               SAVE_PATH, scale=None, groups=None):
    # create key sets for single parameter sweeps for plotting
    # change the ones that were sweeped and fix the other ones

    # cmpas: list of colormap names where list[0] is cmap for cells, list[1] is cmap for inds and list[2] cmap for std dev

    import plotly.express as px

    if not os.path.exists(SAVE_PATH + "/pixelplots"):
        os.mkdir(SAVE_PATH + "/pixelplots")

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

    print(pairs)
    print(PARAM_COMBS)

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

        print("Plotting figures...")

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
            for name in variables:
                matrix = np.zeros((len(parameter_list[param_loc1]), len(parameter_list[param_loc2])), dtype=float)
                std_matrix = np.zeros((len(parameter_list[param_loc1]), len(parameter_list[param_loc2])), dtype=float)
                for i in range(np.shape(matrix)[0]):
                    for j in range(np.shape(matrix)[1]):
                        matrix[i][j] = float(data['mean'].unstack('observables').xs(key=tuple(A[i][j]),
                                                                                    level=parameter_name_list).loc[
                                                 timestep, name] / nc)
                        std_matrix[i][j] = float(data['std'].unstack('observables').xs(key=tuple(A[i][j]),
                                                                                       level=parameter_name_list).loc[
                                                     timestep, name] / nc)
                        if groups:
                            if j > i:
                                matrix[i][j] = None
                                std_matrix[i][j] = None

                matrices = [matrix, std_matrix]
                if name == "Cell.stock":
                    m_names = [r"$\langle S \rangle$", r"$\sigma_{\langle S \rangle}$"]
                elif name == "Individual.behaviour":
                    m_names = [r"$\langle n_s \rangle$", r"$\sigma_{\langle n_s \rangle}$"]
                elif name == "Group.group_attitude":
                    m_names = [r"$\langle A \rangle$", r"$\sigma_{\langle A \rangle}$"]
                elif name == "Individual.alignment":
                    m_names = [r"$\langle C \rangle$", r"$\sigma_{\langle C \rangle}$"]
                else:
                    m_names = ["Values", "Std."]
                fig, ax = plt.subplots(1, len(matrices))
                fig.set_figwidth(len(variables) * 4)
                # plt.suptitle(param1 + " vs. " + param2 + " " + name)
                for index, m in enumerate(matrices):
                    ax[index].set_title(f"{m_names[index]}")
                    # extent = [min(param_list2), max(param_list2), min(param_list1), max(param_list1)]
                    if index == 1:
                        im = ax[index].imshow(m, interpolation="None", origin="lower", vmin=0, vmax=0.5, cmap=cmaps[2])
                    else:
                        if name == "Cell.stock":
                            im = ax[index].imshow(m, interpolation="None", origin="lower", vmin=0, vmax=0.5,
                                                  cmap=cmaps[0])
                        else:
                            im = ax[index].imshow(m, interpolation="None", origin="lower", vmin=0, vmax=1,
                                                  cmap=cmaps[1])
                    # plt.colorbar(ax=ax[index])
                    # ax.set_xscale('log', base=2)
                    ax[index].set_xlabel(translate_into_thesis_naming(param2))
                    if index == 0:
                        ax[index].set_ylabel(translate_into_thesis_naming(param1))
                    else:
                        ax[index].yaxis.set_visible(False)
                    xticks = list(np.arange(0, np.shape(m)[1], 1))
                    yticks = list(np.arange(0, np.shape(m)[0], 1))
                    ax[index].set_xticks(xticks)
                    xtickslabels = []
                    for w in param_list2:
                        if w < 1:
                            xtickslabels.append(format(w, '.2f'))
                        else:
                            xtickslabels.append(w)
                    ax[index].set_xticklabels(xtickslabels, rotation=-45, fontsize=6)
                    ax[index].set_yticks(yticks)
                    if index == 0:
                        ytickslabels = []
                        for w in param_list1:
                            if w < 1:
                                ytickslabels.append(format(w, '.2f'))
                            else:
                                ytickslabels.append(w)
                        ax[index].set_yticklabels(ytickslabels, fontsize=6)
                    else:
                        ax[index].set_yticklabels([])

                    if scale == "log":
                        ax[index].set_xscale('log')
                        ax[index].set_yscale('log')
                    if scale == "log2":
                        ax[index].set_yscale('log', base=2)
                        ax[index].set_xscale('log', base=2)

                    divider = make_axes_locatable(ax[index])
                    cax = divider.append_axes('bottom', size='5%', pad=0.8)
                    fig.colorbar(im, cax=cax, orientation='horizontal')

                # fig.subplots_adjust(right=0.8)
                # cbar_ax = fig.add_axes([0.8, 0.0, 0.05, 1])
                # fig.colorbar(im, cax=cbar_ax, orientation='vertical')

                # fig.colorbar(im, ax = ax.ravel().tolist(), orientation="vertical")

                # divider = make_axes_locatable(ax[1])
                # cax = divider.append_axes('right', size='5%', pad=0.05)
                # fig.colorbar(im, cax=cax, orientation='vertical')

                plt.tight_layout()

                naming = list(c)
                naming[param_loc1] = "x"
                naming[param_loc2] = "x"
                id = str(naming)  # convert to sting
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

                plt.savefig(SAVE_PATH + f"/pixelplots/{param1}_{param2}_{name}_{id}" + ".png")
                plt.close("all")
        print("Done plotting figures!")


def stationarity_analysis():
    ids = get_mofa_id(PARAM_COMBS)
    fnames = np.sort(glob.glob(RAW_PATH + "/*"))
    print("Start calculating stationarities with ADF Test.")
    for i in ids:
        n, N = 0, 0
        mean_p_cells, mean_p_inds = ([] for i in range(2))
        for f in fnames:
            if i in f:
                N += 1
                raw = pickle.load(open(f, "rb"))
                # print ('Results of Dickey-Fuller Test:')
                dftest = adfuller(raw["Cell.stock"][0:], autolag='AIC')
                # dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
                # print(dfoutput)
                p_value = dftest[1]
                if p_value < 0.05:
                    # print(f"p-value is {p_value} and TS is stationary")
                    n += 1
        mean_p_cells.append(n / N)
        # print(f"{mean_p * 100}% of cell-stock TS in \n set {i} \n are stationary.")
        n = 0
        N = 0
        for f in fnames:
            if i in f:
                N += 1
                raw = pickle.load(open(f, "rb"))
                # print ('Results of Dickey-Fuller Test:')
                dftest = adfuller(raw["Individual.behaviour"][0:], autolag='AIC')
                # dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
                # print(dfoutput)
                p_value = dftest[1]
                if p_value < 0.05:
                    # print(f"p-value is {p_value} and TS is stationary")
                    n += 1
        mean_p_inds.append(n / N)
        # print(f"{mean_p * 100}% of behaviours TS in \n set {i} \n are stationary.")

    print("Finished calculating stationarities.")

    print("Write csv file.")
    with open(SAVE_PATH + '/stationarity.csv', 'w', encoding='UTF8', newline='') as file:
        writer = csv.writer(file, delimiter=",")
        header = ['ID', 'stationary_TS_cells', 'stationary_TS_inds']
        # write the header
        writer.writerow(header)
        for index, i in enumerate(ids):
            data = [i, mean_p_cells[index], mean_p_inds[index]]
        writer.writerow(data)


def plot_phase_plot(data, parameter_combinations, parameter_name_list, variables, timepoints, nc, SAVE_FOLDER):
    if not os.path.exists(SAVE_FOLDER + "/phasespace"):
        os.mkdir(SAVE_FOLDER + "/phasespace")

    for c in parameter_combinations:
        fig, ax = plt.subplots()

        name_1 = variables[0]
        name_2 = variables[1]

        x = data['mean'].unstack('observables').xs(key=c, level=parameter_name_list)[name_1]
        y = data['mean'].unstack('observables').xs(key=c, level=parameter_name_list)[name_2]
        plt.plot(x / nc, y / nc)
        plt.xlabel(r"$\langle S \rangle$")
        plt.ylabel(r"$\langle n_s \rangle$")
        plt.xlim(0, 1.0)
        plt.ylim(0, 1.0)
        plt.grid()
        # plt.legend(loc="best")
        # plt.suptitle(str(c))
        fig.tight_layout()
        fig.set_figwidth(4)
        plt.tight_layout()
        plt.savefig(SAVE_FOLDER + "/phasespace/" + f"{c}" + ".png")
        plt.close("all")


def plot_phase_plot_with_analytical_h(data, error, parameter_combinations, parameter_name_list, parameter_list,
                                      variables, timepoints, nc, SAVE_FOLDER):
    from scipy.integrate import odeint
    from scipy.special import expit

    def calculate_harvest(stock, E_i):
        return E_i * stock

    def map_harvest(harvest, E_un):
        """Maps harvest range [0, E_u] on range of expit [-1, 1] and then flip it, such
        that a high harvest means low prob to switch"""
        return -1 * (2 / E_un * harvest - 1)

    def calc_prob(stock, E_i, E_un, k):
        return expit(k * map_harvest(calculate_harvest(stock, E_i), E_un))

    def dynamical_system(y, t, k):
        s, n_s = y
        dydt = [s * (1 - s) - s * ((1 - n_s) * 1.5 + n_s * 0.5),
                (1 - n_s) * calc_prob(stock=s, E_i=1.5, E_un=1.5, k=k)
                - n_s * calc_prob(s, 0.5, 1.5, k)]
        return dydt

    if not os.path.exists(SAVE_FOLDER + "/phasespace_and_analytical"):
        os.mkdir(SAVE_FOLDER + "/phasespace_and_analytical")

    count = np.arange(0, 1.05, 0.05)
    y_0_1 = []
    for c in count:
        y_0_1.append([c, 0])
    y_0_2 = []
    for c in count:
        y_0_2.append([1, c])
    y_0_3 = []
    for c in count:
        y_0_3.append([c, 1])
    y_0_4 = []
    for c in count:
        y_0_4.append([0, c])
    y_0 = []
    for y in y_0_2:
        y_0_1.append(y)
    for y in y_0_3[::-1]:
        y_0_1.append(y)
    for y in y_0_4[::-1]:
        y_0_1.append(y)
    y_0 = y_0_1
    y_0_new = []
    [y_0_new.append(item) for item in y_0 if item not in y_0_new]
    y_0 = y_0_new

    for comb in parameter_combinations:
        k = comb[6]
        N = len(timepoints)
        values = range(N)
        jet = plt.get_cmap('jet')
        cNorm = colors.Normalize(vmin=0, vmax=values[-1])
        scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)

        fig, ax = plt.subplots()

        name_1 = variables[0]
        name_2 = variables[1]

        labelcount = 0
        t = np.arange(0, 50, 0.1)
        for count, y in enumerate(y_0):
            # colorVal = scalarMap.to_rgba(values[c])
            sol = odeint(dynamical_system, y, t, args=(k,))
            for index in range(len(t) - 1):
                plt.arrow(sol[index, 0], sol[index, 1], sol[index + 1, 0] - sol[index, 0],
                          sol[index + 1, 1] - sol[index, 1],
                          color="grey", width=0.001, head_width=0.006, alpha=0.5)
                if labelcount == 0:
                    plt.arrow(sol[index, 0], sol[index, 1], sol[index + 1, 0] - sol[index, 0],
                              sol[index + 1, 1] - sol[index, 1],
                              color="grey", width=0.001, head_width=0.006, alpha=0.5, label="analytical traj.")
                    labelcount += 1

        x = data['mean'].unstack('observables').xs(key=comb, level=parameter_name_list)[name_1]
        y = data['mean'].unstack('observables').xs(key=comb, level=parameter_name_list)[name_2]
        # plt.plot(x / nc, y / nc, color="navy", label="model traj.", linewidth=2)

        labelcount = 0
        for index, t in enumerate(timepoints):
            colorVal = scalarMap.to_rgba(values[index])
            if index < (len(timepoints) - 1):
                plt.arrow(x[t] / nc, y[t] / nc, x[timepoints[index + 1]] / nc - x[t] / nc,
                          y[timepoints[index + 1]] / nc - y[t] / nc,
                          color=colorVal, width=0.005, head_width=0, alpha=1)
                if labelcount == 0:
                    plt.arrow(x[t] / nc, y[t] / nc, x[timepoints[index + 1]] / nc - x[t] / nc,
                              y[timepoints[index + 1]] / nc - y[t] / nc,
                              color=colorVal, width=0.005, head_width=0, alpha=1, label="model traj.")
                    labelcount += 1

        if error:
            x_e = data['std'].unstack('observables').xs(key=comb, level=parameter_name_list)[name_1]
            y_e = data['std'].unstack('observables').xs(key=comb, level=parameter_name_list)[name_2]
            error_times = [0, 25, 49]
            for index, e in enumerate(error_times):
                if index == 1:
                    plt.errorbar(x[e] / nc, y[e] / nc, xerr=x_e[e] / nc, yerr=y_e[e] / nc,
                                 color="dimgrey", label=r"$\sigma$", lolims=True, uplims=True)
                plt.errorbar(x[e] / nc, y[e] / nc, xerr=x_e[e] / nc, yerr=y_e[e] / nc, color="dimgrey", lolims=True,
                             uplims=True)

        plt.xlabel(r"$\langle S \rangle$")
        plt.ylabel(r"$\langle n_s \rangle$")
        plt.xlim(0, 1.0)
        plt.ylim(0, 1.0)
        plt.grid()
        plt.legend(loc="upper right")
        # plt.suptitle(str(c))
        fig.tight_layout()
        # fig.set_figwidth(4)
        plt.tight_layout()
        plt.savefig(SAVE_FOLDER + "/phasespace_and_analytical/" + f"{comb}" + ".png")
        plt.close("all")