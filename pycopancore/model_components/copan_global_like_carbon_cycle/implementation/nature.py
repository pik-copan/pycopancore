"""Nature process taxon mixing class.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from .. import interface as I
from pycopancore.data_model.master_data_model.dimensions_and_units import \
    gigatonnes_carbon, years, square_kilometers, kelvins

class Nature (I.Nature):
    """Nature process taxon mixin implementation class."""

    # standard methods:

    def __init__(self,
                 *,  # TODO: uncomment when adding named args behind here
                 total_carbon = 5500 * gigatonnes_carbon, # see Nitzbon 2016
                 ocean_atmosphere_diffusion_coefficient = 0.016 / years, # see Nitzbon 2016
                 carbon_solubility_in_sea_water = 1 / 1.43, # see Nitzbon 2016
                 basic_photosynthesis_productivity =
                    26.4/years / (gigatonnes_carbon/square_kilometers)**.5, # see Nitzbon 2016
                 photosynthesis_sensitivity_on_atmospheric_carbon =
                    1.1e6/years / (gigatonnes_carbon/square_kilometers)**.5
                        / kelvins, # see Nitzbon 2016
                 terrestrial_carbon_capacity_per_area =
                    5000/1.5e8 * gigatonnes_carbon/square_kilometers, # ca. 2 times current value
                 basic_respiration_rate = 0.0298 / years, # see Nitzbon 2016
                 respiration_sensitivity_on_atmospheric_carbon =
                    3200/years / (gigatonnes_carbon/square_kilometers), # see Nitzbon 2016
                 temperature_offset = 0 * kelvins, # TODO!
                 temperature_sensitivity_on_atmospheric_carbon = \
                    0 * kelvins/gigatonnes_carbon, # TODO!
                 **kwargs):
        """Initialize the unique instance of Nature."""
        super().__init__(**kwargs)  # must be the first line

        self.total_carbon = total_carbon
        self.ocean_atmosphere_diffusion_coefficient = \
            ocean_atmosphere_diffusion_coefficient
        self.carbon_solubility_in_sea_water = carbon_solubility_in_sea_water
        self.basic_photosynthesis_productivity = \
            basic_photosynthesis_productivity
        self.photosynthesis_sensitivity_on_atmospheric_carbon = \
            photosynthesis_sensitivity_on_atmospheric_carbon
        self.terrestrial_carbon_capacity_per_area = \
            terrestrial_carbon_capacity_per_area
        self.basic_respiration_rate = basic_respiration_rate
        self.respiration_sensitivity_on_atmospheric_carbon = \
            respiration_sensitivity_on_atmospheric_carbon
        self.temperature_offset = temperature_offset
        self.temperature_sensitivity_on_atmospheric_carbon = \
            temperature_sensitivity_on_atmospheric_carbon

    # process-related methods:

    # TODO: add some if needed...

    processes = []  # TODO: instantiate and list process objects here
