"""Society entity type mixing class template.

TODO: adjust or fill in code and documentation wherever marked by "TODO:",
then remove these instructions
"""
# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

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


class Society (I.Society):
    """Society entity type mixin implementation class."""

    # abbreviations:
    land_area = B.Society.sum.cells.land_area
    terrestrial_carbon = B.Society.sum.cells.terrestrial_carbon
    min_fert = B.Society.metabolism.min_fertility
    fert_exp = B.Society.metabolism.fertility_decay_exponent

    pop = I.Society.population

    fert = (min_fert
            + 2 * (B.Society.metabolism.max_fertility - min_fert) 
              * I.Society.wellbeing 
              * B.Society.metabolism.fertility_maximizing_wellbeing
                ** fert_exp
              / (I.Society.wellbeing ** (1 + fert_exp)
                 + B.Society.metabolism.fertility_maximizing_wellbeing
                   ** (1 + fert_exp)
              )
           )
    
    mort = (B.Society.metabolism.characteristic_mortality
            / (I.Society.wellbeing
               / B.Society.metabolism.fertility_maximizing_wellbeing)
              ** B.Society.metabolism.mortality_decay_exponent
            + B.Society.metabolism.population_spatial_competition_coefficient
            * (I.Society.population / land_area)
            / sp.sqrt(I.Society.physical_capital))
    
    processes = [
                 
        Explicit("wellbeing, fertility, mortality, births, deaths",
            [I.Society.wellbeing,
             I.Society.fertility,
             I.Society.mortality,
             I.Society.births,
             I.Society.deaths],
            [B.Society.metabolism.wellbeing_sensitivity_to_consumption 
               * I.Society.consumption_flow / pop 
             + B.Society.metabolism.wellbeing_sensitivity_to_terrestrial_carbon 
               * terrestrial_carbon / land_area,
             fert,
             mort,
             pop * fert,
             pop * mort]),
                 
        ODE("population dynamics",
            [pop, 
             I.Society.migrant_population],
            [I.Society.births - I.Society.deaths,
             - I.Society.deaths * I.Society.migrant_population / pop])

    ]
