"""Model mixing class maxploit_most_simple_vegetation."""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from . import interface as I
# import all needed entity type implementation classes:
from .implementation import Cell
# import all needed process taxon implementation classes:
# none needed


class Model (I.Model):
    """Model mixin class."""

    # mixins provided by this model component:

    entity_types = [Cell]
    """list of entity types augmented by this component"""
    process_taxa = []
    """list of process taxa augmented by this component"""
