# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
Encapsulates states and dynamics of local environmental stocks.
"""

#
#  Imports
#

from abstract_cell import Cell

#
#  Define class Renweable_Stock
#


class Renewable_Stock(Cell):
    """
    Encapsulates states and dynamics of global environmental stocks.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 cell_identifier,
                 coordinates,
                 stock,
                 capacity,
                 growth_rate,
                 catch_coefficient,
                 cell_effort
                 ):
        """
        Initializes an instance of a renewable stock. Inherits cell_identifier,
        coordinates and stock from class Cell. Creates capacity, growth_rate
        and catch_coefficient for the ODE (Wiedermann 2015).
        """

        super(Renewable_Stock, self).__init__(cell_identifier,
                                              coordinates, stock
                                              )
        self.capacity = None
        self.growth_rate = None
        self.catch_coefficient = None
        self.cell_effort = None

    def __str__(self):
        """
        Returns a string representations of the object of class Renewable_Stock
        """
        return (super(Renewable_Stock, self).__str__() +
                ('capacity % s, \
                 growth rate % s, \
                 catch coefficient % s'
                 ) % (
                 self.capacity,
                 self.growth_rate,
                 self.catch_coefficient
                 )
                )

    #
    #  Definitions of further methods
    #

    def renewable_stock(self, y, time):
        """
        The following ODE describes the stock dynamics of a renewable ressource
        through logistic growth and its harvest (Wiedermann 2015).
        Required variables are capacity, growth_rate,
        catch_coefficient and effort. y is the stock.
        """
        a = self.growth_rate
        K = self.capacity
        q = self.catch_coefficient
        E = self.cell_effort
        dydt = a * y * (1 - y / K) - q * y * E
        return dydt
