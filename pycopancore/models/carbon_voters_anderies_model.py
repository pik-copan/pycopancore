"""Model class template.

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

from .. import base  # all models must use the base component

# TODO: import all other needed model components:
# from ..model_components import COMPONENT1 as ABBR1
# from ..model_components import COMPONENT2 as ABBR2
from ..model_components import adaptive_voter_opinion_formation as avof


# entity types:

# TODO: compose all needed entity type implementation classes
# by mixing the above model components' mixin classes of the same name.
# Only compose those entity types and process taxons that the model needs,
# delete the templates for the unneeded ones, and add those for missing ones:

# TODO: list all mixin classes needed:
class World (avof.World,
             base.World):
    """World entity type."""

    pass


# TODO: list all mixin classes needed:
class Society (
               base.Society):
    """Society entity type."""

    pass


# TODO: list all mixin classes needed:
class Cell (
            base.Cell):
    """Cell entity type."""

    pass


# TODO: list all mixin classes needed:
class Individual (avof.Individual,
                  base.Individual):
    """Individual entity type."""

    pass


# process taxa:

# TODO: do the same for process taxa:


# TODO: list all mixin classes needed:
class Nature (
              base.Nature):
    """Nature process taxon."""


# TODO: list all mixin classes needed:
class Metabolism (
                  base.Metabolism):
    """Metabolism process taxon."""

    pass


# TODO: list all mixin classes needed:
class Culture (avof.Culture,
               base.Culture):
    """Culture process taxon."""

    pass


# Model class:

# TODO: list all used model components:
class Model (avof.Model,
             base.Model):
    """Class representing the whole model."""

    name = "..."
    """Name of the model"""
    description = "..."
    """Longer description"""

    # TODO: list all entity types you composed above:
    entity_types = [World, Individual]
    """List of entity types used in the model"""
    # TODO: list all entity types you composed above:
    process_taxa = [Culture]
    """List of process taxa used in the model"""
