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
from sympy import ITE, Min

# import numpy as np


class Cell (I.Cell):
    """Cell entity type mixin implementation class."""

    # TODO: allocate protected stock more adequately than this:
    quotient = (B.Cell.society.protected_terrestrial_carbon
                / B.Cell.society.sum.cells.terrestrial_carbon)
        
    unprotected_terrestrial_carbon_squared = ITE(quotient < 1, 
                                                 (I.Cell.terrestrial_carbon * (1 - quotient))**2, 
                                                 0) #Min(1, quotient)

    processes = [

        Explicit("sectoral relative productivities",
                 [I.Cell.biomass_relative_productivity,
                  I.Cell.fossil_relative_productivity,
                  I.Cell.renewable_relative_productivity],
                 [
                  I.Cell.biomass_sector_productivity
                  # TODO: verify the following:
                  * ITE(B.Cell.society.has_emissions_tax,
                        ITE(quotient < 1, 
                            (I.Cell.terrestrial_carbon * (1 - quotient))**2 
                            * (1 
                               - B.Cell.society.emissions_tax_level 
                               * I.Cell.total_energy_intensity
                               / B.Cell.metabolism.biomass_energy_density), 
                            0),
                        unprotected_terrestrial_carbon_squared),
                  ITE(B.Cell.society.has_fossil_ban, 0,
                      I.Cell.fossil_sector_productivity
                      # TODO: verify the following:
                      * ITE(B.Cell.society.has_emissions_tax,
                            (I.Cell.fossil_carbon
                             * (1 - B.Cell.society.protected_fossil_carbon_share)
                             )**2 * (
                                1 
                                - B.Cell.society.emissions_tax_level
                                  * I.Cell.total_energy_intensity 
                                  / B.Cell.metabolism.fossil_energy_density),
                            (I.Cell.fossil_carbon
                             * (1 - B.Cell.society.protected_fossil_carbon_share)
                             )**2)
                      ),
                  I.Cell.renewable_sector_productivity
                  # TODO: verify the following:
                  * ITE(B.Cell.society.has_renewable_subsidy,
                        (B.Cell.society.renewable_energy_knowledge)**2 * (
                            1
                            + B.Cell.society.renewable_subsidy_level
                              * I.Cell.total_energy_intensity),
                        (B.Cell.society.renewable_energy_knowledge)**2)
                 ]),

        Explicit("total relative productivity",
                 [I.Cell.total_relative_productivity],
                 [
                     I.Cell.biomass_relative_productivity
                     + I.Cell.fossil_relative_productivity
                     + I.Cell.renewable_relative_productivity 
                 ])

    ]
