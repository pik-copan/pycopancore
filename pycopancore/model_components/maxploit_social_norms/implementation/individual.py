"""Individual entity type of the component exploit_social_learning."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from .. import interface as I
import numpy as np
from pycopancore.model_components.base import interface as B

from .... import Explicit

class Individual(I.Individual):
    """Define properties of exploit_social_learning individual."""

    # standard methods:

    def __init__(self,
                 *,
                 behaviour=0,
                 attitude=0,
                 imitation_tendency=1,
                 rewiring_prob=0,
                 average_waiting_time=1,
                 **kwargs
                 ):
        """Initialize an instance of Individual."""
        super().__init__(**kwargs)  # must be the first line
        self.behaviour = behaviour
        self.attitude = attitude
        self.imitation_tendency = imitation_tendency
        self.rewiring_prob = rewiring_prob
        self.average_waiting_time = average_waiting_time
        self.update_time = np.random.exponential(self.average_waiting_time)

        pass

    def __lt__(self, other):
        """Make objects sortable."""
        return self._uid < other._uid

    def deactivate(self):
        """Deactivate an individual."""
        # TODO: add custom code here:
        pass
        super().deactivate()  # must be the last line

    def reactivate(self):
        """Reactivate an individual."""
        super().reactivate()  # must be the first line
        # TODO: add custom code here:
        pass

    # @profile
    def get_descriptive_norms(self, unused_t):
        """Calculate the mean behaviour of neighbouring individuals, which is taken to represent a descriptive norm."""
        if list(self.acquaintances):
            n = 0
            for i in list(self.acquaintances):
                if i.behaviour:
                    n += 1
            N = len(list(self.acquaintances))
            self.descriptive_norm = n/N
            if n/N > self.culture.majority_threshold:
                self.descriptive_norm_binary = 1
            else:
                self.descriptive_norm_binary = 0

    def get_harvest(self):
        """Compute the harvest rate of the individual on its cell.

        Returns
        -------
        harvest : float
        """
        effort = 0.5 * 1 * (3 - 2 * self.behaviour)
        harvest = effort * self.cell.stock
        return harvest

    processes = []
        # [Explicit("descriptive norm",
        #                   [I.Individual.descriptive_norm],
        #                   B.Individual.sum.acquaintances.behaviour / B.Individual.sum(B.Individual.acquaintances.behaviour**0)
        #                   )]
