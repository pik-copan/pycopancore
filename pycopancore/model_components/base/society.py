"""Define the base society class.

In this module the basic Society mixing class is composed to set the basic
structure for the later in the model used Society class. It Inherits from
Society_ in that basic variables and parameters are defined.
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

from pycopancore.model_components import abstract
from .interface import Society_, World_

#
#  Define class Society
#


class Society(Society_, abstract.Society):
    """Define class base.society.

    Basic Society mixin class that every model must use in composing their
    Society class. Inherits from Society_ as the interface with all necessary
    variables and parameters.
    """

    # standard methods:

    def __init__(self,
                 # *,
                 population=0,
                 **kwargs
                 ):
        """Initialize an instance of Society.

        Parameters
        ----------
        population:
        kwargs:
        """
        super().__init__(**kwargs)

        assert population >= 0, "population must be >= 0"
        self.population = population


    # setters for references:
    
    @world.setter
    def world(self, w):
        assert isinstance(w, World_)
        if self.world is not None: self.world.societies.remove(self) 
        w.societies.add(self) 
        self.world = w


    processes = []

