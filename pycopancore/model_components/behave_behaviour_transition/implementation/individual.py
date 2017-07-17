"""Individual entity type class template.

TODO: adjust or fill in code and documentation wherever marked by "TODO:",
then remove these instructions
"""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from .. import interface as I
# from .... import master_data_model as D

import numpy as np

class Individual (I.Individual):
    """Individual entity type mixin implementation class."""

    # standard methods:

    def __init__(self,
                 *,
                 initial_disposition = None,
                 degree_preference = None,
                 initial_behaviour = None,
                 **kwargs):
        """Initialize an instance of Individual."""
        super().__init__(**kwargs)  # must be the first line

        # set degree preference
        self.degree_preference = degree_preference

        # set disposition
        self.disposition = initial_disposition

        #set behaviour
        self.behaviour = initial_behaviour

        pass

    def deactivate(self):
        """Deactivate an individual."""
        # TODO: add custom code here:
        # remove individual from all networks
        pass
        super().deactivate()  # must be the last line

    def reactivate(self):
        """Reactivate an individual."""
        super().reactivate()  # must be the first line
        # TODO: add custom code here:
        # add individual to networks
        pass

    # process-related methods:

    # TODO: add some if needed...

    def get_characteristics(self):

        pass

    processes = []  # TODO: instantiate and list process objects here
