"""Jobst: write docstring."""

from .... import Explicit, ODE
from .. import interface as I
# from ...base import interface as base
from .... import master_data_model as D


class World (I.World):
    """Jobst: write docstring."""

    # standard methods:

    def __init__(self,
                 *,
                 atmospheric_carbon=1 * D.gigatonnes_carbon,
                 ocean_carbon=1 * D.gigatonnes_carbon,
                 surface_air_temperature=1 * D.kelvins,
                 **kwargs
                 ):
        """Initialize an (typically the unique) instance of World."""
        super().__init__(**kwargs)
        # initial values:
        self.atmospheric_carbon = atmospheric_carbon
        self.ocean_carbon = ocean_carbon
        self.surface_air_temperature = surface_air_temperature

    # process-related methods:

    def convert_temperature(self, unused_t):
        """(See Anderies et al. 2013)."""
        self.surface_air_temperature = self.nature.temperature_offset \
            + self.nature.temperature_sensitivity_on_atmospheric_carbon \
            * self.atmospheric_carbon

    def ocean_atmosphere_diffusion(self, unused_t):
        """(See Anderies et al. 2013)."""
        flow = self.nature.ocean_atmosphere_diffusion_coefficient * (
                self.nature.carbon_solubility_in_sea_water * self.ocean_carbon
                - self.atmospheric_carbon)
        self.d_ocean_carbon -= flow
        self.d_atmospheric_carbon += flow

    processes = [
                 Explicit("convert temperature",
                          [I.World.surface_air_temperature],
                          convert_temperature),
                 ODE("ocean-atmosphere diffusion",
                     [I.World.ocean_carbon, I.World.atmospheric_carbon],
                     ocean_atmosphere_diffusion)
                 ]
