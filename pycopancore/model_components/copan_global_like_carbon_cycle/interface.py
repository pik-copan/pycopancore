"""copan_global_like_carbon_cycle model component Interface."""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from ... import master_data_model as D
from ...data_model.master_data_model import NAT, W, C
from ... import Variable


class Model (object):
    """Interface for Model mixin."""

    # metadata:
    name = "copan:GLOBAL-like carbon cycle"
    """a unique name for the model component"""
    description = "Simple carbon cycle as in copan:GLOBAL, " \
                  "but with cell-based terrestrial and fossil carbon"
    """some longer description"""
    requires = []
    """list of other model components required for this model component to
    make sense"""


# entity types:


class World (object):
    """Interface for World mixin."""

    # variables:
    atmospheric_carbon = W.atmospheric_carbon
    upper_ocean_carbon = W.upper_ocean_carbon
    surface_air_temperature = W.surface_air_temperature


class Cell (object):
    """Interface for Cell mixin."""

    # variables:
    
    land_area = C.land_area
    land_area.default = 1 * D.square_kilometers
    
    terrestrial_carbon = C.terrestrial_carbon
    terrestrial_carbon.default = 1 * D.gigatonnes_carbon
    
    photosynthesis_carbon_flow = C.photosynthesis_carbon_flow
    terrestrial_respiration_carbon_flow = \
        C.terrestrial_respiration_carbon_flow


# process taxa:


class Nature (object):
    """Interface for Nature mixin."""

    # parameters / exogenous veriables:
    
    ocean_atmosphere_diffusion_coefficient = \
        NAT.ocean_atmosphere_diffusion_coefficient
    carbon_solubility_in_sea_water = NAT.carbon_solubility_in_sea_water

    basic_photosynthesis_productivity = \
        Variable("basic photosynthesis productivity", "",
                 unit = D.years**-1
                        / (D.gigatonnes_carbon / D.square_kilometers)**0.5,
                 lower_bound=0,
                 default=26.4)
    photosynthesis_sensitivity_on_atmospheric_carbon = \
        Variable("sensitivity of photosynthesis productivity on atmospheric "
                 "carbon density", "",
                 unit = D.years**-1
                        / (D.gigatonnes_carbon / D.square_kilometers)**0.5
                        / (D.gigatonnes_carbon / D.square_kilometers),
                 default=1e6) # 1.1e6!
    terrestrial_carbon_capacity_per_area = \
        Variable("per-area capacity of terrestrial carbon", "",
                 unit = D.gigatonnes_carbon / D.square_kilometers,
                 lower_bound=0, default = 100 * 2500 / 1.5e8)  
        # P? ca. 100 times current value. TODO: improve default

    basic_respiration_rate = Variable("basic respiration rate", "",
                                      unit=D.years**-1, default=.0298)
    respiration_sensitivity_on_atmospheric_carbon = \
        Variable("sensitivity of respiration rate on atmospheric carbon", "",
                 unit = D.years**-1
                        / (D.gigatonnes_carbon / D.square_kilometers),
                 default=3.2e3)

    reference_temperature = \
        Variable("reference temperature for relationship with atmospheric carbon", 
                 "default: pre-industrial value",
                 unit=D.kelvins, lower_bound=0,
                 default=287)  # TODO: verify!
    reference_atmospheric_carbon = \
        Variable("reference atmospheric carbon for relationship with temperature", 
                 "default: pre-industrial value",
                 unit=D.gigatonnes_carbon, lower_bound=0,
                 default=589)
    temperature_sensitivity_on_atmospheric_carbon = \
        Variable("sensitivity of temperature on atmospheric carbon", "",
                 unit = D.kelvins / D.gigatonnes_carbon, lower_bound=0,
                 default = 1.5 / 1000)
