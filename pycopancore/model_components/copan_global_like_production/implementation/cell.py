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

from .. import interface as I
from pycopancore import master_data_model as D


class Cell (I.Cell):
    """Cell entity type mixin implementation class."""

    # standard methods:

    def __init__(self,
                 *,
                 biomass_sector_productivity =
                    1e5, #* (D.gigajoules / D.years)**5
                        #/ (D.gigatonnes_carbon * D.dollars * D.people)**2,
                fossil_sector_productivity =
                    1e6, #* (D.gigajoules / D.years)**5
                        #/ (D.gigatonnes_carbon * D.dollars * D.people)**2,
                renewable_sector_productivity =
                    1e-18, #* D.gigajoules**3 / D.years**5
                        #/ (D.dollars * D.people)**2,  # TODO!
                total_energy_intensity =
                    1/147, #* D.gigajoules/D.dollars,  # see Nitzbon 2016
                 **kwargs):
        """Initialize an instance of Cell."""
        super().__init__(**kwargs)  # must be the first line

        self.biomass_sector_productivity = biomass_sector_productivity
        self.fossil_sector_productivity = fossil_sector_productivity
        self.renewable_sector_productivity = renewable_sector_productivity
        self.total_energy_intensity = total_energy_intensity

    processes = []
