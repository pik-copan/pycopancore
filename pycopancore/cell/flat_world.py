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

from local_renewable_resource import RenwableResource
from abstract_planet import Planet

#
# Define class flat_world
#

class FlatWorld(Planet):
    """
    Encasulates THE GRID how to sort cells into a rectangular flat lattice.
    Also establishes a simple global athmospheric carbon stock
    """
    
    #
    # Definitions of internal methods
    #

    def __init__(self,
                 global_stocks,
                 grid,
                 planet_geometry
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
        """

        super(FlatWorld, self).__init__(global_stocks,
                                        grid,
                                        planet_geometry
                                        )

    def __str__(self):
        """
        Returns a string representation of an object of class FlatWorld
        """

        return (super(FlatWorld, self).__str__()
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
            local_renewable_resource.RenewableResource(i, None, None) \
            for i in range(N_c)
            ]

