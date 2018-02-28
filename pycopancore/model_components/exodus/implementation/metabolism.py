"""Metabolism process taxon mixin class template.

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
from pycopancore import Step, Explicit

from scipy import optimize
import numpy as np
import math


class Metabolism (I.Metabolism):
    """Metabolism process taxon mixin implementation class."""

    # standard methods:

    def __init__(self,
                 *,
                 market_frequency=1,
                 **kwargs):
        """Initialize the unique instance of Metabolism."""
        super().__init__(**kwargs)  # must be the first line

        self.market_frequency = market_frequency

        # At last, check for validity of all variables that have been
        # initialized and given a value:

        # Following method is defined in abstract_process_taxon_mixin which is
        # inherited only by mixing in the model:
        self.assert_valid()

    @property
    def total_gross_income(self):
        """Get the total gross income."""
        # Chose a world as world. When having several, this must be changed!
        for w in self.worlds:
            world = w
            break
        tgi = 0
        for individual in world.individuals:
            tgi += individual.gross_income
        return tgi

    # process-related methods:

    def do_market_clearing(self, unused_t):
        """Calculate water price and market movements."""
        print('market clearing takes place at time', unused_t)
        # Iterate through worlds
        for w in self.worlds:
            world = w
            w.calc_total_harvest(unused_t)
            w.calc_total_gross_income(unused_t)
            price = world.water_price = w.total_gross_income / w.total_harvest
            for ind in w.individuals:
                ind.nutrition = (ind.gross_income + price * ind.harvest) / (
                    2 * price)
                ind.liquidity = (ind.gross_income + price * ind.harvest) / 2
            w.calc_total_nutrition(unused_t)
            w.calc_total_liquidity(unused_t)
            tgi = world.total_gross_income
            th = world.total_harvest
            tn = world.total_nutrition
            tl = world.total_liquidity
            print('market clearing is done at time', unused_t,
                  'price is now at', world.water_price)
            # Break condition if suppy and demand are not equal:
            if round(tn) != round(th):
                print('Market clearing failed')
                print('nutrition - harvest', tn - th,
                      'income - liquidity', tgi-tl)
                self.non_equilibrium_checker = True

    def market_timing(self, t):
        """Define how often market clearing takes place."""
        return t + 1 / self.market_frequency

    def check_for_market_equilibrium(self):
        """Check if the market equilibrium is still in order."""
        if self.non_equilibrium_checker is True:
            return self.non_equilibrium_checker
        else:
            return False

    processes = [
        Step("market clearing",
             [B.Metabolism.worlds.individuals.liquidity,
              B.Metabolism.worlds.water_price,
              B.Metabolism.worlds.individuals.nutrition
              ],
             [market_timing,
              do_market_clearing]
             )
    ]  # TODO: instantiate and list process objects here
