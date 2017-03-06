from pycopancore import master_data_model as MDM
from pycopancore import Variable
from pycopancore.base_dimensions_units import \
        gigatons_carbon, square_kilometers, years, kelvins


class Model (object):
    """Interface for Model mixin"""

    # metadata:
    name = "copan:GLOBAL-like carbon cycle"
    description = "Simple carbon cycle as in copan:GLOBAL, but with cell-based terrestrial carbon"
    requires = []


# entity types:


class World (object):
    """Interface for World mixin"""

    # variables:
    atmospheric_carbon = MDM.atmospheric_carbon
    ocean_carbon = MDM.ocean_carbon
    surface_air_temperature = MDM.surface_air_temperature


class Cell (object):
    """Interface for Cell mixin"""

    # variables:
    terrestrial_carbon = MDM.terrestrial_carbon
    photosynthesis_carbon_flow = MDM.photosynthesis_carbon_flow
    terrestrial_respiration_carbon_flow = \
        MDM.terrestrial_respiration_carbon_flow


# process taxa:


class Nature (object):
    """Interface for Nature mixin"""

    # parameters / exogenous veriables:
    total_carbon = Variable("total carbon", unit=gigatons_carbon,
                            lower_bound=0)

    ocean_atmosphere_diffusion_coefficient = \
        MDM.ocean_atmosphere_diffusion_coefficient
    carbon_solubility_in_sea_water = MDM.carbon_solubility_in_sea_water

    basic_photosynthesis_productivity = \
        Variable("basic photosynthesis productivity",
                 unit = 1/years / (gigatons_carbon/square_kilometers)**.5,
                 lower_bound=0)
    photosynthesis_sensitivity_on_atmospheric_carbon = \
        Variable("sensitivity of photosynthesis productivity on atmospheric carbon",
                 unit = 1/years / (gigatons_carbon/square_kilometers)**.5
                        / kelvins)
    terrestrial_carbon_capacity_per_area = \
        Variable("per-area capacity of terrestrial carbon",
                 unit=gigatons_carbon/square_kilometers, lower_bound=0)

    basic_respiration_rate = Variable("basic respiration rate", unit=1/years)
    respiration_sensitivity_on_atmospheric_carbon = \
        Variable("sensitivity of respiration rate on atmospheric carbon",
                 unit = 1/years / kelvins)

    temperature_offset = \
        Variable("offset of temperature for zero atmospheric carbon",
                 unit=kelvins, lower_bound=0)
    temperature_sensitivity_on_atmospheric_carbon = \
        Variable("sensitivity of temperature on atmospheric carbon",
                 unit=kelvins/gigatons_carbon, lower_bound=0)
