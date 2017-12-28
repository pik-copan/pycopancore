"""Model class seven_dwarfs."""

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

from ..model_components import seven_dwarfs as sd

# entity types:

# by mixing the above model components' mixin classes of the same name.
# Only compose those entity types and process taxons that the model needs,
# delete the templates for the unneeded ones, and add those for missing ones:


class World(sd.World,
            base.World):
    """World entity type."""

    pass


class SocialSystem(base.SocialSystem):
    """SocialSystem entity type."""

    pass


class Cell(sd.Cell,
           base.Cell):
    """Cell entity type."""

    pass


class Individual(sd.Individual,
                 base.Individual):
    """Individual entity type."""

    pass


# process taxa:

class Culture(sd.Culture,
              base.Culture):
    """Culture process taxon."""

    pass


# Model class:

class Model(sd.Model,
            base.Model):
    """Class representing the whole model."""

    name = "..."
    """Seven dwarfs"""
    description = "..."
    """Tutorial model"""

    entity_types = [World, SocialSystem, Cell, Individual]
    """List of entity types used in the model"""
    process_taxa = [Culture]
    """List of process taxa used in the model"""
