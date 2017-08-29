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
                 pareto_distribution_type=False,
                 base_mean_income=None,
                 pdf_sigma=0.34,  # 0.34 taken from Clementi, Gallegati 2005 for income distribution
                 **kwargs):
        """Initialize an instance of Society."""
        super().__init__(**kwargs)  # must be the first line

        self.municipality_like = municipality_like
        self.pareto_distribution_type = pareto_distribution_type
        self.base_mean_income = base_mean_income
        self.pdf_sigma = pdf_sigma

        self.liquidity_median = None
        self.liquidity_sigma = None
        self.liquidity_loc = None

        # At last, check for validity of all variables that have been
        # initialized and given a value:

        # Following method is defined in abstract_entity_mixin which is
        # inherited only by mixing in the model:
        self.assert_valid()

    @property
    def gross_income_or_farmsize(self):
        "Get random income or farm size distributed log-normal."
        if self.pareto_distribution_type is False:
            # Use log-normal
            number = random.random()
            sigma = self.pdf_sigma
            # calculate ´median from mean:
            median = (self.mean_income_or_farmsize / np.exp(sigma**2 / 2))
            lognormal_random = stats.lognorm.ppf(number, s=sigma, scale=median)
            return lognormal_random
        if self.pareto_distribution_type is True:
            # Use pareto:
            return "not implemented yet"

    @property
    def pdf_mu(self):
        """Get mu of the log-normal distribution"""
        # from mean = exp(mu + sigma**2 / 2) in the log-normal distribution:
        return math.log(self.mean_income_or_farmsize) - (self.pdf_sigma**2) / 2

    @property
    def pdf_y_min(self):
        """Get the y_min of the Pareo distribution"""
        return

    # process-related methods:

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
        self.population = len(self.individuals)

    def update_incomes(self):
        """Update incomes to adjust to population in some manner."""
        # first: Check if really a municipaity:
        if self.municipality_like is not True:
            raise SocietyTypeError('Society not a municipality')
        elif len(self.individuals) == 0 and self.is_active:
            # Everybody left
            self.deactivate()
        elif self.is_active:
            # Define epsilion, which functions as threshold to change incomes
            epsilon = 10
            # Define factor how fast adjusting takes place
            factor = 0.5
            sum = 0
            for ind in self.individuals:
                sum += ind.gross_income
            # Now divide by number of individuals to get mean:
            real_mean = sum / len(self.individuals)
            # get delta:
            delta_mean = self.mean_income_or_farmsize - real_mean
            if delta_mean > epsilon and delta_mean > 0:
                # mean income is smaller than it should be, need to add
                # Define amount to add:
                to_add = delta_mean / len(self.individuals) * factor
                for ind in self.individuals:
                    ind.gross_income += to_add
            if delta_mean > epsilon and delta_mean < 0:
                # mean income is bigger than it should be, need to subtract
                # Define amount to subtract:
                to_subtract = delta_mean / len(self.individuals) * factor
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
        real_mean = sum / len(self.individuals)
        # get delta:
        delta_mean = self.mean_income_or_farmsize - real_mean
        if delta_mean > epsilon and delta_mean > 0:
            # mean farmsize is smaller than it should be, need to add
            # Define amount to add:
            to_add = delta_mean / len(self.individuals) * factor
            for ind in self.individuals:
                ind.farm_size += to_add
        if delta_mean > epsilon and delta_mean < 0:
            # mean farmsize is bigger than it should be, need to subtract
            # Define amount to subtract:
            to_subtract = delta_mean / len(self.individuals) * factor
            for ind in self.individuals:
                ind.farm_size -= to_subtract
        # Else do nothing

    def update_timing(self, t):
        """Decide how often income and farm size are adjusted."""
        return t + 0.2

    def do_update(self, unused_t):
        """Do the adjustment of income or farmsize"""
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
        if self.municipality_like:
            # in case of municipality
            self.mean_income_or_farmsize = self.base_mean_income * (len(self.individuals) ** 1.12)
        if not self.municipality_like:
            # in case of county
            for c in self.direct_cells:
                # mean farm size:
                self.mean_income_or_farmsize = c.land_area / len(self.individuals)

    processes = [
        Explicit('calculate population',
                 [B.Society.population],
                 calc_population),
        Step("Update incomes/farmsizes",
             [I.Individual.farm_size, I.Individual.gross_income],
             [update_timing, do_update]),
        Explicit('calculate mean income or farmsize',
                 [I.Society.mean_income_or_farmsize],
                 calculate_mean_income_or_farmsize)
    ]


class SocietyTypeError(Exception):
    """Error Class if wrong type of society."""
    pass
