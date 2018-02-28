"""SocialSystem entity type mixing class template.
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

from .. import interface as I

import sympy as sp  # to be able to use symbolic constants and functions


class SocialSystem (I.SocialSystem):
    """SocialSystem entity type mixin implementation class."""

    # abbreviations:
    basic_rate = B.SocialSystem.metabolism.basic_emigration_probability_rate
    slope = B.SocialSystem.metabolism.emigration_probability_characteristic_slope
    offset = B.SocialSystem.metabolism.emigration_wellbeing_quotient_offset

    # for pairwise migration formula:
    this_social_system = I.SocialSystem
    other_social_system = B.SocialSystem.world.social_systems  # we will sum about all those!
    
    processes = [
                 
        Explicit("emigration",
            [this_social_system.emigration],
            [basic_rate
             * this_social_system.population 
             * B.SocialSystem.world.sum(  # here is the summation
                other_social_system.population
                * (1/2 + 1/sp.pi * sp.atan(
                    sp.pi
                    * slope
                    * sp.log(other_social_system.wellbeing 
                             / this_social_system.wellbeing 
                             / offset)
                    )
                  )
                )
            ]),
                 
        Explicit("immigration",
            [this_social_system.immigration],
            [basic_rate
             * this_social_system.population 
             * B.SocialSystem.world.sum(  # here is the summation again
                other_social_system.population
                * (1/2 + 1/sp.pi * sp.atan(
                    sp.pi
                    * slope
                    * sp.log(this_social_system.wellbeing 
                             / other_social_system.wellbeing 
                             / offset)
                    )
                  )
                )
            ]),
                 
        ODE("effect of migration",
            [I.SocialSystem.population,
             I.SocialSystem.migrant_population],
            [I.SocialSystem.immigration 
             - I.SocialSystem.emigration,
             I.SocialSystem.immigration 
             # assuming an equal emigration probability among migrants:
             - I.SocialSystem.emigration * I.SocialSystem.migrant_population 
                                    / I.SocialSystem.population])

    ]
