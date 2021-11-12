# ATTENTION: run from studies folder for correct file paths

import sys
sys.path.insert(0, "leanders_model/codevonnils/")

from os import listdir, path, makedirs
from time import time

import Create_Nodesets as cnodes
import Create_Network as cnets


input_folder = sys.path[0] + "Input"
output_nodesets_folder = sys.path[0] + "Output_Nodesets"
output_networks_folder = sys.path[0] + "Output_Networks"

def create_non_existing_folders(list_of_paths_to_folder):
    for path_to_folder in list_of_paths_to_folder:
        if not path.exists(path_to_folder):
            makedirs(path_to_folder)

def create_nodesets_and_networks(number_of_nodes, number_of_nodesets, number_of_networks_per_nodeset):
    
    create_non_existing_folders([output_nodesets_folder, output_networks_folder])
    
    
    if listdir(output_nodesets_folder):
        print("Nodesets found, proceed with network creation")
    else:
        print("Nodesets not found, creating them now")
        start = time()
        cnodes.create_nodesets(number_of_nodes, number_of_nodesets, 0, input_folder, output_nodesets_folder)
        print(f"Nodesets creation finished. Took {time()-start} s")
    
    start = time()
    n = cnets.Network(number_of_nodes=number_of_nodes, 
                potentially_active_connection_corr=0.8)

    for nodeset in range(number_of_nodesets):
        for network_index in range(number_of_networks_per_nodeset):
            network = (number_of_networks_per_nodeset*nodeset) + network_index
            n.create_network(nodeset, 
                             network,
                             input_folder,
                             output_nodesets_folder,
                             output_networks_folder)
    print(f"Networks creation finished. Took {time()-start} s")

if __name__ == "__main__":
    if path.exists(input_folder):
        create_nodesets_and_networks(1000, 1, 1)
    else:
        print("Input folder not found, check path")
