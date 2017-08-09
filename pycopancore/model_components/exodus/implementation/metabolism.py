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
        # Chose a world as world. When having several, this must be changed!
        for w in self.worlds:
            world = w
            break
        tgi = 0
        for individual in world.individuals:
            tgi += individual.gross_income
        return tgi

    # process-related methods:

    def market_clearing_rhs(self, logp_and_logys, tgi):
        """Do the market clearing for all individuals in the world.

        Return right hand side of equation to optimize all agents' utility.
        Parameters
        ----------
        logp_and_logys: list
            list with log of current price of water and all individuals' log
            of liquidity.
        self: entity object
            Metabolism of the world in which the market clearing is calculated

        Returns
        -------
        errors: numpy.array
            1 D array with equations to be solved by fsolve
        """
        price = np.exp(logp_and_logys[0])
        ys = np.exp(logp_and_logys[1:])
        errors = np.zeros(shape=len(logp_and_logys))
        total_gross_income = tgi
        # Chose a world as world. When having several, this must be changed!
        for w in self.worlds:
            world = w
            break
        for i, e in enumerate(world.individuals):
            # Get the individual's society's pdf of liquidity:
            sigma = e.society.liquidity_sigma
            loc = e.society.liquidity_loc
            median = e.society.liquidity_median
            # Calculate the individual's subjective income rank:
            sri = stats.lognorm.cdf(ys[i],
                                    s=sigma,
                                    loc=loc,
                                    scale=median)
            # Calculate the subjects nutrition
            w_i = e.harvest - ((ys[i] - e.gross_income) / price)
            # Get the rhs of the equation for the individual
            errors[1 + i] = (sri - (w_i * price * stats.lognorm.pdf(ys[i],
                                                                    s=sigma,
                                                                    loc=loc,
                                                                    scale=median
                                                                    )
                                    )
                             ) / (2 * np.sqrt(w_i * sri))
        # Sum over liquidity must be equal to sum over gross income:
        errors[0] = sum(ys) - total_gross_income
        # return rhs of the system of equations:
        return errors

    def do_market_clearing(self, unused_t):
        """Calculate water price and market movements."""
        print('market cleraing takes place at time', unused_t)
        # Chose a world as world. When having several, this must be changed!
        for w in self.worlds:
            world = w
            break
        # Calculate pdfs for all societies:
        for s in world.societies:
            s.liquidity_pdf()
        log_liquidities = []
        for i in world.individuals:
            log_liquidities.append(np.log(i.liquidity))
        logp_and_logys = [np.log(self.water_price)] + log_liquidities
        # Get total gross income once, so that it doesn't need to be
        # calculated each time the function is called:
        tgi = self.total_gross_income
        solution = optimize.root(fun=self.market_clearing_rhs,
                                 x0=logp_and_logys,
                                 args=(tgi)
                                 # method='broyden1'
                                 )
        print(solution)
        self.water_price = np.exp(solution['x'][0])
        print('solution', solution)
        for i, e in enumerate(world.individuals):
            # Account for shift, since price of water is at first position of
            # list, write solution of market clearing into entities:
            e.liquidity = np.exp(solution['x'][i+1])
            # Calculate amount of water traded:
            # traded water = - traded money / price
            # traded money = liquidity - gross_income
            traded_water = - (e.liquidity - e.gross_income) / self.water_price
            e.nutrition = e.harvest + traded_water
        print('market clearing is done at time', unused_t,
              'price is now at', self.water_price)
        # Calculate liquidities again, so that sri can be calculated correctly
        for s in world.societies:
            s.liquidity_pdf()

    def market_timing(self, t):
        """Define how often market clearing takes place."""
        return t + 1 / self.market_frequency

    processes = [
        Step("market clearing", [I.Individual.liquidity,
                                 I.Metabolism.water_price],
             [market_timing, do_market_clearing])
    ]  # TODO: instantiate and list process objects here
