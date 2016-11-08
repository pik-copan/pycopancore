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

import numpy as np

#
#  Define class Cell
#


class Cell(object):
    """
    Encapsulates states and dynamics of global environmental stocks.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 cell_identifier,
                 coordinates=None,
                 neighbours=None,
                 stocks=np.full((10, 3), np.nan)
                 ):
        """
        Initialize an instance of LocalStocks.

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
        """

        self.cell_identifier = cell_identifier
        self.coordinates = None
        self.neighbours = None
        self.stocks = stocks

    def __str__(self):
        """
        Return a string representation of the object of class cells
        """
        return ('Cell with identifier % s, \
                coordinates % s, \
                neighbours % s, \
                stock % s'
                ) % (
                self.cell_identifier,
                self.coordinates,
                self.neighbours,
                self.stocks
                )

    def set_coordinates(self, coordinates):
        """
        A function to set the coordinates from the identifiers of each cell
        """
        self.coordinates = coordinates

    def set_stocks(self, stocks):
        """
        A function to set the stock of a cell.
        """
        self.stocks = stocks

    def set_neighbours(self, neighb):
        """
        A function to set neighbours

        Parameters
        ----------
        neighb : list
            This is a list with identifiers of other cells which are
            neighbouring
        """

    #
    #  Definitions of further methods
    #
