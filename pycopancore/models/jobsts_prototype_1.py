"""
jobsts_prototype_1 model.
"""
# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

import pycopancore.model_components.base as base  # all models must use the base component

import pycopancore.model_components.copan_global_like_carbon_cycle \
    as cc
import pycopancore.model_components.copan_global_like_production \
    as prod
import pycopancore.model_components.copan_global_like_economic_growth \
    as growth
#import pycopancore.model_components.copan_global_like_population_growth \
#    as population
#import pycopancore.model_components....migration \
#    as migration


# entity types:


class World (cc.World, prod.World,  # TODO: list all mixin classes needed
             base.World):
    """World entity type"""
    pass


class Society (prod.Society, growth.Society,  # TODO: list all mixin classes needed
               base.Society):
    """Society entity type"""
    pass


class Cell (cc.Cell, prod.Cell,  # TODO: list all mixin classes needed
            base.Cell):
    """Cell entity type"""
    pass


#class Individual (ABBR1.Individual, ABBR2.Individual,  # TODO: list all mixin classes needed
#             base.Individual):
#    """Individual entity type"""
#    pass


# process taxa:


class Nature (cc.Nature,  # TODO: list all mixin classes needed
              base.Nature):
    """Nature process taxon"""
    pass


class Metabolism (prod.Metabolism,  # TODO: list all mixin classes needed
                  base.Metabolism):
    """Metabolism process taxon"""
    pass


#class Culture (ABBR1.Culture, ABBR2.Culture,  # TODO: list all mixin classes needed
#               base.Culture):
#    """Culture process taxon"""
#    pass


# Model class:


class Model (cc.Model, prod.Model, growth.Model,
             base.Model):
    """Class representing the whole model"""

    name = "Jobst's prototype 1"
    """Name of the model"""
    description = "(as presented internally at PIK in fall 2016)"
    """Longer description"""

    entity_types = [World, Society, Cell]
    """List of entity types used in the model"""
    process_taxa = [Nature, Metabolism]
    """List of process taxa used in the model"""
