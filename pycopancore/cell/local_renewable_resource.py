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


class RenewableResource(Cell):
    """
    Encapsulates states and dynamics of local renewable resource with logistic
    growth equation due to Wiedermann 2015.
    This class is a simple cell model with only one resource which is
    renewable, for example fish. It follows a logistic growth model.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 cell_identifier,
                 coordinates,
                 stocks,
                 capacity,
                 growth_rate,
                 current_stock
                 ):
        """
        Initializes an instance of a renewable resource. Inherits
        cell_identifier, coordinates and stock from class Cell.
        Generates capacity and growth_rate for the ODE of
        Wiedermann (2015).

        Parameters
        ----------
        cell_identifier : integer
            this is a number which identifies each cell
        coordinates : integer or tuple?
            It is not clear yet how to locate cells on the grid, either just
            number them or give them real coordinates like lat/lon
        stock : np.array of 3 rows and 10 lines
            In this array, the Capacity, the growthrate and the current stock
            of all resources are saved. If a slot in the array is not used, 
            it is filled with np.nan
        capacitiy : float
            The capacity of the resource stock
        growth_rate : float
            The growth-rate of the stock
        current_stock: float
            This is the current capacity of the stock which is equal or less
            than the capacity
        """

        super(Renewable_Resource, self).__init__(cell_identifier,
                                                 coordinates,
                                                 stocks
                                                 )
        self.capacity = capacity
        self.growth_rate = growth_rate
        self.current_stock = current_stock

        self.stocks[0,0] = self.capacity
        self.stocks[0,1] = self.current_stock
        self.stocks[0,2] = self.growth_rate

    def __str__(self):
        """
        Returns a string representation of the object of class
        'Renewable_Stock'.
        """
        return (super(Renewable_Resource, self).__str__() +
                ('capacity % s, \
                 growth rate % s \
                 current stock % s'
                 ) % (
                 self.capacity,
                 self.growth_rate,
                 self.current_stock
                 )
                )

    def set_capacity(self, capacity):
            """
            A function to set the capacity of the renewable resource
            """
            self.capacity = capacity
            self.stocks[0,0] = capacity

    def set_growth_rate(self, growth_rate):
            """
            A function to set the growth_rate of the renewable resource
            """
            self.growth_rate = growth_rate
            self.stocks[0,1] = growth_rate

    def set_current_stock(self, current_stock):
            """
            A function to set the current stock of the renewable resource
            """
            self.current_stock = current_stock
            self.stocks[0,1] = current_stock

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

    def recursive_logistic_solver(self,
                                  max_cap,
                                  cur_stock,
                                  gro_rate,
                                  time_step):
        """
        Solver for logistic growth in dependece of maximum capacity, 
        current_capacity and grwoth_rate

        Parameters
        ----------
        max_cap : float
            The maximum caoacity of the resource
        cur_cap : float
            the current capacity of the resource, smaller or equal to the
            max_cap
        gro_rate : float
            the growth-rate
        time_step: float
            the time for which the result is desired
        """
        k = gro_rate
        dt = time_step
        s0 = cur_stock
        s = max_cap
        return (s*s0)/(s0+(s-s0)*exp(-k*s*dt)) 

