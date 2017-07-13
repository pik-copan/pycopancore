"""Metabolism process taxon mixin class template.

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

from scipy import stats


class Metabolism (I.Metabolism):
    """Metabolism process taxon mixin implementation class."""

    # standard methods:

    def __init__(self,
                 *,
                 water_price,
                 **kwargs):
        """Initialize the unique instance of Metabolism."""
        super().__init__(**kwargs)  # must be the first line

        self.water_price = water_price

        # At last, check for validity of all variables that have been
        # initialized and given a value:

        # Following method is defined in abstract_process_taxon_mixin which is
        # inherited only by mixing in the model:
        self.assert_valid()

    # process-related methods:

    def market_clearing(self, individual):
        """Do the market clearing for all individuals in the world.
        
        Returns
        -------

        """
        # Calculate pdf of liquidities in society of individual:
        sigma = individual.society.liquidity_sigma,
        loc = individual.society.liquidity_loc,
        mean = individual.society.liquidity_mean
        liquidity = individual.liquidity
        individual_liquidity_pdf = stats.lognorm.pdf(liquidity,
                                                     s=sigma,
                                                     loc=loc,
                                                     scale=mean)
        # Return rhs of equation
        return (individual.subjective_income_rank
                - (individual.harvest * self.water_price
                   - individual.liquidity + individual.brutto_income)
                * individual_liquidity_pdf
                )


    # TODO: add some if needed...

    processes = []  # TODO: instantiate and list process objects here
