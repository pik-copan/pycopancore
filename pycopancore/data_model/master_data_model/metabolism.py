"""Master data model for metabolism."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from .. import Variable
from . import gigajoules, dollars, gigatonnes_carbon, years, utils, people, kelvins
from .. import unity


class Metabolism:

    # Population, demographics:
    
    population = Variable("human population", "",
                          IAMC="Population",
                          CETS="SP.POP",
                          unit=people,
                          is_extensive=True, lower_bound=0, default=0)
    
    # Note: when using the following, include
    # Implicit(population == sum(population_by_age))
    population_by_age = Variable("human population by age",
                                 "(in years from 0 to 99+)",
                                 IAMC="Population",
                                 CETS="SP.POP",
                                 unit=people,
                                 is_extensive=True, lower_bound=0,
                                 array_shape=(100,))  # 1d-array
    
    migrant_population = Variable("first-generation migrant population", "",
                                  unit=people,
                                  is_extensive=True, lower_bound=0, default=0)
    
    fertility = Variable("current human fertility rate", "",
                         unit=years**-1,
                         lower_bound=0, is_intensive=True, 
                         default=0.02)
    min_fertility = Variable("minimum human fertility rate", "",
                             unit=years**-1,
                             lower_bound=0, is_intensive=True,
                             default=0.008)
    max_fertility = Variable("maximum human fertility rate", "",
                             unit=years**-1,
                             lower_bound=0, is_intensive=True,
                             default=0.05)
    
    mortality = Variable("current human mortility rate", "",
                         unit=years**-1,
                         lower_bound=0, is_intensive=True,
                         default=0.01)
    mortality_temperature_sensitivity = \
        Variable("mortality temperature sensitivity", "",
                 unit = years**-1 / kelvins,
                 lower_bound=0, is_intensive=True,
                 default = 5e-5/years / kelvins
                 )
    mortality_reference_temperature = \
        Variable("reference temperature for relationship with mortality", 
                 "default: pre-industrial value",
                 unit=kelvins, lower_bound=0,
                 default=287)  # TODO: verify! 
    
    births = Variable("births per time", "",
                      unit = people / years,
                      lower_bound=0, is_extensive=True, default=0)
    deaths = Variable("deaths per time", "",
                      unit = people / years,
                      lower_bound=0, is_extensive=True, default=0)
    
    immigration = Variable("immigrants per time", "",
                           unit = people / years,
                           lower_bound=0, is_extensive=True, default=0)
    emigration = Variable("emigrants per time", "",
                          unit = people / years,
                          lower_bound=0, is_extensive=True, default=0)
    
    
    # Resource extraction and waste:
    
    biomass_harvest_flow = Variable("biomass harvest flow", "",
                                    unit = gigatonnes_carbon / years, # leave whitespace as it is, for g*ds sake!!!!
                                    lower_bound=0, is_extensive=True, default=0)
    
    fossil_extraction_flow = Variable("fossil extraction flow", "",
                                      unit = gigatonnes_carbon / years,
                                      lower_bound=0, is_extensive=True, default=0)
    
    carbon_emission_flow = Variable("carbon emission flow", "",
                                    unit = gigatonnes_carbon / years,
                                    IAMC="Emissions|CO2",
                                    lower_bound=0, is_extensive=True, default=0)
    
    # Economy:
    
    # labour, physical capital, energy input, other factors,
    # and their elasticities, prices (wages, capital rents, energy prices etc.),
    # depreciation rates
    # (total and by sector: energy(fossil/biomass/renewables)/final(clean/dirty)
    
    # stocks:
    
    physical_capital = \
        Variable("physical capital", "(in value units)", unit=dollars,
                 lower_bound=0, is_extensive=True, default=0)
    
    renewable_energy_knowledge = \
        Variable("renewable energy production knowledge stock",
                 "= non-depreciated cumulative energy produced in the past. "
                 "Interpreted as in Wright's law",
                 unit=gigajoules,
                 lower_bound=0, is_extensive=True, default=0)
    
    # flows:
    
    # TODO: clarify whether biomass should include food...
    biomass_input_flow = \
        Variable("biomass input flow",
                 "(in carbon units)",
                 IAMC="Primary Energy|Biomass",
                 unit = gigatonnes_carbon / years,
                 lower_bound=0, is_extensive=True, default=0)
    
    fossil_fuel_input_flow = \
        Variable("fossil fuels input flow",
                 "(in carbon units)",
                 IAMC="Primary Energy|Fossil",
                 unit = gigatonnes_carbon / years,
                 lower_bound=0, is_extensive=True, default=0)
    
    renewable_energy_input_flow = \
        Variable("non-biomass renewable energy input flow",
                 "",
                 IAMC="Primary Energy|Non-Biomass Renewables",
                 unit = gigajoules / years,
                 lower_bound=0, is_extensive=True, default=0)
    
    secondary_energy_flow = \
        Variable("secondary energy flow",
                 "(all sources)",
                 IAMC="Secondary Energy",
                 unit = gigajoules / years,
                 lower_bound=0, is_extensive=True, default=0)
    
    total_energy_intensity = \
        Variable("total energy intensity", "",
                 unit = gigajoules / dollars,
                 lower_bound=0, is_intensive=True, default = 1/147)
    
    economic_output_flow = \
        Variable("total economic output flow",
                 "(in value units)",
                 IAMC="GDP|PPP",  # or GDP|MER?
                 unit = dollars / years,
                 lower_bound=0, is_extensive=True, default=0)
    
    consumption_flow = \
        Variable("consumption flow", """(in value units)""",
                 IAMC="Consumption",
                 unit = dollars / years,
                 lower_bound=0, is_extensive=True, default=0)
    
    investment_flow = \
        Variable("flow of total investment into physical capital", "",
                 #             IAMC="Investment",
                 unit = dollars / years,
                 lower_bound=0, is_extensive=True, default=0)
    
    # per-capita quantities:
    
    welfare_flow_per_capita = \
        Variable("cardinal social welfare flow 'per capita'",
                 "Note that 'per capita' here does not imply that the value is "
                 "an average, but only that it is an intensive quantity",
                 unit = utils / people / years,
                 is_intensive=True, default=0)
    
    wellbeing = \
        Variable("well-being", "(in utility flow units)",
                 unit = utils / people / years,
                 is_intensive=True, default=0)
    
    # productivities, efficiencies etc.
    
    biomass_energy_density = Variable("biomass energy density", 
                                      "(default from Nitzbon 2016)",
                                      unit = gigajoules / gigatonnes_carbon,
                                      lower_bound=0, is_intensive=True,
                                      default=40e9)
    
    fossil_energy_density = Variable("fossil energy density", 
                                     "(default from Nitzbon 2016)",
                                     unit = gigajoules / gigatonnes_carbon,
                                     lower_bound=0, is_intensive=True,
                                     default=47e9)
    
    
    # protected shares:
    
    protected_terrestrial_carbon = \
        Variable("protected stock of terrestrial carbon",
                 """what stock of the current terrestrial carbon will be treated
                 as protected and thus not harvested at each point in time""",
                 unit=gigatonnes_carbon, lower_bound=0,
                 default=0)  # may be increased by cultural components
    protected_fossil_carbon = \
        Variable("protected stock of fossil carbon",
                 """what stock of the current fossil carbon will be treated
                 as protected and thus not extracted at each point in time""",
                 unit=gigatonnes_carbon, lower_bound=0,
                 default=0)  # may be increased by cultural components
    protected_terrestrial_carbon_share = \
        Variable("protected share of terrestrial carbon",
                 """what share of the current terrestrial carbon will be treated
                 as protected and thus not harvested at each point in time""",
                 unit=unity, lower_bound=0, upper_bound=1,
                 default=0)  # may be increased by cultural components
    protected_fossil_carbon_share = \
        Variable("protected share of fossil carbon",
                 """what share of the current fossil carbon will be treated
                 as protected and thus not extracted at each point in time""",
                 unit=unity, lower_bound=0, upper_bound=1,
                 default=0)  # may be increased by cultural components
    
    
    # depreciation, learning, discounting, interest etc. rates
    
    physical_capital_depreciation_rate = \
        Variable("physical capital depreciation rate", "",
                 unit = years**-1,
                 lower_bound=0, is_intensive=True,
                 default=0.1)
    basic_physical_capital_depreciation_rate = \
        Variable("basic physical capital depreciation rate", "",
                 unit = years**-1,
                 lower_bound=0, is_intensive=True,
                 default=0.1)
    physical_capital_depreciation_rate_temperature_sensitivity = \
        Variable("physical capital depreciation rate temperature sensitivity", "",
                 unit = years**-1 / kelvins,
                 lower_bound=0, is_intensive=True,
                 default = 0.05/years / kelvins
                    # the following gives much too large sensitivity:
                    # (40e9 * dollars / years) / (6e13 * dollars)
                    #    / ((1.5*kelvins) / (1000*gigatonnes_carbon))
                 )
    physical_capital_depreciation_rate_reference_temperature = \
        Variable("reference temperature for relationship with capital depreciation", 
                 "default: pre-industrial value",
                 unit=kelvins, lower_bound=0,
                 default=287)  # TODO: verify! 
    
    renewable_energy_knowledge_depreciation_rate = \
        Variable("renewable energy production knowledge depreciation rate", "",
                 unit = years**-1,
                 lower_bound=0, is_intensive=True,
                 default=0.02)
    
    # other non-time rates:
    
    savings_rate = \
        Variable("savings (investment) rate", "(as a fraction of income)",
                 unit=unity,
                 lower_bound=0, upper_bound=1, is_intensive=True,
                 default=0.244)
    
    renewable_energy_knowledge_spillover_fraction = \
        Variable("renewable_energy_knowledge_spillover_fraction", "",
                 unit=unity,
                 lower_bound=0, upper_bound=1, is_intensive=True,
                 default=0)
    
    # financial capital?
    
    # transaction costs?
    
    # trade network?
    
    
    # Infrastructure:
    
    # transportation network?
    
    # housing and similar assets?
