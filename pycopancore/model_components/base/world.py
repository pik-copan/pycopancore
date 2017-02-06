"""Define base.world class.

In this module the basic World mixing class is composed to set the basic
structure for the later use in the model used World class. It Inherits from
World_ in that basic variables and parameters are defined.
"""
# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate Impact
# Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

#
#  Imports
#

from pycopancore.model_components import abstract
from .interface import World_

# Should the type of graph already be determined?
# Like igraph, networkx, sparse matrix, ...?
# from igraph import Graph


class World (World_, abstract.World):
    """Define properties of base.world.

    Basic World mixin class that every model must use in composing their World
    class. Inherits from World_ as the interface with all necessary variables
    and parameters.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self, *,
                 contact_network=None,
                 **kwargs
                 ):
        """Initialize an instance of World.

        Parameters
        ----------
        contact_network
        """
        super().__init__(**kwargs)

        if len(self.__class__.entities) > 1:
            raise ValueError('Only one world allowed!')

        self.contact_network = contact_network

    processes = []

#
#  Definitions of further methods
#
