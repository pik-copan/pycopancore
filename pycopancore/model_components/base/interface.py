"""Base model component interface.

Specifies the variables used by this component,
by entity type and process taxon
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from ...private import _MixinType, unknown
from ... import Variable, ReferenceVariable, SetVariable
from ... import master_data_model as D
from ...data_model.master_data_model import ENV, CUL, W, S, C


# model component:


class Model (object):
    """Basic Model component interface."""

    # necessary metadata:
    name = "copan:CORE Base"
    description = "Basic model component only providing basic relationships " \
                  "between entity types."
    requires = []


# process taxa:


class Environment (object):
    """Basic Environment interface.

    It contains all variables specified as mandatory ("base variables").
    """

    geographic_network = ENV.geographic_network  # copies the specification from the master data model
    worlds = SetVariable("worlds", "set of Worlds on this Environment")


class Metabolism (object):
    """Basic Metabolism interface.

    It contains all variables specified as mandatory ("base variables").
    """

    worlds = SetVariable("worlds", "set of Worlds on this Metabolism")


class Culture (object):
    """Basic Culture interface.

    It contains all variables specified as mandatory ("base variables").
    """

    acquaintance_network = CUL.acquaintance_network
    worlds = SetVariable("worlds", "set of Worlds on this Culture")

    # read-only attributes storing redundant information:
    worlds = SetVariable("worlds",
                         "set of Worlds this Culture acts in",
                         readonly=True)

# entity types:


# TODO: clarify whether it is necessary to specify the metaclass here!
class World (object, metaclass=_MixinType):
    """Basic World interface.

    It contains all variables specified as mandatory ("base variables").
    """
    # the metaclass is needed to allow for intercepting class attribute calls
    # when constructing DotConstructs like World.environment.geographic_network.
    # similarly for the other entity types.


    # references to other entities and taxa:
    environment = ReferenceVariable("environment",
                               "Environment taxon working on this world",
                               type=Environment, allow_none=True)
    metabolism = ReferenceVariable("metabolism",
                                   "Metabolism taxon working on this world",
                                   type=Metabolism, allow_none=True)
    culture = ReferenceVariable("culture",
                                "Culture taxon working on this world",
                                type=Culture, allow_none=True)

    # variables taken from the master data model:
    population = W.population  # TODO: make sure it is no smaller than aggregate top-level social_systems'?
    atmospheric_carbon = W.atmospheric_carbon
    surface_air_temperature = W.surface_air_temperature
    ocean_carbon = W.ocean_carbon
    terrestrial_carbon = W.terrestrial_carbon
    fossil_carbon = W.fossil_carbon

    # attributes storing redundant information (backward references):
    social_systems = SetVariable("social systems",
                            "set of all SocialSystems on this world",
                            readonly=True)  # type is SocialSystem, hence it can only be specified after class SocialSystem is defined, see below
    top_level_social_systems = SetVariable(
        "top level social systems",
        "set of top-level SocialSystems on this world",
        readonly=True)
    cells = SetVariable("cells", "set of Cells on this world",
                        readonly=True)
    individuals = SetVariable("individuals",
                              "set of Individuals residing on this world",
                              readonly=True)


# specified only now to avoid recursion errors:
Culture.worlds.type = World
Metabolism.worlds.type = World
Environment.worlds.type = World


class SocialSystem (object, metaclass=_MixinType):
    """Basic SocialSystem interface.

    It contains all variables specified as mandatory ("base variables").
    """

    # references:
    world = ReferenceVariable("world", "", type=World)
    next_higher_social_system = ReferenceVariable("next higher social_system", "optional",
                                            allow_none=True)  # type is SocialSystem, hence it can only be specified after class SocialSystem is defined, see below

    # other variables:
    # population is explicitly allowed to be non-integer so that we can use
    # ODEs:
    # TODO: replace by suitable CETSVariable!
    population = S.population
    # TODO: make sure it is no smaller than
    # aggregate next_lower_level social_systems'

    # read-only attributes storing redundant information:
    environment = ReferenceVariable("environment", "", type=Environment,
                               readonly=True)
    metabolism = ReferenceVariable("metabolism", "", type=Metabolism,
                                   readonly=True)
    culture = ReferenceVariable("culture", "", type=Culture,
                                readonly=True)
    higher_social_systems = SetVariable(
        "higher social systems",
        "upward list of (in)direct super-SocialSystems",
        readonly=True)
    next_lower_social_systems = SetVariable(
        "next lower social systems",
        "set of sub-SocialSystems of next lower level",
        readonly=True)
    lower_social_systems = SetVariable(
        "lower social systems",
        "set of all direct and indirect sub-SocialSystems",
        readonly=True)
    direct_cells = SetVariable("direct cells", "set of direct territory Cells",
                               readonly=True)
    cells = SetVariable("cells", "set of direct and indirect territory Cells",
                        readonly=True)
    direct_individuals = SetVariable(
        "direct individuals",
        "set of resident Individuals not in subsocial_systems",
        readonly=True)
    individuals = SetVariable("individuals",
                              "set of direct or indirect resident Individuals",
                              readonly=True)


# specified only now to avoid recursion errors:
SocialSystem.next_higher_social_system.type = SocialSystem
SocialSystem.higher_social_systems.type = SocialSystem
SocialSystem.next_lower_social_systems.type = SocialSystem
SocialSystem.lower_social_systems.type = SocialSystem
World.social_systems.type = SocialSystem
World.top_level_social_systems.type = SocialSystem


class Cell (object, metaclass=_MixinType):
    """Basic Cell interface.

    It contains all variables specified as mandatory ("base variables").
    """

    # references:
    world = ReferenceVariable("world", "", type=World)
    social_system = ReferenceVariable("social_system",
                                "optional lowest-level soc. cell belongs to",
                                type=SocialSystem, allow_none=True)

    # other variables:
    location = Variable("location", "pair of coordinates?",
                        allow_none=True, default=None)  # TODO: specify data type
    land_area = C.land_area

    terrestrial_carbon = C.terrestrial_carbon
    fossil_carbon = C.fossil_carbon

    # attributes storing redundant information:
    environment = ReferenceVariable("environment", "", type=Environment,
                               readonly=True)
    metabolism = ReferenceVariable("metabolism", "", type=Metabolism,
                                   readonly=True)
    culture = ReferenceVariable("culture", "", type=Culture,
                                readonly=True)
    social_systems = SetVariable(
        "social_systems",
        "upward list of SocialSystems it belongs to (in)directly",
        type=SocialSystem,
        readonly=True)
    individuals = SetVariable("individuals",
                              "set of resident Individuals",
                              readonly=True)


# specified only now to avoid recursion:
World.cells.type = Cell
SocialSystem.direct_cells.type = Cell
SocialSystem.cells.type = Cell


class Individual (object, metaclass=_MixinType):
    """Basic Individual interface.

    It contains all variables specified as mandatory ("base variables").
    """

    # references:
    cell = ReferenceVariable("cell", "cell of residence", type=Cell)

    # other variables:
    relative_weight = \
        Variable("relative representation weight",
                 "relative representation weight for social_system's population, "
                 "to be used in determining how many people this individual "
                 "represents",
                 unit=D.unity, lower_bound=0, default=1)

    # attributes storing redundant information:
    world = ReferenceVariable("world", "", type=World,
                              readonly=True)
    environment = ReferenceVariable("environment", "", type=Environment,
                               readonly=True)
    metabolism = ReferenceVariable("metabolism", "", type=Metabolism,
                                   readonly=True)
    culture = ReferenceVariable("culture", "", type=Culture,
                                readonly=True)
    social_system = ReferenceVariable(
        "social_system",
        "lowest level SocialSystem this individual is resident of",
        type=SocialSystem,
        readonly=True)
    social_systems = SetVariable(
        "social_systems",
        "upward list of all SocialSystems it is resident of",
        type=SocialSystem,
        readonly=True)
    acquaintances = SetVariable("acquaintances",
                    "set of Individuals this one is acquainted with",
                    readonly=True)

    # TODO: specify Variable objects for the following:
    population_share = None
    """share of social_system's direct population represented by this individual"""
    represented_population = Variable(
        "represented population", 
        "absolute population represented by this individual",
        readonly=True,
        unit=D.people,
        is_extensive=True)


# specified only now to avoid recursion:
World.individuals.type = Individual
SocialSystem.direct_individuals.type = Individual
SocialSystem.individuals.type = Individual
Cell.individuals.type = Individual
Individual.acquaintances.type = Individual
