"""
Model class template.

TODO:
Copy this file, rename it to the name of your model, 
then adjust or fill in code and documentation wherever marked by "TODO:", 
finally remove these instructions.
See the model development tutorial for details.
"""
# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

import pycopancore.model_components.base as base  # all models must use the base component

# TODO: import all other needed model components:
#import pycopancore.model_components.COMPONENT1 as ABBR1
#import pycopancore.model_components.COMPONENT2 as ABBR2


# entity types:

# TODO: compose all needed entity type implementation classes
# by mixing the above model components' mixin classes of the same name.
# Only compose those entity types and process taxons that the model needs,
# delete the templates for the unneeded ones, and add those for missing ones:


class World (ABBR1.World, ABBR2.World,  # TODO: list all mixin classes needed
             base.World):
    """World entity type"""
    pass


class Society (ABBR1.Society, ABBR2.Society,  # TODO: list all mixin classes needed
               base.Society):
    """Society entity type"""
    pass


class Cell (ABBR1.Cell, ABBR2.Cell,  # TODO: list all mixin classes needed
            base.Cell):
    """Cell entity type"""
    pass


class Individual (ABBR1.Individual, ABBR2.Individual,  # TODO: list all mixin classes needed
             base.Individual):
    """Individual entity type"""
    pass


# process taxa:

# TODO: do the same for process taxa:


class Nature (ABBR1.Nature, ABBR2.Nature,  # TODO: list all mixin classes needed
              base.Nature):
    """Nature process taxon"""
    pass


class Metabolism (ABBR1.Metabolism, ABBR2.Metabolism,  # TODO: list all mixin classes needed
                  base.Metabolism):
    """Metabolism process taxon"""
    pass


class Culture (ABBR1.Culture, ABBR2.Culture,  # TODO: list all mixin classes needed
               base.Culture):
    """Culture process taxon"""
    pass


# Model class:


class Model (ABBR1.Model, ABBR2.Model,  # TODO: list all used model components
             base.Model):
    """Class representing the whole model"""

    name = "..."
    """Name of the model"""
    description = "..."
    """Longer description"""

    entity_types = [World, Society, Cell, Individual]  # TODO: list all entity types you composed above
    """List of entity types used in the model"""
    process_taxa = [Nature, Metabolism, Culture]  # TODO: list all entity types you composed above
    """List of process taxa used in the model"""
