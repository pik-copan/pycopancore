"""SocialSystem entity type mixing class template.

TODO: adjust or fill in code and documentation wherever marked by "TODO:",
then remove these instructions
"""
# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from .... import Explicit, ODE
from ...base import interface as B
from .... import master_data_model as D

from .. import interface as I

import sympy as sp  # to be able to use sp.sqrt


# TODO: move this to a suitable place (like pycopancore.util?):
def sqrtorzero(expr):
    """square root if positive, zero otherwise.
    needed since ODE solver may pass negative values in Jacobian estimation"""
    return sp.sqrt(sp.Max(0, expr))


class SocialSystem (I.SocialSystem):
    """SocialSystem entity type mixin implementation class."""

    # abbreviations:
    land_area = B.SocialSystem.sum.cells.land_area
    terrestrial_carbon = B.SocialSystem.sum.cells.terrestrial_carbon
    min_fert = B.SocialSystem.metabolism.min_fertility
    fert_exp = B.SocialSystem.metabolism.fertility_decay_exponent
 
    pop = I.SocialSystem.population
 
    fert = (min_fert
            + 2 * (B.SocialSystem.metabolism.max_fertility - min_fert) 
              * I.SocialSystem.wellbeing 
              * B.SocialSystem.metabolism.fertility_maximizing_wellbeing
                ** fert_exp
              / (I.SocialSystem.wellbeing ** (1 + fert_exp)
                 + B.SocialSystem.metabolism.fertility_maximizing_wellbeing
                   ** (1 + fert_exp)
              )
           )
     
    mort = (B.SocialSystem.metabolism.characteristic_mortality
            / (I.SocialSystem.wellbeing
               / B.SocialSystem.metabolism.fertility_maximizing_wellbeing)
              ** B.SocialSystem.metabolism.mortality_decay_exponent
            + I.SocialSystem.mortality_temperature_sensitivity
            * (B.SocialSystem.world.surface_air_temperature
               - I.SocialSystem.mortality_reference_temperature)
            + B.SocialSystem.metabolism.population_spatial_competition_coefficient
            * (I.SocialSystem.population / land_area)
            / sp.sqrt(I.SocialSystem.physical_capital))
    
    processes = [
                 
        Explicit("wellbeing, fertility, mortality, births, deaths",
            [I.SocialSystem.wellbeing,
             I.SocialSystem.fertility,
             I.SocialSystem.mortality,
             I.SocialSystem.births,
             I.SocialSystem.deaths],
            [B.SocialSystem.metabolism.wellbeing_sensitivity_to_consumption 
               * I.SocialSystem.consumption_flow / pop 
             + B.SocialSystem.metabolism.wellbeing_sensitivity_to_terrestrial_carbon 
               * terrestrial_carbon / land_area,
             fert,
             mort,
             pop * fert,
             pop * mort]),
                 
        ODE("population dynamics",
            [pop, 
             I.SocialSystem.migrant_population],
            [I.SocialSystem.births - I.SocialSystem.deaths,
             - I.SocialSystem.deaths * I.SocialSystem.migrant_population / pop])

    ]
