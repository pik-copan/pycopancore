"""Individual entity type class template.
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
from numpy import arctan, log, pi, random

class Individual (I.Individual):
    """Individual entity type mixin implementation class."""

    def learn_environmental_friendliness(self, unused_t):
        """stochastically change environmental friendliness status depending on
        acquaintances' environmental friendliness.
        
        This method is called by Culture's learning process
        """
        # choose random acquaintance if there are any:
        neighbors = self.culture.acquaintance_network.neighbors(self)
        if len(neighbors) == 0:
            return
        other = random.choice(neighbors)
        # consider imitating her if your traits differ:
        othertrait = other.is_environmentally_friendly
        if othertrait == self.is_environmentally_friendly:
            return
        # compute quotient of respective terrestrial carbon densities:
        here = self.cell
        there = other.cell
        cul = self.culture
        slope = cul.environmental_friendliness_learning_probability_characteristic_slope
        offset = cul.environmental_friendliness_learning_density_quotient_offset
        quotient = ((there.terrestrial_carbon / there.land_area) /
                    (here.terrestrial_carbon / here.land_area))
        # imitate other with probability = sigmoid-shaped function of quotient: 
        if random.uniform() < (1/2 
                + 1/pi * arctan(pi * slope * log(quotient / offset))):
            self.is_environmentally_friendly = othertrait

    processes = []
