"""Individual entity type class template.

TODO: adjust or fill in code and documentation wherever marked by "TODO:",
then remove these instructions
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from .. import interface as I
#from .... import master_data_model as D

import random


class Individual (I.Individual):
    """Individual entity type mixin implementation class."""

    # standard methods:

    def __init__(self,
                 *,
                 initial_opinion,
                 **kwargs):
        """Initialize an instance of Individual."""
        super().__init__(**kwargs)  # must be the first line
        self.opinion = initial_opinion
        pass

    def __lt__(self, other):
        """make objects sortable, so big sorted lists can be used for quick look-ups"""
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

    # TODO: add some if needed...

    processes = []  # TODO: instantiate and list process objects here
