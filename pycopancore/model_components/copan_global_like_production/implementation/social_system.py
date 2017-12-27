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

from .... import Explicit, ODE
from .. import interface as I
from ...base import interface as B

import numpy as np


class Society (I.Society):
    """Society entity type mixin implementation class."""

    
    # process-related methods:

    def do_economic_production(self, unused_t):
        """Do something.

        It needs to be described so other people want to use it.
        Parameters
        ----------
        unused_t
        """
        # list of cells in some fixed order, so that we can use arrays below:
        C = list(self.cells)
        # collect cellwise input for energy subsectors:
        intensity = np.array([c.total_energy_intensity for c in C])
        # use the copan:GLOBAL Leontieff/Cobb-Douglas nested production
        # function:
        relative_productivity = np.array([c.total_relative_productivity
                                          for c in C])
        """an aggregate, production-function specific indicator"""
        # distribute population and capital to cells so that wages and rents
        # are equal across cells (efficient allocation):
        if np.any(relative_productivity == np.inf):
            # give equal prod. to those with inf relative prod.:
            wh = np.where(relative_productivity < np.inf)[0]
            relative_productivity[:] = 1
            relative_productivity[wh] = 0
            relative_weight = relative_productivity
            total_relative_weight = sum(relative_weight)
        else:
            relative_weight = relative_productivity
            total_relative_weight = sum(relative_weight)
            if total_relative_weight == 0:
                # unimportant since relative_weight == 0, just to avoid division error:
                total_relative_weight = 1
        weight = relative_weight / total_relative_weight
        P = weight * self.population
        K = weight * self.physical_capital
        # resulting cell-wise harvest, extraction and production:
        denom = relative_productivity**0.8
        # unimportant since numerator is then 0, just to avoid division error:
        denom[np.where(denom == 0)] = 1
        fac = (P * K)**0.4 / denom
        if any(np.isnan(fac)):
            w = np.where(np.isnan(fac))[0] 
#            print("fac",self.physical_capital,P[w],K[w],weight[w],relative_productivity[w],intensity[w])
            exit()
        eB = self.metabolism.biomass_energy_density
        eF = self.metabolism.fossil_energy_density
        # TODO: FIX occurrence of intensity:
        B = np.array([c.biomass_relative_productivity for c in C]) * fac / eB
        F = np.array([c.fossil_relative_productivity for c in C]) * fac / eF
        R = np.array([c.renewable_relative_productivity for c in C]) * fac
        E = eB * B + eF * F + R
        Y = E / intensity
        if any(Y < 0):
            w = np.where(np.isnan(fac))[0] 
#            print("Y",P[w],K[w],weight[w],relative_productivity[w],intensity[w],E[w])
            exit()
            
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
        self.economic_output_flow = sum(Y)
        self.carbon_emission_flow = \
            self.biomass_input_flow + self.fossil_fuel_input_flow

    def do_harvest_extraction_emissions(self, unused_t):
        """Add carbon emission flow to world's athmospheric carbon.

        Parameters
        ----------
        unused_t
        """
        # this is an example of a process that is owned by Society
        # but affects its cells and the world:
        for c in self.cells:
            c.d_terrestrial_carbon -= c.biomass_harvest_flow
            c.d_fossil_carbon -= c.fossil_extraction_flow
        self.world.d_atmospheric_carbon += self.carbon_emission_flow


    # abbreviations:
    
    this = I.Society
    met = B.Society.metabolism
    cs = B.Society.cells
    # distribute population and capital to cells so that wages and rents
    # are equal across cells (efficient allocation):
    relative_weight = cs.total_relative_productivity
    total_relative_weight = B.Society.sum(relative_weight)
    weight = relative_weight / total_relative_weight
    P = weight * this.population
    K = weight * this.physical_capital
    # resulting cell-wise harvest, extraction and production:
    intensity = cs.total_energy_intensity
    denom = (cs.total_relative_productivity * intensity)**0.8
    fac = (P * K)**0.4 / denom
    eB = met.biomass_energy_density
    eF = met.fossil_energy_density
    Bcell = cs.biomass_relative_productivity * fac / eB
    Fcell = cs.fossil_relative_productivity * fac / eF
    Rcell = cs.renewable_relative_productivity * fac
    Ecell = eB * Bcell + eF * Fcell + Rcell
    Ycell = Ecell / intensity
    # societal aggregates:
    Bsoc = B.Society.sum(Bcell)
    Fsoc = B.Society.sum(Fcell)
    Rsoc = B.Society.sum(Rcell)
    Esoc = B.Society.sum(Ecell)
    Ysoc = B.Society.sum(Ycell)
    emissions = Bsoc + Fsoc

    processes = [

        Explicit("economic production",
                 [B.Society.cells.biomass_harvest_flow,
                  B.Society.cells.fossil_extraction_flow,
                  I.Society.biomass_input_flow,
                  I.Society.fossil_fuel_input_flow,
                  I.Society.renewable_energy_input_flow,
                  I.Society.secondary_energy_flow,
                  I.Society.economic_output_flow,
                  I.Society.carbon_emission_flow],
#                 [Bcell,
#                  Fcell,
#                  Bsoc,
#                  Fsoc,
#                  Rsoc,
#                  Esoc,
#                  Ysoc,
#                  emissions
#                  ]),
                 do_economic_production),

        ODE("harvest, extraction, emissions",
            [B.Society.cells.terrestrial_carbon,
             B.Society.cells.fossil_carbon,
             B.Society.world.atmospheric_carbon],
#            [-Bcell,
#             -Fcell,
#             emissions
#             ])
            do_harvest_extraction_emissions)

    ]
