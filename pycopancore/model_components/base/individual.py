# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
In this module the basic Individual mixing class is composed to set the basic
structure for the later in the model used Indvidual class. It Inherits from
Individual_ in that basic variables and parameters are defined.
"""

#
#  Imports
#

from pycopancore import Variable
from .interface import Cell_, Nature_, Individual_, Culture_, Society_, Metabolism_, Model_

#
#  Define class Individual
#


class Individual(Individual_):
    """
    Basic Individual mixin class that every model must use in composing their
    Individual class. Inherits from Individual_ as the interface with all necessary
    variables and parameters.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 # *,
                 cell=None,
                 **kwargs
                 ):
        """
        Initialize an instance of Individual.

        Parameters
        ----------
        cell:
        kwargs:
        """
        super(Individual, self).__init__(**kwargs)

        assert isinstance(cell, Cell_), "cell must be an instance of Cell"
        self.cell = cell

    def __str__(self):
        """
        Return a string representation of the object of class Individual.
        """

    processes = []

    #
    #  Definitions of further methods
    #
