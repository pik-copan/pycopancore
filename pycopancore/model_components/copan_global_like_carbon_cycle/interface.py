from pycopancore import master_data_model as MDM
from pycopancore import Variable, CFVariable
from pycopancore.base_dimensions_units import gigatons_carbon, square_kilometers, years, kelvins

class Model_(object):
    """Interface for Model mixin"""
    
    # metadata:
    name = "copan:GLOBAL-like carbon cycle" # a unique name for the model component
    description = "Simple carbon cycle as in copan:GLOBAL, but with cell-based terrestrial carbon" # some description
    requires = [] # list of other model components required for this model component to make sense


# entity types:

class World_(object):
    """Interface for World mixin"""
    
    # variables:
    atmospheric_carbon = MDM.atmospheric_carbon
    upper_ocean_carbon = MDM.upper_ocean_carbon
    mean_surface_air_temperature = MDM.mean_surface_air_temperature

class Cell_(object):
    """Interface for Cell mixin"""

    # variables:
    photosynthesis_flow = MDM.photosynthesis_flow
    respiration_flow = Variable("respiration flow", unit=gigatons_carbon/years)
    terrestrial_carbon = MDM.terrestrial_carbon


# process taxa:

class Nature_(object):
    """Interface for Nature mixin"""
    
    # parameters / exogenous veriables:
    total_carbon = Variable("total carbon", unit=gigatons_carbon)
    basic_photosynthesis_productivity = Variable("basic photosynthesis productivity", 
                                                 unit = 1/years / sqrt(gigatons_carbon/square_kilometers))
    photosynthesis_temperature_sensitivity = Variable("sensitivity of photosynthesis productivity on temperature", 
                                                      unit = 1/years / sqrt(gigatons_carbon/square_kilometers) / kelvins)
    terrestrial_carbon_capacity_per_area = Variable("per-area capacity of terrestrial carbon", unit=gigatons_carbon/square_kilometers)
    basic_respiration_rate = Variable("basic respiration rate", unit=1/years)
    respiration_temperature_sensitivity = Variable("sensitivity of respiration rate on temperature", unit = 1/years / kelvins)

   
