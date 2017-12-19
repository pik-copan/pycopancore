"""Jobst: write docstring."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from .... import Explicit, ODE
from .. import interface as I
from ...base import interface as B
from .... import master_data_model as D

import sympy as sp


class World (I.World):
    """Jobst: write docstring."""

    # standard methods:

    def __init__(self,
                 *,
                 atmospheric_carbon=1 * D.gigatonnes_carbon,
                 ocean_carbon=1 * D.gigatonnes_carbon,
                 surface_air_temperature=1 * D.kelvins,
                 **kwargs
                 ):
        """Initialize an (typically the unique) instance of World."""
        super().__init__(**kwargs)
        # initial values:
        self.atmospheric_carbon = atmospheric_carbon
        self.ocean_carbon = ocean_carbon
        self.surface_air_temperature = surface_air_temperature

    # process-related methods:

    def convert_temperature(self, unused_t):
        """(see Anderies et al. 2013)"""
        self.surface_air_temperature = self.environment.temperature_offset \
            + self.environment.temperature_sensitivity_on_atmospheric_carbon \
            * self.atmospheric_carbon

    def ocean_atmosphere_diffusion(self, unused_t):
        """(see Anderies et al. 2013)"""
        flow = self.environment.ocean_atmosphere_diffusion_coefficient * (
            self.environment.carbon_solubility_in_sea_water * self.ocean_carbon
            - self.atmospheric_carbon)
        self.d_ocean_carbon -= flow
        self.d_atmospheric_carbon += flow

    processes = [
        Explicit("convert temperature",
                 [I.World.surface_air_temperature],
                 convert_temperature),
        ODE("ocean-atmosphere diffusion",
            [I.World.ocean_carbon, I.World.atmospheric_carbon],
            ocean_atmosphere_diffusion),

        Explicit("respiration rate",
                 [I.World.respiration_rate],
                 [(B.World.environment.scaling_factor_temperature_respiration
                   * I.World.surface_air_temperature ** B.World.environment.exponent_for_increase_in_respiration_low_T
                   * sp.exp(-B.World.environment.exponent_for_increase_in_respiration_high_T
                            * B.Cell.world.surface_air_temperature))]),

        Explicit("fertilization",
                 [I.World.fertilization],
                 [B.World.environment.strength_of_fertilization_effect * I.World.atmospheric_carbon
                  ** B.World.environment.rapidity_of_fertilization_saturation]),

        Explicit("photosynthesis rate",
                 [I.World.photosynthesis_rate],
                 [I.World.fertilization
                  * B.World.environment.scaling_factor_temperature_photosynthesis * I.World.surface_air_temperature
                  ** B.World.environment.exponent_for_increase_in_photosynthesis_low_T
                  * sp.exp(-B.World.environment.exponent_for_increase_in_photosynthesis_high_T
                           * I.World.surface_air_temperature)])
    ]
