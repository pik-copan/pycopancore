"""Model mixing class template.

It is composed to give an
example of the basic structure of it. It inherits from Model_ in that variables
and parameters are defined.
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
# from . import Cell, Nature, Individual, Culture, Society, Metabolism
from pycopancore.model_components import abstract

#
#  Define class Model
#


class Model(Model_, abstract.Model):
    """Define your model class.

    A template for the basic structure of the Model mixin class that every
    component must use. Inherits from Model_ via the
    interface with all necessary variables and parameters.
    """

    #
    # Mixins
    #

    # Use Mixins as wanted

    entity_types = []
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

    def __repr__(self):
        """Return a string representation of the object of the class."""
        return (super().__repr__() +
                ('TEMPLATE.model object')
                )
