from pycopancore.data_model import Variable, CFVariable
from pycopancore.data_model.base_dimensions_units import \
        gigatons_carbon, kelvins, years

# Atmosphere:
atmospheric_carbon = CFVariable(ref="???", unit=gigatons_carbon)
mean_surface_air_temperature = CFVariable(ref="???", unit=kelvins)
# higher layers as a vector by geopotential hight?
# pressures as well?

# Oceans:
ocean_carbon = CFVariable(ref="???", unit=gigatons_carbon)
# in base: Implicit(ocean_carbon == upper_ocean_carbon + deep_ocean_carbon)
upper_ocean_carbon = CFVariable(ref="???", unit=gigatons_carbon)
deep_ocean_carbon = CFVariable(ref="???", unit=gigatons_carbon)

# Land:
photosynthesis_flow = Variable("photosynthesis flow", "TODO!",
                               unit=gigatons_carbon/years)
terrestrial_carbon = CFVariable(ref="???", unit=gigatons_carbon)
# in base: Implicit(terrestrial_carbon == soil_carbon + biomass_carbon)
soil_carbon = CFVariable(ref="???", unit=gigatons_carbon)
biomass_carbon = CFVariable(ref="???", unit=gigatons_carbon)
# in base: Implicit(biomass_carbon == harvestable_biomass_carbon + other_biomass_carbon)
harvestable_biomass_carbon = CFVariable(ref="???", unit=gigatons_carbon)
other_biomass_carbon = CFVariable(ref="???", unit=gigatons_carbon)
