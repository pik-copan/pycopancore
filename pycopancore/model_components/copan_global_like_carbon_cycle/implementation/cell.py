"""Jobst: write docstring."""
from pycopancore import ODE
from pycopancore import master_data_model as D
from .. import interface as I
from numpy import sqrt


class Cell (I.Cell):
    """Jobst: write docstring."""

    # standard methods:

    def __init__(self,
                 *,
                 terrestrial_carbon = 1 * D.gigatonnes_carbon,
                 fossil_carbon = 1 * D.gigatonnes_carbon,
                 **kwargs
                 ):
        """Initialize a cell"""
        super().__init__(**kwargs)
        # initial values:
        self.terrestrial_carbon = terrestrial_carbon
        self.fossil_carbon = fossil_carbon

    # process-related methods:

    def do_photosynthesis(self, unused_t):
        """compute and store rhs of ODE photosynthesis"""

        # abbreviations:
        L = self.terrestrial_carbon
        Sigma = self.land_area

        self.photosynthesis_carbon_flow = \
            ((self.nature.basic_photosynthesis_productivity
              - self.nature.photosynthesis_sensitivity_on_atmospheric_carbon
                * self.world.atmospheric_carbon)
             * sqrt(self.world.atmospheric_carbon / Sigma)
             * (1 - L / (self.nature.terrestrial_carbon_capacity_per_area 
                         * Sigma))) \
            * L

        self.d_terrestrial_carbon += self.photosynthesis_carbon_flow

    def do_respiration(self, unused_t):
        """compute and store rhs of ODE respiration"""

        self.terrestrial_respiration_carbon_flow = \
            (self.nature.basic_respiration_rate
             + self.nature.respiration_sensitivity_on_atmospheric_carbon
               * self.world.atmospheric_carbon) \
            * self.terrestrial_carbon

        self.d_terrestrial_carbon += - self.terrestrial_respiration_carbon_flow

    processes = [
                 ODE("photosynthesis", [I.Cell.terrestrial_carbon],
                     do_photosynthesis),
                 ODE("respiration", [I.Cell.terrestrial_carbon],
                     do_respiration),
                 ]
