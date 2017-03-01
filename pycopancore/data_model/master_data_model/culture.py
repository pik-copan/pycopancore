from pycopancore.data_model import Variable
from networkx import Graph

# Social networks:
acquaintance_network = \
    Variable("acquaintance network",
             "basic social network of acquaintance between Individuals",
             datatype=Graph)
