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
from numpy.random import exponential

class Individual (I.Individual):
    """Individual entity type mixin implementation class."""

    def update_awareness(self, unused_t):
        """stochastically change awareness status depending on
        terrestrial carbon density.
        
        This method is called by Culture's awareness updating process
        """
        r = exponential()
        density = self.cell.terrestrial_carbon / self.cell.land_area
        if r * self.culture.awareness_lower_carbon_density > density: 
            self.is_environmentally_friendly = True
        elif r * self.culture.awareness_upper_carbon_density < density:
            self.is_environmentally_friendly = False

    processes = []
