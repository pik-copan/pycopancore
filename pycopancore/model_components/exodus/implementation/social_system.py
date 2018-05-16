"""SocialSystem entity type mixing class template.

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
from pycopancore import Explicit, Step
# from .... import master_data_model as D

from scipy import stats
import numpy as np
import math
import random


class SocialSystem (I.SocialSystem):
    """SocialSystem entity type mixin implementation class."""

    # standard methods:

    def __init__(self,
                 *,
                 municipality_like=False,
                 base_mean_income=1000,
                 pdf_sigma=0.34,  # 0.34 taken from Clementi, Gallegati 2005 for income distribution
                 scaling_parameter=1.12, # taken from Bettencourt paper
                 migration_cost=1000,
                 last_one_standing=False,  # measures to ensure ergodicity
                 continuous_exploration=False,  # kind of a noise term
                 **kwargs):
        """Initialize an instance of SocialSystem."""
        super().__init__(**kwargs)  # must be the first line

        self.municipality_like = municipality_like
        self.base_mean_income = base_mean_income
        self.pdf_sigma = pdf_sigma
        self.scaling_parameter = scaling_parameter
        self.migration_cost = migration_cost
        self.migration_counter = [0, [], []]
        self.last_one_standing = last_one_standing
        self.continuous_exploration = continuous_exploration
        # Initializing self.migration_rates list with length of number of
        # social systems not possibble here, since not all social systems
        # are initialized yet.

    def calc_gross_income_or_farmsize(self):
        "Get random income or farm size distributed log-normal."

        # Use log-normal
        number = random.random()
        sigma = self.pdf_sigma
        # calculate ´median from mean:
        median = (self.mean_income_or_farmsize / np.exp(sigma**2 / 2))
        lognormal_random = stats.lognorm.ppf(number, s=sigma, scale=median)
        return lognormal_random

    def calc_population(self, unused_t):
        """Calculate the social_systems population explicitly.

        Parameters
        ----------
        unused_t
        """
        if len(self.individuals) == 0:
            self.deactivate()
            print(f'social_system {self} died out at time {unused_t}')
            # to prevent division by zero:
            self.population = 1
        else:
            self.population = len(self.individuals)

    def update_incomes(self):
        """Update incomes to adjust to population in some manner."""
        # first: Check if really a municipaity:
        if self.municipality_like is not True:
            raise SocialSystemTypeError('SocialSystem not a municipality')
        # Define factor how fast adjusting takes place
        factor = 0.5
        sum = 0
        for ind in self.individuals:
            sum += ind.gross_income
        # Now divide by number of individuals to get mean:
        real_mean = sum / self.population
        adaption_rate = self.mean_income_or_farmsize / real_mean
        adaption = adaption_rate + (1 - adaption_rate) * factor
        for ind in self.individuals:
            ind.gross_income *= adaption

    def update_farmsizes(self):
        """Update farmsizes to adjust to population."""
        # first: Check if really a county:
        if self.municipality_like is not False:
            raise SocialSystemTypeError('SocialSystem not a county')
        # Define factor how fast adjusting takes place
        factor = 0.5
        sum = 0
        for ind in self.individuals:
            sum += ind.farm_size
        # Now divide by number of individuals to get mean:
        real_mean = sum / self.population
        adaption_rate = self.mean_income_or_farmsize / real_mean
        adaption = adaption_rate + (1 - adaption_rate) * factor
        for ind in self.individuals:
            ind.farm_size *= adaption

    def update_timing(self, t):
        """Decide how often income and farm size are adjusted."""
        return t + 1

    def do_update(self, unused_t):
        """Do the adjustment of income or farmsize"""
        if self.is_active:
            if self.municipality_like is True:
                self.update_incomes()
                print('incomes updated of social_system', self)
            elif self.municipality_like is False:
                self.update_farmsizes()
                print('farmsizes updated of social_system', self)
            else:
                raise SocialSystemTypeError('Neither County nor Municipality!')

    def calculate_mean_income_or_farmsize(self, unused_t):
        """Calculate mean income (if municipality) or farm size (county)."""
        if self.is_active:
            if self.municipality_like:
                # in case of municipality
                total_income = self.base_mean_income * (
                    self.population**self.scaling_parameter)
                self.mean_income_or_farmsize = total_income / self.population
            if not self.municipality_like:
                # in case of county
                for c in self.direct_cells:
                    # mean farm size:
                    self.mean_income_or_farmsize = c.land_area / self.population

    def calculate_average_liquidity(self, unused_t):
        """Calculate average liquidity of social_system."""
        if self.is_active:
            sum = 0
            for ind in self.individuals:
                sum += ind.liquidity
            self.average_liquidity = sum / self.population
        else:
            # This should not happen, but apparently does nevertheless...
            self.average_liquidity = 1

    def calculate_average_utility(self, unused_t):
        """Calculate the average utility in this social_system."""
        if self.is_active:
            summe = 0
            for ind in self.individuals:
                summe += ind.utility
            self.average_utility = summe / self.population

    def calculate_gini(self, unused_t):
        """Calculate the gini coefficient of the utility. 
        
        This is using the Relative mean absolute difference:
        https://en.wikipedia.org/wiki/Mean_absolute_difference#Relative_mean_absolute_difference
        """
        # Mean absolute difference
        if self.is_active:
            utilities = []
            for ind in self.individuals:
                utilities.append(ind.utility)
            mad = np.abs(np.subtract.outer(utilities, utilities)).mean()
            # Relative mean absolute difference
            rmad = mad / np.mean(utilities)
            # Gini coefficient
            self.gini_coefficient = 0.5 * rmad

    def calculate_migration_rate(self, unused_t):
        """Calculate migration rates"""
        # First time this is called, a list of length of number of social
        # systems is generated:
        if self.migration_rates is None:
            self.migration_rates = [0] * len(self.world.social_systems)

        # Every time this is called, this list needs to be reset:
        for i in range(len(self.migration_rates)):
            self.migration_rates[i] = 0
        # The two above steps are not performed as one, since some social
        # systems might be deactivated during run, resulting in a new length
        # for the list.

        # Now copy this list for theoretical migration rates:
        self.theoretical_mig_rate = list(self.migration_rates)
        if self.is_active:
            # print(self.migration_counter)
            tot_tries = self.migration_counter[0]  # total number of tries
            mig_attempts = self.migration_counter[1]  # list of social systems where attempted
            mig_moves = self.migration_counter[2]  # list of social system where success

            # for the following to work, it is important, that we know the
            # smallest uid of the social systems and all other social systems
            # have following uids!
            min_uid = min(ss._uid for ss in self.world.social_systems)
            # attempted moves:
            attempt_list = self.migration_rates.copy()
            for element in mig_attempts:
                for i, soc in enumerate(attempt_list):
                    # since uids start with min_uid, we need to add it:
                    if str(element).endswith(str(i+min_uid)+']'):
                        attempt_list[i] += 1

            # successful moves:
            for element in mig_moves:
                for i, soc in enumerate(self.migration_rates):
                    # print(i)
                    # since uids start with min_uid, we need to add it:
                    if element._uid == i+min_uid:
                        self.migration_rates[i] += 1
            # Now divide success by attempts
            for i, el in enumerate(self.migration_rates):
                try:
                    self.migration_rates[i] = self.migration_rates[i]
                    # If probability is needed, following is needed:
                    #  self.migration_rates[i] = (self.migration_rates[i]
                    #                             / attempt_list[i])
                except ZeroDivisionError:
                    # Both entries 0
                    self.migration_rates[i] = 0

            # Theoretical Calculation:
            for ss in self.world.social_systems:
                # Put in values according to the uids. Since uids start with
                # min_uid, we have to account for that by subtracting it:
                self.theoretical_mig_rate[(ss._uid-min_uid)] = (1/2 + (
                    math.sqrt(ss.average_liquidity)
                    - math.sqrt(self.average_liquidity))/(4 * math.sqrt(
                    self.world.water_price * 1240))) * attempt_list[(ss._uid-min_uid)]
                # if probability is wanted, leave out * attempt_list[(ss._uid-min_uid)]
            # 1240 is the water need, also set in Individual.calculate_utility
            # print(self.migration_rates, self.theoretical_mig_rate)
            # reset migration counter for next step:
            self.migration_counter = [0, [], []]
            #print(self.migration_counter)

    processes = [
        Explicit('calculate population',
                 [B.SocialSystem.population,
                  # Following is only done to determine if soc is a city or
                  # not afterwards, since this is not saved otherwise:
                  I.SocialSystem.municipality_like],
                 calc_population),
        Explicit('calculate mean income or farmsize',
                 [I.SocialSystem.mean_income_or_farmsize],
                 calculate_mean_income_or_farmsize),
        Explicit("Calculate average liquidities",
                 [I.SocialSystem.average_liquidity],
                 calculate_average_liquidity),
        Explicit("Calculate average utilities",
                 [I.SocialSystem.average_utility],
                 calculate_average_utility),
        Explicit("Calculate gini",
                 [I.SocialSystem.gini_coefficient],
                 calculate_gini),
        Step("Calculate Migration Rates",
             [I.SocialSystem.migration_rates,
              I.SocialSystem.theoretical_mig_rate],
             [update_timing, calculate_migration_rate]),
        Step("Update incomes/farmsizes",
             [B.SocialSystem.individuals.farm_size,
              B.SocialSystem.individuals.gross_income],
             [update_timing, do_update])
    ]


class SocialSystemTypeError(Exception):
    """Error Class if wrong type of social_system."""
    pass
