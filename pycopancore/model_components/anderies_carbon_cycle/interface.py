"""copan_global_like_carbon_cycle model component Interface
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from ... import master_data_model as D
from ...data_model.master_data_model import ENV, MET, CUL, W, S, C, I
from ... import Variable


class Model (object):
    """Interface for Model mixin"""

    # metadata:
    name = "Anderies carbon cycle"
    """a unique name for the model component"""
    description = "see Anderies 2013"
    """some longer description"""
    requires = []
    """list of other model components required for this model component to
    make sense"""


# entity types:


class World (object):
    """Interface for World mixin"""

    # variables:
    atmospheric_carbon = W.atmospheric_carbon
    ocean_carbon = W.ocean_carbon
    surface_air_temperature = W.surface_air_temperature
    respiration_rate = Variable("respiration rate", "")  # unit
    fertilization = Variable("fertilization", "")  # unit
    photosynthesis_rate = Variable("photosynthesis rate", "")  # unit


class Cell (object):
    """Interface for Cell mixin"""

    # variables:
    terrestrial_carbon = C.terrestrial_carbon
    photosynthesis_carbon_flow = C.photosynthesis_carbon_flow
    terrestrial_respiration_carbon_flow = \
        C.terrestrial_respiration_carbon_flow
    human_offtake = Variable("human offtake", "")  # unit
    net_ecosystem_production = Variable(
        "net ecosystem production", "")  # unit


class SocialSystem (object):

    # variables:
    harvest_rate = Variable("harvest rate", "")  # unit


# process taxa:


class Environment (object):
    """Interface for Environment mixin"""

    # parameters / exogenous veriables:
    ocean_atmosphere_diffusion_coefficient = \
        ENV.ocean_atmosphere_diffusion_coefficient
    carbon_solubility_in_sea_water = ENV.carbon_solubility_in_sea_water

    basic_photosynthesis_productivity = \
        Variable("basic photosynthesis productivity", "",
                 unit=D.years**-1
                 / (D.gigatonnes_carbon / D.square_kilometers)**.5,
                 lower_bound=0)
    photosynthesis_sensitivity_on_atmospheric_carbon = \
        Variable("sensitivity of photosynthesis productivity on atmospheric carbon", "",
                 unit=D.years**-1
                 / (D.gigatonnes_carbon / D.square_kilometers)**.5
                 / D.kelvins)
    terrestrial_carbon_capacity_per_area = \
        Variable("per-area capacity of terrestrial carbon", "",
                 unit=D.gigatonnes_carbon / D.square_kilometers,
                 lower_bound=0)

    basic_respiration_rate = Variable("basic respiration rate", "",
                                      unit=D.years**-1)
    respiration_sensitivity_on_atmospheric_carbon = \
        Variable("sensitivity of respiration rate on atmospheric carbon", "",
                 unit=D.years**-1
                 / (D.gigatonnes_carbon / D.square_kilometers))

    temperature_offset = \
        Variable("offset of temperature for zero atmospheric carbon", "",
                 unit=D.kelvins, lower_bound=0)
    temperature_sensitivity_on_atmospheric_carbon = \
        Variable("sensitivity of temperature on atmospheric carbon", "",
                 unit=D.kelvins / D.gigatonnes_carbon, lower_bound=0)
