"""Master data model for society."""

from . import metabolism as MET

# metabolic:

population = MET.population.copy()
population_by_age = MET.population_by_age.copy()

fertility = MET.fertility.copy()
mortality = MET.mortality.copy()
births = MET.births.copy()
deaths = MET.deaths.copy()

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
wellbeing = MET.wellbeing.copy()

biomass_energy_density = MET.biomass_energy_density.copy()
fossil_energy_density = MET.fossil_energy_density.copy()

physical_capital_depreciation_rate = \
    MET.physical_capital_depreciation_rate.copy()
renewable_energy_knowledge_depreciation_rate = \
    MET.renewable_energy_knowledge_depreciation_rate.copy()

savings_rate = MET.savings_rate.copy()
