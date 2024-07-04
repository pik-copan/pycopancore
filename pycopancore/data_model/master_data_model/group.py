"""Master data model for group."""

from .. import Variable

from networkx import Graph

class Group:

    #TODO: specify edges

    intra_group_network = \
        Variable("intra group network",
                 """Basic undirected social network between
                 Group members.""",
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
        
        
        
        

