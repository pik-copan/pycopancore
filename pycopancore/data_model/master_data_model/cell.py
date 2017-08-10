"""Master data model for cell."""

from . import nature as NAT
from . import metabolism as MET

# natural:

land_area = NAT.land_area.copy()
atmospheric_carbon = NAT.atmospheric_carbon.copy()
surface_air_temperature = NAT.surface_air_temperature.copy()
ocean_carbon = NAT.ocean_carbon.copy()
upper_ocean_carbon = NAT.upper_ocean_carbon.copy()
deep_ocean_carbon = NAT.deep_ocean_carbon.copy()
terrestrial_carbon = NAT.terrestrial_carbon.copy()
soil_carbon = NAT.soil_carbon.copy()
biomass_carbon = NAT.biomass_carbon.copy()
harvestable_biomass_carbon = NAT.harvestable_biomass_carbon.copy()
other_biomass_carbon = NAT.other_biomass_carbon.copy()
fossil_carbon = NAT.fossil_carbon.copy()
discovered_fossil_reserves = NAT.discovered_fossil_reserves.copy()
undiscovered_fossil_reserves = NAT.undiscovered_fossil_reserves.copy()

ocean_atmosphere_diffusion_coefficient = \
    NAT.ocean_atmosphere_diffusion_coefficient
carbon_solubility_in_sea_water = NAT.carbon_solubility_in_sea_water.copy()

photosynthesis_carbon_flow = NAT.photosynthesis_carbon_flow.copy()
terrestrial_respiration_carbon_flow = \
    NAT.terrestrial_respiration_carbon_flow.copy()
plant_respiration_carbon_flow = NAT.plant_respiration_carbon_flow.copy()
soil_respiration_carbon_flow = NAT.soil_respiration_carbon_flow.copy()

# metabolic:

biomass_harvest_flow = MET.biomass_harvest_flow.copy()
fossil_extraction_flow = MET.fossil_extraction_flow.copy()
carbon_emission_flow = MET.carbon_emission_flow.copy()

biomass_input_flow = MET.biomass_input_flow.copy()
fossil_fuel_input_flow = MET.fossil_fuel_input_flow.copy()
renewable_energy_input_flow = MET.renewable_energy_input_flow.copy()

biomass_energy_density = MET.biomass_energy_density.copy()
fossil_energy_density = MET.fossil_energy_density.copy()

secondary_energy_flow = MET.secondary_energy_flow.copy()
total_energy_intensity = MET.total_energy_intensity.copy()
total_output_flow = MET.total_output_flow.copy()
