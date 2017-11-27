"""Model class template.

TODO:
Copy this file, rename it to the name of your model, then adjust or fill in
code and documentation wherever marked by "TODO:", finally remove these
instructions.  See the model development tutorial for details.
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
from model_components import one_component

# entity types:

# TODO: compose all needed entity type implementation classes
# by mixing the above model components' mixin classes of the same name.
# Only compose those entity types and process taxons that the model needs,
# delete the templates for the unneeded ones, and add those for missing ones:

# TODO: list all mixin classes needed:
class World(SOMECOMPONENT.World,
            one_component.World,
            base.World):
    """World entity type."""
    pass


# TODO: list all mixin classes needed:
class Society(SOMECOMPONENT.Society,
              one_component.Society,
              base.Society):
    """Society entity type."""
    pass


# TODO: list all mixin classes needed:
class Cell(SOMECOMPONENT.Cell,
           one_component.Cell,
           base.Cell):
    """Cell entity type."""
    pass


# TODO: list all mixin classes needed:
class Individual(SOMECOMPONENT.Individual,
                 one_component.Individual,
                 base.Individual):
    """Individual entity type."""
    pass


# process taxa:

# TODO: do the same for process taxa:

# TODO: list all mixin classes needed:
class Nature(SOMECOMPONENT.Nature,
             one_component.Nature,
             base.Nature):
    """Nature process taxon."""
    pass


# TODO: list all mixin classes needed:
class Metabolism(SOMECOMPONENT.Metabolism,
                 one_component.Metabolism,
                 base.Metabolism):
    """Metabolism process taxon."""
    pass


# TODO: list all mixin classes needed:
class Culture(SOMECOMPONENT.Culture,
              one_component.Culture,
              base.Culture):
    """Culture process taxon."""
    pass


# Model class:

# TODO: list all used model components:
class Model(SOMECOMPONENT.Model,
            one_component.Model,
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
