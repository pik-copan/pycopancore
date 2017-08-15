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

    fert = (2 * B.Society.metabolism.max_fertility * I.Society.wellbeing 
            * B.Society.metabolism.fertility_maximizing_wellbeing
            / (I.Society.wellbeing**2
               + B.Society.metabolism.fertility_maximizing_wellbeing**2))
    
    mort = (B.Society.metabolism.characteristic_mortality
            / sqrtorzero(I.Society.wellbeing
                         / B.Society.metabolism.fertility_maximizing_wellbeing)
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
               * I.Society.consumption_flow / (1e-10 + I.Society.population) 
             + B.Society.metabolism.wellbeing_sensitivity_to_terrestrial_carbon 
               * terrestrial_carbon / (1e-10 + land_area),
             fert,
             mort,
             I.Society.population * fert,
             I.Society.population * mort]),
                 
        ODE("population dynamics",
            [I.Society.population],
            [I.Society.births - I.Society.deaths])

    ]
