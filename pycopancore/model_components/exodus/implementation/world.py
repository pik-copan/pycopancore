"""World entity type mixing class template.

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
import numpy
from pycopancore import Explicit
# from .... import master_data_model as D


class World (I.World):
    """World entity type mixin implementation class."""

    # standard methods:

    def __init__(self,
                 *,
                 water_price,
                 **kwargs):
        """Initialize an instance of World."""
        super().__init__(**kwargs)  # must be the first line

        self.water_price = water_price
        # At last, check for validity of all variables that have been
        # initialized and given a value:

        # Following method is defined in abstract_entity_mixin which is
        # inherited only by mixing in the model:
        self.assert_valid()

    @property
    def total_gross_income(self):
        """Get the total gross income."""
        tgi = 0
        for individual in self.individuals:
            tgi += individual.gross_income
        return tgi

    @property
    def total_harvest(self):
        """Get the total harvest."""
        th = 0
        for individual in self.individuals:
            th += individual.harvest
        return th

    @property
    def total_nutrition(self):
        """Get the total nutrition."""
        tn = 0
        for individual in self.individuals:
            # print(individual.nutrition)
            tn += individual.nutrition
            if numpy.isnan(tn):
                raise BaseException('some individuals nutrition is nan!')
        return tn

    @property
    def total_liquidity(self):
        """Get the total liquidity."""
        tl = 0
        for individual in self.individuals:
            # print(individual.liquidity)
            tl += individual.liquidity
            if numpy.isnan(tl):
                raise BaseException('some individuals liquidity is nan!')
        return tl

    # process-related methods:
    def normalize_utilities(self, unused_t):
        """Calculate the maximal utility to be able to normalize utilities."""
        max_u = 0
        for ind in self.individuals:
            if ind.utility > max_u:
                max_u = ind.utility
        # max_u = max(self.individuals.utility) somehow this is not yet possible
        for ind in self.individuals:
            ind.utility = ind.utility / max_u

    processes = [
        Explicit("normalize utilities",
                 [B.World.individuals.utility],
                 normalize_utilities)
        ]
