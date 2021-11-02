import sys
sys.path.insert(0, '/home/leander/Dokumente/Studium/13/Masterthesis/pycopancore/create_graph/codevonnils')

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from Do_Simulations import Simulations

networks_folder = './codevonnils/Output_Networks'
nodesets_folder = './codevonnils/Output_Nodesets'

network_data = np.load(networks_folder + '/network_0.npz', allow_pickle=True)

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

s = Simulations(first_year=2020,
                last_year=2050,
                n_networks=1,
                event_forcing=0.12)

G = s.create_graph(nodes=number_of_nodes, node_lons=node_lons, node_lats=node_lats,
                            adjacency_matrix=adjacency_matrix)

nx.draw(G, nodelist=range(10), with_labels=False, font_weight='bold')
plt.show()
