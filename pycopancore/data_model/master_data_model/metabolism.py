"""Master data model for metabolism."""

from .. import Variable
from . import gigajoules, dollars, gigatonnes_carbon, years, utils, people
from .. import unity

# Population, demographics:

population = Variable("human population", "",
                      IAMC="Population",
                      CETS="SP.POP",
                      unit=people,
                      is_extensive=True, lower_bound = 0 * people)

# Note: when using the following, include
# Implicit(population == sum(population_by_age))
population_by_age = Variable("human population by age",
                             "(in years from 0 to 99+)",
                             IAMC="Population",
                             CETS="SP.POP",
                             unit=people,
                             is_extensive=True, lower_bound = 0 * people,
                             array_shape=(100,))  # 1d-array

fertility = Variable("current human fertility rate", "",
                     unit=years**-1,
                     lower_bound=0, is_intensive=True)
max_fertility = Variable("maximum human fertility rate", "",
                         unit=years**-1,
                         lower_bound=0, is_intensive=True,
                         default = 0.04 / years)
mortality = Variable("current human mortility rate", "",
                     unit=years**-1,
                     lower_bound=0, is_intensive=True)

births = Variable("births per time", "",
                  unit = people / years,
                  lower_bound=0, is_extensive=True, default=0)
deaths = Variable("deaths per time", "",
                  unit = people / years,
                  lower_bound=0, is_extensive=True, default=0)

# Resource extraction and waste:

biomass_harvest_flow = Variable("biomass harvest flow", "",
                                unit = gigatonnes_carbon / years, # leave whitespace as it is, for g*ds sake!!!!
                                lower_bound=0, is_extensive=True)

fossil_extraction_flow = Variable("fossil extraction flow", "",
                                  unit = gigatonnes_carbon / years,
                                  lower_bound=0, is_extensive=True)

carbon_emission_flow = Variable("carbon emission flow", "",
                                unit = gigatonnes_carbon / years,
                                IAMC="Emissions|CO2",
                                lower_bound=0, is_extensive=True)

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
             lower_bound=0, is_intensive=True)

total_output_flow = \
    Variable("total economic output flow",
             "(in value units)",
             IAMC="GDP|PPP",  # or GDP|MER?
             unit = dollars / years,
             lower_bound=0, is_extensive=True, default=1e-10)

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
             is_intensive=True, default=1e-1)

# productivities, efficiencies etc.

biomass_energy_density = Variable("biomass energy density", "",
                                  unit = gigajoules / gigatonnes_carbon,
                                  lower_bound=0, is_intensive=True)

fossil_energy_density = Variable("fossil energy density", "",
                                 unit = gigajoules / gigatonnes_carbon,
                                 lower_bound=0, is_intensive=True)

# depreciation, learning, discounting, interest etc. rates

physical_capital_depreciation_rate = \
    Variable("physical capital depreciation rate", "",
             unit = years**-1,
             lower_bound=0, is_intensive=True)

renewable_energy_knowledge_depreciation_rate = \
    Variable("renewable energy production knowledge depreciation rate", "",
             unit = years**-1,
             lower_bound=0, is_intensive=True)

# other non-time rates:

savings_rate = \
    Variable("savings (investment) rate", "(as a fraction of income)",
             unit=unity,
             lower_bound=0, upper_bound=1, is_intensive=True)


# financial capital?

# transaction costs?

# trade network?


# Infrastructure:

# transportation network?

# housing and similar assets?
