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

from pycopancore import Explicit, ODE
from .. import interface as I
import numpy as np


class Society (I.Society):
    """Society entity type mixin implementation class."""

    # standard methods:

    def __init__(self,
                 #*,
                 **kwargs):
        """Initialize an instance of Society."""
        super().__init__(**kwargs)  # must be the first line

    # process-related methods:

    def do_economic_production(self, unused_t):
        # list of cells in some fixed order, so that we can use arrays below:
        C = list(self.cells)
        # collect cellwise input for energy subsectors:
        L = np.array([c.terrestrial_carbon for c in C]) \
                    * (1 - self.protected_terrestrial_carbon_share)
        G = np.array([c.fossil_carbon for c in C]) \
                    * (1 - self.protected_fossil_carbon_share)
        S = self.renewable_energy_knowledge
        intensity = np.array([c.total_energy_intensity for c in C])
        # use the copan:GLOBAL Leontieff/Cobb-Douglas nested production function
        aB = np.array([c.biomass_sector_productivity for c in C])
        aF = np.array([c.fossil_sector_productivity for c in C])
        aR = np.array([c.renewable_sector_productivity for c in C])
        relative_productivity = (aB * L**2 + aF * G**2 + aR * S**2) / intensity
        """an aggregate, production-function specific indicator"""
        # distribute population and capital to cells so that wages and rents
        # are equal across cells (efficient allocation):
        relative_weight = relative_productivity
        total_relative_weight = sum(relative_weight)
        weight = relative_weight / total_relative_weight
        P = weight * self.population
        K = weight * self.physical_capital
        # resulting cell-wise harvest, extraction and production:
        fac = (P * K)**0.4 / (relative_productivity * intensity)**0.8
        eB = self.metabolism.biomass_energy_density
        eF = self.metabolism.fossil_energy_density
        B = aB * L**2 * fac / eB
        F = aF * G**2 * fac / eF
        R = aR * S**2 * fac
        E = eB * B + eF * F + R
        Y = E / intensity
        # tell cells what their harvest and extraction is:
        for i in range(len(C)):
            C[i].biomass_harvest_flow = B[i]
            C[i].fossil_extraction_flow = F[i]
        # store societies' total harvest and extraction, emissions,
        # and production:
        self.biomass_input_flow = sum(B)
        self.fossil_fuel_input_flow = sum(F)
        self.renewable_energy_input_flow = sum(R)
        self.secondary_energy_flow = sum(E)
        self.total_output_flow = sum(Y)
        self.carbon_emission_flow = \
            self.biomass_input_flow + self.fossil_fuel_input_flow

    def do_harvest_extraction_emissions(self, unused_t):
        for c in self.cells:
            c.d_terrestrial_carbon -= c.biomass_harvest_flow
            c.d_fossil_carbon -= c.fossil_extraction_flow
        self.world.d_atmospheric_carbon += self.carbon_emission_flow

    processes = [
                 Explicit("economic production",
                          [I.Cell.biomass_harvest_flow,
                           I.Cell.fossil_extraction_flow,
                           I.Society.biomass_input_flow,
                           I.Society.fossil_fuel_input_flow,
                           I.Society.renewable_energy_input_flow,
                           I.Society.secondary_energy_flow,
                           I.Society.total_output_flow],
                          do_economic_production),
                 ODE("harvest, extraction, emissions",
                     [I.Cell.terrestrial_carbon,
                      I.Cell.fossil_carbon,
                      I.World.atmospheric_carbon],
                     do_harvest_extraction_emissions)
                 ]
