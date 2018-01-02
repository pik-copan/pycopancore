"""Jobst: write docstring."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from .... import Explicit, ODE
from .... import master_data_model as D
from ...base import interface as B

from .. import interface as I

import numpy as np
import sympy as sp


class Cell (I.Cell):
    """Jobst: write docstring."""

    # standard methods:

    def __init__(self,
                 *,
                 terrestrial_carbon=1 * D.gigatonnes_carbon,
                 fossil_carbon=1 * D.gigatonnes_carbon,
                 **kwargs
                 ):
        """Initialize a cell"""
        super().__init__(**kwargs)
        # initial values:
        self.terrestrial_carbon = terrestrial_carbon
        self.fossil_carbon = fossil_carbon

    # abbreviations:

    balance = I.Cell.net_ecosystem_production - I.Cell.human_offtake

    processes = [  # using symbolic expressions for performance reasons:

        Explicit("net ecosystem production",
                 [I.Cell.net_ecosystem_production],
                 [B.Cell.environment.ecosystem_dependent_conversion_factor
                  * I.Cell.terrestrial_carbon * (1 - (I.Cell.terrestrial_carbon
                                                      / B.Cell.environment.terrestrial_carbon_carrying_capacity))
                  * (I.World.photosynthesis_rate - I.World.respiration_rate)
                  ]),


        # capacity per area?
        # Explicit("net ecosystem production",
        #          [I.Cell.net_ecosystem_production],
        #          [B.Cell.environment.ecosystem_dependent_conversion_factor
        #           * I.Cell.terrestrial_carbon * (1 - (I.Cell.terrestrial_carbon
        #                                               / (B.Cell.environment.terrestrial_carbon_capacity_per_area
        #             * B.Cell.land_area)))
        #           * (I.World.photosynthesis_rate - I.World.respiration_rate)
        #           ]),

        Explicit("human offtake",  # Interface
                 [I.Cell.human_offtake],
                 [I.SocialSystem.harvest_rate * I.Cell.terrestrial_carbon
                  ]),

        ODE("effect of photosynthesis and respiration",
            [I.Cell.terrestrial_carbon, B.Cell.world.atmospheric_carbon],
            [balance, -balance]),

    ]

# instead of:
#
#    def do_photosynthesis(self, unused_t):
#        """compute and store rhs of ODE photosynthesis"""
#
#        # abbreviations:
#        L = self.terrestrial_carbon
#        Sigma = self.land_area
#
#        self.photosynthesis_carbon_flow = \
#            ((self.environment.basic_photosynthesis_productivity
#              - self.environment.photosynthesis_sensitivity_on_atmospheric_carbon
#                * self.world.atmospheric_carbon)
#             * np.sqrt(self.world.atmospheric_carbon / Sigma)
#             * (1 - L / (self.environment.terrestrial_carbon_capacity_per_area
#                         * Sigma))) \
#            * L
#
#        self.world.d_atmospheric_carbon -= self.photosynthesis_carbon_flow
#        self.d_terrestrial_carbon += self.photosynthesis_carbon_flow
#
#    def do_respiration(self, unused_t):
#        """compute and store rhs of ODE respiration"""
#
#        self.terrestrial_respiration_carbon_flow = \
#            (self.environment.basic_respiration_rate
#             + self.environment.respiration_sensitivity_on_atmospheric_carbon
#               * self.world.atmospheric_carbon) \
#            * self.terrestrial_carbon
#
#        self.d_terrestrial_carbon -= self.terrestrial_respiration_carbon_flow
#        self.world.d_atmospheric_carbon += self.terrestrial_respiration_carbon_flow
#
#    processes = [
#                 ODE("photosynthesis", [I.Cell.terrestrial_carbon,
#                                        B.Cell.world.atmospheric_carbon],
#                     do_photosynthesis),
#                 ODE("respiration", [I.Cell.terrestrial_carbon, I.World.atmospheric_carbon],
#                     do_respiration),
#                 ]
