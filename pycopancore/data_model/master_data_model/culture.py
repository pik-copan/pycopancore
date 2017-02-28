from pycopancore.data_model import Variable, CETSVariable
from networkx import Graph

# Social networks:
basic_social_network = Variable("basic social network", datatype=Graph,
                                desc="basic social network of acquaintance between Individuals")
