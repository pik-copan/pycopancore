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


class Individual(I.Individual):
    """Define properties of exploit_social_learning individual."""

    # standard methods:

    def __init__(self,
                 *,
                 strategy=0,
                 imitation_tendency=1,
                 rewiring_prob=0,
                 average_waiting_time=1,
                 **kwargs
                 ):
        """Initialize an instance of Individual."""
        super().__init__(**kwargs)  # must be the first line
        self.strategy = strategy
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

    # process-related methods:

    def get_harvest_rate(self):
        """Compute a random harvest rate of individual.

        This method should be overwritten with a method of the class
        simple_extraction.individual.
        """
        return np.random.rand()

    processes = []
