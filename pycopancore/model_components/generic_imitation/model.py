"""Model mixing class template.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016-2021 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# Contact: core@pik-potsdam.de
# License: BSD 2-clause license

from . import interface as I
# import all needed process taxon implementation classes:
from .implementation import Culture


class Model (I.Model):
    """Model mixin class."""

    # mixins provided by this model component:

    entity_types = []
    """list of entity types augmented by this component"""
    process_taxa = [Culture]
    """list of process taxa augmented by this component"""
