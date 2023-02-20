from pickle import load
import os
import networkx as nx
from matplotlib import pyplot as plt

path = "C:\\Users\\bigma\\Documents\\Uni\\Master\\MA_Masterarbeit\\plots\\maxploit\\Run_2022_09_15_18_47_12\\networks\\"
target = "culture.acquaintance_network.pickle"

if os.path.getsize(path+target) == 0:
    print("file empty")

acquaintance_network = load(open(path+target,"rb"))

# print(list(acquaintance_network.neighbors("Individual[UID=103]")))

# nx.draw(acquaintance_network)
# plt.show()