import pandas as pd
import numpy as np
import Cluster_Utils as utils
from profilehooks import profile


general_input_folder = "Z:/Uni Nils/Energy Science Master/Masterarbeit/Python/Marc GranovetterModell/pygranovetter/Workprogress Scripts/Cluster Skripte/Cluster Input/"

local_path = "Z:/Uni Nils/Energy Science Master/Masterarbeit/Python/Marc GranovetterModell/pygranovetter/Workprogress Scripts/"
nodeset_input_folder = local_path + "Cluster Skripte/Output Nodesets/"
network_output_folder = local_path + "Cluster Skripte/Output Networks/"


class Network:
    def __init__(self, number_of_nodes, potentially_active_connection_corr):
        self._N = number_of_nodes
        self._potentially_active_connection_corr = potentially_active_connection_corr

#    @profile
    def create_network(self, nodeset_number, network_number, 
                       # JH added these to enable variable folders:
                       metadata_folder=None, nodesets_folder=None, networks_folder=None):
        """
        Creates one network with alpha and beta to meet the mean degree.
        Node distance from coast, [(lon,lat), distance from coast[km], elevation[m]], node neighbours,
        certainly actives(depending on sea level rise), centainly inactives, and potentially actives calculated.
        """
        # JH added these to enable variable folders:
        if metadata_folder is None:
            metadata_folder = general_input_folder
        if nodesets_folder is None:
            nodesets_folder = nodeset_input_folder
        if networks_folder is None:
            networks_folder = network_output_folder
            
        print('Proceed network number {0} from nodeset {1}...'.format(network_number,nodeset_number))
        # values for all counties and their respective shares for potentially actives
        df = pd.read_csv(metadata_folder + '/Country_Codes_and_imputed_shares.csv', sep=';')
        country_shares_array = df.to_numpy()

        nodeset = np.load(
            nodesets_folder + "/nodeset_{0}.npz".format(
                nodeset_number))

        node_lats = nodeset['arr_0']
        node_lons = nodeset['arr_1']
        # node_pops = nodeset['arr_2']
        # node_alts = nodeset['arr_3']
        node_land = nodeset['arr_4']

        A, L, D, is_pa = utils.generate_adjacency_matrix_and_potentially_actives(
                            N=self._N, 
                            lats=node_lats,
                            lons=node_lons,
                            land=node_land,
                            country_shares_array=country_shares_array,
                            potentially_active_connection_corr=self._potentially_active_connection_corr)

        adjacency_matrix_array = A.toarray()
        adjacency_matrix = adjacency_matrix_array.astype(np.int8)

        np.savez_compressed(
            networks_folder + '/network_{0}'.format(network_number),
            *[adjacency_matrix, is_pa, nodeset_number, network_number, self._potentially_active_connection_corr])
        print('>>>Network saved to '+networks_folder+'/network_{0}'.format(network_number))


if __name__ == "__main__":
    n = Network(number_of_nodes=10000,
                potentially_active_connection_corr=0.8)

    number_of_nodesets = 3
    number_of_networks_per_nodeset = 2

    for nodeset_number in range(number_of_nodesets):
        for network in range(number_of_networks_per_nodeset):
            network_number = (number_of_networks_per_nodeset*nodeset_number)+network
            n.create_network(nodeset_number, network_number,
                             metadata_folder="./Cluster Input",
                             nodesets_folder="./Output Nodesets",
                             networks_folder="./Output Networks")
            
