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
                 coordinates,
                 stock
                 ):
        """
        Initialize an instance of LocalStocks.
        """

        self.cell_identifier = cell_identifier
        self.coordinates = None
        self.stock = None

    def __str__(self):
        """
        Return a string representation of the object of class cells
        """
        return ('Cell with identifier % s, \
                coordinates % s, \
                stock % s'
                ) % (
                self.cell_identifier,
                self.coordinates,
                self.stock
                )

    def set_coordinates(self, coordinates):
        """
        A function to get the coordinates from the identifiers of each cell
        """
        self.coordinates = coordinates

    def set_stock(self, stock):
        """
        A function to set the stock of a cell.
        """
        self.stock = stock

    #
    #  Definitions of further methods
    #
