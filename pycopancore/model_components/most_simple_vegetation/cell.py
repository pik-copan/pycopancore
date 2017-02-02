"""The most_simple_vegetation cell module has some dynamics of its resource."""

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

from pycopancore import ODE
# from pycopancore import Step, Explicit, Event
from pycopancore.model_components import abstract
from .interface import Cell_

#
#  Define class Cell
#


class Cell(Cell_, abstract.Cell):
    """Define properties of most_simple_vegetation cell.

    Inherits from Cell_ as the interface
    with all necessary variables and parameters.
    """

    #
    #  Definitions of internal methods
    #

    def __init__(self,
                 *,
                 stock=1,
                 capacity=1,
                 growth_rate=1,
                 **kwargs
                 ):
        """Initialize an instance of Cell."""
        super(Cell, self).__init__(**kwargs)

        self.stock = stock
        self.capacity = capacity
        self.growth_rate = growth_rate

    #
    #  Definitions of further methods
    #

    def logistic_growth(self, t):
        """Compute the biophysical logistic growth function of cell's stock.

        Parameters
        ----------
        t : float
            time

        Returns
        -------

        """
        g = self.growth_rate
        s = self.stock
        smax = self.capacity
        # TODO:
        # Is this the right ode?
        self.d_stock += g * (1 - s / smax) * s

    # TODO:
    # not sure here what has to go into the processes list.
    # What is name, variables, specification, smoothness?
    processes = [
        ODE('logistic_growth_function',
            [Cell_.stock,
             Cell_.capacity,
             Cell_.growth_rate],
            logistic_growth)
        ]
