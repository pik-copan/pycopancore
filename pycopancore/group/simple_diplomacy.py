# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
SimpleDiplomacy is a subclass of 'Metabolism' and describes a simple 
Network of Groups. It does not include real things, this is just a 
demonstrator
"""

#
#  Imports
#

from .abstract_metabolism import Metabolism

#
#  Define class MacroAgents
#


class SimpleDiplomacy(Metabolism):
    """
    SimpleDiplomacy is a subclass of 'Metabolism' and describes a simple 
    Network of Groups. It does not include real things, this is just a 
    demonstrator
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 group_connections=None):
        """
        Initializes an instance of 'SimpleDiplomacy'.
        Inherits group_connections from 'Metabolism'.

        Parameters
        ----------
        group_connections: array?
            Describes connections between groups
        """
        super(SimpleDiplomacy, self).__init__(group_connections)


    def __str__(self):
        """
        Returns a string representation of the instance
        """
        return (super(SimpleDiplomacy, self).__str__())

    #
    # Function to create a Network of groups like create_grid in donut_world
    #

    #
    #  Definitions of further methods
    #