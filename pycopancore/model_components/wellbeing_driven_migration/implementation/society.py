"""Society entity type mixing class template.
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

from .. import interface as I

import sympy as sp  # to be able to use symbolic constants and functions


class Society (I.Society):
    """Society entity type mixin implementation class."""

    # abbreviations:
    basic_rate = B.Society.metabolism.basic_emigration_probability_rate
    slope = B.Society.metabolism.emigration_probability_characteristic_slope
    offset = B.Society.metabolism.emigration_wellbeing_quotient_offset

    # for pairwise migration formula:
    this_society = I.Society
    other_society = B.Society.world.societies  # we will sum about all those!
    
    processes = [
                 
        Explicit("emigration",
            [this_society.emigration],
            [basic_rate
             * this_society.population 
             * B.Society.world.sum(  # here is the summation
                other_society.population
                * (1/2 + 1/sp.pi * sp.atan(
                    sp.pi
                    * slope
                    * (other_society.wellbeing 
                       / this_society.wellbeing
                       - offset)
                    )
                  )
                )
            ]),
                 
        Explicit("immigration",
            [this_society.immigration],
            [basic_rate
             * this_society.population 
             * B.Society.world.sum(  # here is the summation again
                other_society.population
                * (1/2 + 1/sp.pi * sp.atan(
                    sp.pi
                    * slope
                    * (this_society.wellbeing 
                       / other_society.wellbeing
                       - offset)
                    )
                  )
                )
            ]),
                 
        ODE("effect of migration",
            [I.Society.population,
             I.Society.migrant_population],
            [I.Society.immigration 
             - I.Society.emigration,
             I.Society.immigration 
             - I.Society.emigration * I.Society.migrant_population 
                                    / I.Society.population])

    ]
