"""Master data model for group."""

"""https://github.com/pik-copan/pycopancore/blob/master/docs/framework_documentation/abstract_level/entity_types/group.rst"""

from .. import Variable

from networkx import Graph

class Group:

    #TODO: add a group network possibility (in culture.py (?))

    group_network = \
        Variable("group network",
                 """Basic undirected social network between
                 Groups.""",
                 ref="https://en.wikipedia.org/wiki/Social_network#Meso_level",
                 scale='nominal',
                 datatype=Graph)    

    has_leader = \
        Variable("has a leader",
                 "whether the group has a leader",
                 scale="ordinal", levels=[False, True], default=False)

    has_headquarter = \
        Variable("has a headquarter",
                 "whether the group has a headquarter located in a cell",
                 scale="ordinal", levels=[False, True], default=False)
        
        
        
        

