"""The dummy cell module has some dynamics.

That's about it.
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

from pycopancore import ODE, Step, Explicit, Event
from pycopancore.model_components import abstract
from .interface import Cell_

#
#  Define class Cell
#


class Cell(Cell_, abstract.Cell):
    """Define properties of dummy cell.

    Inherits from Cell_ as the interface
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
                 step_width=2,
                 last_execution=None,
                 **kwargs
                 ):
        """Initialize an instance of Cell."""
        super(Cell, self).__init__(**kwargs)

        self.resource = resource
        self.capacity = capacity
        self.event_value = event_value
        self.explicit_value = explicit_value
        self.step_resource = step_resource
        self.step_width = step_width
        self.last_execution = last_execution

    #
    #  Definitions of further methods
    #

    def a_ode_function(self, t):
        """Add a d_resource to resource.

        Just a test function for ODEs.
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
        self.d_resource += b * growth_rate * (1 - b / a)

    def a_step_function(self, t):
        """Add something to step_resource.

        Another testfunction with dummy dynamics.
        Parameters
        ----------

        Returns
        -------
        return_list : list
            [first execution-time, time-step, new step_resource]
        """
        nt = self.step_timing(t)
        assert t == nt, "it's not time yet, t = %r and not %r" % (t, nt)
        self.step_resource += 2
        self.last_execution = t
        self.resource += -0.1

    def a_event_function(self, t):
        """Add 1 to event_value.

         Another dumb test function.
        Parameters
        ----------

        Returns
        -------
        """
        self.event_value += 1

    def step_timing(self,
                    t):
        """Return the next time step is to be called.

        This function is used to geet to know when the step function is
        to be called.
        Parameters
        ----------
        t

        Returns
        -------

        """
        if isinstance(self.last_execution, type(None)):
            self.last_execution = 0
        if t < self.last_execution:
            print('last execution time after t!')

        return self.last_execution + self.step_width

    def a_explicit_function(self, t):
        """Add something to explicit_value.

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
             [step_timing,
              a_step_function]),
        Event('event_function',
              [Cell_.event_value],
              ['rate', 0.1, a_event_function]),
        Explicit('explicit_function', [Cell_.explicit_value],
                 a_explicit_function)
                 ]
