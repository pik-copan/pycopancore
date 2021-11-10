"""Cell entity type mixing class template.

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

from .... import Explicit, ODE, ITE
from .. import interface as I
from ...base import interface as B

class Cell (I.Cell):
    """Cell entity type mixin implementation class."""

    processes = [
        ODE("exponentially discounted running mean of carbon",
            [I.Cell.mean_past_terrestrial_carbon],
            [ITE(B.Cell.world.culture.terrestrial_carbon_averaging_time > 0,
                 (I.Cell.terrestrial_carbon - I.Cell.mean_past_terrestrial_carbon) 
                    / B.Cell.world.culture.terrestrial_carbon_averaging_time,
                 0)  # if zero, then the Explicit process governs this variable
            ]),
        Explicit("infinitely fast discounted running mean of carbon",
            [I.Cell.mean_past_terrestrial_carbon],
            [ITE(B.Cell.world.culture.terrestrial_carbon_averaging_time > 0,
                 I.Cell.mean_past_terrestrial_carbon,  # if nonzero, then the ODE process governs this variable
                 I.Cell.terrestrial_carbon)
            ])
    ]
