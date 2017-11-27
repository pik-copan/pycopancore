"""Model class template.

NEED TO:
Copy this file, rename it to the name of your model,
then adjust or fill in code and documentation wherever marked by "NEED TO:",
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

# NEED TO: import all other needed model components:
#from ..model_components import COMPONENT1 as ABBR1
#from ..model_components import COMPONENT2 as ABBR2

# entity types:

# NEED TO: compose all needed entity type implementation classes
# by mixing the above model components' mixin classes of the same name.
# Only compose those entity types and process taxons that the model needs,
# delete the templates for the unneeded ones, and add those for missing ones:

# NEED TO: list all mixin classes needed:
class World(ABBR1.World, ABBR2.World,
            base.World):
    """World entity type."""

    pass


# NEED TO: list all mixin classes needed:
class SocialSystem(ABBR1.SocialSystem, ABBR2.SocialSystem,
              base.SocialSystem):
    """SocialSystem entity type."""

    pass


# NEED TO: list all mixin classes needed:
class Cell(ABBR1.Cell, ABBR2.Cell,
           base.Cell):
    """Cell entity type."""

    pass


# NEED TO: list all mixin classes needed:
class Individual(ABBR1.Individual, ABBR2.Individual,
                 base.Individual):
    """Individual entity type."""

    pass


# process taxa:

# NEED TO: do the same for process taxa:


# NEED TO: list all mixin classes needed:
class Nature(ABBR1.Nature, ABBR2.Nature,
             base.Nature):
    """Nature process taxon."""

    pass


# NEED TO: list all mixin classes needed:
class Metabolism(ABBR1.Metabolism, ABBR2.Metabolism,
                 base.Metabolism):
    """Metabolism process taxon."""

    pass


# NEED TO: list all mixin classes needed:
class Culture(ABBR1.Culture, ABBR2.Culture,
              base.Culture):
    """Culture process taxon."""

    pass


# Model class:

# NEED TO: list all used model components:
class Model(ABBR1.Model, ABBR2.Model,
            base.Model):
    """Class representing the whole model."""

    name = "..."
    """Name of the model"""
    description = "..."
    """Longer description"""

    # NEED TO: list all entity types you composed above:
    entity_types = [World, SocialSystem, Cell, Individual]
    """List of entity types used in the model"""
    # NEED TO: list all entity types you composed above:
    process_taxa = [Nature, Metabolism, Culture]
    """List of process taxa used in the model"""
