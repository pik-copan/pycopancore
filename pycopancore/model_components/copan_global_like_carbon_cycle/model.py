"""Model mixing class template.

It is composed to give an example of the basic structure of it. 
It inherits from Model_.
"""

# This file is part of pycopancore.
#
# Copyright (C) 2016 by COPAN team at Potsdam Institute for Climate
# Impact Research
#
# URL: <http://www.pik-potsdam.de/copan/software>
# License: MIT license

#
#  Imports
#

from .interface import Model_ 
# import all needed entity type implementation classes:
from . import World, Cell
# import all needed process taxon implementation classes:
from . import Nature
from pycopancore.model_components import abstract

#
#  Define class Model
#


class Model(Model_, abstract.Model):
    """Define your model class.

    A template for the basic structure of the Model mixin class that every
    component must use.
    """
    # Note: Model_ does NOT define variables or parameters, only entity types and process taxons do!

    #
    # Mixins
    #

    # Use Mixins as wanted

    entity_types = [World, Cell]
    process_taxa = [Nature]

    def __init__(self,
                 **kwargs
                 ):
        """Initialize your model component.

        Parameters
        ----------
        kwargs
        """
        super().__init__(**kwargs)

    def __repr__(self):
        """Return a string representation of the object of the class."""
        return (super().__repr__() +
                ('Copan_Global_Like_Carbon_Cycle.model component object')
                )
