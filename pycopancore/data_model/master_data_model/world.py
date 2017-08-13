"""Master data model for world."""

from . import nature as NAT
from . import metabolism as MET
from . import gigatonnes_carbon as GtC
from . import square_kilometers as km2

# natural:

land_area = NAT.land_area.copy(default=1.5e8*km2)
atmospheric_carbon = NAT.atmospheric_carbon.copy(default=589*GtC)
surface_air_temperature = NAT.surface_air_temperature.copy()
ocean_carbon = NAT.ocean_carbon.copy(default=38000*GtC)
upper_ocean_carbon = NAT.upper_ocean_carbon.copy(default=900*GtC)
deep_ocean_carbon = NAT.deep_ocean_carbon.copy(default=37100*GtC)
terrestrial_carbon = NAT.terrestrial_carbon.copy(default=2550*GtC)
soil_carbon = NAT.soil_carbon.copy(default=2000*GtC)
biomass_carbon = NAT.biomass_carbon.copy(default=550*GtC)
harvestable_biomass_carbon = NAT.harvestable_biomass_carbon.copy()
other_biomass_carbon = NAT.other_biomass_carbon.copy()
fossil_carbon = NAT.fossil_carbon.copy(default=1500*GtC)
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

population = MET.population.copy()
population_by_age = MET.population_by_age.copy()

biomass_harvest_flow = MET.biomass_harvest_flow.copy()
fossil_extraction_flow = MET.fossil_extraction_flow.copy()
carbon_emission_flow = MET.carbon_emission_flow.copy()

physical_capital = MET.physical_capital.copy()
renewable_energy_knowledge = MET.renewable_energy_knowledge.copy()

biomass_input_flow = MET.biomass_input_flow.copy()
fossil_fuel_input_flow = MET.fossil_fuel_input_flow.copy()
renewable_energy_input_flow = MET.renewable_energy_input_flow.copy()
secondary_energy_flow = MET.secondary_energy_flow.copy()

total_energy_intensity = MET.total_energy_intensity.copy()

total_output_flow = MET.total_output_flow.copy()
consumption_flow = MET.consumption_flow.copy()
investment_flow = MET.investment_flow.copy()

welfare_flow_per_capita = MET.welfare_flow_per_capita.copy()

biomass_energy_density = MET.biomass_energy_density.copy()
fossil_energy_density = MET.fossil_energy_density.copy()

physical_capital_depreciation_rate = \
    MET.physical_capital_depreciation_rate.copy()
renewable_energy_knowledge_depreciation_rate = \
    MET.renewable_energy_knowledge_depreciation_rate.copy()

savings_rate = MET.savings_rate.copy()
