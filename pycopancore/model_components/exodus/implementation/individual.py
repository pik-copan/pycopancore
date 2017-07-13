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
from pycopancore import Event
import math, random
from scipy import stats


class Individual (I.Individual):
    """Individual entity type mixin implementation class."""

    # standard methods:

    def __init__(self,
                 *,
                 profession=None,
                 nutrition_need=1240,
                 liquidity=None,
                 nutrtiton=None,
                 **kwargs):
        """Initialize an instance of Cell."""
        super().__init__(**kwargs)  # must be the first line
        self.profession = profession
        self.nutrition_need = nutrition_need

        self._subjective_income_rank = None
        self._farm_size = None
        self._gross_income = None
        self.liquidity = liquidity
        self.nutrition = nutrtiton

        # At last, check for validity of all variables that have been
        # initialized and given a value:

        # Following method is defined in abstract_entity_mixin which is
        # inherited only by mixing in the model:
        self.assert_valid()

    @property
    def harvest(self):
        """Get the amount of water a farmer is harvesting"""
        return self.farm_size * self.cell.average_precipitation

    @property
    def utility(self):
        """Get the Cobb-Douglas utility of an individual"""
        # Have a measure to limit nutrition to 1:
        effective_nutrition = 1 - 1 / (self.nutrition / self.nutrition_need + 1)
        return math.sqrt(self.subjective_income_rank * effective_nutrition)
        # TODO: Add parameter to compensate for frequency of market clearing!
        # 1240 m^3 is the annual need

    @property
    def farm_size(self):
        """Get the farm size."""
        # Check, if not already been calculated:
        if self._farm_size is None:
            # If townsman, individual has no farm:
            if self.society.municipality_like is True:
                self._farm_size = 0
            # If farmer, distribute farm size:
            if self.society.municipality_like is False:
                # Let society distribute farm size
                self._farm_size = self.society.gross_income_or_farmsize
        return self._farm_size

    @property
    def gross_income(self):
        """Get the gross income."""
        # Check if not already been calculated:
        if self._gross_income is None:
            # Check if farmer or townsman:
            if self.society.municipality_like is True:
                # Let society distribute income:
                self._gross_income = self.society.gross_income_or_farmsize
            # If not townsman, income = 0
            if self.society.municipality_like is False:
                self._gross_income = 0
        return self._gross_income

    @property
    def subjective_income_rank(self):
        """Get subjective income rank of individual."""
        # Get parameters of the liquidity pdf:
        sigma, loc, mean = self.society.liquidity_pdf[0], \
                           self.society.liquidity_pdf[1], \
                           self.society.liquidity_pdf[2]
        # Calculate place in liquidity cdf:
        sri = stats.lognorm.cdf(self.liquidity,
                                s=self.society.liquidity_sigma,
                                loc=self.society.liquidity_loc,
                                scale=self.society.liquidity_mean)
        self._subjective_income_rank = sri
        return self._subjective_income_rank

    # process-related methods:
    def social_update_timer(t):
        """Calculate when a social update takes place"""

    def migrate_or_befriend(self, unused_t):
        """Do social update.
        
        Either migration or de- and re-friending takes place"""
        # List friends with different profession:
        distant_friends = []
        for friend in self.acquaintances:
            if self.profession is not friend.profession:
                distant_friends.append(friend)
        # Pick a distant friend if possible:
        if len(distant_friends) != 0:
            # chose one at random:
            chosen_one = random.choice(distant_friends)
            # Compare utility

    processes = [
        Event("social update",
              [I.Individual.society, I.Culture.acquaintance_network],
              "rate", social_update_timer, migrate_or_befriend)
    ]  # TODO: instantiate and list process objects here
