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

    def market_clearing_rhs(self, logp_and_logws, th, world):
        """Do the market clearing for all individuals in the world.

        Return right hand side of equation to optimize all agents' utility.
        Parameters
        ----------
        logp_and_logws: list
            list with log of current price of water and all individuals' log
            of nutrition.
        th: float
            total harvest of water in a world
        world: object
            world object in which market takes place
        self: entity object
            Metabolism of the world in which the market clearing is calculated

        Returns
        -------
        errors: numpy.array
            1 D array with equations to be solved by fsolve
        """
        price = np.exp(logp_and_logws[0])
        ws = np.exp(logp_and_logws[1:])
        errors = np.zeros(shape=len(logp_and_logws))
        for i, e in enumerate(world.individuals):
            # Get the individual's society's pdf of liquidity:
            sigma = e.society.liquidity_sigma
            loc = e.society.liquidity_loc
            median = e.society.liquidity_median
            # Calculate the subjects nutrition
            w_i = ws[i]
            # Calculate liquidity to get sri and f_y:
            y_i = (e.harvest - w_i) * price + e.gross_income
            # Calculate the individual's subjective income rank:
            sri = lognorm_cdf(x=y_i, sigma=sigma, median=median)
            pdf = lognorm_pdf(x=y_i, sigma=sigma, median=median)
            # Get the rhs of the equation for the individual
            errors[1 + i] = (sri - (w_i * price * pdf
                                    )
                             ) / (2 * np.sqrt(w_i * sri))
        # Sum over liquidity must be equal to sum over gross income:
        errors[0] = sum(ws) - th
        # return rhs of the system of equations:
        # print('errors during solve', errors)
        return errors

    def do_market_clearing(self, unused_t):
        """Calculate water price and market movements."""
        print('market cleraing takes place at time', unused_t)
        # Iterate through worlds
        for w in self.worlds:
            world = w
            # Calculate pdfs for all societies:
            for s in world.societies:
                s.liquidity_pdf()
            log_nutritions = []
            for i in world.individuals:
                nutrition = i.harvest - (i.liquidity - i.gross_income) / world.water_price
                log_nutritions.append(np.log(nutrition))
            logp_and_logws = [np.log(world.water_price)] + log_nutritions
            # Get total gross income once, so that it doesn't need to be
            # calculated each time the function is called:
            tgi = world.total_gross_income
            th = world.total_harvest
            solution = optimize.root(fun=self.market_clearing_rhs,
                                     x0=logp_and_logws,
                                     args=(th, world),
                                     method='lm',
                                     options={'ftol': 0.01}
                                     )
            if solution['success'] is not True:
                print('solution', solution)
                raise BaseException('Market clearing has failed!')
            world.water_price = np.exp(solution['x'][0])
            for i, e in enumerate(world.individuals):
                # Account for shift, since price of water is at first position
                # of list, write solution of market clearing into entities:
                e.nutrition = np.exp(solution['x'][i+1])
                # Calculate liquidity:
                # nutrition = harvest-(liquidity-gross_income)/water_price
                # liquidity = (harvest-nutrition)*water_price + gross_income
                e.liquidity = (e.harvest - e.nutrition) * world.water_price + e.gross_income
            print('market clearing is done at time', unused_t,
                  'price is now at', world.water_price)
            # Calculate liquidities again, so that sri can be calculated
            # correctly
            for s in world.societies:
                s.liquidity_pdf()

    def market_timing(self, t):
        """Define how often market clearing takes place."""
        return t + 1 / self.market_frequency

    processes = [
        Step("market clearing", [I.Individual.liquidity,
                                 I.World.water_price,
                                 I.Individual.nutrition],
             [market_timing, do_market_clearing])
    ]  # TODO: instantiate and list process objects here


def lognorm_pdf(x, sigma, median):
    """Own lognorm pdf function."""
    mu = math.log(median)
    output = 1 / (
        x * sigma * math.sqrt(2 * math.pi)
                  ) * math.exp(-(np.log(x) - mu) ** 2 / (2 * sigma ** 2))
    return output


def lognorm_cdf(x, sigma, median):
    """Own lognorm cdf function."""
    mu = math.log(median)
    output = 1/2 + math.erf((np.log(x)-mu)/(math.sqrt(2)*sigma)) / 2
    return output
