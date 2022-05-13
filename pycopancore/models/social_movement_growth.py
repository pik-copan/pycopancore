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
from .. import base

#
# TODO: import all other needed model components (adjust as needed):
#
from ..model_components import social_movement_growth as smg


# entity types:

# TODO: compose all needed entity type implementation classes
# by mixing the above model components' mixin classes of the same name.
# Only compose those entity types and process taxons that the model needs,
# delete the templates for the unneeded ones, and add those for missing ones:

# TODO: list all mixin classes needed:
class World(base.World):
    """World entity type."""
    pass


# TODO: list all mixin classes needed:
class SocialSystem(base.SocialSystem):
    """SocialSystem entity type."""
    pass


# TODO: list all mixin classes needed:
class Cell(base.Cell):
    """Cell entity type."""
    pass


# TODO: list all mixin classes needed:
class Individual(smg.Individual,
                 base.Individual):
    """Individual entity type."""
    pass


# process taxa:

# TODO: do the same for process taxa:

# TODO: list all mixin classes needed:
class Environment(base.Environment):
    """Environment process taxon."""
    pass


# TODO: list all mixin classes needed:
class Metabolism(base.Metabolism):
    """Metabolism process taxon."""
    pass


# TODO: list all mixin classes needed:
class Culture(smg.Culture,
              base.Culture):
    """Culture process taxon."""
    pass


# Model class:

# TODO: list all used model components:
class Model(smg.Model,
            base.Model):
    """Class representing the whole model."""

    name = "social movement growth model"
    """Name of the model"""
    description = "Model to compare the influence of different growth strategies on the movement network and success"
    """Longer description"""

    # TODO: list all entity types you composed above:
    entity_types = [World, SocialSystem, Cell, Individual]
    """List of entity types used in the model"""

    # TODO: list all entity types you composed above:
    process_taxa = [Environment, Metabolism, Culture]
    """List of process taxa used in the model"""
