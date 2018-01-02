"""model component Interface template.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

# TODO: use variables from the master data model wherever possible:
from ... import master_data_model as D
from ...data_model.master_data_model import MET, S
from ... import Variable


class Model (object):
    """Interface for Model mixin."""

    # metadata:
    name = "copan:GLOBAL-like population growth"
    """a unique name for the model component"""
    description = "fertility and mortality act on SocialSystem level and depend on well-being"
    """some longer description"""
    requires = []
    """list of other model components required for this model component to
    make sense"""

    # Notes:
    # - Model does NOT define variables or parameters, only entity types
    #   and process taxons do!
    # - implementation.Model lists these entity-types and process taxons


# entity types:


class SocialSystem (object):
    """Interface for SocialSystem entity type mixin."""

    # endogenous variables:
    
    population = S.population
    population.default = 1 * D.people
    
    migrant_population = S.migrant_population
    
    wellbeing = S.wellbeing
    wellbeing.default = 1 * D.utils / D.people / D.years

    fertility = S.fertility
    mortality = S.mortality
    mortality_temperature_sensitivity = S.mortality_temperature_sensitivity
    mortality_reference_temperature = S.mortality_reference_temperature

    births = S.births
    deaths = S.deaths

    # exogenous variables / parameters:
    
    physical_capital = S.physical_capital
    consumption_flow = S.consumption_flow
    

# process taxa:


class Metabolism (object):
    """Interface for Metabolism process taxon mixin."""

    # endogenous variables:

    # exogenous variables / parameters:
    min_fertility = MET.min_fertility
    max_fertility = MET.max_fertility
    fertility_maximizing_wellbeing = Variable(
        "fertility-maximizing value of well-being", 
        "",
        unit = D.utils / D.people / D.years,
        lower_bound=0, is_intensive=True,
        default=2000)
    fertility_decay_exponent = Variable(
        "exponent of power-law shaped asymptotic decay of fertility "
        "for large wellbeing", "",
        unit = D.unity,
        strict_lower_bound=0, is_intensive=True,
        default=1/2)
    characteristic_mortality = Variable(
        "characteristic mortality rate",
        "mortality rate at fertility-maximizing value of well-being",
        unit = D.years**-1,
        lower_bound=0, is_intensive=True, 
        default=0.02)
    mortality_decay_exponent = Variable(
        "exponent of power-law shaped asymptotic decay of mortality "
        "for large wellbeing", "",
        unit = D.unity,
        strict_lower_bound=0, is_intensive=True,
        default=1/12)
#    renewable_energy_knowledge_depreciation_rate = \
#        MET.renewable_energy_knowledge_depreciation_rate
    population_spatial_competition_coefficient = Variable(
        "coeff. of spatial competition in population dynamics", 
        "causes a capital- and well-being-dependent per-area population limit",
        unit = D.dollars**0.5 / (D.people / D.square_kilometers) / D.years,
        lower_bound=0, is_intensive=True,
        default=0  # TODO: set properly
        )
    wellbeing_sensitivity_to_consumption = Variable(
        "sensitivity of wellbeing to per capita consumption flow", "",
        is_intensive=True, allow_None=False,
        default = 1 * D.utils / D.dollars)
    wellbeing_sensitivity_to_terrestrial_carbon = Variable(
        "sensitivity of wellbeing to terrestrial carbon density", "",
        unit = (D.utils/D.people/D.years) 
               / (D.gigatonnes_carbon/D.square_kilometers),
        is_intensive=True, allow_None=False,
        default = 1e-8 * (2000*D.utils / D.people / D.years) 
                  / (5500*D.gigatonnes_carbon / (1.5e8*D.square_kilometers)))
