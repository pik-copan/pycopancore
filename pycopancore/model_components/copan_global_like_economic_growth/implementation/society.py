"""provides this model component's Society mixin class"""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from .. import interface as I
from .... import Explicit, ODE
from ...base import interface as B


class Society (I.Society):
    """Society entity type mixin implementation class."""

    processes = [

        Explicit("investment", 
                 [I.Society.investment_flow, 
                  I.Society.consumption_flow],
                 [I.Society.savings_rate * I.Society.total_output_flow,
                  (1 - I.Society.savings_rate) * I.Society.total_output_flow]
                 ),

        ODE("growth and depreciation",
            [I.Society.physical_capital, 
             I.Society.renewable_energy_knowledge],
            [I.Society.investment_flow
             - I.Society.physical_capital_depreciation_rate
             * I.Society.physical_capital,
             I.Society.renewable_energy_input_flow
             + B.Society.metabolism.renewable_energy_knowledge_spillover_fraction
               * (B.Society.world.sum.societies.renewable_energy_input_flow
                  - I.Society.renewable_energy_input_flow)
             - I.Society.renewable_energy_knowledge_depreciation_rate
             * I.Society.renewable_energy_knowledge])

    ]
