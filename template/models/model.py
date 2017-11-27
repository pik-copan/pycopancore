"""Model class template.

TODO: Go through the file and adjust all parts of the code marked with the TODO
flag. Pay attention to those variables and object written in capital letters.
These are placeholders and must be adjusted as needed. For further details see
also the model development tutorial.
"""
# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>

# all models must use the base component
from pycopancore import base

#
# TODO: import all other needed model components (adjust as needed):
#
# Model components are either provided by pycopancore
from pycopancore.model_components import SOMECOMPONENT

# Or you implement your own components
from model_components import one_component as ONECOMPONENT

# entity types:

# TODO: compose all needed entity type implementation classes
# by mixing the above model components' mixin classes of the same name.
# Only compose those entity types and process taxons that the model needs,
# delete the templates for the unneeded ones, and add those for missing ones:

# TODO: list all mixin classes needed:
class World(SOMECOMPONENT.World,
            ONECOMPONENT.World,
            base.World):
    """World entity type."""
    pass


# TODO: list all mixin classes needed:
class Society(SOMECOMPONENT.Society,
              ONECOMPONENT.Society,
              base.Society):
    """Society entity type."""
    pass


# TODO: list all mixin classes needed:
class Cell(SOMECOMPONENT.Cell,
           ONECOMPONENT.Cell,
           base.Cell):
    """Cell entity type."""
    pass


# TODO: list all mixin classes needed:
class Individual(SOMECOMPONENT.Individual,
                 ONECOMPONENT.Individual,
                 base.Individual):
    """Individual entity type."""
    pass


# process taxa:

# TODO: do the same for process taxa:

# TODO: list all mixin classes needed:
class Nature(SOMECOMPONENT.Nature,
             ONECOMPONENT.Nature,
             base.Nature):
    """Nature process taxon."""
    pass


# TODO: list all mixin classes needed:
class Metabolism(SOMECOMPONENT.Metabolism,
                 ONECOMPONENT.Metabolism,
                 base.Metabolism):
    """Metabolism process taxon."""
    pass


# TODO: list all mixin classes needed:
class Culture(SOMECOMPONENT.Culture,
              ONECOMPONENT.Culture,
              base.Culture):
    """Culture process taxon."""
    pass


# Model class:

# TODO: list all used model components:
class Model(SOMECOMPONENT.Model,
            ONECOMPONENT.Model,
            base.Model):
    """Class representing the whole model."""

    name = "..."
    """Name of the model"""
    description = "..."
    """Longer description"""

    # TODO: list all entity types you composed above:
    entity_types = [World, Society, Cell, Individual]
    """List of entity types used in the model"""

    # TODO: list all entity types you composed above:
    process_taxa = [Nature, Metabolism, Culture]
    """List of process taxa used in the model"""
