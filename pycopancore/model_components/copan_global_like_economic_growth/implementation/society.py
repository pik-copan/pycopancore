"""Society entity type mixing class.
"""
# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from .. import interface as I
from .... import Explicit, ODE
from .... import master_data_model as D


class Society (I.Society):
    """Society entity type mixin implementation class."""

    # standard methods:

    def __init__(self,
                 *,
                 population = 1 * D.people,
                 physical_capital = 1 * D.dollars,
                 renewable_energy_knowledge = 1 * D.gigajoules,
                 savings_rate = 0.244,  # see Nitzbon 2016
                 physical_capital_depreciation_rate = 0.1 / D.years,  # see Nitzbon 2016
                 renewable_energy_knowledge_depreciation_rate = 0.02 / D.years,
                 **kwargs):
        """Initialize an instance of Society."""
        super().__init__(**kwargs)  # must be the first line

        self.population = population
        self.physical_capital = physical_capital
        self.renewable_energy_knowledge = \
            renewable_energy_knowledge
        self.savings_rate = savings_rate
        self.physical_capital_depreciation_rate = \
            physical_capital_depreciation_rate
        self.renewable_energy_knowledge_depreciation_rate = \
            renewable_energy_knowledge_depreciation_rate

    # process-related methods:

    def do_investment(self, unused_t):
        self.investment_flow = self.savings_rate * self.total_output_flow
        self.consumption_flow = self.total_output_flow - self.investment_flow

    def do_growth_and_depreciation(self, unused_t):
        self.d_physical_capital += self.investment_flow \
            - self.physical_capital_depreciation_rate \
                * self.physical_capital
        self.d_renewable_energy_knowledge += self.renewable_energy_input_flow \
            - self.renewable_energy_knowledge_depreciation_rate \
                * self.renewable_energy_knowledge

    processes = [
        Explicit("investment", [I.Society.investment_flow],
                 do_investment),
        ODE("growth and depreciation",
            [I.Society.physical_capital, I.Society.renewable_energy_knowledge],
            do_growth_and_depreciation)
        ]
