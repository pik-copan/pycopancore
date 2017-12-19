"""provides this model component's Cell mixin class"""

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

import sympy as sp  # to be able to use sp.sqrt


class Cell (I.Cell):
    """Jobst: write docstring."""

    # abbreviation:

    balance = (I.Cell.photosynthesis_carbon_flow
               - I.Cell.terrestrial_respiration_carbon_flow)
    atmospheric_carbon_density = sp.Max(0, B.Cell.world.atmospheric_carbon 
                               / B.Cell.world.sum.cells.land_area)

    processes = [  # using symbolic expressions for performance and legibility:

        Explicit("photosynthesis flow",
                 [I.Cell.photosynthesis_carbon_flow],
                 [((B.Cell.environment.basic_photosynthesis_productivity
                    - B.Cell.environment.photosynthesis_sensitivity_on_atmospheric_carbon
                      * atmospheric_carbon_density)
                   * sp.sqrt(atmospheric_carbon_density)
                   * (1 - I.Cell.terrestrial_carbon
                          / (B.Cell.environment.terrestrial_carbon_capacity_per_area
                             * B.Cell.land_area))
                   )
                  * I.Cell.terrestrial_carbon
                  ]),

        Explicit("respiration flow",
                 [I.Cell.terrestrial_respiration_carbon_flow],
                 [(B.Cell.world.environment.basic_respiration_rate
                   + B.Cell.world.environment.respiration_sensitivity_on_atmospheric_carbon
                     * atmospheric_carbon_density)
                  * I.Cell.terrestrial_carbon
                  ]),

        ODE("effect of photosynthesis and respiration",
            [I.Cell.terrestrial_carbon, 
             B.Cell.world.atmospheric_carbon],
            [balance, 
             -balance]),

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
#        self.world.d_atmospheric_carbon += (self
#                                            .terrestrial_respiration_carbon_flow)
#
#    processes = [
#                 ODE("photosynthesis", [I.Cell.terrestrial_carbon,
#                                        B.Cell.world.atmospheric_carbon],
#                     do_photosynthesis),
#                 ODE("respiration", [I.Cell.terrestrial_carbon,
#                                     I.World.atmospheric_carbon],
#                     do_respiration),
#                 ]
