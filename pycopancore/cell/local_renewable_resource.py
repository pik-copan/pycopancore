# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
Encapsulates states and dynamics of local renewable resource with logistic
growth equation due to Wiedermann 2015.
"""

#
#  Imports
#

from abstract_cell import Cell

#
#  Define class Renweable_Resource
#


class Renewable_Resource(Cell):
    """
    Encapsulates states and dynamics of local renewable resource with logistic
    growth equation due to Wiedermann 2015.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 cell_identifier,
                 coordinates,
                 stock,
                 capacity,
                 growth_rate
                 ):
        """
        Initializes an instance of a renewable resource. Inherits
        cell_identifier, coordinates and stock from class Cell.
        Generates capacity and growth_rate for the ODE of
        Wiedermann (2015).
        """

        super(Renewable_Resource, self).__init__(cell_identifier,
                                                 coordinates,
                                                 stock
                                                 )
        self.capacity = None
        self.growth_rate = None

    def __str__(self):
        """
        Returns a string representation of the object of class
        'Renewable_Stock'.
        """
        return (super(Renewable_Resource, self).__str__() +
                ('capacity % s, \
                 growth rate % s'
                 ) % (
                 self.capacity,
                 self.growth_rate
                 )
                )

        def set_capacity(self, capacity):
            """
            A function to set the capacity of the renewable resource
            """
            self.capacity = capacity

        def set_growth_rate(self, growth_rate):
            """
            A function to set the growth_rate of the renewable resource
            """
            self.growth_rate = growth_rate

    #
    #  Definitions of further methods
    #

    def time_differential(self, y, time):
        """
        The following ODE describes the dynamics of the renewable
        ressource through logistic growth (cf. Wiedermann 2015).
        Required variables are capacity and growth_rate. Variable y is the
        stock of the renewable resource.

        Parameters
        ---------
        y : float
            Stock in dependence of time
        time : float
            Time y is dependent on
        """
        a = self.growth_rate
        K = self.capacity
        dydt = a * y * (1 - y / K)
        return dydt
