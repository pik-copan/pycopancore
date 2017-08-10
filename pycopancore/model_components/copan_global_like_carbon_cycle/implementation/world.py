"""provides this model component's World mixin class"""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from .... import Explicit, ODE
from .. import interface as I
from ...base import interface as B
from .... import master_data_model as D


class World (I.World):
    """World with ocean-atmosphere diffusion 
    and linear relationship between temperature and atmospheric carbon
    """

    # abbreviation:
    flow = (B.World.nature.ocean_atmosphere_diffusion_coefficient 
            * (B.World.nature.carbon_solubility_in_sea_water 
               * I.World.ocean_carbon
               - I.World.atmospheric_carbon))
    """(See Anderies et al. 2013)."""

    processes = [

        Explicit("convert temperature",
                 [I.World.surface_air_temperature],
                 [B.World.nature.reference_temperature
                  + B.World.nature.temperature_sensitivity_on_atmospheric_carbon
                  * (I.World.atmospheric_carbon 
                     - B.World.nature.reference_atmospheric_carbon)]),

        ODE("ocean-atmosphere diffusion",
            [I.World.ocean_carbon, I.World.atmospheric_carbon],
            [-flow, flow])

    ]
