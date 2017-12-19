"""World entity type mixing class template.

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

    def calc_total_gross_income(self, unused_t):
        """Calculate total gross income explicitly."""
        tgi = 0
        for individual in self.individuals:
            tgi += individual.gross_income
        self.total_gross_income = tgi

    def calc_total_harvest(self, unused_t):
        """Calculate total harves exlicitly"""
        th = 0
        for individual in self.individuals:
            th += individual.harvest
        self.total_harvest = th

    def calc_total_nutrition(self, unused_t):
        """Calculate total nutrition explicitly."""
        """Get the total nutrition."""
        tn = 0
        for individual in self.individuals:
            # print(individual.nutrition)
            tn += individual.nutrition
            if numpy.isnan(tn):
                self.exception_checker = True
                # raise BaseException('some individuals nutrition is nan!')
                print('some individuals nutrition is nan!')
        self.total_nutrition = tn

    def calc_total_liquidity(self, unused_t):
        """Calculate total liquidity explicitly."""
        tl = 0
        for individual in self.individuals:
            # print(individual.liquidity)
            tl += individual.liquidity
            if numpy.isnan(tl):
                self.exception_checker = True
                # raise BaseException('some individuals liquidity is nan!')
                print('some individuals nutrition is nan!')
        self.total_liquidity = tl

    def check_for_exceptions(self):
        """Check if the market equilibrium is still in order."""
        if self.exception_checker is True:
            return self.exception_checker
        else:
            return False

    processes = [
        Explicit('calculate total gross income',
                 [I.World.total_gross_income],
                 calc_total_gross_income),
        Explicit('calculate total harvest',
                 [I.World.total_harvest],
                 calc_total_harvest),
        Explicit('calculate total nutrition',
                 [I.World.total_nutrition],
                 calc_total_nutrition),
        Explicit('calculate total liquidity',
                 [I.World.total_liquidity],
                 calc_total_liquidity)
        ]
