"""Cell entity type mixing of class maxploit_simple_extraction."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from pycopancore import ODE
from .. import interface as I


class Cell(I.Cell):
    """Cell entity type mixin implementation class."""

    # standard methods:

    # def __init__(self,
    #              *,
    #              stock=1,
    #              growth_rate=1,
    #              **kwargs
    #              ):
    #     """Initialize an instance of Cell."""
    #     super().__init__(**kwargs)
    #
    #     self.stock = stock
    #     self.growth_rate = growth_rate

    # def deactivate(self):
    #     """Deactivate a cell."""
    #     TODO: add custom code here:
    #     super().deactivate()  # must be the last line

    # def reactivate(self):
    #     """Reactivate a cell."""
    #     super().reactivate()  # must be the first line
    #     TODO: add custom code here:
    # process-related methods:

    def harvesting(self, t):
        """Compute the harvesting dynamics.

        Parameters
        ----------
        t : float
            time

        Returns
        -------

        """
        self.d_stock -= self.individual.get_harvest_rate()

    processes = [ODE('harvesting function', [I.Cell.stock], harvesting)]
