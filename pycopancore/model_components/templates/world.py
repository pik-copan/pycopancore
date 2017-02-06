"""World mixing class template.

It is composed to give an example of the basic structure for
the World class used in the model. It inherits from World_
in which variables and parameters are defined.
"""
# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

#
#  Imports
#

from .interface import World_
from pycopancore.model_components import abstract

#
#  Define class World
#


class World (World_, abstract.World):
    """Define your World class.

    A template for the basic structure of the World mixin class that every
    component may use to compose their World class.
    Inherits from World_ as the interface
    with all necessary variables and parameters.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 **kwargs
                 ):
        """Initialize an instant of World."""
        super().__init__(**kwargs)

    processes = []

    #
    #  Definitions of further methods
    #
