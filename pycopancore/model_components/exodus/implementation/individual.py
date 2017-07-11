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
                 farm_size=None,
                 base_income=None,
                 liquidity=None,
                 nutrtiton=None,
                 **kwargs):
        """Initialize an instance of Cell."""
        super().__init__(**kwargs)  # must be the first line
        self.profession = profession
        self.subjective_income_rank = subjective_income_rank
        self.farm_size = farm_size
        self.base_income = base_income
        self.liquidity = liquidity
        self.nutrition = nutrtiton

        # At last, check for validity of all variables that have been
        # initialized and given a value:

        # Following method is defined in abstract_entity_mixin which is
        # inherited only by mixing in the model:
        self.assert_valid()

    @property
    def base_water(self):
        """Get the amount of water a farmer is harvesting"""
        return self.farm_size * self.cell.average_precipitation

    @property
    def utility(self):
        """Get the Cobb-Douglas utility of an individual"""
        return math.sqrt(self.subjective_income_rank * self.nutrition)


    # process-related methods:

    # TODO: add some if needed...

    processes = []  # TODO: instantiate and list process objects here
