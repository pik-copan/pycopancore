# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
This is a simple class to test the Planet parent-class. It sorts the cells
into a rectangular grid of some sort and assignes cooridnates
"""

#
# Imports
#

import numpy as np
from local_renewable_resource import RenewableResource
from abstract_planet import Planet

#
# Define class flat_world
#


class DonutWorld(Planet):
    """
    Encasulates THE GRID how to sort cells into a rectangular lattice on a
    torus.
    Also establishes a simple global athmospheric carbon stock
    """

    #
    # Definitions of internal methods
    #

    def __init__(self,
                 global_stocks=None,
                 grid=None,
                 planet_geometry=None,
                 width=5,
                 height=3
                 ):
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
        width = integer
            Defines how many cells make the width or circumfrence of the torus
        height = integer
            Defines how many cells make the height of the torus
        """

        super(DonutWorld, self).__init__(global_stocks,
                                         planet_geometry,
                                         grid
                                         )
        self.width = width
        self.height = height
        self.grid = np.full((height, width), np.nan)

    def __str__(self):
        """
        Returns a string representation of an object of class FlatWorld
        """

        return (super(DonutWorld, self).__str__() +
                ('width % s, \
                 height % s'
                 ) % (
                 self.width,
                 self.height
                 )
                )

    def create_grid(self, x_dim, y_dim):
        """
        Create a grid of x_dim cells in x direction and y_dim cells in
        y direction.

        Parameters
        ----------
        x_dim : integer
            This defines how many cells shall be in x-direction
        y_dim : integer
            This defines how many cells shall be in y-direction
        """
        assert type(x_dim) == int
        assert type(y_dim) == int
        N_c = x_dim * y_dim

        # Now create cells

        List_c = [
            RenewableResource(i) for i in range(N_c)]

        # Now give them coordinates in respect to their place in the list

        for i in range(0, x_dim):
            for j in range(0, y_dim):
                # To get one less loop, use this to get index in list
                x = j * x_dim + i
                # Set coordinates
                List_c[x].set_coordinates((i, j))
                # Set grid
                self.grid[j, i] = List_c[x].cell_identifier

        # Now give neighbour information
        for i in range(0, N_c):
            # coordinates of i:
            coordinates = List_c[i].coordinates
            i = coordinates[0]
            j = coordinates[1]
            # upper neighbour
            a = self.grid[(j-1), i]
            # lower neighbour
            if j == (y_dim - 1):
                b = self.grid[0, i]
            else:
                b = self.grid[(j+1), i]
            # left neighbour
            c = self.grid[j, (i-1)]
            # right neighbour
            if i == (x_dim - 1):
                d = self.grid[j, 0]
            else:
                d = self.grid[j, (i+1)]
            List_c[i].set_neighbours((a, b, c, d))
