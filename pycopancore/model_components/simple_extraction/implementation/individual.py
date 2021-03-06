"""Individual entity type of the component simple_extraction."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from .. import interface as I


class Individual(I.Individual):
    """Define properties of simple_extraction individual."""

    # standard methods:

    def __init__(self,
                 *,
                 strategy=0,
                 **kwargs
                 ):
        """Initialize an instance of Individual."""
        super().__init__(**kwargs)  # must be the first line
        self.strategy = strategy


    def __lt__(self, other):
        """Make objects sortable."""
        return self._uid < other._uid

    def deactivate(self):
        """Deactivate an individual."""
        # TODO: add custom code here:

        super().deactivate()  # must be the last line

    def reactivate(self):
        """Reactivate an individual."""
        super().reactivate()  # must be the first line
        # TODO: add custom code here:


    # process-related methods:

    def get_harvest_rate(self):
        """Compute the harvest rate of the individual on its cell.

        Returns
        -------
        harvest : float
        """
        effort = 0.5 * self.cell.growth_rate * (3 - 2 * self.strategy)
        harvest = effort * self.cell.stock
        return harvest

    processes = []
