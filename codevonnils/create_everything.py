import Create_Nodesets as cnodes
import Create_Network as cnets

from os import listdir, path, makedirs

metadata_folder = './Cluster Input'
output_nodesets_folder = './Output_Nodesets'
output_networks_folder = './Output_Networks'

number_of_nodes = 10000
number_of_nodesets = 5

def create_non_existing_folders(list_of_paths_to_folder):
    for path_to_folder in list_of_paths_to_folder:
        if not path.exists(path_to_folder):
            makedirs(path_to_folder)

def create_everything():
    create_non_existing_folders([output_nodesets_folder, output_networks_folder])

    if not listdir(output_nodesets_folder):
        print("Nodesets are not found, creating them now")
        cnodes.create_nodesets(number_of_nodes, number_of_nodesets, 0, metadata_folder, output_nodesets_folder)
    else:
        print("Nodesets folder is not empty, proceed with network creation")
    
    
    n = cnets.Network(number_of_nodes=number_of_nodes, 
                potentially_active_connection_corr=0.8)

    number_of_networks_per_nodeset = 2

    for nodeset_number in range(number_of_nodesets):
        for network in range(number_of_networks_per_nodeset):
            network_number = (number_of_networks_per_nodeset*nodeset_number)+network
            n.create_network(nodeset_number, network_number,
                             metadata_folder,
                             output_nodesets_folder,
                             output_networks_folder)

if path.exists(metadata_folder):
    create_everything()
