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

import numpy as np
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

    def create_group_network(self, list_groups, av_network_degree):
        """
        Creates a network in between groups

        Parameters
        ----------
        list_groups : list
            list of the existing instances of groups
        av_network_degree : integer
            The average amount of connections in between groups
        """
        N_g = len(list_groups)
        adj_mat = np.zeros(shape=(N_g, N_g))
        k = av_network_degree
        N_c = (k * N_g)/2
        N_co = 0
        while N_co <= N_c:
            g_1 = np.random.randint(0, N_g)
            g_2 = np.random.randint(0, N_g)
            if g_1 == g_2:
                # Check for self-connections
                continue
            if g_2 in list_groups[g_1].connections:
                # Check for double-connection
                continue
            list_groups[g_1].group_connection.append(g_2)
            list_groups[g_2].group_connection.append(g_1)
            adj_mat[g_1, g_2] = 1
            adj_mat[g_2, g_1] = 1
            N_co += 1
        Metabolism.set_group_connections(adj_mat)

    #
    #  Definitions of further methods
    #

    def get_ingredients(self):
        """
        This function returns a list of tuples, each of the form (label, type,
        list of affected variables, specification). Entries of each tuple are
        specified in the following clarification

        Clarification
        -------------
        label : string
            The denotation of the dynamical system
        type : string
            The type of the dynamics. Can be either "explicit", "derived",
            "ODE", "step" or "event"
        list of affected variables: any dtype
            List of all variables that are affected from the specified dynamics
        specification : any dtype
            Further specifications that are necessary for the global
            integration (e.g. methods to solve the specified dynamics)
        """
        return [] 


