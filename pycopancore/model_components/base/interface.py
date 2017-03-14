"""Base model component interface.

In this base interface module, variables for each entity are defined in
corresponding class as sympy objects . The corresponding classes are World_,
Cell_, Nature_, Individual_, Culture_, Society_, Metabolism_ and Model_.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from pycopancore import Variable, ReferenceVariable
from pycopancore import master_data_model as D


# model component:


class Model (object):
    """Basic Model component interface."""

    # metadata:
    name = "copan:CORE Base"
    description = "Basic model component only providing basic relationships between " \
                  "entity types."
    requires = []


# process taxa:


class Nature (object):
    """Basic Nature interface.

    It contains all variables specified as mandatory ("base variables").
    """

    pass


class Metabolism (object):
    """Basic Metabolism interface.

    It contains all variables specified as mandatory ("base variables").
    """

    pass


class Culture (object):
    """Basic Culture interface.

    It contains all variables specified as mandatory ("base variables").
    """

    acquaintance_network = D.acquaintance_network


# entity types:


class World (object):
    """Basic World interface.

    It contains all variables specified as mandatory ("base variables").
    """

    # references:
    nature = ReferenceVariable("nature",
                               "Nature taxon working on this world",
                               type=Nature)
    metabolism = ReferenceVariable("metabolism",
                                   "Metabolism taxon working on this world",
                                   type=Metabolism)
    culture = ReferenceVariable("culture",
                                "Culture taxon working on this world",
                                type=Culture)

    population = D.population
    # TODO: make sure it is no smaller than aggregate top-level societies'

    geographic_network = D.geographic_network

    atmospheric_carbon = D.atmospheric_carbon
    surface_air_temperature = D.surface_air_temperature
    ocean_carbon = D.ocean_carbon
    terrestrial_carbon = D.terrestrial_carbon
    fossil_carbon = D.fossil_carbon

    # attributes storing redundant information (backward references):
    societies = None
    """set of all Societies on this world"""
    top_level_societies = None
    """set of top-level Societies on this world"""
    cells = None
    """set of Cells on this world"""
    individuals = None
    """set of Individuals residing on this world"""


class Society (object):
    """Basic Society interface.

    It contains all variables specified as mandatory ("base variables").
    """

    # references:
    world = ReferenceVariable("world", "", type=World)
    next_higher_society = ReferenceVariable("next higher society", "optional",
                                            allow_none=True)

    # other variables:
    # population is explicitly allowed to be non-integer so that we can use
    # ODEs:
    # TODO: replace by suitable CETSVariable!
    population = D.population
    # TODO: make sure it is no smaller than
    # aggregate next_lower_level societies'

    # read-only attributes storing redundant information:
    nature = None
    metabolism = None
    culture = None
    higher_societies = None
    """upward list of (in)direct super-Societies"""
    next_lower_societies = None
    """set of sub-Societies of next lower level"""
    lower_societies = None
    """set of all direct and indirect sub-Societies"""
    direct_cells = None
    """set of direct territory Cells"""
    cells = None
    """set of direct and indirect territory Cells"""
    direct_individuals = None
    """set of resident Individuals not in subsocieties"""
    individuals = None
    """set of direct or indirect resident Individuals"""


# specified only now to avoid recursion:
Society.next_higher_society.type = Society


class Cell (object):
    """Basic Cell interface.

    It contains all variables specified as mandatory ("base variables").
    """

    # references:
    world = ReferenceVariable("world", "", type=World)
    society = ReferenceVariable("society",
                                "optional lowest-level soc. cell belongs to",
                                type=Society, allow_none=True)

    # other variables:
    location = Variable("location", "pair of coordinates?")
    land_area = Variable("land area", "", unit=D.square_kilometers,
                    strict_lower_bound=0)

    terrestrial_carbon = D.terrestrial_carbon
    fossil_carbon = D.fossil_carbon

    # attributes storing redundant information:
    nature = None
    metabolism = None
    culture = None
    societies = None
    """upward list of Societies it belongs to (in)directly"""
    individuals = None
    """set of resident Individuals"""


class Individual (object):
    """Basic Individual interface.

    It contains all variables specified as mandatory ("base variables").
    """

    # references:
    cell = ReferenceVariable("cell", "cell of residence", type=Cell)

    # other variables:
    relative_weight = \
        Variable("relative representation weight",
                 "relative representation weight for society's population",
                 unit=D.unity, lower_bound=0, default=1)

    # attributes storing redundant information:
    world = None
    nature = None
    metabolism = None
    culture = None
    society = None
    """lowest level Society this individual is resident of"""
    societies = None
    """upward list of all Societies it is resident of"""

    population_share = None
    """share of society's direct population represented by this individual"""
    represented_population = None
    """absolute population represented by this individual"""

    acquaintances = None
    """Individuals this is acquainted with"""

