"""model component Interface."""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

# from ... import master_data_model as D
from ...data_model.master_data_model import S


class Model (object):
    """Interface for Model mixin."""

    # metadata:
    name = "copan:GLOBAL-like economic growth"
    """a unique name for the model component"""
    description = """capital investments at fixed savings rate,
       learning-by-doing in renewable energy sector"""
    """some longer description"""
    requires = []
    """list of other model components required for this model component to
    make sense"""

    # Notes:
    # - Model does NOT define variables or parameters, only entity types
    #   and process taxons do!
    # - implementation.Model lists these entity-types and process taxons


# entity types:


class Society (object):
    """Interface for Society entity type mixin."""

    # endogenous variables:

    physical_capital = S.physical_capital
    renewable_energy_knowledge = S.renewable_energy_knowledge

    # output-only variables:

    investment_flow = S.investment_flow
    consumption_flow = S.consumption_flow

    # exogenous variables / parameters:

    total_output_flow = S.total_output_flow
    renewable_energy_input_flow = S.renewable_energy_input_flow

    savings_rate = S.savings_rate
    physical_capital_depreciation_rate = S.physical_capital_depreciation_rate
    renewable_energy_knowledge_depreciation_rate = \
        S.renewable_energy_knowledge_depreciation_rate
