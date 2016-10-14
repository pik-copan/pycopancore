# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
Encapsulates states and dynamics of global environmental stocks and 
the planets geometry.
"""

#
#  Imports
#


#
#  Define class GlobalStocks
#


class Planet(object):
    """
    Encapsulates states and dynamics of global environmental stocks.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 global_stocks,
                 grid,
                 planet_geometry):
        """
        Initialize an instance of GlobalStocks and THE GRID!

        Parameters
        ----------
        global_stocks : array?
            This are global stocks like athmospheric carbon or sun?
        grid : list/array?
            This defines where and how cells lie in respect to each other
        planet_geometry : ?
            Defines the geometry of the planet like egg-shaped or a torus
            or a crazy ball-shaped world, like earth!
        """

        self.global_stocks = global_stocks
        self.grid = grid
        self.planet_geometry = planet_geometry

    def __str__(self):
        """
        Returns a string representation of an object of class Planet
        """
        return('Planet with global stocks % s, \
                grid  % s, \
                planet_geometry % s'
                ) % (
                self.global_stocks, 
                self.grid,
                self.planet_geometry
                )

    def set_global_stocks(self, stocks):
        """
        A function to set the global stocks.

        Parameters
        ----------
        stocks: ?
            Whatever you want to put in here
        """
        self.global_stocks = stocks

    def set_grid(self, grid):
        """
        A function to set the grid
        """
        self.grid = grid

    def set_planet_geometry(self, geometry):
        """
        A function to set the planets geometry
        """
        self.planet_geometry = geometry

    #
    #  Definitions of further methods
    #
