"""jobsts_prototype_1 model."""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

#
#  Imports
#

from .. import base  # all models must use the base component

from ..model_components import copan_global_like_carbon_cycle \
    as cc
from ..model_components import copan_global_like_production \
    as prod
from ..model_components import copan_global_like_economic_growth \
    as growth
from ..model_components import copan_global_like_population_growth \
    as pop
# from ..model_components import ...migration \
#    as migration


# entity types:


class World(cc.World,
            prod.World,
            base.World):
    """World entity type."""

    pass


class Society(prod.Society,
              growth.Society,
              pop.Society,
              base.Society):
    """Society entity type."""

    pass


class Cell(cc.Cell,
           prod.Cell,
           base.Cell):
    """Cell entity type."""

    pass

# class Individual (ABBR1.Individual, ABBR2.Individual,
#             base.Individual):
#    """Individual entity type."""

#    pass


# process taxa:


class Nature(cc.Nature,
             base.Nature):
    """Nature process taxon."""

    pass


class Metabolism(prod.Metabolism,
                 pop.Metabolism,
                 base.Metabolism):
    """Metabolism process taxon."""

    pass

# class Culture (ABBR1.Culture, ABBR2.Culture,
#               base.Culture):
#    """Culture process taxon"""
#    pass


# Model class:


class Model(cc.Model,
            prod.Model,
            growth.Model,
            pop.Model,
            base.Model):
    """Class representing the whole model."""

    name = "Jobst's prototype 1"
    """Name of the model"""
    description = "(as presented internally at PIK in fall 2016)"
    """Longer description"""

    entity_types = [World, Society, Cell]
    """List of entity types used in the model"""
    process_taxa = [Nature, Metabolism]
    """List of process taxa used in the model"""
