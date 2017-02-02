"""The most_simple_vegetation model.

This is a very simple model for vegetation growth.
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
from . import Cell
from pycopancore.model_components import abstract

#
#  Define class Model
#


class Model(Model_, abstract.Model):
    """Define properties of the most_simple_vegetation model.

    Inherits from Model_ via the
    interface with all necessary variables and parameters.
    """

    #
    # Mixins
    #

    # Use Mixins as wanted

    entity_types = [Cell]
    process_taxa = []

    def __init__(self,
                 **kwargs
                 ):
        """Initialize your model.

        Parameters
        ----------
        kwargs
        """
        super().__init__(**kwargs)

        print('     Most simple vegetation model component instantiated')

    def __repr__(self):
        """Return a string representation of the object of the class."""
        return (super().__repr__() +
                ('most_simple_vegetation.model object')
                )
