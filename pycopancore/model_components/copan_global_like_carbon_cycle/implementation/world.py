"""provides this model component's World mixin class"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from .... import Explicit, ODE
from .. import interface as I
from ...base import interface as B
from .... import master_data_model as D


class World (I.World):
    """World with ocean-atmosphere diffusion 
    and linear relationship between temperature and atmospheric carbon
    """

    # abbreviation:
    diffusion_flow = (B.World.environment.ocean_atmosphere_diffusion_coefficient 
                      * (I.World.upper_ocean_carbon
                         - B.World.environment.carbon_solubility_in_sea_water 
                           * I.World.atmospheric_carbon))
    """(See Nitzbon et al. 2017)."""

    processes = [

        Explicit("immediate greenhouse effect",
                 [I.World.surface_air_temperature],
                 [B.World.environment.reference_temperature
                  + B.World.environment.temperature_sensitivity_on_atmospheric_carbon
                  * (I.World.atmospheric_carbon 
                     - B.World.environment.reference_atmospheric_carbon)]),

        ODE("ocean-atmosphere diffusion",
            [I.World.upper_ocean_carbon, I.World.atmospheric_carbon],
            [-diffusion_flow, diffusion_flow])

    ]
