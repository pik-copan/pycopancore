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
            w_i = ws[i]
            y_i = (e.harvest - w_i) * price + e.gross_income
            av_y = e.society.average_liquidity
            # Get the rhs of the equation for the individual
            errors[1 + i] = ((y_i - w_i * price)
                             # / (2 * math.sqrt(w_i * y_i * av_y))
                             )
        # Sum over nutrition must be equal to total harvest:
        errors[0] = sum(ws) - th
        # print('sum=sum?', errors[0])
        # return rhs of the system of equations:
        # print('errors during solve', errors)
        return errors

    def do_market_clearing(self, unused_t):
        """Calculate water price and market movements."""
        print('market clearing takes place at time', unused_t)
        # Iterate through worlds
        for w in self.worlds:
            world = w
            log_nutritions = []
            for i in world.individuals:
                nutrition = i.nutrition
                log_nutritions.append(np.log(nutrition))
            logp_and_logws = [np.log(world.water_price)] + log_nutritions
            # Get total harvest once, so that it doesn't need to be
            # calculated each time the function is called:
            w.calc_total_harvest(unused_t)
            th = world.total_harvest
            solution = optimize.root(fun=self.market_clearing_rhs,
                                     x0=logp_and_logws,
                                     args=(th, world),
                                     method='lm',
                                     options={'ftol': 0.01}
                                     )
            if solution['success'] is not True:
                print('solution', solution)
                print('Market clearing has failed!')
                self.non_equilibrium_checker = True
            print('water price=', np.exp(solution['x'][0]))
            world.water_price = np.exp(solution['x'][0])
            for i, e in enumerate(world.individuals):
                # Account for shift, since price of water is at first position
                # of list, write solution of market clearing into entities:
                e.nutrition = np.exp(solution['x'][i+1])
                # Calculate liquidity:
                # nutrition = harvest-(liquidity-gross_income)/water_price
                # liquidity = (harvest-nutrition)*water_price + gross_income
                e.liquidity = (e.harvest - e.nutrition) * world.water_price + e.gross_income
            w.calc_total_gross_income(unused_t)
            w.calc_total_harvest(unused_t)
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
            # Calculate liquidities again, so that sri can be calculated
            # correctly
            #for s in world.societies:
            #    s.liquidity_pdf()

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
