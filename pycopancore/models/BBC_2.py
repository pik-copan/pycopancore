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

from ..model_components import BBC_Climate_Biosphere_2 as CB
#from ..model_components import BBC_Climate_System as CS
#from ..model_components import BBC_Bio_Behaviour as BBH
#from ..model_components import BBC_Clim_Behaviour as CSBH
#from ..model_components import BBC_Bio_Metabolism as BM
#from ..model_components import BBC_Clim_Metabolism as CM


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
class Individual(base.Individual):
    """Individual entity type."""
    pass


# process taxa:

# TODO: do the same for process taxa:

# TODO: list all mixin classes needed:
class Environment(CB.Environment, base.Environment):
    """Environment process taxon."""
    pass


# TODO: list all mixin classes needed:
class Metabolism(base.Metabolism):
    """Metabolism process taxon."""
    pass

#class Metabolism(base.Metabolism, BM.Metabolism, CM.Metabolism):
#    """Metabolism process taxon."""
#    pass

# TODO: list all mixin classes needed:
class Culture(base.Culture):
    """Culture process taxon."""
    pass

#class Culture(base.Culture, BBH.Culture, CSBH.Culture):
 #   """Culture process taxon."""
 #   pass


# Model class:

# TODO: list all used model components:
class Model(CB.Model,
            base.Model):
    """Class representing the whole model."""

    name = "BBC"
    """Name of the model"""
    description = "model foc analysing interactions oc humman Behaviour, Biosphere and Climate"
    """Longer description"""

    # TODO: list all entity types you composed above:
    entity_types = [World, SocialSystem, Cell, Individual]
    """List of entity types used in the model"""

    # TODO: list all entity types you composed above:
    process_taxa = [Environment, Metabolism, Culture]
    """List of process taxa used in the model"""
