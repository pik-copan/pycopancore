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
import math


class Individual (I.Individual):
    """Individual entity type mixin implementation class."""

    # standard methods:

    def __init__(self,
                 *,
                 profession=None,
                 subjective_income_rank=None,
                 nutrition_need=1240,
                 farm_size=None,
                 brutto_income=None,
                 liquidity=None,
                 nutrtiton=None,
                 **kwargs):
        """Initialize an instance of Cell."""
        super().__init__(**kwargs)  # must be the first line
        self.profession = profession
        self.subjective_income_rank = subjective_income_rank
        self.nutrition_need = nutrition_need

        self._farm_size = None
        self.farm_size = farm_size
        self._brutto_income = None
        self.brutto_income = brutto_income
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
        # 1240 m^3 is the annual need!

    @farm_size.setter
    def farm_size(self, society):
        """Set the farm size.

        Done accordingly to the distribution and population of the society.
        """
        if society.municipality_like is True:
            self._farm_size = 0
        if society.municipality_like is False:
            self._farm_size = society.brutto_income_or_farmsize

    @property
    def farm_size(self):
        """Get the farm size."""
        return self._farm_size

    @brutto_income.setter
    def brutto_income(self, society):
        """Set the brutto income.

        Done accordingly to the distribution and population of the society.
        """
        if society.municipality_like is True:
            self._brutto_income = society.brutto_income_or_farmsize
        if society.municipality_like is False:
            self._brutto_income = 0

    @property
    def brutto_income(self):
        """Get the brutto income."""
        return self._brutto_income

    # process-related methods:

    # TODO: add some if needed...

    processes = []  # TODO: instantiate and list process objects here
