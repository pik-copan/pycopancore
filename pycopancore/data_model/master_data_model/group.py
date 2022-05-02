"""Master data model for group."""

"""https://github.com/pik-copan/pycopancore/blob/master/docs/framework_documentation/abstract_level/entity_types/group.rst"""

#from . import MET
from .. import Variable


class Group:

    #TODO: add a group network possibility (in culture.py (?))

    
    has_leader = \
        Variable("has a leader",
                 "whether the group has a leader",
                 scale="ordinal", levels=[False, True], default=False)

    has_headquarter = \
        Variable("has a headquarter",
                 "whether the group has a headquarter located in a cell",
                 scale="ordinal", levels=[False, True], default=False)
        
        
        
        

