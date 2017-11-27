"""Model mixing class template.

TODO: adjust or fill in code and documentation wherever marked by "TODO:",
then remove these instructions
"""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>

from . import interface as I

# TODO: adjust imports of all needed entity type implementation classes:
from .implementation import World, Society, Cell, Individual

# TODO: adjust imports of all needed process taxon implementation classes:
from .implementation import Nature, Metabolism, Culture 


class Model (I.Model):
    """Model mixin class."""

    # mixins provided by this model component:

    # TODO: remove unneccesary entity types
    entity_types = [World, Society, Cell, Individual]      
    """list of entity types augmented by this component"""

    # TODO: remove unneccesary process taxa
    process_taxa = [Nature, Metabolism, Culture]  
    """list of process taxa augmented by this component"""
