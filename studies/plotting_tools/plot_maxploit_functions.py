import numpy as np
import matplotlib.pyplot as plt

def plot_trajectory(list_1, list_2, t):
    for index in range(len(t)):
        plt.scatter(list_1[index], list_2[index], c="navy", )
        plt.xlabel(str(list_1))
        plt.xlabel(str(list_2))
        plt.title(f"Trajectory {str(list_1)} vs. {str(list_2)}")

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

def phase_transition(data, parameter_name_list, parameter_dict, parameter_list, param_1, timestep, value):
    """Create phase transition plots for 1 parameter.
    data: the data
    parameter_name_list: list of parameter names
    parameter_dict: dictionary of parameters and their valuess
    param_combinations: all possible combinations
    param_1: name (str) of parameter of interest
    timestep: evaluation timestep
    value: what to plot, can be "cells" or "inds" """

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
            sem[i] = float(data['sem'].unstack('observables').xs(key=tuple(A[i]),
                                                                 level=parameter_name_list).loc[
                               timestep, "Cell.stock"])

    elif value == "inds":
        for i in range(len(mean)):
            mean[i] = float(data['mean'].unstack('observables').xs(key=tuple(A[i]),
                                                                   level=parameter_name_list).loc[
                                timestep, "Individual.behaviour"])
            sem[i] = float(data['sem'].unstack('observables').xs(key=tuple(A[i]),
                                                                 level=parameter_name_list).loc[
                               timestep, "Individual.behaviour"])

    figure = plt.figure()

    plt.scatter(parameter_values, mean)
    plt.fill_between(parameter_values, list(np.subtract(np.array(mean), np.array(sem))),
                     list(np.add(np.array(mean), np.array(sem))), alpha=0.1)
    return figure