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
#  Define class LocalStocks
#


class Cells(object):
    """
    Encapsulates states and dynamics of global environmental stocks.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 cell_identifier,
                 coordinates):
        """
        Initialize an instance of LocalStocks.
        """

        self.cell_identifier = cell_identifier
        self.coordinates = None

    def __str__(self):
        """
        Return a string representation of the object of class cells
        """
        return ('Cell with identifier % s, \
                coordinates % s'
                ) % (
                self.cell_identifier,
                self.coordinates
                )

    def set_coordinates(self, coordinates):
        """
        A function to get the coordinates from the identifiers of each cell
        """
        self.coordinates = coordinates

    #
    #  Definitions of further methods
    #
