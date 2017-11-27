"""jobsts_prototype_1 model, reduced to carbon cycle only."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

#
#  Imports
#

from .. import base  # all models must use the base component

from ..model_components import copan_global_like_carbon_cycle \
    as cc
# from ..model_components import copan_global_like_production \
#    as prod
# from ..model_components import copan_global_like_economic_growth \
#    as growth
# from ..model_components import copan_global_like_population_growth \
#    as population
# from ..model_components import ...migration \
#    as migration


# entity types:


class World(cc.World,
            # prod.World,
            base.World):
    """World entity type."""

    pass


class SocialSystem(base.SocialSystem):
              # prod.SocialSystem,
              # growth.SocialSystem):
    """SocialSystem entity type."""

    pass


class Cell(cc.Cell,
           # prod.Cell,
           base.Cell):
    """Cell entity type."""

    pass

# class Individual (ABBR1.Individual, ABBR2.Individual,
#                   base.Individual):
#    """Individual entity type."""
#    pass


# process taxa:


class Environment(cc.Environment,
             base.Environment):
    """Environment process taxon."""

    pass


class Metabolism(base.Metabolism):
                # , prod.Metabolism):
    """Metabolism process taxon."""

    pass

# class Culture (ABBR1.Culture, ABBR2.Culture,
#               base.Culture):
#    """Culture process taxon."""

#    pass


# Model class:


class Model(cc.Model,
            # prod.Model,
            # growth.Model,
            base.Model):
    """Class representing the whole model."""

    name = "Jobst's prototype 1, only CC"
    """Name of the model"""
    description = "(as presented internally at PIK in fall 2016)"
    """Longer description"""

    entity_types = [World, SocialSystem, Cell]
    """List of entity types used in the model"""
    process_taxa = [Environment, Metabolism]
    """List of process taxa used in the model"""
