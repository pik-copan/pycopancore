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

import numpy as np
from pycopancore import ODE, Step, Explicit, Event
from pycopancore.model_components import abstract
from .interface import Cell_

#
#  Define class Cell
#


class Cell(Cell_, abstract.Cell):
    """
    A template for the basic structure of the Cell mixin class that every model
    must use to compose their Cell class. Inherits from Cell_ as the interface
    with all necessary variables and parameters.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 *,
                 resource=.5,
                 capacity=1,
                 step_resource=.3,
                 event_value=.2,
                 explicit_value=.1,
                 **kwargs
                 ):
        """
        Initialize an instance of Cell.
        """
        super(Cell, self).__init__(**kwargs)

        self.resource = resource
        self.capacity = capacity
        self.event_value = event_value
        self.explicit_value = explicit_value
        self.step_resource = step_resource

    def __str__(self):
        """
        Return a string representation of the object of class cells
        """

    #
    #  Definitions of further methods
    #

    def a_ode_function(self, t):
        """
        ODE
        Parameters
        ----------
        t : float
            time

        Returns
        -------

        """
        a = self.capacity
        b = self.resource
        growth_rate = 0.5
        self.resource = b * growth_rate * (1 - b / a)

    def a_step_function(self):
        """
        Step-Function

        Parameters
        ----------

        Returns
        -------
        return_list : list
            [first execution-time, time-step, new step_resource]
        """
        self.step_resource += 2

    def a_event_function(self):
        """
        Event-generating function
        Parameters
        ----------

        Returns
        -------
        """
        self.event_value += 1

    def step_timing(self, t):
        """
        Function to return next time of a step-function
        Parameters
        ----------
        t

        Returns
        -------

        """
        return t+1

    def a_explicit_function(self):
        """
        Explicit function, calculates something like fertilizer that is
        dependend on the current resource and capacity
        Returns
        -------

        """
        b = self.capacity
        c = self.resource
        self.explicit_value = 0.3 * b + c

    processes = [
        ODE('growth_function', [Cell_.resource], a_ode_function),
        Step('step_function',
             [Cell_.step_resource],
             [0.1,
              step_timing,
              a_step_function]),
        Event('event_function',
              [Cell_.event_value],
              ['rate', 0.1, a_event_function]),
        Explicit('explicit_function', [Cell_.explicit_value],
                 a_explicit_function)
                 ]
