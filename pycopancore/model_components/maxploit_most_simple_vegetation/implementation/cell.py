"""Cell entity type mixing of class maxploit_most_simple_vegetation."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from pycopancore import ODE
from pycopancore.model_components.simple_extraction import interface as I


class Cell(I.Cell):
    """Cell entity type mixin implementation class."""

    # standard methods:

    # def __init__(self,
    #              *,
    #              stock=1,
    #              capacity=1,
    #              growth_rate=1,
    #              **kwargs
    #              ):
    #     """Initialize an instance of Cell."""
    #     super().__init__(**kwargs)
    #
    #     self.stock = stock
    #     self.capacity = capacity
    #     self.growth_rate = growth_rate
    #
    #     pass
    #
    # def deactivate(self):
    #     """Deactivate a cell."""
    #     TODO: add custom code here:
    #     pass
    #     super().deactivate()  # must be the last line

    # def reactivate(self):
    #     """Reactivate a cell."""
    #     super().reactivate()  # must be the first line
    #     TODO: add custom code here:
    #     pass

    # process-related methods:

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
        self.d_stock += g * (1 - s / smax) * s

    # processes:

    processes = [
        ODE('logistic_growth_function',
            [I.Cell.stock],
            logistic_growth)
    ]
