"""copan_global_like_production model component Interface."""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from ... import master_data_model as D
from ...data_model.master_data_model import MET, W, S, C
from ... import Variable


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

    atmospheric_carbon = W.atmospheric_carbon

    # exogenous variables / parameters:


class Society (object):
    """Interface for Society entity type mixin."""

    # pure output variables:

    biomass_input_flow = S.biomass_input_flow
    fossil_fuel_input_flow = S.fossil_fuel_input_flow
    renewable_energy_input_flow = S.renewable_energy_input_flow
    secondary_energy_flow = S.secondary_energy_flow
    carbon_emission_flow = S.carbon_emission_flow
    economic_output_flow = S.economic_output_flow

    # exogenous variables / parameters:

    population = S.population
    physical_capital = S.physical_capital
    renewable_energy_knowledge = S.renewable_energy_knowledge

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

    terrestrial_carbon = C.terrestrial_carbon
    fossil_carbon = C.fossil_carbon

    # pure output variables:

    biomass_relative_productivity = \
        Variable("biomass relative productivity",
                 "used to determine energy input",
                 unit=D.unity,
                 lower_bound=0, default=1)

    fossil_relative_productivity = \
        Variable("fossil relative productivity",
                 "used to determine energy input",
                 unit=D.unity,
                 lower_bound=0, default=1)

    renewable_relative_productivity = \
        Variable("renewable relative productivity",
                 "used to determine energy input",
                 unit=D.unity,
                 lower_bound=0, default=1)

    total_relative_productivity = \
        Variable("total relative productivity",
                 "used as weights in allocation of labour and capital",
                 unit=D.unity,
                 lower_bound=0, default=3)

    biomass_harvest_flow = C.biomass_harvest_flow
    fossil_extraction_flow = C.fossil_extraction_flow

    # exogenous variables / parameters:

    biomass_sector_productivity = \
        Variable("biomass sector productivity", 
                 "(Parameter aB in Nitzbon et al. 2017)",
                 unit = (D.gigajoules / D.years)**5
                        / (D.gigatonnes_carbon * D.dollars * D.people)**2,
                 lower_bound=0, is_intensive=True, default=1e7) # 2.8??
    fossil_sector_productivity = \
        Variable("fossil sector productivity",
                 "(Parameter aF in Nitzbon et al. 2017)",
                 unit = (D.gigajoules / D.years)**5
                        / (D.gigatonnes_carbon * D.dollars * D.people)**2,
                 lower_bound=0, is_intensive=True, default=3e8) # 24.9??
    renewable_sector_productivity = \
        Variable("renewable sector productivity", "",
                 unit = D.gigajoules**3 / D.years**5
                        / (D.dollars * D.people)**2,
                 lower_bound=0, is_intensive=True, default=1e-17)
    total_energy_intensity = C.total_energy_intensity


# process taxa:


class Metabolism (object):
    """Interface for Metabolism process taxon mixin."""

    # endogenous variables:

    biomass_energy_density = MET.biomass_energy_density
    fossil_energy_density = MET.fossil_energy_density

    # exogenous variables / parameters:
