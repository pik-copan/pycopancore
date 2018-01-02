"""Master data model for world."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from . import ENV, MET
from . import gigatonnes_carbon as GtC
from . import square_kilometers as km2


class World:

    # natural:
    
    land_area = ENV.land_area.copy(default=1.5e8*km2)
    atmospheric_carbon = ENV.atmospheric_carbon.copy(default=589*GtC)
    surface_air_temperature = ENV.surface_air_temperature.copy()
    ocean_carbon = ENV.ocean_carbon.copy(default=38000*GtC)
    upper_ocean_carbon = ENV.upper_ocean_carbon.copy(default=900*GtC)
    deep_ocean_carbon = ENV.deep_ocean_carbon.copy(default=37100*GtC)
    terrestrial_carbon = ENV.terrestrial_carbon.copy(default=2550*GtC)
    soil_carbon = ENV.soil_carbon.copy(default=2000*GtC)
    biomass_carbon = ENV.biomass_carbon.copy(default=550*GtC)
    harvestable_biomass_carbon = ENV.harvestable_biomass_carbon.copy()
    other_biomass_carbon = ENV.other_biomass_carbon.copy()
    fossil_carbon = ENV.fossil_carbon.copy(default=1500*GtC)
    discovered_fossil_reserves = ENV.discovered_fossil_reserves.copy()
    undiscovered_fossil_reserves = ENV.undiscovered_fossil_reserves.copy()
    
    ocean_atmosphere_diffusion_coefficient = \
        ENV.ocean_atmosphere_diffusion_coefficient
    carbon_solubility_in_sea_water = ENV.carbon_solubility_in_sea_water.copy()
    
    photosynthesis_carbon_flow = ENV.photosynthesis_carbon_flow.copy()
    terrestrial_respiration_carbon_flow = \
        ENV.terrestrial_respiration_carbon_flow.copy()
    plant_respiration_carbon_flow = ENV.plant_respiration_carbon_flow.copy()
    soil_respiration_carbon_flow = ENV.soil_respiration_carbon_flow.copy()
    
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
    
    total_output_flow = MET.economic_output_flow.copy()
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
