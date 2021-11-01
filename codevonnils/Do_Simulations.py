import networkx as nx
import numpy as np
import math
import Cluster_Utils as utils

from numba.typed import List
from numba.typed import Dict
from mpl_toolkits.basemap import Basemap as Basemap
from numba import njit
from profilehooks import profile

general_input_folder = "Z:/Uni Nils/Energy Science Master/Masterarbeit/Python/Marc GranovetterModell/pygranovetter/Workprogress Scripts/Cluster Skripte/Cluster Input/"

local_path = "Z:/Uni Nils/Energy Science Master/Masterarbeit/Python/Marc GranovetterModell/pygranovetter/Workprogress Scripts/"
network_input_folder = local_path + "Cluster Skripte/Output Networks/"
nodeset_input_folder = local_path + "Cluster Skripte/Output Nodesets/"
simulation_output_folder = local_path + "Cluster Skripte/Output Simulations/"


@njit
def calculate(number_of_nodes, neighbours, certainly_actives, influenceable_nodes,
              activation_threshold, activation_probability, deactivation_threshold,
              deactivation_probability, timesteps, affected_nodes_from_event,
              event_activation_probability_numba, event_activation_probability_of_friend_numba,
              random_activation_probability, random_deactivation_probability, do_print=False):
    """
    N=no. of nodes, neighbours= network as list of neighbour-list, certainly_actives = list of certainly active nodes
    potentially_actives = list of contingent nodes, timesteps = how long to simulate
    node_x = node latitudes, node_y = node longitudes, event_x = event latitude by time, event_y = event longitude by time
    event_radius = event radius by time (0 if no event at this time) , do_print=False = whether to print progress
    0 if inactive, 1 if active
    """

    is_active = np.zeros((timesteps + 1, number_of_nodes))  # ist quasi die history für is_active und is_affected
    is_affected = np.zeros((timesteps + 1, number_of_nodes))

    for node in certainly_actives:
        is_active[0, node] = 1  # zum Zeitpunkt 0 werden alle certainly actives = 1, also active gesetzt

    degree = [len(nbs) for nbs in neighbours]

    timestep_counter = 0

    for time in range(timesteps):
        # copy state to next time point:
        is_active[time + 1, :] = is_active[time, :]
        # then update it for the potentially active nodes:
        for node in influenceable_nodes:
            # check whether node is affected by event:
            if affected_nodes_from_event[time][node] == 1:
                # activate friends with certain probability
                for nbs in neighbours[node]:
                    if np.random.rand() < event_activation_probability_of_friend_numba and nbs in influenceable_nodes and \
                            affected_nodes_from_event[time][nbs] == 0:
                        # is_affected[time, nbs] = 1
                        is_active[time + 1, nbs] = 1
                if np.random.rand() < event_activation_probability_numba:
                    is_affected[time, node] = 1  # is affected by event

            # count active neighbours of current node:
            active_nbs = len([nbs for nbs in neighbours[node] if is_active[time, nbs] == 1])

            # if inactive, potentially activate it:
            if is_active[
                time, node] == 0:  # in is_active stehen für jeden Zeitschritt alle nodes sowaohl active als auch inactove drin
                if (is_affected[
                        time, node] == 1  # wenn von shock beeinflusst, oder viele aktive Nachbarn dann aktiviere den node, dann im nächsten Zeitschritt aktiv
                    or (active_nbs >= activation_threshold * degree[node]
                        and np.random.rand() < activation_probability)) or np.random.rand() < random_activation_probability:
                    is_active[time + 1, node] = 1
            # if active, potentially deactivate it:
            else:
                if (active_nbs <= deactivation_threshold * degree[node]
                        and np.random.rand() < deactivation_probability):
                    is_active[time + 1, node] = 0

            if is_active[time, node] == 1 and np.random.rand() < random_deactivation_probability:
                is_active[time + 1, node] = 0

        if do_print:  # = True
            print(time, is_active[time, :].sum(), is_affected[time, :].sum())

        timestep_counter += 1

    if do_print:
        print(timesteps, is_active[timesteps, :].sum())
    return is_active, is_affected, timestep_counter  # um für den nächsten Zeitschritt zu schauen


class Simulations:
    def __init__(self, first_year, last_year, n_networks, event_forcing):
        self._first_year = first_year
        self._last_year = last_year
        self.n_networks = n_networks
        self._event_forcing = event_forcing

        self._timesteps = (last_year - first_year) * 52
        self._degree_in_km = 111.12

        llcrnrlon = -180
        llcrnrlat = -70
        urcrnrlon = 180
        urcrnrlat = 75

        self._basemap = Basemap(projection='merc', llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat,
                                urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat, lat_ts=0,
                                resolution='l')

    #    @profile
    def run(self, simulation_number, activation_probability, deactivation_probability, event_activation_probability,
            event_activation_probability_of_friend,
            random_activation_probability, random_deactivation_probability, activation_threshold,
            deactivation_threshold, anticipated_sea_level_rise,
            event_folder=None, nodesets_folder=None, network_folder=None, simulation_folder=None):
        """
        runs one simulation
        """

        # JH added these to enable variable folders:
        if event_folder is None:
            event_folder = general_input_folder
        if nodesets_folder is None:
            nodesets_folder = output_folder_nodesets
        if network_folder is None:
            network_folder = network_input_folder
        if simulation_folder is None:
            simulation_folder = simulation_output_folder

        # Data for the Events
        simulation_folder_number = int(round((simulation_number) // 1000, 0))
        event_array_data = np.load(
            event_folder + "/Events_as_array_already_filtered_mit_meteo.npz")  # ['Year', 'Dis Mag Value', 'Latitude', 'Longitude', 'Calender Week']
        event_array = event_array_data['arr_0']

        network_to_simulate = simulation_number % self.n_networks
        network_data = np.load(
            network_folder + "/network_{0}.npz".format(network_to_simulate), allow_pickle=True)

        adjacency_matrix = network_data['arr_0']
        is_pa = network_data['arr_1']
        nodeset_number = network_data['arr_2']
        network_number = network_data['arr_3']
        potentially_active_connection_corr = network_data['arr_4']

        number_of_nodes = len(adjacency_matrix)

        nodeset = np.load(nodesets_folder + "/nodeset_{0}.npz".format(nodeset_number))
        node_lats = nodeset['arr_0']
        node_lons = nodeset['arr_1']
        node_alts = nodeset['arr_3']

        network = self.create_graph(nodes=number_of_nodes, node_lons=node_lons, node_lats=node_lats,
                                    adjacency_matrix=adjacency_matrix)

        pos_on_land_lon_lat, node_elevation, min_node_distance_from_coast_array = self.calculate_geographical_node_positions(
            network, node_alts)

        random_events_list, random_events_index = self.create_event(pos_on_land_lon_lat, event_array, number_of_nodes)

        # assign nodes to be certainly active,potentially activ, or inactive
        certainly_actives, certainly_inactives, influenceable_nodes, neighbours, is_pa = self.assign_nodes_to_political_activity(
            is_pa, anticipated_sea_level_rise, node_elevation, network, number_of_nodes)

        is_active, is_affected, timestep_counter = calculate(number_of_nodes=number_of_nodes,
                                                             neighbours=neighbours,
                                                             certainly_actives=certainly_actives,
                                                             influenceable_nodes=influenceable_nodes,
                                                             activation_threshold=activation_threshold,
                                                             activation_probability=activation_probability,
                                                             deactivation_threshold=deactivation_threshold,
                                                             deactivation_probability=deactivation_probability,
                                                             timesteps=self._timesteps,
                                                             affected_nodes_from_event=random_events_list,
                                                             event_activation_probability_numba=event_activation_probability,
                                                             event_activation_probability_of_friend_numba=event_activation_probability_of_friend,
                                                             random_activation_probability=random_activation_probability,
                                                             random_deactivation_probability=random_deactivation_probability)

        statistical_analysis_array = np.zeros((self._timesteps + 1, number_of_nodes, 2),
                                              dtype='int8')  # is_active, is_affected
        certainly_actives_array = np.zeros(number_of_nodes, dtype='int8')
        certainly_inactives_array = np.zeros(number_of_nodes, dtype='int8')

        statistical_analysis_array, certainly_actives_array, certainly_inactives_array = utils.fill_arrays_with_data(
            N=number_of_nodes,
            timesteps=self._timesteps,
            statistical_analysis_array=statistical_analysis_array,
            is_active=is_active,
            is_affected=is_affected,
            certainly_actives=certainly_actives,
            certainly_actives_array=certainly_actives_array,
            certainly_inactives=certainly_inactives,
            certainly_inactives_array=certainly_inactives_array)

        np.savez_compressed(
            simulation_folder + '/{0}xxx/simulation_{1}'.format(simulation_folder_number, simulation_number),
            *[statistical_analysis_array, certainly_actives_array, certainly_inactives_array,
              min_node_distance_from_coast_array, random_events_index])

        metadata_file = open(
            simulation_folder + '/{0}xxx/SimulationParameter_{1}'.format(simulation_folder_number, simulation_number),
            "w")

        metadata = (simulation_number, network_number, nodeset_number, activation_threshold,
                    activation_probability, deactivation_threshold, deactivation_probability,
                    event_activation_probability, event_activation_probability_of_friend,
                    random_activation_probability, random_deactivation_probability,
                    anticipated_sea_level_rise, self._first_year, self._last_year, potentially_active_connection_corr, self._event_forcing)
        metadata_str = "{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10};{11};{12};{13};{14};{15}\n".format(*metadata)
        metadata_file.write(metadata_str)
        metadata_file.close()
        return metadata

    def create_graph(self, nodes, node_lons, node_lats, adjacency_matrix):
        """
        creates a waxman Graph on a Basemap.
        Own definition of Waxman-Graph to be able to hand over a own list of node locations.
        Nodes are on land, located dependend on the population density, and linked dependend on their distance(exp decreasing probability).
        n: number of nodes
        alpha: model parameter
        beta: model parameter
        :return: Graph
        """

        population_weighted_pos_lonlat = Dict()
        for node in range(nodes):
            population_weighted_pos_lonlat[node] = (node_lons[node], node_lats[node])

        population_weighted_pos_projection = Dict()
        for node in population_weighted_pos_lonlat:
            population_weighted_pos_projection[node] = self._basemap(population_weighted_pos_lonlat.get(node)[0],
                                                                     population_weighted_pos_lonlat.get(node)[1])

        G = nx.from_numpy_matrix(adjacency_matrix)
        G.add_nodes_from(range(nodes))

        for node in G:
            G.nodes[node]['pos'] = population_weighted_pos_projection[node]

        return G

    def create_event(self, pos_on_land_lon_lat, event_array, number_of_nodes):
        """
                Events from EM-DAT Database, are integrated into the model.
                It is possibe that multiple events occur at the same calenderweek.
                (long while loop to create an nested list that includes all nodes, and events for a certain time. If none a zero is appended for this timestep)
                More modifications to hand over a numba compatible list of the format [time,node] that includes all affected nodes
                of all rvents within a timestep in binary format.
                """

        year = 2006
        calenderweek = 1

        # sort the array by date
        ind = np.lexsort((event_array[:][:, 4], event_array[:][:, 0]))
        event_array_sorted = event_array[ind]  # ['Year', 'Dis Mag Value', 'Latitude', 'Longitude', 'Calender Week']
        del event_array

        event_center = list()
        event_radius = list()
        node_distance_from_event = list()

        # It can be that there are multiple events in one day. This while loop is making sure, that the events happen at the same day at different locations
        event = 0
        while event < 925:

            if event_array_sorted[:, 0][event] == year and event_array_sorted[:, 4][event] > calenderweek:
                while event_array_sorted[:, 0][event] == year and event_array_sorted[:, 4][event] > calenderweek:
                    event_center.append((0, 0))
                    event_radius.append([0])

                    short_node_list = list()
                    for node in range(number_of_nodes):
                        short_node_list.append(0)
                    node_distance_from_event.append(short_node_list)

                    if calenderweek % 52 != 0:
                        calenderweek += 1
                    elif calenderweek % 52 == 0 and calenderweek != 0:
                        year += 1
                        calenderweek = 1

            elif event_array_sorted[:, 0][event] == year and event_array_sorted[:, 4][event] == calenderweek:
                temporary_list_center = list()
                temporary_list_radius = list()
                temporary_list_nodes = list()
                while event_array_sorted[:, 0][event] == year and event_array_sorted[:, 4][event] == calenderweek:
                    temporary_list_center.append((event_array_sorted[:, 3][event], event_array_sorted[:, 2][event]))
                    temporary_list_radius.append(math.sqrt(event_array_sorted[:, 1][event] / math.pi))

                    short_node_list = list()
                    for node in range(number_of_nodes):
                        short_node_list.append(
                            (utils.lonlatdist(pos_on_land_lon_lat[node][0], pos_on_land_lon_lat[node][1],
                                              event_array_sorted[:, 3][event],
                                              event_array_sorted[:, 2][event])))
                    temporary_list_nodes.append(short_node_list)

                    event += 1

                event_center.append(temporary_list_center)
                event_radius.append(temporary_list_radius)
                node_distance_from_event.append(temporary_list_nodes)

                if calenderweek % 52 != 0:
                    calenderweek += 1
                elif calenderweek % 52 == 0 and calenderweek != 0:
                    year += 1
                    calenderweek = 1

            elif event_array_sorted[:, 0][event] == year and event_array_sorted[:, 4][event] < calenderweek:
                while event_array_sorted[:, 0][event] == year and event_array_sorted[:, 4][event] < calenderweek:
                    event_center.append((0, 0))
                    event_radius.append([0])

                    short_node_list = list()
                    for node in range(number_of_nodes):
                        short_node_list.append(0)
                    node_distance_from_event.append(short_node_list)

                    if event_array_sorted[:, 0][event] == year:
                        calenderweek -= 1
                    elif event_array_sorted[:, 0][event] != year:
                        calenderweek += 1

                    if calenderweek % 52 == 0 and calenderweek != 0:
                        year += 1
                        calenderweek = 1

            elif event_array_sorted[:, 0][event] != year and event_array_sorted[:, 4][event] < calenderweek:
                while event_array_sorted[:, 0][event] != year and event_array_sorted[:, 4][event] < calenderweek:
                    event_center.append((0, 0))
                    event_radius.append([0])

                    short_node_list = list()
                    for node in range(number_of_nodes):
                        short_node_list.append(0)
                    node_distance_from_event.append(short_node_list)

                    if calenderweek % 52 != 0:
                        calenderweek += 1
                    elif calenderweek % 52 == 0 and calenderweek != 0:
                        year += 1
                        calenderweek = 1
            else:
                event_center.append((0, 0))
                event_radius.append([0])

                short_node_list = list()
                for node in range(number_of_nodes):
                    short_node_list.append(0)
                node_distance_from_event.append(short_node_list)

                if calenderweek % 52 != 0:
                    calenderweek += 1
                    event += 1
                elif calenderweek % 52 == 0 and calenderweek != 0:
                    year += 1
                    calenderweek = 1

        # now i have all the event arrays per day
        event_radius_array = np.array(event_radius, dtype=object)  # event is approximtely a circle with radius r
        for day in range(len(event_radius_array)):
            for event in range(len(event_radius_array[day])):
                event_radius_array[day][event] = event_radius_array[day][
                    event]  # sometimes it is necessary to multiply the event radius, because otherwise very few array are affected, due to sparse density of nodes in relation to real number of people

        maxLength = max(len(x) for x in event_radius_array)  # maximum events per day = 7
        node_distance_from_event_array = np.array(node_distance_from_event,
                                                  dtype=object)  # is a list with every node per event, and calculates its distance to the event

        is_affected = np.zeros((len(event_radius_array), abs(maxLength), number_of_nodes))  # [time,event,node]

        for time in range(len(event_radius_array)):
            for node in range(number_of_nodes):
                for event in range(len(event_radius_array[time])):
                    if isinstance(node_distance_from_event_array[time][event], list):
                        if node_distance_from_event_array[time][event][node] < event_radius_array[time][event]:
                            is_affected[time, event, node] = 1
                    else:
                        if node_distance_from_event_array[time][node] < event_radius_array[time][event]:
                            is_affected[time, event, node] = 0

        events_complete = np.zeros(
            (len(event_radius_array), number_of_nodes))  # now i have all affected nodes at every possible timestep

        for time in range(len(event_radius_array)):
            for event in range(maxLength):
                for node in range(number_of_nodes):
                    if is_affected[time, event, node]:
                        events_complete[time, node] = 1

        events_complete_final = events_complete

        """random_events_index = np.random.randint(len(events_complete_final), size=self._timesteps, dtype=int)
        random_events_list = List(events_complete[random_events_index, :])"""

        # here i am implementing the forcing. i take one year complete and the events of a randomly selected year just with a probability of "event_forcing"

        event_forcing = self._event_forcing
        number_of_years = int(self._timesteps / 52)
        random_events_index_years = np.random.randint(14, size=number_of_years, dtype=int)
        random_forcing_year = np.random.randint(14, size=number_of_years, dtype=int)

        random_forcing_index_complete = np.zeros((self._timesteps, 2))

        random_events_index = np.zeros(self._timesteps, dtype='int')
        for random_year in range(len(random_events_index_years)):
            for random_week in range(52):
                random_events_index[random_year * 52 + random_week] = random_events_index_years[
                                                                          random_year] * 52 + random_week
                random_forcing_index_complete[random_year * 52 + random_week, 0] = random_events_index_years[
                                                                                       random_year] * 52 + random_week

        random_forcing_index = np.zeros(self._timesteps, dtype='int')
        for random_year in range(len(random_forcing_year)):
            for random_week in range(52):
                random_forcing_index[random_year * 52 + random_week] = random_forcing_year[
                                                                           random_year] * 52 + random_week

        random_events = events_complete[random_events_index, :]

        for event in range(len(random_events)):
            if np.random.rand() < event_forcing:
                random_events[event, :] = random_events[event, :] + events_complete[random_forcing_index[event], :]
                random_forcing_index_complete[event, 1] = random_forcing_index[event]

        for i in range(len(random_events)):
            for j in range(len(random_events[0, :])):
                if random_events[i, j] > 1:
                    random_events[i, j] = 1

        random_events_list = List(random_events)

        return random_events_list, random_forcing_index_complete

    def assign_nodes_to_political_activity(self, is_pa, anticipated_sea_level_rise, node_elevation, network,
                                           number_of_nodes):
        pos_sorted = dict(sorted(node_elevation.items(), key=lambda item: item[1]))
        pos_sorted_keys = List(pos_sorted.keys())

        nodes = List(range(number_of_nodes))
        neighbours = List()
        empty = [0]
        for i in nodes:
            if list(network.neighbors(i)):
                neighbours.append(List(network.neighbors(i)))
            else:
                neighbours.append(List(empty))

        potentially_actives = List()
        for i in range(len(nodes)):
            if is_pa[i]:
                potentially_actives.append(nodes[i])

        certainly_actives = List()
        for active in range(len(potentially_actives)):
            if list(pos_sorted.values())[active] <= anticipated_sea_level_rise:
                certainly_actives.append(pos_sorted_keys[active])
            else:
                break
        if len(certainly_actives) == 0:
            certainly_actives.append(pos_sorted_keys[0])

        certainly_inactives = List(set(nodes).difference(certainly_actives, potentially_actives))

        influenceable_nodes = List(set(potentially_actives).difference(certainly_inactives, certainly_actives))

        return certainly_actives, certainly_inactives, influenceable_nodes, neighbours, is_pa

    def calculate_geographical_node_positions(self, network, node_alts):
        pos = nx.get_node_attributes(network, "pos")
        node_positions = List()
        for i in pos.values():
            node_positions.append(List(i))

        coast = self._basemap.drawcoastlines()
        coordinates = np.vstack(coast.get_segments())
        lons, lats = self._basemap(coordinates[:, 0], coordinates[:, 1],
                                   inverse=True)  # polygon of coast segments in lon and lat

        pos_on_land_lon_lat = Dict()
        for elem in pos:
            pos_on_land_lon_lat[elem] = self._basemap(pos[elem][0], pos[elem][1], inverse=True)

        min_node_distance_from_coast = {}
        for elem in pos_on_land_lon_lat:
            min_node_distance_from_coast[elem] = np.min(np.sqrt(
                (lons - pos_on_land_lon_lat[elem][0]) ** 2 + (
                        lats - pos_on_land_lon_lat[elem][1]) ** 2) * self._degree_in_km)
        min_node_distance_from_coast_array = np.fromiter(min_node_distance_from_coast.values(), dtype=np.float16)

        node_elevation = {}
        for node in pos:
            node_elevation[node] = node_alts[node]

        return pos_on_land_lon_lat, node_elevation, min_node_distance_from_coast_array


if __name__ == "__main__":
    s = Simulations(first_year=2020,
                    last_year=2050,
                    n_networks=3,
                    event_forcing=0.12)

    metadata_file = open(
        simulation_output_folder + 'SimulationParameter', "w")
    metadata_file.write(
        '#simulation_number;network_number;nodeset_number;activation_threshold;activation_probability;deactivation_threshold;deactivation_probability;event_activation_probability;'
        'event_activation_probability_of_friend;random_activation_probability;random_deactivation_probability;anticipated_sea_level_rise;first_year;last_year'
        ';potentially_active_connection_corr \n')
    metadata_file.close()

    # TODO: delete this when running on Cluster
    activation_probability = 0.3
    deactivation_probability = 0.2
    event_activation_probability = 0.9
    event_activation_probability_of_friend = 0.01
    random_activation_probability = 0.001
    random_deactivation_probability = 0.001
    activation_threshold = 0.2
    deactivation_threshold = 0.2
    anticipated_sea_level_rise = 5

    for simulations in range(2):
        s.run(simulations, activation_probability, deactivation_probability, event_activation_probability,
              event_activation_probability_of_friend,
              random_activation_probability, random_deactivation_probability, activation_threshold,
              deactivation_threshold, anticipated_sea_level_rise)
