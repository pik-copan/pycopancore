"""provides this model component's SocialSystem mixin class"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from .. import interface as I
from .... import Explicit, ODE
from ...base import interface as B


class SocialSystem (I.SocialSystem):
    """SocialSystem entity type mixin implementation class."""

    processes = [

        Explicit("investment", 
                 [I.SocialSystem.investment_flow, 
                  I.SocialSystem.consumption_flow],
                 [I.SocialSystem.savings_rate * I.SocialSystem.economic_output_flow,
                  (1 - I.SocialSystem.savings_rate) * I.SocialSystem.economic_output_flow]
                 ),
                 
        Explicit("capital depreciation rate",
                 [I.SocialSystem.physical_capital_depreciation_rate],
                 [I.SocialSystem.basic_physical_capital_depreciation_rate
                  + I.SocialSystem.physical_capital_depreciation_rate_temperature_sensitivity
                  * (B.SocialSystem.world.surface_air_temperature
                     - I.SocialSystem.physical_capital_depreciation_rate_reference_temperature)]
                 ),

        ODE("growth, spillovers, depreciation",
            [I.SocialSystem.physical_capital, 
             I.SocialSystem.renewable_energy_knowledge],
            [I.SocialSystem.investment_flow
             - I.SocialSystem.physical_capital_depreciation_rate
             * I.SocialSystem.physical_capital,
             I.SocialSystem.renewable_energy_input_flow
             + B.SocialSystem.metabolism.renewable_energy_knowledge_spillover_fraction
               * (B.SocialSystem.world.renewable_energy_input_flow
                  - I.SocialSystem.renewable_energy_input_flow)
             - I.SocialSystem.renewable_energy_knowledge_depreciation_rate
             * I.SocialSystem.renewable_energy_knowledge])

    ]
