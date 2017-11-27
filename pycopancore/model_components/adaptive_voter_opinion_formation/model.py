"""Model mixing class template.

TODO: adjust or fill in code and documentation wherever marked by "TODO:",
then remove these instructions
"""

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
from .implementation import Individual
# import all needed process taxon implementation classes:
from .implementation import Culture


class Model (I.Model):
    """Model mixin class"""

    # mixins provided by this model component:

    entity_types = [Individual]
    """list of entity types augmented by this component"""
    process_taxa = [Culture]
    """list of process taxa augmented by this component"""
