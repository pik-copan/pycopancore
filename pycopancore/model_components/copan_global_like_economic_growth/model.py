"""Model mixing class.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2017 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from . import interface as I
# import all needed entity type implementation classes:
from .implementation import World, Society, Cell, Individual  # TODO: adjust!
# import all needed process taxon implementation classes:
from .implementation import Nature, Metabolism, Culture  # TODO: adjust!


class Model (I.Model):
    """Model mixin class"""

    # mixins provided by this model component:

    entity_types = [Society]
    process_taxa = []
