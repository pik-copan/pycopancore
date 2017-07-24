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
from ..model_components import behave_behaviour_transition as bbt

# entity types:

# NEED TO: compose all needed entity type implementation classes
# by mixing the above model components' mixin classes of the same name.
# Only compose those entity types and process taxons that the model needs,
# delete the templates for the unneeded ones, and add those for missing ones:

# NEED TO: list all mixin classes needed:
class World(base.World):
    """World entity type."""

    pass


# NEED TO: list all mixin classes needed:
class Cell(base.Cell):
    """Cell entity type."""

    pass

# NEED TO: list all mixin classes needed:
class Individual(bbt.Individual,
                 base.Individual):
    """Individual entity type."""

    pass


# process taxa:

# NEED TO: do the same for process taxa:


# NEED TO: list all mixin classes needed:
class Culture(bbt.Culture,
              base.Culture):
    """Culture process taxon."""

    pass


# Model class:

# NEED TO: list all used model components:
class Model(bbt.Model,
            base.Model):
    """Class representing the whole model."""

    name = "Behave"
    """Name of the model"""
    description = "Schleussner et al. 2016"
    """Longer description"""

    # NEED TO: list all entity types you composed above:
    entity_types = [World, Individual]
    """List of entity types used in the model"""
    # NEED TO: list all entity types you composed above:
    process_taxa = [Culture]
    """List of process taxa used in the model"""
