import sys
sys.path.insert(0, '/home/leander/Dokumente/Studium/13/Masterthesis/pycopancore/create_graph/codevonnils')

from os import listdir, path, makedirs
import time

import Create_Nodesets as cnodes
import Create_Network as cnets


input_folder = '/home/leander/Dokumente/Studium/13/Masterthesis/pycopancore/create_graph/codevonnils/Input'
output_nodesets_folder = '/home/leander/Dokumente/Studium/13/Masterthesis/pycopancore/create_graph/codevonnils/Output_Nodesets'
output_networks_folder = '/home/leander/Dokumente/Studium/13/Masterthesis/pycopancore/create_graph/codevonnils/Output_Networks'

number_of_nodes = 1000
number_of_nodesets = 1
number_of_networks_per_nodeset = 1

def create_non_existing_folders(list_of_paths_to_folder):
    for path_to_folder in list_of_paths_to_folder:
        if not path.exists(path_to_folder):
            makedirs(path_to_folder)

def create_everything():
    create_non_existing_folders([output_nodesets_folder, output_networks_folder])

    if not listdir(output_nodesets_folder):
        print("Nodesets not found, creating them now")
        start = time.time()
        cnodes.create_nodesets(number_of_nodes, number_of_nodesets, 0, input_folder, output_nodesets_folder)
        end = time.time()
        print(f"Nodesets creation finished. Took {end-start} s")
    else:
        print("Nodesets folder is not empty, proceed with network creation")
    
    start = time.time()
    n = cnets.Network(number_of_nodes=number_of_nodes, 
                potentially_active_connection_corr=0.8)

    for nodeset_number in range(number_of_nodesets):
        for network in range(number_of_networks_per_nodeset):
            network_number = (number_of_networks_per_nodeset*nodeset_number)+network
            n.create_network(nodeset_number, network_number,
                             input_folder,
                             output_nodesets_folder,
                             output_networks_folder)
    end = time.time()
    print(f"Networks creation finished. Took {end-start} s")

if path.exists(input_folder):
    create_everything()
else:
    print("Input folder not found, check path")
