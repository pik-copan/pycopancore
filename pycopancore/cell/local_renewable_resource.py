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

import numpy as np
from .abstract_cell import Cell

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
                 coordinates=None,
                 neighbours=None,
                 stocks=np.full((10, 3), np.nan),
                 capacity=1,
                 growth_rate=0.2,
                 current_stock=1
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

        super(RenewableResource, self).__init__(cell_identifier,
                                                coordinates,
                                                neighbours,
                                                stocks
                                                )
        self.capacity = capacity
        self.growth_rate = growth_rate
        self.current_stock = current_stock

        self.stocks[0, 0] = self.capacity
        self.stocks[0, 1] = self.current_stock
        self.stocks[0, 2] = self.growth_rate

    def __str__(self):
        """
        Returns a string representation of the object of class
        'Renewable_Stock'.
        """
        return (super(RenewableResource, self).__str__() +
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
            self.stocks[0, 0] = capacity

    def set_growth_rate(self, growth_rate):
            """
            A function to set the growth_rate of the renewable resource
            """
            self.growth_rate = growth_rate
            self.stocks[0, 1] = growth_rate

    def set_current_stock(self, current_stock):
            """
            A function to set the current stock of the renewable resource
            """
            self.current_stock = current_stock
            self.stocks[0, 1] = current_stock

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
        return[
               ("renewable stock", 
                "ODE", 
                [renewable_stock_],
                self.renewable_stock_dynamics)
               ]

    def renewable_stock_dynamics(self, state, time):
        """
        The following ODE describes the dynamics of the renewable
        ressource through logistic growth (cf. Wiedermann 2015).
        Required variables are capacity and growth_rate. Variable y is the
        stock of the renewable resource.

        Parameters
        ---------
        state : float
            The current state for the ODE
        time : float
            Time for the ODE
        """
        a = self.growth_rate
        K = self.capacity
        dydt = a * state * (1 - state / K)
        return [dydt]
