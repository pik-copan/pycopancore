"""jobsts_prototype_1 model adapted to test generic_imitation component."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2021 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

#
#  Imports
#

import numpy as np

from .... import base  # all models must use the base component

# from ...model_components import social_learning_of_environmental_friendliness
#    as learn
from ....model_components import config
from ....model_components import copan_global_like_carbon_cycle as cc
from ....model_components import (
    copan_global_like_economic_growth as growth,
)
from ....model_components import (
    copan_global_like_population_growth as pop,
)
from ....model_components import copan_global_like_production as prod
from ....model_components import environmental_awareness as aware
from ....model_components import generic_imitation as imi
from ....model_components import voting_on_climate_policy as vote
from ....model_components import wellbeing_driven_migration as mig

config.generic_imitation = {
    "variables": [
        base.interface.Culture.individuals.is_environmentally_friendly,
        base.interface.Culture.social_systems.has_emissions_tax,
        base.interface.Culture.social_systems.emissions_tax_level,
    ]
}

# entity types:


class World(cc.World, prod.World, growth.World, base.World):
    """World entity type."""

    pass


class SocialSystem(
    prod.SocialSystem,
    growth.SocialSystem,
    pop.SocialSystem,
    mig.SocialSystem,
    aware.SocialSystem,
    vote.SocialSystem,
    base.SocialSystem,
):
    """SocialSystem entity type."""

    pass


class Cell(cc.Cell, prod.Cell, aware.Cell, base.Cell):
    """Cell entity type."""

    pass


class Individual(
    aware.Individual,
    #                 learn.Individual,
    base.Individual,
):
    """Individual entity type."""

    def imi_p_imitate_env(self, own_trait=None, other_trait=None):
        return 1 / (1 + np.exp(self.relative_weight))

    def imi_imitate_env(self, variables=None, values=None):
        for index, var in enumerate(variables):
            var.set_value(self, values[index])


# process taxa:


class Environment(cc.Environment, base.Environment):
    """Environment process taxon."""

    pass


class Metabolism(
    prod.Metabolism,
    growth.Metabolism,
    pop.Metabolism,
    mig.Metabolism,
    base.Metabolism,
):
    """Metabolism process taxon."""

    pass


class Culture(
    aware.Culture,
    #               learn.Culture,
    imi.Culture,
    base.Culture,
):
    """Culture process taxon"""

    imi.Culture.imi_traits.default = {
        "env": (aware.Individual.is_environmentally_friendly,),
        "tax": (
            prod.SocialSystem.has_emissions_tax,
            prod.SocialSystem.emissions_tax_level,
        ),
    }


# Model class:


class Model(
    cc.Model,
    prod.Model,
    growth.Model,
    pop.Model,
    mig.Model,
    aware.Model,
    #            learn.Model,
    imi.Model,
    vote.Model,
    base.Model,
):
    """Class representing the whole model."""

    name = "Jobst's prototype 1"
    """Name of the model"""
    description = "(as presented internally at PIK in fall 2016)"
    """Longer description"""

    entity_types = [World, SocialSystem, Cell, Individual]
    """List of entity types used in the model"""
    process_taxa = [Environment, Metabolism, Culture]
    """List of process taxa used in the model"""
