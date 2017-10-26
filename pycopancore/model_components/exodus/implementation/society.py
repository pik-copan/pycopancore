"""Society entity type mixing class template.

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
from pycopancore import Explicit, Step
# from .... import master_data_model as D

from scipy import stats
import numpy as np
import math
import random


class Society (I.Society):
    """Society entity type mixin implementation class."""

    # standard methods:

    def __init__(self,
                 *,
                 municipality_like=False,
                 base_mean_income=1000,
                 pdf_sigma=0.34,  # 0.34 taken from Clementi, Gallegati 2005 for income distribution
                 scaling_parameter=1.12,
                 migration_cost=1000,
                 **kwargs):
        """Initialize an instance of Society."""
        super().__init__(**kwargs)  # must be the first line

        self.municipality_like = municipality_like
        self.base_mean_income = base_mean_income
        self.pdf_sigma = pdf_sigma
        self.scaling_parameter = scaling_parameter
        self.migration_cost = migration_cost

        self.liquidity_median = None
        self.liquidity_sigma = None
        self.liquidity_loc = None

    def calc_gross_income_or_farmsize(self):
        "Get random income or farm size distributed log-normal."

        # Use log-normal
        number = random.random()
        sigma = self.pdf_sigma
        # calculate ´median from mean:
        median = (self.mean_income_or_farmsize / np.exp(sigma**2 / 2))
        lognormal_random = stats.lognorm.ppf(number, s=sigma, scale=median)
        return lognormal_random

    def liquidity_pdf(self):
        """Calculate the PDF of the liquidity of the society."""
        print('liquidity_pdf is calculated for society', self)
        liquidities = []
        # Check if there are any individuals:
        if self.individuals:
            for individual in self.individuals:
                liquidities.append(individual.liquidity)
            self.liquidity_sigma, self.liquidity_loc, self.liquidity_median = (
                stats.lognorm.fit(liquidities, floc=0))
            print('sigma, loc, median are',
                  self.liquidity_sigma, self.liquidity_loc, self.liquidity_median)
            print('population is', self.population)
        else:
            print('Society died out')

    def calc_population(self, unused_t):
        """Calculate the societies population explicitly.

        Parameters
        ----------
        unused_t
        """
        if len(self.individuals) == 0:
            self.deactivate()
        self.population = len(self.individuals)

    def update_incomes(self):
        """Update incomes to adjust to population in some manner."""
        # first: Check if really a municipaity:
        if self.municipality_like is not True:
            raise SocietyTypeError('Society not a municipality')
        # Define epsilion, which functions as threshold to change incomes
        epsilon = 10
        # Define factor how fast adjusting takes place
        factor = 0.5
        sum = 0
        for ind in self.individuals:
            sum += ind.gross_income
        # Now divide by number of individuals to get mean:
        real_mean = sum / self.population
        # get delta:
        delta_mean = self.mean_income_or_farmsize - real_mean
        if delta_mean > epsilon and delta_mean > 0:
            # mean income is smaller than it should be, need to add
            # Define amount to add:
            to_add = delta_mean / self.population * factor
            for ind in self.individuals:
                ind.gross_income += to_add
        if delta_mean > epsilon and delta_mean < 0:
            # mean income is bigger than it should be, need to subtract
            # Define amount to subtract:
            to_subtract = delta_mean / self.population * factor
            for ind in self.individuals:
                ind.gross_income -= to_subtract
        # Else do nothing

    def update_farmsizes(self):
        """Update farmsizes to adjust to population."""
        # first: Check if really a county:
        if self.municipality_like is not False:
            raise SocietyTypeError('Society not a county')
        # Define epsilion, which functions as threshold to change farmsize
        epsilon = 10
        # Define factor how fast adjusting akes place
        factor = 0.5
        sum = 0
        for ind in self.individuals:
            sum += ind.farm_size
        # Now divide by number of individuals to get mean:
        real_mean = sum / self.population
        # get delta:
        delta_mean = self.mean_income_or_farmsize - real_mean
        if delta_mean > epsilon and delta_mean > 0:
            # mean farmsize is smaller than it should be, need to add
            # Define amount to add:
            to_add = delta_mean / self.population * factor
            for ind in self.individuals:
                ind.farm_size += to_add
        if delta_mean > epsilon and delta_mean < 0:
            # mean farmsize is bigger than it should be, need to subtract
            # Define amount to subtract:
            to_subtract = delta_mean / self.population * factor
            for ind in self.individuals:
                ind.farm_size -= to_subtract
        # Else do nothing

    def update_timing(self, t):
        """Decide how often income and farm size are adjusted."""
        return t + 1

    def do_update(self, unused_t):
        """Do the adjustment of income or farmsize"""
        if self.is_active:
            if self.municipality_like is True:
                self.update_incomes()
                print('incomes updated of society', self)
            elif self.municipality_like is False:
                self.update_farmsizes()
                print('farmsizes updated of society', self)
            else:
                raise SocietyTypeError('Neither County nor Municipality!')

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
        """Calculate average liquidity of society."""
        if self.is_active:
            sum = 0
            for ind in self.individuals:
                sum += ind.liquidity
            self.average_liquidity = sum / self.population
        else:
            # This shoul not happen, but apparently does nevertheless...
            self.average_liquidity = 1

    def calculate_average_utility(self, unused_t):
        """Calculate the average utility in this society."""
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

    processes = [
        Explicit('calculate population',
                 [B.Society.population],
                 calc_population),
        Step("Update incomes/farmsizes",
             [B.Society.individuals.farm_size,
              B.Society.individuals.gross_income],
             [update_timing, do_update]),
        Explicit('calculate mean income or farmsize',
                 [I.Society.mean_income_or_farmsize],
                 calculate_mean_income_or_farmsize),
        Explicit("Calculate average liquidities",
                 [I.Society.average_liquidity],
                 calculate_average_liquidity),
        Explicit("Calculate average utilities",
                 [I.Society.average_utility],
                 calculate_average_utility),
        Explicit("Calculate gini",
                 [I.Society.gini_coefficient],
                 calculate_gini)
    ]


class SocietyTypeError(Exception):
    """Error Class if wrong type of society."""
    pass
