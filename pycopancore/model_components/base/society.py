# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
In this module the basic Society mixing class is composed to set the basic
structure for the later in the model used Society class. It Inherits from
Society_ in that basic variables and parameters are defined.
"""

#
#  Imports
#

from pycopancore import Variable
from pycopancore.model_components import abstract
from .interface import Cell_, Nature_, Individual_, Culture_, Society_, Metabolism_, Model_

#
#  Define class Society
#


class Society(Society_, abstract.Society):
    """
    Basic Society mixin class that every model must use in composing their
    Society class. Inherits from Society_ as the interface with all necessary
    variables and parameters.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 # *,
                 population=0,
                 **kwargs
                 ):
        """
        Initialize an instance of Society.

        Parameters
        ----------
        population:
        kwargs:
        """
        super(Society, self).__init__(**kwargs)

        assert population >= 0, "population must be >= 0"
        self.population = population

    def __repr__(self):
        """
        Return a string representation of the object of class base.Society.
        """
        return (super().__repr__() +
                ('base.society object with population %r'
                 ) % (self.population)
                )

    processes = []

    #
    #  Definitions of further methods
    #
