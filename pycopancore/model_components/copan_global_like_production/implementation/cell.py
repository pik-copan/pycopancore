"""Cell entity type mixing class template.

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

from .... import Explicit
from .... import master_data_model as D
from .. import interface as I
from ...base import interface as B

# import numpy as np


class Cell (I.Cell):
    """Cell entity type mixin implementation class."""

    # standard methods:

    processes = [

        Explicit("sectoral relative productivities",
                 [I.Cell.biomass_relative_productivity,
                  I.Cell.fossil_relative_productivity,
                  I.Cell.renewable_relative_productivity],
                 [
                     I.Cell.biomass_sector_productivity
                     * (I.Cell.terrestrial_carbon
                        * (1 - B.Cell.society.protected_terrestrial_carbon_share)
                        )**2,
                     I.Cell.fossil_sector_productivity
                     * (I.Cell.fossil_carbon
                         * (1 - B.Cell.society.protected_fossil_carbon_share)
                        )**2,
                     I.Cell.renewable_sector_productivity
                     * (B.Cell.society.renewable_energy_knowledge
                        )**2
                 ]),

        Explicit("total relative productivity",
                 [I.Cell.total_relative_productivity],
                 [
                     (I.Cell.biomass_relative_productivity
                      + I.Cell.fossil_relative_productivity
                      + I.Cell.renewable_relative_productivity)
                     / I.Cell.total_energy_intensity
                 ])

    ]
