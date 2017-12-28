"""Master data model for social_system."""

from . import MET
from .. import Variable
from . import dollars, gigatonnes_carbon, gigajoules


class SocialSystem:
    
    # metabolic:
    
    population = MET.population.copy()
    population_by_age = MET.population_by_age.copy()
    migrant_population = MET.migrant_population.copy()
    
    fertility = MET.fertility.copy()
    
    mortality = MET.mortality.copy()
    mortality_temperature_sensitivity = \
        MET.mortality_temperature_sensitivity.copy()
    mortality_reference_temperature = \
        MET.mortality_reference_temperature.copy()    
    
    births = MET.births.copy()
    deaths = MET.deaths.copy()
    immigration = MET.immigration.copy()
    emigration = MET.emigration.copy()
    
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
    
    economic_output_flow = MET.economic_output_flow.copy()
    consumption_flow = MET.consumption_flow.copy()
    investment_flow = MET.investment_flow.copy()
    
    welfare_flow_per_capita = MET.welfare_flow_per_capita.copy()
    wellbeing = MET.wellbeing.copy()
    
    biomass_energy_density = MET.biomass_energy_density.copy()
    fossil_energy_density = MET.fossil_energy_density.copy()
    
    protected_terrestrial_carbon = MET.protected_terrestrial_carbon.copy()
    protected_fossil_carbon = MET.protected_fossil_carbon.copy()
    protected_terrestrial_carbon_share = MET.protected_terrestrial_carbon_share.copy()
    protected_fossil_carbon_share = MET.protected_fossil_carbon_share.copy()
    
    physical_capital_depreciation_rate = \
        MET.physical_capital_depreciation_rate.copy()
    basic_physical_capital_depreciation_rate = \
        MET.basic_physical_capital_depreciation_rate.copy()
    physical_capital_depreciation_rate_temperature_sensitivity = \
        MET.physical_capital_depreciation_rate_temperature_sensitivity.copy()
    physical_capital_depreciation_rate_reference_temperature = \
        MET.physical_capital_depreciation_rate_reference_temperature.copy()    
    
    renewable_energy_knowledge_depreciation_rate = \
        MET.renewable_energy_knowledge_depreciation_rate.copy()
    
    savings_rate = MET.savings_rate.copy()
    
    has_renewable_subsidy = \
        Variable("has renewable subsidy",
                 "whether a subsidy for renewables is in force",
                 scale="ordinal", levels=[False, True], default=False)
    has_emissions_tax = \
        Variable("has emissions tax",
                 "whether an emissions tax is in force",
                 scale="ordinal", levels=[False, True], default=False)
    has_fossil_ban = \
        Variable("has fossil ban",
                 "whether a fossil ban is in force",
                 scale="ordinal", levels=[False, True], default=False)
    emissions_tax_level = \
        Variable("emissions tax level",
                 "level of emissions tax when introduced",
                 unit = dollars / gigatonnes_carbon, 
                 lower_bound=0, default=100e9*3.5)
    renewable_subsidy_level = \
        Variable("renewable subsidy level",
                 "level of renewable subsidy when introduced",
                 unit = dollars / gigajoules, 
                 lower_bound=0, default=50)
