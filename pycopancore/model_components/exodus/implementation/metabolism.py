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
from pycopancore import Step

from scipy import stats, optimize
import numpy as np


class Metabolism (I.Metabolism):
    """Metabolism process taxon mixin implementation class."""

    # standard methods:

    def __init__(self,
                 *,
                 water_price,
                 market_frequency=0.1,
                 **kwargs):
        """Initialize the unique instance of Metabolism."""
        super().__init__(**kwargs)  # must be the first line

        self.water_price = water_price
        self.market_frequency = market_frequency

        # At last, check for validity of all variables that have been
        # initialized and given a value:

        # Following method is defined in abstract_process_taxon_mixin which is
        # inherited only by mixing in the model:
        self.assert_valid()

    @property
    def total_gross_income(self):
        """Get the total gross income."""
        tgi = 0
        for individual in self.world.individuals:
            tgi += individual.gross_income
        return tgi

    # process-related methods:

    def market_clearing_rhs(met, p_and_ys):
        """Do the market clearing for all individuals in the world.

        Return right hand side of equation to optimize all agents' utility.
        Parameters
        ----------
        p_and_ys: list
            list with current price of water and all individuals' liquidity.
        met: entity object
            Metabolism of the world in which the market clearing is calculated

        Returns
        -------
        errors: numpy.array
            1 D array with equations to be solved by fsolve
        """
        price = p_and_ys[0]
        ys = p_and_ys[1:]
        errors = np.zeros(shape=len(p_and_ys))
        for i, e in enumerate(met.world.individuals):
            # Get the individual's society's pdf of liquidity:
            sigma = e.society.liquidity_sigma
            loc = e.society.liquidity_loc
            mean = e.society.liquidity_mean
            # Calculate the individual's subjective income rank:
            sri = stats.lognorm.cdf(ys[i],
                                    s=sigma,
                                    loc=loc,
                                    scale=mean)
            # Get the rhs of the equation for the individual
            errors[1 + i] = (sri - (e.harvest * price
                                    - ys[i] + e.gross_income
                                    )
                             * stats.lognorm.pdf(ys[i],
                                                 s=sigma,
                                                 loc=loc,
                                                 scale=mean
                                                 )
                             )
        # Sum over liquidity must be equal to sum over gross income:
        errors[0] = sum(ys) - met.total_gross_income
        # return rhs of the system of equations:
        return errors

    def do_market_clearing(self, unused_t):
        """Calculate water price and market movements."""
        print('market cleraing takes place at time', unused_t)
        # Calculate pdfs for all societies:
        for s in self.world.societies:
            s.liquidity_pdf()
        liquidities = []
        for i in self.world.individuals:
            liquidities.append(i.liquidity)
        p_and_ys = [self.water_price] + liquidities
        solution = optimize.fsolve(func=self.market_clearing_rhs,
                                   x0=p_and_ys)
        self.water_price = solution[0]
        for i, e in enumerate(self.world.individuals):
            # Account for shift, since price of water is at first position of
            # list, write solution of market clearing into entities:
            e.liquidity = solution[i+1]
            # Calculate amount of water traded:
            # traded water = - traded money / price
            # traded money = gross_income - liquidity
            traded_water = - (solution[i+1] - e.gross_income) / solution[0]
            e.nutririon = e.harvest + traded_water
        print('market clearing is done at time', unused_t)

    def market_timing(self, t):
        """Define how often market clearing takes place."""
        return t + 1 / self.market_frequency


    processes = [
        Step("market clearing", [I.Individual.liquidity,
                                 I.Metabolism.water_price],
             [market_timing, do_market_clearing])
    ]  # TODO: instantiate and list process objects here
