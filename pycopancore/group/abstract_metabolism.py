# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
Encapsulates states and dynamics of social metabolism.
"""

#
#  Imports
#

#
#  Define class Group
#


class Metabolism(object):
    """
    Encapsulates states and dynamics of connections between groups.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 group_connections):
        """
        Initialize an instance of 'Metabolism'.

        Parameters
        ----------
        group_connections: arrays?
            Describes all sort of connections between groups
        """

    def __str__(self):
        """
        Return a string representation of the object of class individual
        """
        return ('group_connections % s'
                ) % (self.group_connections)

    def set_group_connections(self, connections):
        """
        A function to set connections.

        Parameters
        ----------
        connections : array?
            This may be adjacency matrices, maybe an igraph object?
        """
        self.group_connections = connections

    #
    #  Definitions of further methods
    #
