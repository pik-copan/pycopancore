"""model component Interface."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from ... import master_data_model as D
from ...data_model.master_data_model import MET, S, W


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


class Metabolism (object):
    """Interface for Metabolism process taxon mixin."""

    renewable_energy_knowledge_spillover_fraction = \
        MET.renewable_energy_knowledge_spillover_fraction


# entity types:


class World (object):
    """Interface for World entity type mixin."""

    renewable_energy_input_flow = W.renewable_energy_input_flow


class SocialSystem (object):
    """Interface for SocialSystem entity type mixin."""

    # endogenous variables:

    physical_capital = S.physical_capital
    physical_capital.default = 1 * D.dollars
    
    renewable_energy_knowledge = S.renewable_energy_knowledge
    renewable_energy_knowledge.default = 1 * D.gigajoules

    physical_capital_depreciation_rate = S.physical_capital_depreciation_rate

    # output-only variables:

    investment_flow = S.investment_flow
    consumption_flow = S.consumption_flow

    # exogenous variables / parameters:

    economic_output_flow = S.economic_output_flow
    renewable_energy_input_flow = S.renewable_energy_input_flow

    savings_rate = S.savings_rate
    basic_physical_capital_depreciation_rate = \
        S.basic_physical_capital_depreciation_rate
    physical_capital_depreciation_rate_temperature_sensitivity = \
        S.physical_capital_depreciation_rate_temperature_sensitivity
    physical_capital_depreciation_rate_reference_temperature = \
        S.physical_capital_depreciation_rate_reference_temperature
    renewable_energy_knowledge_depreciation_rate = \
        S.renewable_energy_knowledge_depreciation_rate
    