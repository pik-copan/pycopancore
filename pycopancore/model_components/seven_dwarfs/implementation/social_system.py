"""SocialSystem entity type class template.

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
from pycopancore.model_components.base import interface as B
# from .... import master_data_model as D
from pycopancore import ODE, Step, Explicit, Event
import numpy as np


class SocialSystem(I.SocialSystem):
    """SocialSystem entity type mixin implementation class."""

    # process-related methods:
    def register_dwarf(self, dwarf):
        """Connect dwarf with other individuals in network.

        When a dwarf is instantiated, this function is called and
        connects the dwarf with all other ones in its social_system."""
        for ind in self.individuals:
            if (ind not in dwarf.acquaintances
                    and dwarf != ind):
                # Add edge:
                self.culture.acquaintance_network.add_edge(dwarf, ind)
                print(self.culture.acquaintance_network.edges())
    processes = []
