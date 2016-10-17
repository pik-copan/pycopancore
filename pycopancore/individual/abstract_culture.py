# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license


"""
Encapsulates states and dynamics of the network between Individuals
"""

#
#  Imports
#

#
#  Define class Culture
#

class Culture(object):
    """
    Encapsulates states and dynamics of the network between Individuals
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 individual_connections):

        """
        Initializes an instance of Culture:
        The objects of Culture define connections and/or interactions 
        between objects of class Individual

        Parameters
        ----------
        individual_connections: matrix or set of matrices?
            This is an array to describe different types of connections.
            Maybe several adjacency matrices will make sense, this is not 
            yet clear. 
        """

        self.individual_connections = individual_connections

    def __str__(self):
        """
        Return a string representation of the object of class Culture
        """
        return ('Individual connections % s'
                ) % (
                self.individual_connections)

    def set_individual_connections(self, connections):
        """
        A function to set connections.
        
        Parameters
        ----------
        connections : array?
            This may be adjacency matrices, maybe an igraph object?
        """
        self.individual_connections = connections

    #
    #  Definitions of further methods
    #
