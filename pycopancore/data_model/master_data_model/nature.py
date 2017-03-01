from pycopancore.data_model import Variable
from . import gigatons_carbon, kelvins, years

# TODO: complete desc strings!

# Atmosphere:

atmospheric_carbon = Variable("atmospheric carbon stock",
                              "(mass of C in any chemical compound)",
                              unit=gigatons_carbon,
                              is_extensive=True, lower_bound=0)
# Note: this is NOT the same as the CF var. atmosphere_mass_of_carbon_dioxide

surface_air_temperature = \
    Variable("surface air temperature",
             """(in the meaning used in climate policy debates,
             i.e., at 2m above surface, averaged over the day)""",
             AMIP="tas",  # CF="air_temperature"?
             unit=kelvins,
             is_intensive=True, lower_bound=0)
# TODO: higher layers as a vector by (geopotential) hight?


# Oceans:

ocean_carbon = Variable("ocean carbon stock",
                        "(mass of C in any chemical compound)",
                        unit=gigatons_carbon,
                        is_extensive=True, lower_bound=0)

# Note: when using the following, include
# Implicit(ocean_carbon == upper_ocean_carbon + deep_ocean_carbon)
upper_ocean_carbon = \
    Variable("upper ocean carbon stock",
             "(that which interacts relatively much/fast with atmosphere)",
             unit=gigatons_carbon,
             is_extensive=True, lower_bound=0)
deep_ocean_carbon = \
    Variable("deep ocean carbon stock",
             "(that which interacts relatively little/slow with atmosphere)",
             unit=gigatons_carbon,
             is_extensive=True, lower_bound=0)

# Note: there are no corresponding CF vars. yet


# Land:

terrestrial_carbon = Variable("terrestrial carbon stock",
                              "(mass of C in any chemical compound)",
                              unit=gigatons_carbon, 
                              is_extensive=True, lower_bound=0)

# Note: when using the following, include
# Implicit(terrestrial_carbon == soil_carbon + biomass_carbon)
soil_carbon = Variable("soil carbon stock",
                       "(mass of C in any chemical compound)",
                       unit=gigatons_carbon,
                       is_extensive=True, lower_bound=0)
# Note: has to do with CF var. soil_carbon_content
biomass_carbon = Variable("biomass/plant carbon stock",
                          "(mass of C in any chemical compound)",
                          unit=gigatons_carbon,
                          is_extensive=True, lower_bound=0)

# Note: when using the following, include
# Implicit(biomass_carbon == harvestable_biomass_carbon + other_biomass_carbon)
harvestable_biomass_carbon = \
    Variable("harvestable biomass carbon stock",
             """(that which can be accessed easily for direct harvesting,
                in particular agricultural biomass)""",
             unit=gigatons_carbon,
             is_extensive=True, lower_bound=0)
other_biomass_carbon = \
    Variable("other (non-harvestable) biomass carbon stock",
             "(that which cannot be accessed easily for direct harvesting)",
             unit=gigatons_carbon,
             is_extensive=True, lower_bound=0)

# Note: there are no corresponding CF vars. yet


# Other:

fossil_carbon = Variable("fossil carbon stock",
                         """(mass of C in any chemical compound,
                         potentially accessible for human extraction
                         and combustion)""",
                         unit=gigatons_carbon,
                         is_extensive=True, lower_bound=0)

# Note: when using the following, include
# Implicit(fossil_carbon == harvestable_biomass_carbon + other_biomass_carbon)
discovered_fossil_reserves = \
    Variable("discovered fossil reserves carbon stock",
             """(that which can currently be accessed for extraction)""",
             unit=gigatons_carbon,
             is_extensive=True, lower_bound=0)
undiscovered_fossil_reserves = \
    Variable("undiscovered fossil reserves carbon stock",
             "(that which cannot currently be accessed for extraction)",
             unit=gigatons_carbon,
             is_extensive=True, lower_bound=0)

# For land-atmosphere interactions:

photosynthesis_carbon_flow = \
    Variable("photosynthesis carbon flow", "",
             ref="https://en.wikipedia.org/wiki/Photosynthesis",
             unit=gigatons_carbon/years,
             is_extensive=True, lower_bound=0)
terrestrial_respiration_carbon_flow = \
    Variable("plant and soil respiration carbon flow", "",
             unit=gigatons_carbon/years,
             is_extensive=True, lower_bound=0)

# Note: when using the following, include
# Implicit(terrestrial_respiration_carbon_flow
#          == plant_respiration_carbon_flow + soil_respiration_carbon_flow)
plant_respiration_carbon_flow = \
    Variable("plant respiration carbon flow", "",
             ref="https://en.wikipedia.org/wiki/Cellular_respiration",
             unit=gigatons_carbon/years,
             is_extensive=True, lower_bound=0)
soil_respiration_carbon_flow = \
    Variable("soil respiration carbon flow", "",
             ref="https://en.wikipedia.org/wiki/Soil_respiration",
             unit=gigatons_carbon/years,
             is_extensive=True, lower_bound=0)

# Note: there are no corresponding CF vars. yet

