"""The most_simple_vegetation cell module has some dynamics of its resource."""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license


from pycopancore import ODE
# from pycopancore import Step, Explicit, Event
from pycopancore.model_components import abstract
from . import interface as I


class Cell(I.Cell, abstract.Cell):
    """Define properties of most_simple_vegetation cell.

    Inherits from Cell_ as the interface
    with all necessary variables and parameters.
    """

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
        # Why += and not = ?
        self.d_stock += g * (1 - s / smax) * s

    processes = [
        ODE('logistic_growth_function',
            [I.Cell.stock],
            logistic_growth)
        ]
