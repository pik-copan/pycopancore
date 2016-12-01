# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

"""
In this module a template for the Cell mixing class is composed to give an
example of the basic structure for the in the model used Cell class. It
Inherits from Cell_ in which variables and parameters are defined.
"""

#
#  Imports
#


from pycopancore import ODE
from .interface import Cell_  # , Nature_, Individual_, Culture_, Society_, Metabolism_, Model_

#
#  Define class Cell
#


class Cell(Cell_):
    """
    A template for the basic structure of the Cell mixin class that every model
    must use to compose their Cell class. Inherits from Cell_ as the interface
    with all necessary variables and parameters.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 # ,*,
                 capacity=None,
                 resource=None
                 **kwargs):
        """
        Initialize an instance of Cell.
        """
        super(Cell, self).__init__(**kwargs)

    def __str__(self):
        """
        Return a string representation of the object of class cells
        """

    processes = [
        ODE('growth_function', [Cell_.resource], a_growth_funtion)
                 ]

    #
    #  Definitions of further methods
    #

    def a_growth_funtion(self, t):
        """
        ODE
        Parameters
        ----------
        t

        Returns
        -------

        """
        a = self.capacity
        b = self.resource
        growth_rate = 0.5
        self.resource += b * growth_rate * (1 - b / a)
