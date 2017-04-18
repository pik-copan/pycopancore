"""The simple_extraction cell module."""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from pycopancore import ODE
from pycopancore.model_components import abstract
from . import interface as I


class Cell(I.Cell, abstract.Cell):
    """Define properties of simple_extraction cell.

    Inherits from I.Cell as the interface
    with all necessary variables and parameters.
    """

    def __init__(self,
                 *,
                 stock=1,
                 growth_rate=1,
                 **kwargs
                 ):
        """Initialize an instance of Cell."""
        super(Cell, self).__init__(**kwargs)

        self.stock = stock
        self.growth_rate = growth_rate

        self.individual = None

    def harvest(self, t):
        """Compute the harvesting dynamics.

        Parameters
        ----------
        t : float
            time

        Returns
        -------

        """
        # strat = self.individual.strategy
        # effort = 0.5 * self.growth_rate * (3 - 2 * strat)
        # self.d_stock -= effort * self.stock
        self.d_stock -= self.individual.get_harvest_rate()

    processes = [ODE('harvesting function', [I.Cell.stock], harvest)]
