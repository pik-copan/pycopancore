"""copan_global_like_production model component Interface
"""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from pycopancore import master_data_model as D
from pycopancore import Variable


class Model (object):
    """Interface for Model mixin."""

    # metadata:
    name = "copan:GLOBAL-like economic production"
    """a unique name for the model component"""
    description = """Simple four-sector (three energy, one final) economy
        as in copan:GLOBAL, but with cell-based harvesting of terrestrial
        and extraction of fossil carbon and perfect allocation between cells.
        Restriction: cannot deal with nested societies yet."""
    """some longer description"""
    requires = []
    """list of other model components required for this model component to
    make sense"""


# entity types:


class World (object):
    """Interface for World mixin."""

    # endogenous variables:

    atmospheric_carbon = D.atmospheric_carbon

    # exogenous variables / parameters:


class Society (object):
    """Interface for Society entity type mixin."""

    # pure output variables:

    biomass_input_flow = D.biomass_input_flow
    fossil_fuel_input_flow = D.fossil_fuel_input_flow
    renewable_energy_input_flow = D.renewable_energy_input_flow
    secondary_energy_flow = D.secondary_energy_flow
    carbon_emission_flow = D.carbon_emission_flow
    total_output_flow = D.total_output_flow

    # exogenous variables / parameters:

    population = D.population
    physical_capital = D.physical_capital
    renewable_energy_knowledge = D.renewable_energy_knowledge

    protected_terrestrial_carbon_share = \
        Variable("protected share of terrestrial carbon",
                 """what share of the current terrestrial carbon will be treated
                 as protected and thus not harvested at each point in time""",
                 unit=D.unity, lower_bound=0, upper_bound=1,
                 default=0)  # may be increased by cultural components
    protected_fossil_carbon_share = \
        Variable("protected share of fossil carbon",
                 """what share of the current fossil carbon will be treated
                 as protected and thus not extracted at each point in time""",
                 unit=D.unity, lower_bound=0, upper_bound=1,
                 default=0)  # may be increased by cultural components


class Cell (object):
    """Interface for Cell entity type mixin."""

    # endogenous variables:

    terrestrial_carbon = D.terrestrial_carbon
    fossil_carbon = D.fossil_carbon

    # pure output variables:

    biomass_harvest_flow = D.biomass_harvest_flow
    fossil_extraction_flow = D.fossil_extraction_flow

    # exogenous variables / parameters:

    biomass_sector_productivity = \
        Variable("biomass sector productivity", "",
                 unit = (D.gigajoules / D.years)**5 \
                        / (D.gigatonnes_carbon * D.dollars * D.people)**2,
                 lower_bound=0, is_intensive=True)
    fossil_sector_productivity = \
        Variable("fossil sector productivity", "",
                 unit = (D.gigajoules / D.years)**5 \
                        / (D.gigatonnes_carbon * D.dollars * D.people)**2,
                 lower_bound=0, is_intensive=True)
    renewable_sector_productivity = \
        Variable("renewable sector productivity", "",
                 unit = D.gigajoules**3 / D.years**5 \
                        / (D.dollars * D.people)**2,
                 lower_bound=0, is_intensive=True)
    total_energy_intensity = D.total_energy_intensity


# process taxa:


class Metabolism (object):
    """Interface for Metabolism process taxon mixin."""

    # endogenous variables:

    biomass_energy_density = D.biomass_energy_density
    fossil_energy_density = D.fossil_energy_density

    # exogenous variables / parameters:
