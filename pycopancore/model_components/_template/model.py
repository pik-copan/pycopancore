"""Model component mixing class template.

TODO: adjust or fill in code and documentation wherever marked by "TODO:", 
then remove these instructions
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

from .interface import Model_ 
# import all needed entity type implementation classes:
from . import World, Society, Cell, Individual # TODO: adjust!
# import all needed process taxon implementation classes:
from . import Nature, Metabolism, Culture # TODO: adjust!


class Model (Model_):
    """Model component mixin class"""

    # mixins provided by this model component:

    entity_types = [World, Society, Cell, Individual] # TODO: adjust!
    process_taxa = [Nature, Metabolism, Culture] # TODO: adjust!
