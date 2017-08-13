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
from .... import master_data_model as D

from .. import interface as I

import sympy as sp  # to be able to use sp.sqrt


class Society (I.Society):
    """Society entity type mixin implementation class."""

    # abbreviations:

    # for pairwise migration formula:
    this_society = I.Society
    other_society = B.Society.world.societies  # we will sum about all those!

    processes = [
                 
        Explicit("emigration",
            [this_society.emigration],
            [B.Society.metabolism.basic_emigration_probability_rate
             * this_society.population 
             * B.Society.world.sum(  # here is the summation
                other_society.population
                * (1/2 + 1/sp.pi * sp.atan(
                    sp.pi
                    * B.Society.metabolism.emigration_probability_characteristic_slope
                    * (other_society.wellbeing 
                       - this_society.wellbeing
                       - B.Society.metabolism.emigration_wellbeing_difference_offset)
                    )
                  )
                )
            ]),
                 
        Explicit("immigration",
            [this_society.immigration],
            [B.Society.metabolism.basic_emigration_probability_rate
             * this_society.population 
             * B.Society.world.sum(  # here is the summation again
                other_society.population
                * (1/2 + 1/sp.pi * sp.atan(
                    sp.pi
                    * B.Society.metabolism.emigration_probability_characteristic_slope
                    * (this_society.wellbeing 
                       - other_society.wellbeing
                       - B.Society.metabolism.emigration_wellbeing_difference_offset)
                    )
                  )
                )
            ]),
                 
        ODE("migration dynamics",
            [I.Society.population],
            [I.Society.immigration - I.Society.emigration])

    ]
