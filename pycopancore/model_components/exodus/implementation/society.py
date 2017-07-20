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
# from .... import master_data_model as D

from scipy import stats
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

        self.liquidity_mean = None
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
            mean = self.mean_income_or_farmsize
            lognormal_random = stats.lognorm.ppf(number, s=sigma, scale=mean)
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

    @property
    def mean_income_or_farmsize(self):
        "Get mean income or mean farmsize."
        if self.municipality_like is True:
            # mean income:
            return self.base_mean_income * (len(self.individuals) ** 1.12)
        if self.municipality_like is False:
            # Get cell. This complicated code is necessary, since direct_cells
            # is a set:
            for c in self.direct_cells:
                cell = c
                break
            # mean farm size:
            return cell.land_area / len(self.individuals)

    # process-related methods:

    def liquidity_pdf(self):
        """Calculate the PDF of the liquidity of the society."""
        print('liquidity_pdf is calculated')
        liquidities = []
        for individual in self.individuals:
            liquidities.append(individual.liquidity)
        self.liquidity_sigma, self.liquidity_loc, self.liquidity_mean = (
            stats.lognorm.fit(liquidities, floc=0))

    processes = []
