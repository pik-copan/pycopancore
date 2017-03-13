"""Metabolism process taxon mixin class.
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


class Metabolism (I.Metabolism):
    """Metabolism process taxon mixin implementation class."""

    # standard methods:

    def __init__(self,
                 *,
                 biomass_energy_density = 
                    40e9 * D.gigajoules/D.gigatonnes_carbon,  # see Nitzbon 2016
                 fossil_energy_density =
                    47e9 * D.gigajoules/D.gigatonnes_carbon,  # see Nitzbon 2016
                 **kwargs):
        """Initialize the unique instance of Metabolism."""
        super().__init__(**kwargs)  # must be the first line

        self.biomass_energy_density = biomass_energy_density
        self.fossil_energy_density = fossil_energy_density

    processes = []
