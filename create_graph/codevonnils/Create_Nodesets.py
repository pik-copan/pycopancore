import numpy as np
import hickle as hkl
from numba.typed import List
from time import time

population_input_folder = "Z:/Uni Nils/Energy Science Master/Masterarbeit/Python/Marc Bevölkerungsdaten/"
output_folder_nodesets = "Z:/Uni Nils/Energy Science Master/Masterarbeit/Python/Marc GranovetterModell/pygranovetter/Workprogress Scripts/Cluster Skripte/Output Nodesets/"


def create_nodesets(number_of_nodes, number_of_nodesets, first_nodeset_index, population_folder=None, nodesets_folder=None):

    # JH added these to enable variable folders:
    if population_folder is None:
        population_folder = population_input_folder
    if nodesets_folder is None:
        nodesets_folder = output_folder_nodesets

    N = number_of_nodes  # network size
    M = number_of_nodesets  # number of networks
    K = N*M  # no. of nodes to be drawn in one go (choose as large as possible given your memory)
    R = int(np.ceil(N * M / K))
    print("drawing a total of %d nodes in %d rounds" % (N * M, R))

    whole_population_elevation_data = hkl.load(
        population_folder + '/whole_population_elevation_array_all_countries_inverted.hkl')

    whole_population_elevation_array = whole_population_elevation_data
    a = whole_population_elevation_array[1][1]
    list_of_country_ids = List()
    for country in range(len(whole_population_elevation_array)):
        list_of_country_ids.append(whole_population_elevation_array[country, 0])

    cell_size = 1 / 120
    alt_resolution = 1

    def get_country_table(country):
        cell_ids = np.array([i for i, _ in enumerate(whole_population_elevation_array[country][1][:, 0])])
        cell_lons = whole_population_elevation_array[country][1][:, 0]
        cell_lats = whole_population_elevation_array[country][1][:, 1]
        cell_pops = whole_population_elevation_array[country][1][:, 2]
        cell_alts = whole_population_elevation_array[country][1][:, 3]
        return cell_ids, cell_lats, cell_lons, cell_pops, cell_alts

    country_pops = {}
    total_pop = 0

    for country in range(len(list_of_country_ids)):
        start = time()
        p = country_pops[country] = whole_population_elevation_array[country][1][:, 2].sum()
        total_pop += p
        print("country %d first pass took %f sec." % (country, time() - start))

    keys = list(country_pops.keys())
    weights = np.array(list(country_pops.values())) / total_pop

    for round in range(R):
        print("ROUND %d" % round)

        start = time()
        node_countries = np.random.choice(keys, p=weights, size=K)
        country_nodes = {country: [] for country in keys}
        for i, country in enumerate(node_countries):
            country_nodes[country].append(i)
        print("drawing countries took %f sec." % (time() - start))

        node_cells = np.zeros(K, dtype="int")
        node_lats = np.zeros(K, dtype="float32")
        node_lons = np.zeros(K, dtype="float32")
        node_pops = np.zeros(K, dtype="float32")
        node_alts = np.zeros(K, dtype="float32")
        node_land = np.zeros(K, dtype="int")

        for country in range(len(list_of_country_ids)):
            start = time()
            cell_ids, cell_lats, cell_lons, cell_pops, cell_alts = get_country_table(country)
            ns = country_nodes[country]
            nc = len(ns)
            total_country_population = sum(
                cell_pops)
            if total_country_population != 0:
                cells = node_cells[ns] = np.random.choice(cell_ids, p=cell_pops / total_country_population, size=nc,
                                                          replace=True)
                node_lats[ns] = cell_lats[cells] + (np.random.rand(nc) - 0.5) * cell_size
                node_lons[ns] = cell_lons[cells] + (np.random.rand(nc) - 0.5) * cell_size
                node_pops[ns] = cell_pops[cells] + (np.random.rand(nc) - 0.5) * alt_resolution
                node_alts[ns] = cell_alts[cells] + (np.random.rand(nc) - 0.5) * alt_resolution
                node_land[ns] = list_of_country_ids[country]
                print("country %d second pass took %f sec. for %d nodes" % (country, time() - start, len(ns)))

        np.savez_compressed(
            nodesets_folder + "/{0}_nodesets_with_{1}_nodes_from_{2}".format(number_of_nodesets, number_of_nodes, first_nodeset_index), *[node_cells, node_lats, node_lons, node_pops, node_alts, node_land])

        split_big_population_data_into_parts(number_of_nodes, number_of_nodesets, first_nodeset_index, nodesets_folder)


def split_big_population_data_into_parts(number_of_nodes, number_of_nodesets, first_nodeset_index, nodesets_folder):
    """ Sometimes it is better to create one big file including 10000 Networks with 10000 each, and then split it.
    This makes the creation of nodesets way faster.
    This funtion is taking ne "big" file and splits it up into multiple small networks
    """
    data = np.load(
        nodesets_folder + "/{0}_nodesets_with_{1}_nodes_from_{2}.npz".format(number_of_nodesets, number_of_nodes, first_nodeset_index))

    # node_cells_array = data['arr_0']
    node_lats_array = data['arr_1']
    node_lons_array = data['arr_2']
    node_pops_array = data['arr_3']
    node_alts_array = data['arr_4']
    node_land_array = data['arr_5']

    for run in range(number_of_nodesets):
        load_data_from = run * number_of_nodes
        load_data_to = (run + 1) * number_of_nodes
        node_lats = node_lats_array[load_data_from:load_data_to]
        node_lons = node_lons_array[load_data_from:load_data_to]
        node_pops = node_pops_array[load_data_from:load_data_to]
        node_alts = node_alts_array[load_data_from:load_data_to]
        node_land = node_land_array[load_data_from:load_data_to]

        np.savez_compressed(
            nodesets_folder + "/nodeset_{0}".format(run + first_nodeset_index),
            *[node_lats, node_lons, node_pops, node_alts, node_land])


if __name__ == "__main__":
    create_nodesets(10000, 5)

